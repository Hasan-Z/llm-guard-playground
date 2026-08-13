"""
Scan engine: caches LLM-Guard scanner instances so models are loaded only once.
"""

import time
import traceback
from typing import Any

from backend.models import ScannerConfig, ScannerResult

# ── Global scanner cache ─────────────────────────────────────────────────────
# Key: (prefix, scanner_id, frozenset of params items)
# Value: instantiated scanner object
_scanner_cache: dict[tuple, Any] = {}

# We keep a single shared Vault for Anonymize <-> Deanonymize pairing
_shared_vault = None

def _get_vault():
    global _shared_vault
    if _shared_vault is None:
        from llm_guard.vault import Vault
        _shared_vault = Vault()
    return _shared_vault


def _cache_key(prefix: str, name: str, params: dict) -> tuple:
    try:
        params_frozen = frozenset(
            (k, v if not isinstance(v, list) else tuple(v))
            for k, v in sorted(params.items())
        )
    except Exception:
        params_frozen = frozenset()
    return (prefix, name, params_frozen)


# ── Input scanner factory ────────────────────────────────────────────────────

def _build_input_scanner(cfg: ScannerConfig):
    name = cfg.name
    p = cfg.params

    key = _cache_key("in", name, p)
    if key in _scanner_cache:
        return _scanner_cache[key]

    scanner = _create_input_scanner(name, p)
    if scanner is not None:
        _scanner_cache[key] = scanner
    return scanner


def _create_input_scanner(name: str, p: dict):
    if name == "Anonymize":
        from llm_guard.input_scanners import Anonymize
        return Anonymize(vault=_get_vault())

    if name == "BanCode":
        from llm_guard.input_scanners import BanCode
        return BanCode()

    if name == "BanCompetitors":
        from llm_guard.input_scanners import BanCompetitors
        competitors = _csv_to_list(p.get("competitors", ""))
        if not competitors:
            return None
        return BanCompetitors(competitors=competitors)

    if name == "BanSubstrings":
        from llm_guard.input_scanners import BanSubstrings
        substrings = _csv_to_list(p.get("substrings", ""))
        if not substrings:
            return None
        return BanSubstrings(substrings=substrings)

    if name == "BanTopics":
        from llm_guard.input_scanners import BanTopics
        topics = _csv_to_list(p.get("topics", ""))
        if not topics:
            return None
        return BanTopics(topics=topics)

    if name == "Code":
        from llm_guard.input_scanners import Code
        languages = _csv_to_list(p.get("languages", "Python,JavaScript,SQL"))
        return Code(languages=languages)

    if name == "Gibberish":
        from llm_guard.input_scanners import Gibberish
        return Gibberish()

    if name == "InvisibleText":
        from llm_guard.input_scanners import InvisibleText
        return InvisibleText()

    if name == "Language":
        from llm_guard.input_scanners import Language
        valid_languages = _csv_to_list(p.get("valid_languages", "en"))
        return Language(valid_languages=valid_languages)

    if name == "PromptInjection":
        from llm_guard.input_scanners import PromptInjection
        return PromptInjection()

    if name == "Regex":
        from llm_guard.input_scanners import Regex
        patterns = _csv_to_list(p.get("patterns", ""))
        if not patterns:
            return None
        return Regex(patterns=patterns)

    if name == "Secrets":
        from llm_guard.input_scanners import Secrets
        return Secrets()

    if name == "Sentiment":
        from llm_guard.input_scanners import Sentiment
        threshold = float(p.get("threshold", -0.1))
        return Sentiment(threshold=threshold)

    if name == "TokenLimit":
        from llm_guard.input_scanners import TokenLimit
        limit = int(p.get("limit", 512))
        return TokenLimit(limit=limit)

    if name == "Toxicity":
        from llm_guard.input_scanners import Toxicity
        threshold = float(p.get("threshold", 0.5))
        return Toxicity(threshold=threshold)

    return None


# ── Output scanner factory ───────────────────────────────────────────────────

def _build_output_scanner(cfg: ScannerConfig):
    name = cfg.name
    p = cfg.params

    key = _cache_key("out", name, p)
    if key in _scanner_cache:
        return _scanner_cache[key]

    scanner = _create_output_scanner(name, p)
    if scanner is not None:
        _scanner_cache[key] = scanner
    return scanner


