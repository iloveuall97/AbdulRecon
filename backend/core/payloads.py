from __future__ import annotations

import html
import itertools
import random
from typing import Generator, Iterable, List


def url_encode(s: str) -> str:
    from urllib.parse import quote

    return quote(s, safe="")


def html_entity_encode(s: str) -> str:
    return html.escape(s)


def case_obfuscate(s: str) -> str:
    # Randomize case of letters
    return "".join(c.upper() if random.random() < 0.5 else c.lower() for c in s)


def whitespace_insert(s: str) -> str:
    # Insert random whitespace or comments (simple approach)
    parts = []
    for c in s:
        parts.append(c)
        if random.random() < 0.1:
            parts.append(" ")
    return "".join(parts)


class PayloadManager:
    """Generates payload variants for given payload templates.

    Aggressive mode will produce many variants; modules should limit how many they try.
    """

    def __init__(self, aggressiveness: str = "low") -> None:
        self.aggressiveness = aggressiveness

    def variants(self, payload: str) -> Iterable[str]:
        # Base variants
        funcs = [lambda x: x, url_encode, html_entity_encode, case_obfuscate, whitespace_insert]

        # For aggressive mode, generate combinations and nested encodings
        if self.aggressiveness in ("high", "aggressive"):
            # produce nested encodings and pairwise combinations
            for fcount in range(1, 4):
                for combo in itertools.permutations(funcs, fcount):
                    v = payload
                    for f in combo:
                        v = f(v)
                    yield v
        else:
            # conservative: yield a few straightforward variants
            for f in funcs:
                yield f(payload)

    def take(self, payload: str, limit: int = 10) -> List[str]:
        return list(itertools.islice(self.variants(payload), limit))
