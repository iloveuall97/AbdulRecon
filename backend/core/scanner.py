from __future__ import annotations

import asyncio
import logging
import random
import re
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Set
from urllib.parse import urljoin, urlparse

import aiohttp

from core.vulnerability import VulnerabilityModule
from core.payloads import PayloadManager


class ScanError(Exception):
    pass


class SecurityScanner:
    """Async security scanning engine with basic crawling, module orchestration,
    proxy rotation integration, fingerprinting and payload support.

    Modules should be instances of VulnerabilityModule and may use the
    provided `context['request']` helper to perform requests with retries,
    fingerprint headers and optional payload variants supplied by PayloadManager.
    """

    URL_EXTRACT_RE = re.compile(r"href=[\"']([^\"'#]+)[\"']", re.IGNORECASE)

    def __init__(self, config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        # lazy import ScannerConfig for validation
        try:
            from core.config_models import ScannerConfig  # type: ignore
        except Exception:
            ScannerConfig = None  # type: ignore

        if ScannerConfig is not None and not isinstance(config, ScannerConfig):
            try:
                self.config = ScannerConfig.model_validate(config)  # type: ignore
            except Exception:
                self.config = config
        else:
            self.config = config

        self.logger = logger or logging.getLogger("SecurityScanner")
        self.scan_id: Optional[str] = None
        self.results: Dict[str, List[Dict[str, Any]]] = {}
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

        # Build helpers if available
        try:
            from core.proxy_manager import ProxyManager  # type: ignore
            from core.fingerprint import RequestFingerprinter  # type: ignore
        except Exception:
            ProxyManager = None  # type: ignore
            RequestFingerprinter = None  # type: ignore

        self.proxy_mgr = ProxyManager(getattr(self.config, "proxies", None)) if ProxyManager else None
        self.fingerprinter = (
            RequestFingerprinter(getattr(self.config, "user_agents", None), getattr(self.config, "fingerprint_aggressiveness", "low"))
            if RequestFingerprinter
            else None
        )
        self.payload_mgr = PayloadManager(getattr(self.config, "fingerprint_aggressiveness", "low"))

        # Concurrency and timeouts
        self._concurrency = int(getattr(self.config, "concurrency", 10))
        self._semaphore = asyncio.Semaphore(self._concurrency)
        self._connector_limit = int(getattr(self.config, "concurrency", 10))
        self._retries = int(getattr(self.config, "retries", 2))
        self._timeout_seconds = int(getattr(self.config, "timeout_seconds", 15))

    async def _make_session(self) -> aiohttp.ClientSession:
        timeout = aiohttp.ClientTimeout(total=self._timeout_seconds)
        connector = aiohttp.TCPConnector(limit_per_host=self._connector_limit)
        return aiohttp.ClientSession(timeout=timeout, connector=connector)

    async def _request_with_retries(
        self,
        session: aiohttp.ClientSession,
        method: str,
        url: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        proxy: Optional[str] = None,
        data: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """Make a request with retries and return a small result dict.

        Note: we return the response status and a short text snippet (first 2048 chars)
        to be used as evidence by vulnerability modules.
        """
        last_exc: Optional[Exception] = None
        for attempt in range(self._retries + 1):
            try:
                kwargs: Dict[str, Any] = {}
                if headers:
                    kwargs["headers"] = headers
                if data:
                    kwargs["data"] = data
                if proxy:
                    kwargs["proxy"] = proxy

                async with session.request(method.upper(), url, **kwargs) as resp:
                    text = ""
                    try:
                        text = await resp.text()
                    except Exception:
                        text = "<non-text response>"
                    snippet = text[:2048]
                    return {"status": resp.status, "text": text, "snippet": snippet, "url": str(resp.url)}

            except Exception as exc:  # retryable network error
                last_exc = exc
                backoff = (2 ** attempt) + random.random()
                self.logger.debug("request attempt %d failed for %s, sleeping %.2fs: %s", attempt, url, backoff, exc)
                # If proxy manager present, report failure to influence rotation
                if getattr(self, "proxy_mgr", None) is not None and proxy:
                    try:
                        # best-effort: report failure if manager supports it
                        report = getattr(self.proxy_mgr, "report_failure", None)
                        if callable(report):
                            report(proxy)
                    except Exception:
                        pass
                await asyncio.sleep(backoff)
        raise ScanError(f"All retries failed for {url}; last error: {last_exc}")

    def _extract_links(self, base_url: str, html_text: str) -> Set[str]:
        found: Set[str] = set()
        for m in self.URL_EXTRACT_RE.finditer(html_text):
            href = m.group(1)
            # normalize and only include same-host links
            joined = urljoin(base_url, href)
            p_base = urlparse(base_url)
            p_join = urlparse(joined)
            if p_base.netloc == p_join.netloc:
                # strip fragments
                cleaned = joined.split("#")[0]
                found.add(cleaned)
        return found

    async def _crawl(self, root: str, max_depth: int = 1) -> List[str]:
        # very small crawler: BFS up to max_depth, same-domain only
        to_visit = {root}
        visited: Set[str] = set()
        results: List[str] = []
        session = await self._make_session()
        try:
            for depth in range(max_depth):
                if not to_visit:
                    break
                next_round: Set[str] = set()
                for url in list(to_visit):
                    if url in visited:
                        continue
                    try:
                        headers = self.fingerprinter.generate_headers() if self.fingerprinter else None
                        proxy = self.proxy_mgr.pick() if self.proxy_mgr else None
                        res = await self._request_with_retries(session, "GET", url, headers=headers, proxy=proxy)
                        visited.add(url)
                        results.append(url)
                        links = self._extract_links(url, res.get("text", ""))
                        next_round.update(links - visited)
                    except Exception as exc:
                        self.logger.debug("Crawler error for %s: %s", url, exc)
                        visited.add(url)
                to_visit = next_round
        finally:
            await session.close()
        return results

    async def _run_module_on_target(self, module: VulnerabilityModule, target: str, context: Dict[str, Any]) -> None:
        """Run a single module against a target and store findings with evidence."""
        async with self._semaphore:
            session = await self._make_session()
            # Build helper request function for modules
            async def request(
                method: str,
                url: str,
                *,
                headers: Optional[Dict[str, str]] = None,
                payload: Optional[str] = None,
                try_variants: bool = True,
            ) -> Dict[str, Any]:
                # choose proxy and headers for this request
                proxy = self.proxy_mgr.pick() if getattr(self, "proxy_mgr", None) else None
                if self.fingerprinter:
                    hdrs = self.fingerprinter.generate_headers(headers)
                else:
                    hdrs = headers

                # If payload provided and we should try variants, iterate variants from payload manager
                if payload and try_variants:
                    variants = self.payload_mgr.take(payload, limit=20)
                    for variant in variants:
                        # mutate headers slightly between attempts if aggressive
                        if self.fingerprinter and getattr(self.fingerprinter, "aggressiveness", "low") in ("high", "aggressive"):
                            hdrs = self.fingerprinter.generate_headers(headers)
                        try:
                            return await self._request_with_retries(session, method, url, headers=hdrs, proxy=proxy, data=variant)
                        except Exception:
                            # report failures to proxy manager if available and try next variant
                            if getattr(self, "proxy_mgr", None) is not None and proxy:
                                report = getattr(self.proxy_mgr, "report_failure", None)
                                if callable(report):
                                    report(proxy)
                            continue
                    # last attempt without variant
                    return await self._request_with_retries(session, method, url, headers=hdrs, proxy=proxy, data=payload)
                else:
                    return await self._request_with_retries(session, method, url, headers=hdrs, proxy=proxy, data=payload)

            # expose helpers to module via context
            module_context = dict(context)
            module_context.update({"request": request, "payloads": self.payload_mgr, "fingerprinter": self.fingerprinter})

            try:
                findings = await module.run(target, session, module_context)
                # Normalize findings and attach evidence if missing
                if findings:
                    normalized = []
                    for f in findings:
                        if "evidence" not in f:
                            f["evidence"] = None
                        if "payload" not in f:
                            f["payload"] = None
                        if "proxy" not in f and getattr(self, "proxy_mgr", None):
                            f["proxy"] = None
                        normalized.append(f)
                    self.results.setdefault(module.name, []).extend(normalized)
            except Exception as exc:
                self.logger.exception("Module %s failed against %s: %s", getattr(module, "name", module.__class__.__name__), target, exc)
            finally:
                await session.close()

    async def scan(self, target: str, modules: List[VulnerabilityModule], depth: int = 1) -> Dict[str, Any]:
        """Orchestrate crawling and module execution across discovered URLs."""
        self.start_time = datetime.utcnow()
        self.scan_id = self._generate_scan_id()
        self.logger.info("Starting scan %s on %s", self.scan_id, target)

        # warm-up proxy health checks
        if getattr(self, "proxy_mgr", None) is not None:
            try:
                await self.proxy_mgr.ensure_health()
            except Exception:
                self.logger.debug("Proxy health check failed; continuing")

        # Crawl targets (root + discovered) up to configured depth
        max_depth = int(getattr(self.config, "max_depth", depth))
        try:
            urls = await self._crawl(target, max_depth)
            # always include root
            if target not in urls:
                urls.insert(0, target)
        except Exception:
            self.logger.debug("Crawl failed, falling back to single target")
            urls = [target]

        context: Dict[str, Any] = {
            "scan_id": self.scan_id,
            "target": target,
            "config": getattr(self.config, "model_dump", lambda: dict(self.config))(),
            "fingerprinter": self.fingerprinter,
            "proxy_manager": self.proxy_mgr,
            "logger": self.logger,
        }

        tasks: List[asyncio.Task] = []
        for module in modules:
            for url in urls:
                tasks.append(asyncio.create_task(self._run_module_on_target(module, url, context)))

        await asyncio.gather(*tasks)

        self.end_time = datetime.utcnow()
        duration = (self.end_time - self.start_time).total_seconds()
        self.logger.info("Scan %s completed in %.2fs", self.scan_id, duration)
        return {"scan_id": self.scan_id, "results": self.results, "duration": duration}

    def _generate_scan_id(self) -> str:
        import uuid

        return str(uuid.uuid4())[:8]

    async def generate_report(self, fmt: str = "html", output_path: Optional[str] = None) -> None:
        self.logger.info("Generating report fmt=%s output=%s", fmt, output_path)
        # minimal report: write JSON or HTML later
        return