def _create_output_scanner(name: str, p: dict):
    if name == "BanCode":
        from llm_guard.output_scanners import BanCode
        return BanCode()

    if name == "BanCompetitors":
        from llm_guard.output_scanners import BanCompetitors
        competitors = _csv_to_list(p.get("competitors", ""))
        if not competitors:
            return None
        return BanCompetitors(competitors=competitors)

    if name == "BanSubstrings":
        from llm_guard.output_scanners import BanSubstrings
        substrings = _csv_to_list(p.get("substrings", ""))
        if not substrings:
            return None
        return BanSubstrings(substrings=substrings)

    if name == "BanTopics":
        from llm_guard.output_scanners import BanTopics
        topics = _csv_to_list(p.get("topics", ""))
        if not topics:
            return None
        return BanTopics(topics=topics)

    if name == "Bias":
        from llm_guard.output_scanners import Bias
        return Bias()

    if name == "Code":
        from llm_guard.output_scanners import Code
        languages = _csv_to_list(p.get("languages", "Python,JavaScript,SQL"))
        return Code(languages=languages)

    if name == "Deanonymize":
        from llm_guard.output_scanners import Deanonymize
        return Deanonymize(vault=_get_vault())

    if name == "JSON":
        from llm_guard.output_scanners import JSON
        return JSON()

    if name == "Language":
        from llm_guard.output_scanners import Language
        valid_languages = _csv_to_list(p.get("valid_languages", "en"))
        return Language(valid_languages=valid_languages)

    if name == "LanguageSame":
        from llm_guard.output_scanners import LanguageSame
        return LanguageSame()

    if name == "MaliciousURLs":
        from llm_guard.output_scanners import MaliciousURLs
        return MaliciousURLs()

    if name == "NoRefusal":
        from llm_guard.output_scanners import NoRefusal
        return NoRefusal()

    if name == "ReadingTime":
        from llm_guard.output_scanners import ReadingTime
        max_time = float(p.get("max_time", 5))
        return ReadingTime(max_time=max_time)

    if name == "FactualConsistency":
        from llm_guard.output_scanners import FactualConsistency
        return FactualConsistency()

    if name == "Gibberish":
        from llm_guard.output_scanners import Gibberish
        return Gibberish()

    if name == "Regex":
        from llm_guard.output_scanners import Regex
        patterns = _csv_to_list(p.get("patterns", ""))
        if not patterns:
            return None
        return Regex(patterns=patterns)

    if name == "Relevance":
        from llm_guard.output_scanners import Relevance
        return Relevance()

    if name == "Sensitive":
        from llm_guard.output_scanners import Sensitive
        return Sensitive()

    if name == "Sentiment":
        from llm_guard.output_scanners import Sentiment
        threshold = float(p.get("threshold", -0.1))
        return Sentiment(threshold=threshold)

    if name == "Toxicity":
        from llm_guard.output_scanners import Toxicity
        threshold = float(p.get("threshold", 0.5))
        return Toxicity(threshold=threshold)

    if name == "URLReachability":
        from llm_guard.output_scanners import URLReachability
        return URLReachability()

    return None


# ── Main scan function ───────────────────────────────────────────────────────

