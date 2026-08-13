"""
Latency statistics tracker and system info collector.
Tracks per-scanner timing across all scan requests.
"""

import platform
import time
import psutil
from collections import deque
from dataclasses import dataclass, field
from typing import Optional

# ── Per-scanner timing record ────────────────────────────────────────────────

@dataclass
class ScanRecord:
    scanner: str
    scanner_type: str          # "input" | "output"
    latency_ms: float
    is_valid: bool
    risk_score: float
    timestamp: float = field(default_factory=time.time)


@dataclass
class RequestRecord:
    request_id: int
    total_ms: float
    input_ms: float
    output_ms: float
    scanner_records: list[ScanRecord]
    message_len: int
    blocked: bool
    timestamp: float = field(default_factory=time.time)


# ── In-memory store ──────────────────────────────────────────────────────────

MAX_HISTORY = 100   # keep last 100 requests in memory

_request_history: deque[RequestRecord] = deque(maxlen=MAX_HISTORY)
_request_counter = 0


def record_request(rec: RequestRecord):
    global _request_counter
    _request_counter += 1
    rec.request_id = _request_counter
    _request_history.append(rec)


def get_stats() -> dict:
    """Aggregate statistics across all stored requests."""
    if not _request_history:
        return _empty_stats()

    reqs = list(_request_history)

    # ── Per-scanner aggregates ──────────────────────────────────────────────
    scanner_stats: dict[str, dict] = {}
    for req in reqs:
        for sr in req.scanner_records:
            key = f"{sr.scanner_type}:{sr.scanner}"
            if key not in scanner_stats:
                scanner_stats[key] = {
                    "scanner": sr.scanner,
                    "type": sr.scanner_type,
                    "calls": 0,
                    "total_ms": 0.0,
                    "min_ms": float("inf"),
                    "max_ms": 0.0,
                    "failures": 0,
                }
            s = scanner_stats[key]
            s["calls"] += 1
            s["total_ms"] += sr.latency_ms
            s["min_ms"] = min(s["min_ms"], sr.latency_ms)
            s["max_ms"] = max(s["max_ms"], sr.latency_ms)
            if not sr.is_valid:
                s["failures"] += 1

    # Compute averages and failure rates
    for s in scanner_stats.values():
        s["avg_ms"] = round(s["total_ms"] / s["calls"], 1) if s["calls"] else 0
        s["min_ms"] = round(s["min_ms"], 1) if s["min_ms"] != float("inf") else 0
        s["max_ms"] = round(s["max_ms"], 1)
        s["failure_rate"] = round(s["failures"] / s["calls"] * 100, 1) if s["calls"] else 0
        del s["total_ms"]

    # ── Request-level aggregates ────────────────────────────────────────────
    totals = [r.total_ms for r in reqs]
    avg_total = round(sum(totals) / len(totals), 1)
    min_total = round(min(totals), 1)
    max_total = round(max(totals), 1)

    # Last 20 requests for the latency chart
    recent = [
        {
            "id": r.request_id,
            "total_ms": round(r.total_ms, 1),
            "input_ms": round(r.input_ms, 1),
            "output_ms": round(r.output_ms, 1),
            "blocked": r.blocked,
            "message_len": r.message_len,
            "ts": round(r.timestamp, 2),
            "scanners": [
                {
                    "scanner": sr.scanner,
                    "type": sr.scanner_type,
                    "ms": round(sr.latency_ms, 1),
                    "valid": sr.is_valid,
                    "score": round(sr.risk_score, 3),
                }
                for sr in r.scanner_records
            ],
        }
        for r in list(reqs)[-20:]
    ]

    return {
        "total_requests": len(reqs),
        "avg_total_ms": avg_total,
        "min_total_ms": min_total,
        "max_total_ms": max_total,
        "scanner_stats": sorted(scanner_stats.values(), key=lambda x: -x["avg_ms"]),
        "recent_requests": recent,
        "system": _system_info(),
        "cache_size": _get_cache_size(),
    }


def _empty_stats() -> dict:
    return {
        "total_requests": 0,
        "avg_total_ms": 0,
        "min_total_ms": 0,
        "max_total_ms": 0,
        "scanner_stats": [],
        "recent_requests": [],
        "system": _system_info(),
        "cache_size": 0,
    }


def _system_info() -> dict:
    try:
        cpu_freq = psutil.cpu_freq()
        freq_ghz = round(cpu_freq.current / 1000, 2) if cpu_freq else None
        freq_max_ghz = round(cpu_freq.max / 1000, 2) if cpu_freq and cpu_freq.max else None
    except Exception:
        freq_ghz = None
        freq_max_ghz = None

    try:
        mem = psutil.virtual_memory()
        ram_total_gb = round(mem.total / (1024 ** 3), 1)
        ram_used_pct = mem.percent
    except Exception:
        ram_total_gb = None
        ram_used_pct = None

    try:
        cpu_pct = psutil.cpu_percent(interval=0.1)
    except Exception:
        cpu_pct = None

    # Detect inference device
    device = "CPU"
    device_detail = platform.processor() or platform.machine()
    try:
        import torch
        if torch.cuda.is_available():
            device = "CUDA"
            device_detail = torch.cuda.get_device_name(0)
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            device = "MPS (Apple Silicon)"
            device_detail = platform.processor()
    except ImportError:
        pass

    return {
        "os": f"{platform.system()} {platform.release()}",
        "python": platform.python_version(),
        "cpu_name": platform.processor() or platform.machine(),
        "cpu_cores_logical": psutil.cpu_count(logical=True),
        "cpu_cores_physical": psutil.cpu_count(logical=False),
        "cpu_freq_ghz": freq_ghz,
        "cpu_freq_max_ghz": freq_max_ghz,
        "cpu_usage_pct": cpu_pct,
        "ram_total_gb": ram_total_gb,
        "ram_used_pct": ram_used_pct,
        "inference_device": device,
        "device_detail": device_detail,
    }


def _get_cache_size() -> int:
    try:
        from backend.scan_engine import _scanner_cache
        return len(_scanner_cache)
    except Exception:
        return 0


def clear_stats():
    _request_history.clear()
    global _request_counter
    _request_counter = 0