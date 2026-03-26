"""Tests for domain_profile_loader module."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.lib.domain_profile_loader import (
    DomainCheck,
    DomainProfile,
    get_available_profiles,
    inject_domain_checks,
    load_domain_profile,
)


@pytest.fixture
def profiles_dir():
    """Return the real domain_profiles directory."""
    return Path(__file__).parent.parent / "core" / "domain_profiles"


@pytest.fixture
def temp_profile(tmp_path):
    """Create a temporary YAML profile for testing."""
    content = """
name: Test Domain
description: A test domain profile.
checks:
  - id: TD-001
    title: "Test check 1"
    description: "First test check"
    severity: critical
    keywords: ["test", "example"]
  - id: TD-002
    title: "Test check 2"
    description: "Second test check"
    severity: major
    keywords: ["foo"]
"""
    yaml_file = tmp_path / "testdomain.yaml"
    yaml_file.write_text(content, encoding="utf-8")
    return tmp_path


class TestLoadDomainProfile:

    def test_load_health_profile(self, profiles_dir):
        """Verify the health.yaml profile loads with all expected checks."""
        profile = load_domain_profile("health", profiles_dir)
        assert profile.name == "AI Health"
        assert len(profile.checks) == 7
        assert all(isinstance(c, DomainCheck) for c in profile.checks)

    def test_health_profile_check_ids(self, profiles_dir):
        """Verify health profile check IDs are sequential."""
        profile = load_domain_profile("health", profiles_dir)
        ids = [c.id for c in profile.checks]
        assert "DH-001" in ids
        assert "DH-007" in ids

    def test_health_profile_severities(self, profiles_dir):
        """Verify health profile has both critical and major checks."""
        profile = load_domain_profile("health", profiles_dir)
        severities = {c.severity for c in profile.checks}
        assert "critical" in severities
        assert "major" in severities

    def test_load_custom_profile(self, temp_profile):
        """Test loading a custom profile from a temp directory."""
        profile = load_domain_profile("testdomain", temp_profile)
        assert profile.name == "Test Domain"
        assert len(profile.checks) == 2
        assert profile.checks[0].severity == "critical"

    def test_load_nonexistent_raises(self, profiles_dir):
        """Loading a missing profile raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="nonexistent"):
            load_domain_profile("nonexistent", profiles_dir)

    def test_load_malformed_raises(self, tmp_path):
        """Loading a malformed YAML raises ValueError."""
        bad_file = tmp_path / "bad.yaml"
        bad_file.write_text("just a string", encoding="utf-8")
        with pytest.raises(ValueError, match="Invalid domain profile"):
            load_domain_profile("bad", tmp_path)


class TestGetAvailableProfiles:

    def test_real_profiles_dir(self, profiles_dir):
        """At least 'health' should be available."""
        profiles = get_available_profiles(profiles_dir)
        assert "health" in profiles

    def test_empty_dir(self, tmp_path):
        """Empty directory returns empty list."""
        profiles = get_available_profiles(tmp_path)
        assert profiles == []

    def test_nonexistent_dir(self, tmp_path):
        """Nonexistent directory returns empty list."""
        profiles = get_available_profiles(tmp_path / "nope")
        assert profiles == []


class TestInjectDomainChecks:

    def test_injection_into_prompt(self, profiles_dir):
        """Verify domain checks are inserted into the prompt string."""
        profile = load_domain_profile("health", profiles_dir)
        prompt = "Review this SRS.\n\nSRS Content:\n{{SRS_CONTENT}}"
        result = inject_domain_checks(prompt, profile)
        assert "DOMAIN SAFETY CHECKS" in result
        assert "AI Health" in result
        assert "DH-001" in result

    def test_injection_preserves_srs_placeholder(self, profiles_dir):
        """SRS_CONTENT placeholder must survive after injection."""
        profile = load_domain_profile("health", profiles_dir)
        prompt = "SRS Content:\n{{SRS_CONTENT}}"
        result = inject_domain_checks(prompt, profile)
        assert "{{SRS_CONTENT}}" in result

    def test_injection_fallback_append(self, profiles_dir):
        """If no SRS_CONTENT placeholder, append to end."""
        profile = load_domain_profile("health", profiles_dir)
        prompt = "Just some prompt text."
        result = inject_domain_checks(prompt, profile)
        assert "DOMAIN SAFETY CHECKS" in result
        assert result.startswith("Just some prompt text.")
