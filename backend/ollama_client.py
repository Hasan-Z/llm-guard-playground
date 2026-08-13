"""
Ollama client — list local models and stream/complete chat messages.
Ollama runs locally at http://localhost:11434 by default.
"""

import json
import httpx
from typing import AsyncGenerator

OLLAMA_BASE = "http://localhost:11434"


async def list_models() -> list[dict]:
    """Return list of locally available Ollama models."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            res = await client.get(f"{OLLAMA_BASE}/api/tags")
            if res.status_code != 200:
                return []
            data = res.json()
            models = data.get("models", [])
            return [
                {
                    "name": m["name"],
                    "size_gb": round(m.get("size", 0) / 1e9, 1),
                    "family": m.get("details", {}).get("family", ""),
                    "params": m.get("details", {}).get("parameter_size", ""),
                }
                for m in models
            ]
    except Exception:
        return []


async def chat_complete(model: str, prompt: str, system: str = "") -> str:
    """
    Non-streaming chat completion via Ollama /api/chat.
    Returns the assistant message text.
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.7},
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        res = await client.post(f"{OLLAMA_BASE}/api/chat", json=payload)
        if res.status_code != 200:
            raise RuntimeError(f"Ollama error {res.status_code}: {res.text[:200]}")
        data = res.json()
        return data["message"]["content"]


async def check_ollama() -> dict:
    """Check if Ollama is running and reachable."""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            res = await client.get(f"{OLLAMA_BASE}/api/tags")
            models = res.json().get("models", [])
            return {"running": True, "model_count": len(models)}
    except Exception as e:
        return {"running": False, "error": str(e)}