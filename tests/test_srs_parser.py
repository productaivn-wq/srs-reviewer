"""Tests for SRSParser."""

import os
import tempfile

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.lib.srs_parser import SRSParser


@pytest.fixture
def sample_srs(tmp_path):
    """Create a minimal SRS file for testing."""
    content = """# 1. Introduction

## 1.1 Purpose
Test purpose.

## 1.2 Scope
Test scope.

# 2. Overall Description

## 2.1 Product Functions
- Feature A
- Feature B

# 3. Specific Requirements

## 3.1 Functional Requirements

### FR-001: Login
The system shall allow users to log in.

### FR-002: Dashboard
The system shall display a dashboard.

## 3.2 Non-Functional Requirements

### NFR-001: Performance
Response time < 500ms.
"""
    srs_file = tmp_path / "test_srs.md"
    srs_file.write_text(content, encoding="utf-8")
    return str(srs_file)


@pytest.fixture
def empty_srs(tmp_path):
    """Create an empty SRS file."""
    srs_file = tmp_path / "empty.md"
    srs_file.write_text("", encoding="utf-8")
    return str(srs_file)


class TestSRSParser:
    """Tests for SRSParser class."""

    def test_load_valid_file(self, sample_srs):
        parser = SRSParser(sample_srs)
        assert parser.content != ""
        assert len(parser.sections) > 0

    def test_load_missing_file(self):
        with pytest.raises(FileNotFoundError):
            SRSParser("nonexistent_file.md")

    def test_parse_sections(self, sample_srs):
        parser = SRSParser(sample_srs)
        section_list = parser.get_section_list()
        assert len(section_list) > 0
        # Should find Introduction, Overall Description, Specific Requirements
        assert any("Introduction" in s for s in section_list)

    def test_get_section_exact(self, sample_srs):
        parser = SRSParser(sample_srs)
        result = parser.get_section("Purpose")
        assert result is not None
        assert "Test purpose" in result

    def test_get_section_fuzzy(self, sample_srs):
        parser = SRSParser(sample_srs)
        # Should match "Functional Requirements" via fuzzy lookup
        result = parser.get_section("Functional")
        assert result is not None

    def test_get_section_missing(self, sample_srs):
        parser = SRSParser(sample_srs)
        result = parser.get_section("Nonexistent Section XYZ")
        assert result is None

    def test_get_all_sections(self, sample_srs):
        parser = SRSParser(sample_srs)
        all_sections = parser.get_all_sections()
        assert isinstance(all_sections, dict)
        assert len(all_sections) > 0

    def test_empty_file(self, empty_srs):
        parser = SRSParser(empty_srs)
        # Should have at most a frontmatter section
        assert len(parser.sections) <= 1

    def test_heading_number_stripping(self, sample_srs):
        parser = SRSParser(sample_srs)
        section_list = parser.get_section_list()
        # Section names should not start with "1." or "1.1"
        for name in section_list:
            if name == "frontmatter":
                continue
            assert not name[0].isdigit(), f"Section name starts with digit: {name}"
