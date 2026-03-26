"""
SRS Review Engine
Orchestrates the 10-dimension IEEE 830 based scoring using the LLM client,
validates scores, and produces structured ReviewResult dicts.
"""

import json
from typing import Dict

from .llm_client import LLMClient
from .report_renderer import DIMENSION_WEIGHTS, recalculate_score
from .srs_parser import SRSParser

# System instruction for the LLM
SYSTEM_INSTRUCTION = (
    "You are an expert system architect and business analyst reviewing an SRS document "
    "according to IEEE 830 and ISO 29148 standards. "
    "CRITICAL: Your ENTIRE response must be a single valid JSON object — no explanation, "
    "no markdown, no text before or after. Just pure JSON. "
    "Each dimension MUST have at least 2 issues. Review must be in Vietnamese. "
    "IMPORTANT: DO NOT use any tools. DO NOT attempt to write files or use the terminal. "
    "You MUST output ONLY the raw JSON string directly in your response message. "
    "DO NOT output the template variables verbatim; you must fill them with your actual evaluation."
)


class SRSReviewEngine:
    """Orchestrates SRS review: prompt injection, LLM call, score validation."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def review_srs(self, srs_parser: SRSParser, prompt_template: str) -> Dict:
        """
        Execute the review by sending the SRS content to the LLM.

        Args:
            srs_parser: Parsed SRS document.
            prompt_template: Prompt text with {{SRS_CONTENT}} placeholder.

        Returns:
            Parsed JSON dict from LLM, or error dict.
        """
        prompt = prompt_template.replace("{{SRS_CONTENT}}", srs_parser.content)

        response = self.llm_client.generate_content(
            prompt=prompt,
            system_instruction=SYSTEM_INSTRUCTION,
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
