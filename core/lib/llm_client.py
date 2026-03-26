"""
LLM Client Module — OpenRouter API

Sends SRS review prompts to LLMs via OpenRouter's OpenAI-compatible API.
Default model: anthropic/claude-sonnet-4-20250514 (Claude).
Requires OPENROUTER_API_KEY environment variable or constructor param.
"""

import json
import logging
import os
import re
from typing import Optional

import httpx

log = logging.getLogger("srs_llm_client")

# Regex to extract JSON from markdown-fenced responses
_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*\n?(.*?)\n?```", re.DOTALL)

DEFAULT_MODEL = "anthropic/claude-sonnet-4-20250514"
DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"


def _extract_json(text: str) -> str:
    """Extract JSON from an LLM response, stripping markdown fences.

    LLMs often wrap JSON in ```json ... ``` blocks. This function
    extracts the inner JSON content. Falls back to raw text if no fence.
    """
    match = _JSON_FENCE_RE.search(text)
    if match:
        return match.group(1).strip()

    # Try to find raw JSON object
    text = text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]

    return text


class LLMClient:
    """OpenRouter LLM client for SRS review.

    Uses the OpenAI-compatible chat completions endpoint.
    API key is read from constructor param or OPENROUTER_API_KEY env var.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        base_url: str = DEFAULT_BASE_URL,
    ):
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        self.model = model
        self.base_url = base_url.rstrip("/")

        if not self.api_key:
            log.warning(
                "No OpenRouter API key provided. "
                "Set OPENROUTER_API_KEY env var or pass api_key to constructor."
            )

    def generate_content(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        timeout: int = 300,
    ) -> str:
        """Send prompt to OpenRouter and return the response text.

        Args:
            prompt: The prompt text (with SRS content already injected).
            system_instruction: Optional system message prepended.
            timeout: Max seconds to wait for the API response.

        Returns:
            Raw JSON string extracted from the LLM response.
        """
        if not self.api_key:
            return json.dumps(
                {"error": "OpenRouter API key not configured. Set OPENROUTER_API_KEY."}
            )

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0,
            "max_tokens": 16384,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://srs-reviewer.app",
            "X-Title": "SRS Reviewer",
        }

        url = f"{self.base_url}/chat/completions"

        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.post(url, json=payload, headers=headers)

            if response.status_code == 401:
                return json.dumps({"error": "Invalid OpenRouter API key (401 Unauthorized)."})

            if response.status_code == 429:
                return json.dumps({"error": "OpenRouter rate limit exceeded (429). Please retry."})

            if response.status_code != 200:
                return json.dumps(
                    {"error": f"OpenRouter API error ({response.status_code}): {response.text[:300]}"}
                )

            data = response.json()
            content = data["choices"][0]["message"]["content"]
            log.info("Response received (%d chars)", len(content))

            return _extract_json(content)

        except httpx.TimeoutException:
            return json.dumps({"error": f"OpenRouter API timed out after {timeout}s."})

        except Exception as e:
            return json.dumps({"error": f"OpenRouter API error: {e}"})

    def close(self) -> None:
        """No-op for API client (kept for interface compatibility)."""
        pass
