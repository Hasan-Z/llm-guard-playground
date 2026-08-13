"""
Registry of all LLM-Guard scanners with metadata, default params, and UI hints.
"""

INPUT_SCANNERS = [
    {
        "id": "Anonymize",
        "label": "Anonymize",
        "description": "Detects and redacts PII (names, emails, phone numbers, credit cards, etc.) from the prompt using NER models.",
        "heavy": True,
        "configurable": False,
        "params": {},
    },
    {
        "id": "BanCode",
        "label": "Ban Code",
        "description": "Detects and blocks code snippets in the input prompt.",
        "heavy": False,
        "configurable": False,
        "params": {},
    },
    {
        "id": "BanCompetitors",
        "label": "Ban Competitors",
        "description": "Detects mentions of competitor names in the prompt.",
        "heavy": False,
        "configurable": True,
        "config_fields": [
            {
                "key": "competitors",
                "label": "Competitor names (comma-separated)",
                "type": "textarea",
                "placeholder": "OpenAI, Google, Microsoft",
            }
        ],
        "params": {"competitors": []},
    },
    {
        "id": "BanSubstrings",
        "label": "Ban Substrings",
        "description": "Blocks prompts containing specific forbidden substrings or words.",
        "heavy": False,
        "configurable": True,
        "config_fields": [
            {
                "key": "substrings",
                "label": "Banned words/phrases (comma-separated)",
                "type": "textarea",
                "placeholder": "badword, forbidden phrase, secret",
            }
        ],
        "params": {"substrings": []},
    },
    {
        "id": "BanTopics",
        "label": "Ban Topics",
        "description": "Uses a zero-shot classifier to detect and block prompts related to specific topics.",
        "heavy": True,
        "configurable": True,
        "config_fields": [
            {
                "key": "topics",
                "label": "Banned topics (comma-separated)",
                "type": "textarea",
                "placeholder": "violence, politics, weapons",
            }
        ],
        "params": {"topics": []},
    },
    {
        "id": "Code",
        "label": "Code Detector",
        "description": "Detects programming code in the prompt using language detection.",
        "heavy": False,
        "configurable": True,
        "config_fields": [
            {
                "key": "languages",
                "label": "Languages to detect (comma-separated)",
                "type": "text",
                "placeholder": "Python, JavaScript, SQL",
            }
        ],
        "params": {"languages": ["Python", "JavaScript", "SQL"]},
    },
    {
        "id": "Gibberish",
        "label": "Gibberish",
        "description": "Detects nonsensical or gibberish text that may be used to confuse the LLM.",
        "heavy": True,
        "configurable": False,
        "params": {},
    },
    {
        "id": "InvisibleText",
        "label": "Invisible Text",
        "description": "Detects hidden/invisible Unicode characters that may carry hidden instructions.",
        "heavy": False,
        "configurable": False,
        "params": {},
    },
    {
        "id": "Language",
        "label": "Language Filter",
        "description": "Restricts the prompt to specific allowed languages.",
        "heavy": False,
        "configurable": True,
        "config_fields": [
            {
                "key": "valid_languages",
                "label": "Allowed language codes (comma-separated)",
                "type": "text",
                "placeholder": "en, tr, de",
            }
        ],
        "params": {"valid_languages": ["en"]},
    },
    {
        "id": "PromptInjection",
        "label": "Prompt Injection",
        "description": "Detects prompt injection attacks — attempts to hijack LLM instructions.",
        "heavy": True,
        "configurable": False,
        "params": {},
    },
    {
        "id": "Regex",
        "label": "Regex Filter",
        "description": "Blocks prompts matching a custom regular expression pattern.",
        "heavy": False,
        "configurable": True,
        "config_fields": [
            {
                "key": "patterns",
                "label": "Regex patterns (comma-separated)",
                "type": "text",
                "placeholder": r"\b\d{16}\b, \bpassword\b",
            }
        ],
        "params": {"patterns": []},
    },
    {
        "id": "Secrets",
        "label": "Secrets Detection",
        "description": "Detects secrets like API keys, tokens, passwords, and credentials in the prompt.",
        "heavy": False,
        "configurable": False,
        "params": {},
    },
    {
        "id": "Sentiment",
        "label": "Sentiment",
        "description": "Detects highly negative sentiment in the prompt. Configurable threshold.",
        "heavy": False,
        "configurable": True,
        "config_fields": [
            {
                "key": "threshold",
                "label": "Negativity threshold (0.0 – 1.0)",
                "type": "slider",
                "min": 0.0,
                "max": 1.0,
                "step": 0.05,
                "default": 0.5,
            }
        ],
        "params": {"threshold": -0.1},
    },
    {
        "id": "TokenLimit",
        "label": "Token Limit",
        "description": "Enforces a maximum token count on the prompt.",
        "heavy": False,
        "configurable": True,
        "config_fields": [
            {
                "key": "limit",
                "label": "Max tokens",
                "type": "number",
                "min": 1,
                "max": 8192,
                "default": 512,
            }
        ],
        "params": {"limit": 512},
    },
    {
        "id": "Toxicity",
        "label": "Toxicity",
        "description": "Detects toxic, hateful, or abusive language in the prompt using a classifier.",
        "heavy": True,
        "configurable": True,
        "config_fields": [
            {
                "key": "threshold",
                "label": "Toxicity threshold (0.0 – 1.0)",
                "type": "slider",
                "min": 0.0,
                "max": 1.0,
                "step": 0.05,
                "default": 0.5,
            }
        ],
        "params": {"threshold": 0.5},
    },
]

