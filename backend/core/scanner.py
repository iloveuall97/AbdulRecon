from __future__ import annotations

import asyncio
import logging
import random
from datetime import datetime
from typing import Any, Dict, List, Optional

import aiohttp

from core.vulnerability import VulnerabilityModule


class ScanError(Exception):
    pass


class SecurityScanner:
    """Async security scanning engine.

    Responsibilities:
    - Validate config (via ScannerConfig if provided)
    - Manage concurrency and sessions (aiohttp)
    - Rotate proxies and fingerprints
    - Run VulnerabilityModule instances concurrently and collect findings
    - Provide simple WAF-evasion helpers (header shuffling, retries, payload variants)
    """

    def __init__(self, config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        # Lazy import of heavy config class to avoid hard dependency during import-time
        try:
            from core.config_models import ScannerConfig  # type: ignore
        except Exception:
            ScannerConfig = None  # type: ignore

        if ScannerConfig is not None and not isinstance(config, ScannerConfig):
            try:
                # If the user passed a dict, validate it
                self.config = ScannerConfig.model_validate(config)  # type: ignore
            except Exception:
                # If validation fails or ScannerConfig unavailable, fall back to raw dict
                self.config = config
        else:
            self.config = config

        self.logger = logger or logging.getLogger("SecurityScanner")
        self.scan_id: Optional[str] = None
        self.results: Dict[str, List[Dict[str, Any]]] = {}
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

        # Proxy manager and fingerprint are not mandatory for basic runs; attempt import
        try:
            from core.proxy_manager import ProxyManager  # type: ignore
            from core.fingerprint import RequestFingerprinter  # type: ignore

            self.proxy_mgr = ProxyManager(getattr(self.config, "proxies", None))
            self.fingerprint = RequestFingerprinter(getattr(self.config, "user_agents", None))
        except Exception:
            self.proxy_mgr = None
            self.fingerprint = None

        # Concurrency control: default to 10 if not present in validated config
        self._concurrency = int(getattr(self.config, "concurrency", 10))
        self._semaphore = asyncio.Semaphore(self._concurrency)

        # aiohttp connector limits
        self._connector_limit = int(getattr(self.config, "concurrency", 10))

        # retry policy
        self._retries = int(getattr(self.config, "retries", 2))
        self._timeout_seconds = int(getattr(self.config, "timeout_seconds", 15))

    async def _make_session(self, proxy: Optional[str] = None) -> aiohttp.ClientSession:
        timeout = aiohttp.ClientTimeout(total=self._timeout_seconds)
        connector = aiohttp.TCPConnector(limit_per_host=self._connector_limit, ssl=False)
        session = aiohttp.ClientSession(timeout=timeout, connector=connector)
        # Note: headers will be applied per-request using fingerprint.generate_headers()
        return session

    async def _request_with_retries(
        self,
        session: aiohttp.ClientSession,
        method: str,
        url: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        proxy: Optional[str] = None,
        data: Optional[Any] = None,
    ) -> aiohttp.ClientResponse:
        """Perform an HTTP request with simple retry logic and jitter."""
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

                # Use aiohttp request API (method lowercased)
                async with session.request(method.upper(), url, **kwargs) as resp:
                    # Treat 429 and 5xx as retryable
                    if resp.status == 429 or 500 <= resp.status < 600:
                        last_exc = ScanError(f"Retryable status: {resp.status}")
                        raise last_exc
                    return resp
            except Exception as exc:
                last_exc = exc
                backoff = (2 ** attempt) + random.random()
                self.logger.debug("Request attempt %d failed, sleeping %.2fs: %s", attempt, backoff, exc)
                await asyncio.sleep(backoff)
        # If we get here, all retries failed
        raise ScanError(f"All retries failed for {url}; last error: {last_exc}")

    async def _run_module_on_target(self, module: VulnerabilityModule, target: str, context: Dict[str, Any]) -> None:
        """Execute a single module against a target using concurrency control."""
        async with self._semaphore:
            proxy = None
            if getattr(self, "proxy_mgr", None) is not None:
                proxy = self.proxy_mgr.pick()

            session = await self._make_session(proxy=proxy)
            # Provide client-helpers to the module via context if needed
            # The module should use session + helper functions to make requests
            try:
                findings = await module.run(target, session, context)
                if findings:
                    self.results.setdefault(module.name, []).extend(findings)
            except Exception as exc:
                self.logger.exception("Module %s error on %s: %s", getattr(module, "name", module.__class__.__name__), target, exc)
            finally:
                await session.close()

    async def scan(self, target: str, modules: List[VulnerabilityModule], depth: int = 1) -> Dict[str, Any]:
        """High-level scan orchestration.

        Behavior:
        - warms up proxy health checks (if proxy manager present)
        - constructs a per-scan context including fingerprinter and config snapshot
        - schedules module tasks concurrently using a semaphore
        - returns structured results including scan id and duration
        """
        self.start_time = datetime.utcnow()
        self.scan_id = self._generate_scan_id()
        self.logger.info("Starting scan %s target=%s modules=%d", self.scan_id, target, len(modules))

        # If proxy manager exists, ensure health checks happen
        if getattr(self, "proxy_mgr", None) is not None:
            try:
                await self.proxy_mgr.ensure_health()
            except Exception:
                self.logger.debug("Proxy health check failed or not available; continuing without blocking")

        context: Dict[str, Any] = {
            "scan_id": self.scan_id,
            "target": target,
            "depth": depth,
            "config": getattr(self.config, "model_dump", lambda: dict(self.config))(),
            "fingerprinter": self.fingerprint,
            "proxy_manager": self.proxy_mgr,
            "logger": self.logger,
        }

        # Simple crawl/dispatch: run each module against the root target.
        tasks = [asyncio.create_task(self._run_module_on_target(mod, target, context)) for mod in modules]
        await asyncio.gather(*tasks)

        self.end_time = datetime.utcnow()
        duration = (self.end_time - self.start_time).total_seconds()
        self.logger.info("Scan %s completed in %.2fs", self.scan_id, duration)
        return {"scan_id": self.scan_id, "results": self.results, "duration": duration}

    def _generate_scan_id(self) -> str:
        import uuid

        return str(uuid.uuid4())[:8]

    async def generate_report(self, fmt: str = "html", output_path: Optional[str] = None) -> None:
        """Asynchronous placeholder for report generation (I/O heavy)."""
        self.logger.info("Generating report fmt=%s output=%s", fmt, output_path)
        # Real implementation would render templates and write files
        return