def run_scan(
    message: str,
    input_scanner_configs: list[ScannerConfig],
    output_scanner_configs: list[ScannerConfig],
    strict_mode: bool = False,
) -> dict[str, Any]:
    from llm_guard import scan_prompt, scan_output
    from backend.stats import record_request, RequestRecord, ScanRecord

    start = time.perf_counter()

    input_results: list[ScannerResult] = []
    output_results: list[ScannerResult] = []
    scanner_records: list[ScanRecord] = []
    sanitized_input = message
    blocked = False

    # ── INPUT SCANNING ──────────────────────────────────────────────────────
    built_input_scanners = []
    scanner_names_in = []

    for cfg in input_scanner_configs:
        try:
            scanner = _build_input_scanner(cfg)
            if scanner is not None:
                built_input_scanners.append(scanner)
                scanner_names_in.append(cfg.name)
        except Exception as e:
            input_results.append(ScannerResult(
                scanner=cfg.name,
                is_valid=False,
                risk_score=0.0,
                error=f"Failed to initialize: {str(e)}",
            ))

    input_start = time.perf_counter()

    if built_input_scanners:
        try:
            # Run each scanner individually to capture per-scanner latency
            current_text = message
            for scanner_name, scanner_obj in zip(scanner_names_in, built_input_scanners):
                sc_start = time.perf_counter()
                sanitized_input, input_scores, input_valid_map = scan_prompt(
                    [scanner_obj], current_text
                )
                sc_ms = (time.perf_counter() - sc_start) * 1000

                raw_score = input_scores.get(scanner_name, 0.0)
                raw_valid = input_valid_map.get(scanner_name, True)
                score    = abs(float(raw_score))
                is_valid = _normalise_valid(raw_valid)
                detail   = _build_detail(scanner_name, score, is_valid, current_text, sanitized_input)

                input_results.append(ScannerResult(
                    scanner=scanner_name,
                    is_valid=is_valid,
                    risk_score=round(score, 4),
                    sanitized_text=sanitized_input if sanitized_input != current_text else None,
                    details=detail,
                    latency_ms=round(sc_ms, 1),
                ))

                scanner_records.append(ScanRecord(
                    scanner=scanner_name,
                    scanner_type="input",
                    latency_ms=sc_ms,
                    is_valid=is_valid,
                    risk_score=score,
                ))

                # pass sanitized text down the pipeline
                current_text = sanitized_input

                if strict_mode and not is_valid:
                    blocked = True
                    break

        except Exception as e:
            input_results.append(ScannerResult(
                scanner="scan_prompt",
                is_valid=False,
                risk_score=0.0,
                error=f"Scan failed: {traceback.format_exc()}",
            ))

    input_ms = (time.perf_counter() - input_start) * 1000

    # ── OUTPUT SCANNING ─────────────────────────────────────────────────────
    output_text = sanitized_input
    output_start = time.perf_counter()

    if output_scanner_configs and not blocked:
        built_output_scanners = []
        scanner_names_out = []

        for cfg in output_scanner_configs:
            try:
                scanner = _build_output_scanner(cfg)
                if scanner is not None:
                    built_output_scanners.append(scanner)
                    scanner_names_out.append(cfg.name)
            except Exception as e:
                output_results.append(ScannerResult(
                    scanner=cfg.name,
                    is_valid=False,
                    risk_score=0.0,
                    error=f"Failed to initialize: {str(e)}",
                ))

        if built_output_scanners:
            try:
                current_out = output_text
                for scanner_name, scanner_obj in zip(scanner_names_out, built_output_scanners):
                    sc_start = time.perf_counter()
                    sanitized_output, output_scores, output_valid_map = scan_output(
                        [scanner_obj], message, current_out
                    )
                    sc_ms = (time.perf_counter() - sc_start) * 1000

                    raw_score = output_scores.get(scanner_name, 0.0)
                    raw_valid = output_valid_map.get(scanner_name, True)
                    score    = abs(float(raw_score))
                    is_valid = _normalise_valid(raw_valid)
                    detail   = _build_detail(scanner_name, score, is_valid, current_out, sanitized_output)

                    output_results.append(ScannerResult(
                        scanner=scanner_name,
                        is_valid=is_valid,
                        risk_score=round(score, 4),
                        sanitized_text=sanitized_output if sanitized_output != current_out else None,
                        details=detail,
                        latency_ms=round(sc_ms, 1),
                    ))

                    scanner_records.append(ScanRecord(
                        scanner=scanner_name,
                        scanner_type="output",
                        latency_ms=sc_ms,
                        is_valid=is_valid,
                        risk_score=score,
                    ))

                    current_out = sanitized_output

                    if strict_mode and not is_valid:
                        blocked = True
                        break

            except Exception as e:
                output_results.append(ScannerResult(
                    scanner="scan_output",
                    is_valid=False,
                    risk_score=0.0,
                    error=f"Scan failed: {traceback.format_exc()}",
                ))

    output_ms = (time.perf_counter() - output_start) * 1000
    elapsed_ms = (time.perf_counter() - start) * 1000

    overall_input_valid  = all(r.is_valid for r in input_results  if not r.error)
    overall_output_valid = all(r.is_valid for r in output_results if not r.error)

    # Record to stats store
    record_request(RequestRecord(
        request_id=0,  # assigned inside record_request
        total_ms=elapsed_ms,
        input_ms=input_ms,
        output_ms=output_ms,
        scanner_records=scanner_records,
        message_len=len(message),
        blocked=blocked,
    ))

    return {
        "original_message":    message,
        "sanitized_input":     sanitized_input,
        "input_results":       [r.model_dump() for r in input_results],
        "output_results":      [r.model_dump() for r in output_results],
        "overall_input_valid": overall_input_valid,
        "overall_output_valid":overall_output_valid,
        "blocked":             blocked,
        "scan_duration_ms":    round(elapsed_ms, 2),
        "input_duration_ms":   round(input_ms, 2),
        "output_duration_ms":  round(output_ms, 2),
        "raw_input_scores":    {},
        "raw_output_scores":   {},
    }


