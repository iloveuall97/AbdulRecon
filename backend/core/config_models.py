from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ValidationError


class ScannerConfig(BaseModel):
    concurrency: int = Field(10, ge=1, le=200)
    timeout_seconds: int = Field(15, ge=1)
    retries: int = Field(2, ge=0, le=10)
    delay_between_requests_ms: int = Field(0, ge=0)
    proxies: Optional[List[str]] = None
    user_agents: Optional[List[str]] = None
    respect_robots_txt: bool = Field(False)
    max_depth: int = Field(3, ge=1, le=10)
    fingerprint_aggressiveness: str = Field("low")

    class Config:
        extra = "forbid"


class ModuleConfig(BaseModel):
    name: str
    enabled: bool = True
    options: Optional[Dict[str, Any]] = None


def validate_config(raw: Dict[str, Any]) -> ScannerConfig:
    try:
        return ScannerConfig.model_validate(raw)
    except ValidationError as e:
        # Re-raise with clearer message
        raise
