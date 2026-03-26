"""
SRS Review Engine
Orchestrates the 12-dimension ISO/IEC/IEEE 29148 based scoring using the LLM client,
validates scores, and produces structured ReviewResult dicts.

Supports optional PRD alignment checking and domain safety profiles.
"""

import json
from pathlib import Path
from typing import Dict, Optional

from .domain_profile_loader import inject_domain_checks, load_domain_profile
from .llm_client import LLMClient
from .report_renderer import DIMENSION_WEIGHTS, recalculate_score
from .srs_parser import SRSParser

# System instruction for the LLM
SYSTEM_INSTRUCTION = (
    "You are an expert system architect and business analyst reviewing an SRS document "
    "according to ISO/IEC/IEEE 29148:2018 standards. "
    "CRITICAL: Your ENTIRE response must be a single valid JSON object — no explanation, "
    "no markdown, no text before or after. Just pure JSON. "
    "Each dimension MUST have at least 2 issues. Review must be in Vietnamese. "
    "IMPORTANT: DO NOT use any tools. DO NOT attempt to write files or use the terminal. "
    "You MUST output ONLY the raw JSON string directly in your response message. "
    "DO NOT output the template variables verbatim; you must fill them with your actual evaluation."
)

SYSTEM_INSTRUCTION_ALIGNMENT = (
    SYSTEM_INSTRUCTION
    + " You are also performing PRD alignment checking — compare the SRS against "
    "the provided reference document and identify missing items, scope creep, "
    "intent mismatches, and sign-off gaps."
)

# Paths to prompt templates
_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


class SRSReviewEngine:
    """Orchestrates SRS review: prompt injection, LLM call, score validation."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def review_srs(
        self,
        srs_parser: SRSParser,
        prompt_template: str,
        reference_content: Optional[str] = None,
        domain_profile: Optional[str] = None,
    ) -> Dict:
        """
        Execute the review by sending the SRS content to the LLM.

        Args:
            srs_parser: Parsed SRS document.
            prompt_template: Prompt text with {{SRS_CONTENT}} placeholder.
            reference_content: Optional PRD/US/AC content for alignment checking.
                               If provided, uses the alignment prompt template.
            domain_profile: Optional domain profile name (e.g., 'health') for
                            domain-specific safety checks.

        Returns:
            Parsed JSON dict from LLM, or error dict.
        """
        # Select prompt template and system instruction
        if reference_content:
            prompt = self._build_alignment_prompt(
                srs_parser.content, reference_content, prompt_template
            )
            system_instruction = SYSTEM_INSTRUCTION_ALIGNMENT
        else:
            prompt = prompt_template.replace("{{SRS_CONTENT}}", srs_parser.content)
            system_instruction = SYSTEM_INSTRUCTION

        # Inject domain safety checks if requested
        if domain_profile:
            prompt = self._inject_domain_profile(prompt, domain_profile)

        response = self.llm_client.generate_content(
            prompt=prompt,
            system_instruction=system_instruction,
        )

        try:
            result = json.loads(response)
        except json.JSONDecodeError as e:
            return {
                "error": (
                    f"Failed to parse LLM response into JSON: {e}\n"
                    f"Raw Response: {response[:300]}..."
                )
            }

        return self._validate_and_enrich(result)

    def _build_alignment_prompt(
        self,
        srs_content: str,
        reference_content: str,
        prompt_template: str,
    ) -> str:
        """
        Build an alignment-aware prompt by injecting both SRS and reference content.

        If the prompt has a {{REFERENCE_CONTENT}} placeholder, use it.
        Otherwise, load the default alignment prompt template.
        """
        if "{{REFERENCE_CONTENT}}" in prompt_template:
            prompt = prompt_template.replace(
                "{{REFERENCE_CONTENT}}", reference_content
            )
            prompt = prompt.replace("{{SRS_CONTENT}}", srs_content)
            return prompt

        # Load default alignment prompt
        alignment_prompt_path = _PROMPTS_DIR / "srs_alignment_prompt.txt"
        if alignment_prompt_path.exists():
            template = alignment_prompt_path.read_text(encoding="utf-8")
            template = template.replace("{{REFERENCE_CONTENT}}", reference_content)
            template = template.replace("{{SRS_CONTENT}}", srs_content)
            return template

        # Fallback: append reference to standard prompt
        prompt = prompt_template.replace("{{SRS_CONTENT}}", srs_content)
        prompt += (
            f"\n\nREFERENCE DOCUMENT (PRD / User Story / AC):\n{reference_content}"
        )
        return prompt

    def _inject_domain_profile(self, prompt: str, profile_name: str) -> str:
        """Load and inject domain safety checks into the prompt."""
        try:
            profile = load_domain_profile(profile_name)
            return inject_domain_checks(prompt, profile)
        except (FileNotFoundError, ValueError) as e:
            # Log but don't fail the review
            print(f"[WARNING] Could not load domain profile '{profile_name}': {e}")
            return prompt

    def _validate_and_enrich(self, result: Dict) -> Dict:
        """
        Validate LLM output and enrich with recalculated score.

        Adds:
            - recalculatedScore: independently computed weighted total
            - scoreValid: whether LLM score matches recalculated (±2 tolerance)
        """
        if "error" in result:
            return result

        sections = result.get("sections", [])
        if not sections:
            return result

        recalc = recalculate_score(sections)
        llm_score = result.get("totalScore", 0)

        result["recalculatedScore"] = recalc
        result["scoreValid"] = abs(recalc - llm_score) <= 2

        # Ensure dimension count
        result["dimensionCount"] = len(sections)

        return result

    @staticmethod
    def get_dimension_weights() -> Dict:
        """Return the canonical dimension weight mapping."""
        return dict(DIMENSION_WEIGHTS)
