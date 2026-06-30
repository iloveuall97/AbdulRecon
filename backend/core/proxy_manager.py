from __future__ import annotations

import asyncio
import random
import time
from typing import Dict, List, Optional

import aiohttp


class ProxyManager:
    """Rotates proxies with health checks and temporary blacklisting.

    Behavior:
    - Stores proxies and a health score per proxy
    - `ensure_health()` performs lightweight checks in parallel
    - `pick()` returns a healthy proxy (with some randomness)
    - Repeated failures increase a failure count and can temporarily blacklist proxies
    """

    def __init__(self, proxies: Optional[List[str]] = None, check_url: str = "http://example.com", timeout: int = 5):
        self.proxies: List[str] = list(proxies or [])
        self.check_url = check_url
        self.timeout = timeout
        self._failure_counts: Dict[str, int] = {p: 0 for p in self.proxies}
        self._blacklist_until: Dict[str, float] = {}
        self._lock = asyncio.Lock()

    async def _check_proxy(self, proxy: str) -> bool:
        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as s:
                async with s.get(self.check_url, proxy=proxy) as r:
                    return r.status < 400
        except Exception:
            return False

    async def ensure_health(self) -> None:
        tasks = [self._check_and_update(p) for p in self.proxies]
        await asyncio.gather(*tasks)

    async def _check_and_update(self, proxy: str) -> None:
        ok = await self._check_proxy(proxy)
        async with self._lock:
            if ok:
                self._failure_counts[proxy] = 0
                self._blacklist_until.pop(proxy, None)
            else:
                self._failure_counts[proxy] = self._failure_counts.get(proxy, 0) + 1
                # simple backoff: blacklist for 2^(failures) seconds
                backoff = 2 ** self._failure_counts[proxy]
                self._blacklist_until[proxy] = time.time() + backoff

    def add(self, proxy: str) -> None:
        if proxy not in self.proxies:
            self.proxies.append(proxy)
            self._failure_counts[proxy] = 0

    def pick(self) -> Optional[str]:
        # Filter out blacklisted proxies
        now = time.time()
        candidates = [p for p in self.proxies if self._blacklist_until.get(p, 0) <= now]
        if not candidates:
            # if all blacklisted, return a random proxy (caller should handle errors)
            return random.choice(self.proxies) if self.proxies else None
        # Prefer lower-failure proxies
        candidates.sort(key=lambda p: self._failure_counts.get(p, 0))
        # Return randomly among top 3 to distribute load
        top = candidates[:3] if len(candidates) >= 3 else candidates
        return random.choice(top) if top else None