OUTPUT_SCANNERS = [
    {
        "id": "BanCode",
        "label": "Ban Code",
        "description": "Detects and blocks code snippets in the LLM output.",
        "heavy": False,
        "configurable": False,
        "params": {},
    },
    {
        "id": "BanCompetitors",
        "label": "Ban Competitors",
        "description": "Detects competitor mentions in the LLM output.",
        "heavy": False,
        "configurable": True,
        "config_fields": [
            {
                "key": "competitors",
                "label": "Competitor names (comma-separated)",
                "type": "textarea",
                "placeholder": "OpenAI, Google, Microsoft",
            }
        ],
        "params": {"competitors": []},
    },
    {
        "id": "BanSubstrings",
        "label": "Ban Substrings",
        "description": "Blocks output containing forbidden substrings.",
        "heavy": False,
        "configurable": True,
        "config_fields": [
            {
                "key": "substrings",
                "label": "Banned words/phrases (comma-separated)",
                "type": "textarea",
                "placeholder": "badword, forbidden phrase",
            }
        ],
        "params": {"substrings": []},
    },
    {
        "id": "BanTopics",
        "label": "Ban Topics",
        "description": "Detects and blocks output related to specific banned topics.",
        "heavy": True,
        "configurable": True,
        "config_fields": [
            {
                "key": "topics",
                "label": "Banned topics (comma-separated)",
                "type": "textarea",
                "placeholder": "violence, politics",
            }
        ],
        "params": {"topics": []},
    },
    {
        "id": "Bias",
        "label": "Bias Detection",
        "description": "Detects biased or discriminatory content in the LLM output.",
        "heavy": True,
        "configurable": False,
        "params": {},
    },
    {
        "id": "Code",
        "label": "Code Detector",
        "description": "Detects programming code in the output.",
        "heavy": False,
        "configurable": True,
        "config_fields": [
            {
                "key": "languages",
                "label": "Languages to detect (comma-separated)",
                "type": "text",
                "placeholder": "Python, JavaScript, SQL",
            }
        ],
        "params": {"languages": ["Python", "JavaScript", "SQL"]},
    },
    {
        "id": "Deanonymize",
        "label": "Deanonymize",
        "description": "Reverses anonymization — restores original PII from a vault (pair with Anonymize input scanner).",
        "heavy": False,
        "configurable": False,
        "params": {},
    },
    {
        "id": "JSON",
        "label": "JSON Validator",
        "description": "Validates that the output is valid JSON (useful when expecting structured output).",
        "heavy": False,
        "configurable": False,
        "params": {},
    },
    {
        "id": "Language",
        "label": "Language Filter",
        "description": "Ensures the output is in one of the specified allowed languages.",
        "heavy": False,
        "configurable": True,
        "config_fields": [
            {
                "key": "valid_languages",
                "label": "Allowed language codes (comma-separated)",
                "type": "text",
                "placeholder": "en, tr",
            }
        ],
        "params": {"valid_languages": ["en"]},
    },
    {
        "id": "LanguageSame",
        "label": "Language Same",
        "description": "Ensures the output language matches the input language.",
        "heavy": False,
        "configurable": False,
        "params": {},
    },
    {
        "id": "MaliciousURLs",
        "label": "Malicious URLs",
        "description": "Detects malicious or phishing URLs in the output using a classifier.",
        "heavy": True,
        "configurable": False,
        "params": {},
    },
    {
        "id": "NoRefusal",
        "label": "No Refusal",
        "description": "Detects if the LLM refused to answer the question (useful for compliance).",
        "heavy": True,
        "configurable": False,
        "params": {},
    },
    {
        "id": "ReadingTime",
        "label": "Reading Time",
        "description": "Enforces a maximum estimated reading time on the output.",
        "heavy": False,
        "configurable": True,
        "config_fields": [
            {
                "key": "max_time",
                "label": "Max reading time (minutes)",
                "type": "number",
                "min": 0.5,
                "max": 30,
                "default": 5,
            }
        ],
        "params": {"max_time": 5},
    },
    {
        "id": "FactualConsistency",
        "label": "Factual Consistency",
        "description": "Checks if the output is factually consistent with the input/prompt.",
        "heavy": True,
        "configurable": False,
        "params": {},
    },
    {
        "id": "Gibberish",
        "label": "Gibberish",
        "description": "Detects nonsensical or gibberish output from the LLM.",
        "heavy": True,
        "configurable": False,
        "params": {},
    },
    {
        "id": "Regex",
        "label": "Regex Filter",
        "description": "Blocks output matching a custom regular expression pattern.",
        "heavy": False,
        "configurable": True,
        "config_fields": [
            {
                "key": "patterns",
                "label": "Regex patterns (comma-separated)",
                "type": "text",
                "placeholder": r"\b\d{16}\b",
            }
        ],
        "params": {"patterns": []},
    },
    {
        "id": "Relevance",
        "label": "Relevance",
        "description": "Checks if the output is relevant to the input prompt using semantic similarity.",
        "heavy": True,
        "configurable": False,
        "params": {},
    },
    {
        "id": "Sensitive",
        "label": "Sensitive Data",
        "description": "Detects sensitive data (PII, financial info, health data) in the output.",
        "heavy": True,
        "configurable": False,
        "params": {},
    },
    {
        "id": "Sentiment",
        "label": "Sentiment",
        "description": "Detects highly negative sentiment in the LLM output.",
        "heavy": False,
        "configurable": True,
        "config_fields": [
            {
                "key": "threshold",
                "label": "Negativity threshold (0.0 – 1.0)",
                "type": "slider",
                "min": 0.0,
                "max": 1.0,
                "step": 0.05,
                "default": 0.5,
            }
        ],
        "params": {"threshold": -0.1},
    },
    {
        "id": "Toxicity",
        "label": "Toxicity",
        "description": "Detects toxic or abusive language in the LLM output.",
        "heavy": True,
        "configurable": True,
        "config_fields": [
            {
                "key": "threshold",
                "label": "Toxicity threshold (0.0 – 1.0)",
                "type": "slider",
                "min": 0.0,
                "max": 1.0,
                "step": 0.05,
                "default": 0.5,
            }
        ],
        "params": {"threshold": 0.5},
    },
    {
        "id": "URLReachability",
        "label": "URL Reachability",
        "description": "Checks if URLs in the output are reachable (live HTTP check).",
        "heavy": False,
        "configurable": False,
        "params": {},
    },
]


def get_scanner_meta(scanner_id: str, scanner_type: str = "input") -> dict:
    registry = INPUT_SCANNERS if scanner_type == "input" else OUTPUT_SCANNERS
    for s in registry:
        if s["id"] == scanner_id:
            return s
    return {}