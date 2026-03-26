"""Tests for SRSReviewEngine (with mocked LLM)."""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.lib.review_engine import SRSReviewEngine
from core.lib.srs_parser import SRSParser

# Fixture: a valid LLM JSON response
MOCK_LLM_RESPONSE = json.dumps({
    "totalScore": 78,
    "verdict": "Cần cải thiện — Có lỗ hổng",
    "sections": [
        {"title": "D1 — Mục đích & Phạm vi", "score": 85, "issues": [{"issue": "a", "severity": "minor"}, {"issue": "b", "severity": "minor"}], "praise": [], "suggestions": []},
        {"title": "D2 — Bên liên quan", "score": 70, "issues": [{"issue": "c", "severity": "major"}, {"issue": "d", "severity": "minor"}], "praise": [], "suggestions": []},
        {"title": "D3 — Yêu cầu chức năng", "score": 80, "issues": [{"issue": "e", "severity": "minor"}, {"issue": "f", "severity": "minor"}], "praise": [], "suggestions": []},
        {"title": "D4 — Yêu cầu phi chức năng", "score": 75, "issues": [{"issue": "g", "severity": "major"}, {"issue": "h", "severity": "minor"}], "praise": [], "suggestions": []},
        {"title": "D5 — Kiến trúc hệ thống", "score": 72, "issues": [{"issue": "i", "severity": "minor"}, {"issue": "j", "severity": "minor"}], "praise": [], "suggestions": []},
        {"title": "D6 — Yêu cầu dữ liệu", "score": 80, "issues": [{"issue": "k", "severity": "minor"}, {"issue": "l", "severity": "minor"}], "praise": [], "suggestions": []},
        {"title": "D7 — Use Case & Kịch bản", "score": 78, "issues": [{"issue": "m", "severity": "minor"}, {"issue": "n", "severity": "minor"}], "praise": [], "suggestions": []},
        {"title": "D8 — Tiêu chí nghiệm thu", "score": 70, "issues": [{"issue": "o", "severity": "major"}, {"issue": "p", "severity": "minor"}], "praise": [], "suggestions": []},
        {"title": "D9 — Truy xuất nguồn gốc", "score": 65, "issues": [{"issue": "q", "severity": "critical"}, {"issue": "r", "severity": "minor"}], "praise": [], "suggestions": []},
        {"title": "D10 — Chất lượng tài liệu", "score": 90, "issues": [{"issue": "s", "severity": "nice to have"}, {"issue": "t", "severity": "nice to have"}], "praise": [], "suggestions": []},
    ],
})


@pytest.fixture
def mock_llm_client():
    """Create a mock LLM client that returns fixture data."""
    client = MagicMock()
    client.generate_content.return_value = MOCK_LLM_RESPONSE
    return client


@pytest.fixture
def sample_srs(tmp_path):
    """Create minimal SRS for engine testing."""
    content = """# 1. Introduction
## 1.1 Purpose
Test purpose.

# 2. Overall Description
Test description.

# 3. Specific Requirements
Test requirements.
"""
    srs_file = tmp_path / "test.md"
    srs_file.write_text(content, encoding="utf-8")
    return SRSParser(str(srs_file))


class TestSRSReviewEngine:

    def test_review_returns_result(self, mock_llm_client, sample_srs):
        engine = SRSReviewEngine(mock_llm_client)
        result = engine.review_srs(sample_srs, "{{SRS_CONTENT}}")
        assert "totalScore" in result
        assert result["totalScore"] == 78

    def test_review_enriches_with_recalculated_score(self, mock_llm_client, sample_srs):
        engine = SRSReviewEngine(mock_llm_client)
        result = engine.review_srs(sample_srs, "{{SRS_CONTENT}}")
        assert "recalculatedScore" in result
        assert "scoreValid" in result
        assert isinstance(result["recalculatedScore"], float)

    def test_review_dimension_count(self, mock_llm_client, sample_srs):
        engine = SRSReviewEngine(mock_llm_client)
        result = engine.review_srs(sample_srs, "{{SRS_CONTENT}}")
        assert result["dimensionCount"] == 10

    def test_review_handles_json_error(self, sample_srs):
        bad_client = MagicMock()
        bad_client.generate_content.return_value = "not valid json {{"
        engine = SRSReviewEngine(bad_client)
        result = engine.review_srs(sample_srs, "{{SRS_CONTENT}}")
        assert "error" in result

    def test_prompt_injection(self, mock_llm_client, sample_srs):
        """Verify that {{SRS_CONTENT}} is replaced in the prompt."""
        engine = SRSReviewEngine(mock_llm_client)
        engine.review_srs(sample_srs, "Review this: {{SRS_CONTENT}}")

        call_args = mock_llm_client.generate_content.call_args
        prompt_sent = call_args.kwargs.get("prompt", call_args[1].get("prompt", ""))
        assert "{{SRS_CONTENT}}" not in prompt_sent
        assert "Test purpose" in prompt_sent

    def test_get_dimension_weights(self):
        weights = SRSReviewEngine.get_dimension_weights()
        assert len(weights) == 10
        total = sum(d["weight"] for d in weights.values())
        assert abs(total - 1.0) < 0.001

    def test_review_with_reference_doc(self, mock_llm_client, sample_srs):
        """Verify reference_content is injected into the prompt."""
        engine = SRSReviewEngine(mock_llm_client)
        result = engine.review_srs(
            sample_srs,
            "{{SRS_CONTENT}}",
            reference_content="PRD: The system shall do X.",
        )
        # Should still return a valid result
        assert "totalScore" in result
        # Verify the LLM was called with reference content in prompt
        call_args = mock_llm_client.generate_content.call_args
        prompt_sent = call_args.kwargs.get("prompt", call_args[1].get("prompt", ""))
        assert "PRD: The system shall do X." in prompt_sent

    def test_review_without_reference_doc_backward_compat(self, mock_llm_client, sample_srs):
        """Verify no reference = standard review (backward compatible)."""
        engine = SRSReviewEngine(mock_llm_client)
        result = engine.review_srs(sample_srs, "Review: {{SRS_CONTENT}}")
        assert "totalScore" in result
        # No reference in prompt
        call_args = mock_llm_client.generate_content.call_args
        prompt_sent = call_args.kwargs.get("prompt", call_args[1].get("prompt", ""))
        assert "REFERENCE DOCUMENT" not in prompt_sent

    def test_review_with_domain_profile(self, mock_llm_client, sample_srs):
        """Verify domain profile injects checks into prompt (non-fatal if file missing)."""
        engine = SRSReviewEngine(mock_llm_client)
        result = engine.review_srs(
            sample_srs,
            "SRS Content:\n{{SRS_CONTENT}}",
            domain_profile="health",
        )
        assert "totalScore" in result