# ── Helpers ──────────────────────────────────────────────────────────────────

def _normalise_valid(v) -> bool:
    """
    LLM-Guard's valid_map values can be:
      bool  - normal True/False
      float - -1.0 means valid (safe), 1.0 means invalid (flagged)
    """
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return float(v) <= 0.0
    return bool(v)


def _csv_to_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [v.strip() for v in value if v.strip()]
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return []


def _build_detail(scanner_name: str, score: float, is_valid: bool, original: str, sanitized: str) -> str:
    changed = original != sanitized

    messages = {
        "Anonymize":          f"PII {'detected and redacted' if changed else 'not detected'}.",
        "BanCode":            f"Code {'detected' if not is_valid else 'not detected'} in text.",
        "BanCompetitors":     f"Competitor mention {'found' if not is_valid else 'not found'}.",
        "BanSubstrings":      f"Banned substring {'found' if not is_valid else 'not found'}.",
        "BanTopics":          f"Banned topic {'detected' if not is_valid else 'not detected'} (score: {score:.3f}).",
        "Code":               f"Programming code {'detected' if not is_valid else 'not detected'}.",
        "Gibberish":          f"Text {'appears gibberish' if not is_valid else 'appears coherent'} (score: {score:.3f}).",
        "InvisibleText":      f"Invisible/hidden characters {'found' if not is_valid else 'not found'}.",
        "Language":           f"Language {'not in allowed list' if not is_valid else 'is allowed'} (score: {score:.3f}).",
        "PromptInjection":    f"Prompt injection {'detected' if not is_valid else 'not detected'} (score: {score:.3f}).",
        "Regex":              f"Regex pattern {'matched' if not is_valid else 'not matched'}.",
        "Secrets":            f"Secret/credential {'found' if not is_valid else 'not found'}.",
        "Sentiment":          f"Sentiment score: {score:.3f}. {'Negative sentiment detected.' if not is_valid else 'Sentiment acceptable.'}",
        "TokenLimit":         f"Token count {'exceeds limit' if not is_valid else 'within limit'} (score: {score:.3f}).",
        "Toxicity":           f"Toxicity score: {score:.3f}. {'Toxic content detected.' if not is_valid else 'Content acceptable.'}",
        "Bias":               f"Bias score: {score:.3f}. {'Bias detected.' if not is_valid else 'No significant bias.'}",
        "Deanonymize":        f"PII {'restored from vault' if changed else 'no vault data to restore'}.",
        "JSON":               f"Output {'is not valid JSON' if not is_valid else 'is valid JSON'}.",
        "LanguageSame":       f"Output language {'differs from input' if not is_valid else 'matches input'}.",
        "MaliciousURLs":      f"Malicious URL {'detected' if not is_valid else 'not detected'} (score: {score:.3f}).",
        "NoRefusal":          f"LLM {'appears to have refused' if not is_valid else 'did not refuse'} (score: {score:.3f}).",
        "ReadingTime":        f"Reading time {'exceeds limit' if not is_valid else 'within limit'} (score: {score:.3f}).",
        "FactualConsistency": f"Factual consistency score: {score:.3f}. {'Inconsistency detected.' if not is_valid else 'Consistent.'}",
        "Relevance":          f"Relevance score: {score:.3f}. {'Output may be off-topic.' if not is_valid else 'Output is relevant.'}",
        "Sensitive":          f"Sensitive data {'detected' if not is_valid else 'not detected'} (score: {score:.3f}).",
        "URLReachability":    f"URLs {'unreachable' if not is_valid else 'reachable'} (score: {score:.3f}).",
    }

    return messages.get(scanner_name, f"{'PASS' if is_valid else 'FAIL'} — score: {score:.3f}")