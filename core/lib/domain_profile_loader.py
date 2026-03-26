"""
Domain Profile Loader
Loads YAML-based domain safety profiles and injects domain-specific
checks into SRS review prompts.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import yaml


@dataclass
class DomainCheck:
    """A single domain-specific safety check."""

    id: str
    title: str
    description: str
    severity: str
    keywords: List[str] = field(default_factory=list)


@dataclass
class DomainProfile:
    """A domain safety profile containing multiple checks."""

    name: str
    description: str
    checks: List[DomainCheck]


# Default directory containing domain profile YAML files
_PROFILES_DIR = Path(__file__).parent.parent / "domain_profiles"


def load_domain_profile(
    name: str, profiles_dir: Optional[Path] = None
) -> DomainProfile:
    """
    Load a domain profile from a YAML file.

    Args:
        name: Profile name (without extension), e.g. 'health'.
        profiles_dir: Directory containing profile YAML files.
                      Defaults to core/domain_profiles/.

    Returns:
        DomainProfile dataclass.

    Raises:
        FileNotFoundError: If the profile YAML does not exist.
        ValueError: If the YAML is malformed.
    """
    dir_path = profiles_dir or _PROFILES_DIR
    yaml_path = dir_path / f"{name}.yaml"

    if not yaml_path.exists():
        available = get_available_profiles(dir_path)
        raise FileNotFoundError(
            f"Domain profile '{name}' not found at {yaml_path}. "
            f"Available profiles: {available}"
        )

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict) or "checks" not in data:
        raise ValueError(
            f"Invalid domain profile format in {yaml_path}. "
            "Expected a YAML dict with 'name', 'description', and 'checks' keys."
        )

    checks = [
        DomainCheck(
            id=c.get("id", f"DH-{i:03d}"),
            title=c.get("title", ""),
            description=c.get("description", "").strip(),
            severity=c.get("severity", "major"),
            keywords=c.get("keywords", []),
        )
        for i, c in enumerate(data["checks"], start=1)
    ]

    return DomainProfile(
        name=data.get("name", name),
        description=data.get("description", "").strip(),
        checks=checks,
    )


def get_available_profiles(profiles_dir: Optional[Path] = None) -> List[str]:
    """
    List available domain profile names.

    Returns:
        List of profile names (without .yaml extension).
    """
    dir_path = profiles_dir or _PROFILES_DIR
    if not dir_path.exists():
        return []
    return [p.stem for p in dir_path.glob("*.yaml")]


def inject_domain_checks(prompt: str, profile: DomainProfile) -> str:
    """
    Append domain-specific checklist to a review prompt.

    Inserts a DOMAIN SAFETY CHECKS section before the SRS Content placeholder.

    Args:
        prompt: The review prompt string (must contain '{{SRS_CONTENT}}').
        profile: Loaded DomainProfile with checks.

    Returns:
        Modified prompt with domain checks injected.
    """
    checklist_lines = [
        "",
        f"DOMAIN SAFETY CHECKS ({profile.name}):",
        f"The SRS is for a {profile.name} product. Apply these additional safety checks:",
        "",
    ]

    for check in profile.checks:
        checklist_lines.append(
            f"- [{check.severity.upper()}] {check.id} — {check.title}: {check.description}"
        )
        if check.keywords:
            keywords_str = ", ".join(f'"{k}"' for k in check.keywords)
            checklist_lines.append(f"  Keywords to scan: {keywords_str}")

    checklist_lines.extend([
        "",
        "DOMAIN CHECK OUTPUT:",
        "Add a 'domainChecks' section to the JSON output with this structure:",
        '  "domainChecks": [',
        "    {",
        '      "checkId": "DH-001",',
        '      "title": "<check title>",',
        '      "status": "pass|fail|warning",',
        '      "severity": "critical|major|minor",',
        '      "findings": ["<specific finding with evidence>"],',
        '      "evidence": ["<verbatim quote from SRS>"]',
        "    }",
        "  ]",
        "",
    ])

    checklist_text = "\n".join(checklist_lines)

    # Insert before the SRS Content placeholder
    if "{{SRS_CONTENT}}" in prompt:
        return prompt.replace(
            "SRS Content:\n{{SRS_CONTENT}}",
            f"{checklist_text}\nSRS Content:\n{{{{SRS_CONTENT}}}}",
        )

    # Fallback: append at the end
    return prompt + checklist_text
