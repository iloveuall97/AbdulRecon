from __future__ import annotations

import asyncio
import time
from typing import Any, List, Optional

from core.proxy_manager import ProxyManager


class StealthProxy:
    """Thin stealth wrapper around ProxyManager exposing a stable API for scanner.

    Methods:
    - pick(): return a proxy URL or None
    - report_failure(proxy): record a failed proxy attempt
    - add(proxy): add proxy to pool
    - ensure_health(): run health checks across proxies
    """

    def __init__(self, proxies: Optional[List[str]] = None):
        self._mgr = ProxyManager(proxies)

    def pick(self) -> Optional[str]:
        return self._mgr.pick()

    def report_failure(self, proxy: str) -> None:
        # record failure by calling internal backoff increment
        # best-effort: call _check_and_update with failure semantics by increasing failure count
        try:
            # increase failure count and set blacklist quickly
            # this mirrors logic in ProxyManager._check_and_update
            self._mgr._failure_counts[proxy] = self._mgr._failure_counts.get(proxy, 0) + 1
            backoff = 2 ** self._mgr._failure_counts[proxy]
            self._mgr._blacklist_until[proxy] = time.time() + backoff
        except Exception:
            pass

    def add(self, proxy: str) -> None:
        return self._mgr.add(proxy)

    async def ensure_health(self) -> None:
        await self._mgr.ensure_health()
