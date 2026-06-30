from __future__ import annotations

import asyncio
from typing import List, Optional, Set
from urllib.parse import urljoin, urlparse

import aiohttp


async def _fetch_text(session: aiohttp.ClientSession, url: str, *, proxy: Optional[str] = None, headers: Optional[dict] = None) -> str:
    try:
        async with session.get(url, proxy=proxy, headers=headers) as resp:
            return await resp.text()
    except Exception:
        return ""


async def crawl_aiohttp(root: str, max_depth: int = 2, *, fingerprinter=None, proxy_mgr=None) -> List[str]:
    """Simple aiohttp-based crawler (same-host BFS).

    Falls back to Playwright for JS-heavy pages if available (best-effort).
    """
    to_visit: Set[str] = {root}
    visited: Set[str] = set()
    results: List[str] = []

    timeout = aiohttp.ClientTimeout(total=15)
    conn = aiohttp.TCPConnector(limit_per_host=10)
    session = aiohttp.ClientSession(timeout=timeout, connector=conn)
    try:
        for _ in range(max_depth):
            if not to_visit:
                break
            next_round: Set[str] = set()
            for url in list(to_visit):
                if url in visited:
                    continue
                headers = fingerprinter.generate_headers() if fingerprinter else None
                proxy = proxy_mgr.pick() if proxy_mgr else None
                text = await _fetch_text(session, url, proxy=proxy, headers=headers)
                visited.add(url)
                results.append(url)
                # Extract simple href links
                for href in _extract_links(url, text):
                    p_root = urlparse(root).netloc
                    p_href = urlparse(href).netloc
                    if p_root == p_href and href not in visited:
                        next_round.add(href)
            to_visit = next_round
    finally:
        await session.close()

    return results


def _extract_links(base_url: str, html_text: str):
    import re
    URL_EXTRACT_RE = re.compile(r"href=[\"']([^\"'#]+)[\"']", re.IGNORECASE)
    links = set()
    for m in URL_EXTRACT_RE.finditer(html_text):
        href = m.group(1)
        joined = urljoin(base_url, href)
        links.add(joined.split('#')[0])
    return links


async def crawl(root: str, max_depth: int = 2, *, fingerprinter=None, proxy_mgr=None, use_playwright: bool = False) -> List[str]:
    """Crawl with aiohttp and fallback to Playwright when use_playwright is True and it's available."""
    urls = await crawl_aiohttp(root, max_depth, fingerprinter=fingerprinter, proxy_mgr=proxy_mgr)
    # If Playwright is desired, try to fetch pages that returned empty text
    if use_playwright:
        try:
            from playwright.async_api import async_playwright

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                enhanced: List[str] = []
                for u in urls:
                    try:
                        await page.goto(u, timeout=10000)
                        content = await page.content()
                        enhanced.append(u)
                        # optionally extract links via DOM (skipped here for simplicity)
                    except Exception:
                        continue
                await browser.close()
                return enhanced or urls
        except Exception:
            # Playwright not installed or failed; return aiohttp results
            return urls
    return urls
