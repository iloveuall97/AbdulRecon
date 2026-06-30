from __future__ import annotations

from typing import Any, Dict, List

from core.module_loader import load_module_by_name
from core.vulnerability import VulnerabilityModule
from ..base_module import BaseVulnerabilityDetector


class DetectorAdapter(VulnerabilityModule):
    """Adapter to wrap legacy BaseVulnerabilityDetector modules into the
    new VulnerabilityModule interface expected by the scanner.

    The adapter will call detect(url, params) and translate results to the
    standardized form.
    """

    def __init__(self, legacy_instance: BaseVulnerabilityDetector, config: Dict[str, Any], logger: Any) -> None:
        super().__init__(config, logger)
        self.legacy = legacy_instance
        self.name = getattr(legacy_instance, "module_name", legacy_instance.__class__.__name__)

    async def run(self, target: str, client: Any, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        # For the legacy detectors, we attempt to parse query parameters from the URL
        # and feed them to detect(). This is a best-effort shim.
        from urllib.parse import urlparse, parse_qs

        parsed = urlparse(target)
        params = {k: v[0] if v else "" for k, v in parse_qs(parsed.query).items()}
        findings = await self.legacy.detect(target, params)
        # Normalize legacy findings to scanner expected format
        normalized = []
        for f in findings:
            nf = {
                "name": f.get("name", self.name),
                "payload": f.get("payload"),
                "evidence": f.get("description") or f.get("evidence") or None,
                "status": f.get("status"),
                "url": target,
            }
            normalized.append(nf)
        return normalized
