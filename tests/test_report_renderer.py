"""Tests for ReportRenderer."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.lib.report_renderer import (
    ReportRenderer,
    get_verdict,
    get_status_emoji,
    recalculate_score,
)

# Fixture: a valid ReviewResult dict
SAMPLE_RESULT = {
    "totalScore": 78,
    "verdict": "Cần cải thiện — Có lỗ hổng",
    "sections": [
        {
            "title": "D1 — Mục đích & Phạm vi",
            "score": 85,
            "praise": [{"praise": "Clear scope"}],
            "issues": [{"issue": "Missing context", "severity": "minor"}],
            "suggestions": ["Add system context diagram"],
        },
        {
            "title": "D2 — Bên liên quan",
            "score": 70,
            "praise": [],
            "issues": [{"issue": "No stakeholder map", "severity": "major"}],
            "suggestions": [],
        },
        {"title": "D3 — Yêu cầu chức năng", "score": 80, "praise": [], "issues": [], "suggestions": []},
        {"title": "D4 — Yêu cầu phi chức năng", "score": 75, "praise": [], "issues": [], "suggestions": []},
        {"title": "D5 — Kiến trúc hệ thống", "score": 72, "praise": [], "issues": [], "suggestions": []},
        {"title": "D6 — Yêu cầu dữ liệu", "score": 80, "praise": [], "issues": [], "suggestions": []},
        {"title": "D7 — Use Case & Kịch bản", "score": 78, "praise": [], "issues": [], "suggestions": []},
        {"title": "D8 — Tiêu chí nghiệm thu", "score": 70, "praise": [], "issues": [], "suggestions": []},
        {"title": "D9 — Truy xuất nguồn gốc", "score": 65, "praise": [], "issues": [], "suggestions": []},
        {"title": "D10 — Chất lượng tài liệu", "score": 90, "praise": [], "issues": [], "suggestions": []},
    ],
}


class TestGetVerdict:
    def test_excellent(self):
        assert "Production-ready" in get_verdict(96)

    def test_good(self):
        assert "Solid foundation" in get_verdict(85)

    def test_needs_improvement(self):
        assert "Có lỗ hổng" in get_verdict(75)

    def test_weak(self):
        assert "Cần viết lại" in get_verdict(55)

    def test_critical(self):
        assert "Bắt đầu lại" in get_verdict(30)


class TestGetStatusEmoji:
    def test_high_score(self):
        assert get_status_emoji(90) == "✅"

    def test_mid_score(self):
        assert get_status_emoji(75) == "⚠️"

    def test_low_score(self):
        assert get_status_emoji(50) == "❌"


class TestRecalculateScore:
    def test_with_valid_sections(self):
        score = recalculate_score(SAMPLE_RESULT["sections"])
        assert isinstance(score, float)
        assert 0 <= score <= 100

    def test_empty_sections(self):
        score = recalculate_score([])
        assert score == 0.0


class TestReportRenderer:
    def test_render_produces_markdown(self):
        renderer = ReportRenderer(reviewer="Test Bot", mode="Standard")
        report = renderer.render(SAMPLE_RESULT, srs_filename="test.md")
        assert "# SRS Review: test.md" in report
        assert "Test Bot" in report
        assert "Standard" in report
        assert "78/100" in report

    def test_render_includes_dimensions(self):
        renderer = ReportRenderer()
        report = renderer.render(SAMPLE_RESULT, srs_filename="test.md")
        assert "D1" in report
        assert "D10" in report

    def test_render_error_result(self):
        renderer = ReportRenderer()
        error_result = {"error": "API key not configured"}
        report = renderer.render(error_result, srs_filename="test.md")
        assert "Review Failed" in report
        assert "API key not configured" in report

    def test_save_creates_file(self, tmp_path):
        renderer = ReportRenderer()
        report = "# Test Report"
        output = renderer.save(report, output_path=str(tmp_path / "out.md"))
        assert output.exists()
        assert output.read_text(encoding="utf-8") == "# Test Report"

    def test_save_auto_generates_path(self, tmp_path):
        renderer = ReportRenderer()
        report = "# Auto Test"
        output = renderer.save(report, reviews_dir=str(tmp_path / "reviews"))
        assert output.exists()
        assert "review-" in output.name

    def test_executive_summary_ready(self):
        renderer = ReportRenderer()
        high_result = dict(SAMPLE_RESULT)
        high_result["totalScore"] = 90
        report = renderer.render(high_result, srs_filename="test.md")
        assert "Ready for Development" in report

    def test_executive_summary_needs_revision(self):
        renderer = ReportRenderer()
        report = renderer.render(SAMPLE_RESULT, srs_filename="test.md")
        assert "Needs Revision" in report


class TestRenderAnnotated:
    """Tests for the annotated SRS output."""

    def test_inserts_comments_at_matching_evidence(self):
        """Verify inline PM comments appear where evidence matches."""
        renderer = ReportRenderer()
        original_srs = "# Purpose\nThe system provides health info.\n\n# Requirements\nFR-001: Login"
        result = {
            "sections": [{
                "title": "D1",
                "score": 70,
                "issues": [{
                    "issue": "Ambiguous purpose",
                    "severity": "major",
                    "issueType": "ambiguous_wording",
                    "evidence": ["The system provides health info."],
                }],
            }],
        }
        annotated = renderer.render_annotated(result, original_srs)
        assert "[PM COMMENT — Major]" in annotated
        assert "Wording mơ hồ" in annotated
        assert "The system provides health info." in annotated

    def test_unmatched_issues_appended(self):
        """Verify unmatched issues are appended at the end."""
        renderer = ReportRenderer()
        original_srs = "# Simple SRS\nJust text."
        result = {
            "sections": [{
                "title": "D3",
                "score": 60,
                "issues": [{
                    "issue": "Missing edge case",
                    "severity": "critical",
                    "issueType": "missing_edge_case",
                    "evidence": ["Something not in the SRS at all"],
                }],
            }],
        }
        annotated = renderer.render_annotated(result, original_srs)
        assert "chưa gắn vào vị trí cụ thể" in annotated
        assert "Missing edge case" in annotated

    def test_error_result_returns_original(self):
        """Error results should return original SRS unchanged."""
        renderer = ReportRenderer()
        original = "# My SRS"
        result = {"error": "API failed"}
        assert renderer.render_annotated(result, original) == original


class TestRenderAlignment:
    """Tests for PRD alignment rendering."""

    def test_renders_alignment_section(self):
        renderer = ReportRenderer()
        result = {
            "alignment": {
                "summary": "SRS mostly aligned with PRD",
                "missingFromPRD": [
                    {"prdItem": "Feature X", "evidence": "PRD says X", "severity": "critical"}
                ],
                "scopeCreep": [],
                "intentMismatch": [],
                "signOffGaps": ["Missing UAT criteria"],
            }
        }
        output = renderer.render_alignment(result)
        assert "PRD Alignment Analysis" in output
        assert "Feature X" in output
        assert "Missing UAT criteria" in output

    def test_no_alignment_returns_empty(self):
        renderer = ReportRenderer()
        output = renderer.render_alignment({"totalScore": 80})
        assert output == ""

