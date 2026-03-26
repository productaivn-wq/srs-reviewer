"""Tests for structure_validator."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.lib.srs_parser import SRSParser
from core.lib.structure_validator import validate_structure, normalize_section_name


@pytest.fixture
def full_srs(tmp_path):
    """SRS with all mandatory sections."""
    content = """# 1. Introduction
## 1.1 Purpose
Purpose text.

# 2. Overall Description
Description text.

# 3. Specific Requirements
Requirements text.
"""
    srs_file = tmp_path / "full.md"
    srs_file.write_text(content, encoding="utf-8")
    return SRSParser(str(srs_file))


@pytest.fixture
def partial_srs(tmp_path):
    """SRS missing 'Specific Requirements'."""
    content = """# 1. Introduction
Purpose text.

# 2. Overall Description
Description text.
"""
    srs_file = tmp_path / "partial.md"
    srs_file.write_text(content, encoding="utf-8")
    return SRSParser(str(srs_file))


@pytest.fixture
def empty_srs(tmp_path):
    """SRS with no recognizable sections."""
    content = "Just some random text without headers."
    srs_file = tmp_path / "empty.md"
    srs_file.write_text(content, encoding="utf-8")
    return SRSParser(str(srs_file))


class TestNormalizeSectionName:
    def test_strips_numbering(self):
        assert normalize_section_name("1.2.3 Purpose") == "purpose"

    def test_lowercase(self):
        assert normalize_section_name("Overall Description") == "overall description"

    def test_no_numbering(self):
        assert normalize_section_name("Specific Requirements") == "specific requirements"


class TestValidateStructure:

    def test_full_srs_strict(self, full_srs):
        is_valid, missing, present = validate_structure(full_srs, strict=True)
        assert is_valid is True
        assert len(missing) == 0
        assert len(present) == 3

    def test_full_srs_lenient(self, full_srs):
        is_valid, missing, present = validate_structure(full_srs, strict=False)
        assert is_valid is True

    def test_partial_srs_strict(self, partial_srs):
        is_valid, missing, present = validate_structure(partial_srs, strict=True)
        assert is_valid is False
        assert "Specific Requirements" in missing

    def test_partial_srs_lenient(self, partial_srs):
        """Lenient mode passes if at least one mandatory section is present."""
        is_valid, missing, present = validate_structure(partial_srs, strict=False)
        assert is_valid is True
        assert len(present) > 0

    def test_empty_srs_strict(self, empty_srs):
        is_valid, missing, present = validate_structure(empty_srs, strict=True)
        assert is_valid is False
        assert len(missing) == 3

    def test_empty_srs_lenient(self, empty_srs):
        is_valid, missing, present = validate_structure(empty_srs, strict=False)
        assert is_valid is False
        assert len(present) == 0
