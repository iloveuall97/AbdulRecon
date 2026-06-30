from __future__ import annotations

import random
from typing import Dict, List, Optional


DEFAULT_USER_AGENTS = [
    # Aggressive list sample; real usage should expand and rotate frequently
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
]


class RequestFingerprinter:
    def __init__(self, user_agents: Optional[List[str]] = None, aggressiveness: str = "low") -> None:
        self.user_agents = user_agents or DEFAULT_USER_AGENTS
        self.aggressiveness = aggressiveness.lower()

    def _pick_user_agent(self) -> str:
        # Aggressive: pick randomly every request; conservative might reuse
        return random.choice(self.user_agents)

    def _accept_header(self) -> str:
        options = [
            "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "text/html,application/xhtml+xml",
            "*/*",
        ]
        return random.choice(options)

    def _accept_language(self) -> str:
        return random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8", "en;q=0.7", "es-ES,es;q=0.8"])

    def generate_headers(self, base_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers: Dict[str, str] = dict(base_headers or {})
        # Always set or rotate User-Agent
        headers["User-Agent"] = self._pick_user_agent()
        headers.setdefault("Accept", self._accept_header())
        headers.setdefault("Accept-Language", self._accept_language())

        # Aggressive fingerprinting: shuffle/add noise more frequently
        if self.aggressiveness in ("high", "aggressive"):
            # Add X-Forwarded-For 50% of requests
            if random.random() < 0.5:
                headers["X-Forwarded-For"] = ".".join(str(random.randint(1, 254)) for _ in range(4))
            # Add innocuous custom headers occasionally
            if random.random() < 0.3:
                headers[f"X-Guest-ID"] = "%d" % random.randint(1000, 999999)
        else:
            # low aggressiveness: occasional X-Forwarded-For
            if random.random() < 0.1:
                headers["X-Forwarded-For"] = ".".join(str(random.randint(1, 254)) for _ in range(4))

        # Subtle header shuffling
        if self.aggressiveness in ("high", "aggressive") and random.random() < 0.4:
            headers["Accept-Encoding"] = random.choice(["gzip, deflate, br", "gzip, deflate"])  # vary encoding

        return headers
