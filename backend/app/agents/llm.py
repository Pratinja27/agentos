import json
import re

import httpx

from ..config import settings


def llm_mode() -> str:
    return "gemini" if settings.gemini_api_key else "demo"


def complete_json(prompt: str, fallback: dict) -> dict:
    if not settings.gemini_api_key:
        return fallback
    try:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{settings.gemini_model}:generateContent"
        )
        payload = {
            "contents": [{"parts": [{"text": prompt + "\nReturn only valid JSON."}]}],
            "generationConfig": {"temperature": 0.4},
        }
        response = httpx.post(
            url,
            params={"key": settings.gemini_api_key},
            json=payload,
            timeout=40,
        )
        response.raise_for_status()
        text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        match = re.search(r"\{[\s\S]*\}", text)
        return json.loads(match.group(0)) if match else fallback
    except Exception:
        return fallback
