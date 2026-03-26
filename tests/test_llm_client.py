"""Tests for LLMClient (OpenRouter API via httpx)."""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.lib.llm_client import LLMClient, _extract_json


# ── _extract_json tests ──────────────────────────────────────────────


class TestExtractJson:

    def test_fenced_json(self):
        text = '```json\n{"score": 85}\n```'
        assert _extract_json(text) == '{"score": 85}'

    def test_fenced_no_language(self):
        text = '```\n{"score": 85}\n```'
        assert _extract_json(text) == '{"score": 85}'

    def test_raw_json_with_prefix(self):
        text = 'Here is the result: {"score": 85}'
        result = _extract_json(text)
        assert json.loads(result)["score"] == 85

    def test_pure_json(self):
        text = '{"score": 85}'
        assert _extract_json(text) == '{"score": 85}'

    def test_no_json_returns_raw(self):
        text = "No JSON here"
        assert _extract_json(text) == "No JSON here"

    def test_nested_json(self):
        text = '```json\n{"sections": [{"title": "D1", "score": 80}]}\n```'
        result = _extract_json(text)
        parsed = json.loads(result)
        assert parsed["sections"][0]["score"] == 80


# ── LLMClient tests ─────────────────────────────────────────────────


class TestLLMClient:

    def test_default_constructor(self):
        with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key-123"}):
            client = LLMClient()
            assert client.api_key == "test-key-123"
            assert client.model == "anthropic/claude-sonnet-4-20250514"
            assert "openrouter.ai" in client.base_url

    def test_custom_constructor(self):
        client = LLMClient(
            api_key="custom-key",
            model="openai/gpt-4o",
            base_url="https://custom.api.com/v1",
        )
        assert client.api_key == "custom-key"
        assert client.model == "openai/gpt-4o"
        assert client.base_url == "https://custom.api.com/v1"

    def test_no_api_key_returns_error(self):
        with patch.dict("os.environ", {}, clear=True):
            # Remove OPENROUTER_API_KEY if set
            import os
            os.environ.pop("OPENROUTER_API_KEY", None)

            client = LLMClient(api_key="")
            result = client.generate_content("test prompt")
            parsed = json.loads(result)
            assert "error" in parsed
            assert "API key" in parsed["error"]

    @patch("core.lib.llm_client.httpx.Client")
    def test_generate_content_success(self, mock_httpx_cls):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": '```json\n{"totalScore": 78}\n```'
                    }
                }
            ]
        }

        mock_client = MagicMock()
        mock_client.post.return_value = mock_response
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_httpx_cls.return_value = mock_client

        client = LLMClient(api_key="test-key")
        result = client.generate_content("test prompt", system_instruction="Be helpful")

        parsed = json.loads(result)
        assert parsed["totalScore"] == 78

        # Verify the request was made correctly
        call_args = mock_client.post.call_args
        payload = call_args.kwargs.get("json", call_args[1].get("json", {}))
        assert payload["model"] == "anthropic/claude-sonnet-4-20250514"
        assert len(payload["messages"]) == 2  # system + user
        assert payload["messages"][0]["role"] == "system"
        assert payload["messages"][1]["role"] == "user"

    @patch("core.lib.llm_client.httpx.Client")
    def test_generate_content_no_system_instruction(self, mock_httpx_cls):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": '{"score": 90}'}}]
        }

        mock_client = MagicMock()
        mock_client.post.return_value = mock_response
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_httpx_cls.return_value = mock_client

        client = LLMClient(api_key="test-key")
        client.generate_content("test prompt")

        call_args = mock_client.post.call_args
        payload = call_args.kwargs.get("json", call_args[1].get("json", {}))
        assert len(payload["messages"]) == 1  # user only
        assert payload["messages"][0]["role"] == "user"

    @patch("core.lib.llm_client.httpx.Client")
    def test_handle_401(self, mock_httpx_cls):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"

        mock_client = MagicMock()
        mock_client.post.return_value = mock_response
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_httpx_cls.return_value = mock_client

        client = LLMClient(api_key="bad-key")
        result = client.generate_content("test")
        parsed = json.loads(result)
        assert "error" in parsed
        assert "401" in parsed["error"]

    @patch("core.lib.llm_client.httpx.Client")
    def test_handle_429(self, mock_httpx_cls):
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.text = "Rate limited"

        mock_client = MagicMock()
        mock_client.post.return_value = mock_response
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_httpx_cls.return_value = mock_client

        client = LLMClient(api_key="test-key")
        result = client.generate_content("test")
        parsed = json.loads(result)
        assert "error" in parsed
        assert "429" in parsed["error"]

    @patch("core.lib.llm_client.httpx.Client")
    def test_handle_timeout(self, mock_httpx_cls):
        import httpx as httpx_mod

        mock_client = MagicMock()
        mock_client.post.side_effect = httpx_mod.TimeoutException("timed out")
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_httpx_cls.return_value = mock_client

        client = LLMClient(api_key="test-key")
        result = client.generate_content("test", timeout=10)
        parsed = json.loads(result)
        assert "error" in parsed
        assert "timed out" in parsed["error"]

    def test_close_is_noop(self):
        client = LLMClient(api_key="test")
        client.close()  # Should not raise
