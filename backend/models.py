from pydantic import BaseModel, field_validator
from typing import Any, Optional


class ScannerConfig(BaseModel):
    name: str
    params: dict[str, Any] = {}


class ScanRequest(BaseModel):
    message: str
    input_scanners: list[ScannerConfig] = []
    output_scanners: list[ScannerConfig] = []
    strict_mode: bool = False


class ScannerResult(BaseModel):
    scanner: str
    is_valid: bool
    risk_score: float
    sanitized_text: Optional[str] = None
    details: Optional[str] = None
    error: Optional[str] = None
    latency_ms: Optional[float] = None    # per-scanner execution time

    @field_validator("is_valid", mode="before")
    @classmethod
    def coerce_is_valid(cls, v):
        """
        LLM-Guard's valid_map can return:
          - bool   True/False  (normal case)
          - float  -1.0 = valid (safe), 1.0 = invalid (flagged)
        """
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return float(v) <= 0.0
        return bool(v)

    @field_validator("risk_score", mode="before")
    @classmethod
    def coerce_risk_score(cls, v):
        try:
            return abs(float(v))
        except (TypeError, ValueError):
            return 0.0


class ScanResponse(BaseModel):
    original_message: str
    sanitized_input: str
    input_results: list[ScannerResult]
    output_results: list[ScannerResult]
    overall_input_valid: bool
    overall_output_valid: bool
    blocked: bool
    scan_duration_ms: float
    input_duration_ms: float = 0.0
    output_duration_ms: float = 0.0
    raw_input_scores: dict[str, float] = {}
    raw_output_scores: dict[str, float] = {}