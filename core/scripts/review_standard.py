#!/usr/bin/env python3
"""
Standard SRS Review Script (Mode 1)
Quick ISO/IEC/IEEE 29148 quality assessment with 12-dimension scoring.
"""

import argparse
import sys
from pathlib import Path

# Add project root to sys.path so 'core' can be imported
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from core.lib import SRSParser, validate_structure, SRSReviewEngine, LLMClient, ReportRenderer


def main() -> int:
    parser = argparse.ArgumentParser(description="Standard SRS Review (Mode 1)")
    parser.add_argument("file", help="Path to the SRS markdown file")
    parser.add_argument(
        "--output",
        help="Output file path for review (default: reviews/review-YYYY-MM-DD-HHmm.md)",
        default=None,
    )
    parser.add_argument(
        "--reviewer",
        help="Name of reviewer (default: SRS Review AI)",
        default="SRS Review AI",
    )
    args = parser.parse_args()

    srs_path = Path(args.file)
    if not srs_path.exists():
        print(f"❌ Error: {srs_path} not found.")
        return 1

    print(f"📄 Reviewing SRS: {srs_path}")
    print(f"🔍 Running Standard Review (Mode 1)...\n")

    # 1. Parse SRS
    srs_parser = SRSParser(str(srs_path))
    print(f"✓ Parsed {len(srs_parser.get_section_list())} sections")

    # 2. Structure validation (gate check)
    is_valid, missing, present = validate_structure(srs_parser, strict=True)
    if not is_valid:
        print("\n❌ CRITICAL: SRS Structure Validation Failed!")
        print("Missing mandatory sections:")
        for section in missing:
            print(f"  - {section}")
        print("\nReview process aborted. Please ensure the SRS follows ISO/IEC/IEEE 29148 structure.")
        return 1

    print(f"✓ Structure valid: {len(present)} mandatory sections present")

    # 3. Load prompt
    prompt_path = project_root / "core" / "prompts" / "srs_review_prompt.txt"
    if not prompt_path.exists():
        print(f"❌ Error: Prompt template not found: {prompt_path}")
        return 1

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    # 4. Run LLM review
    print("✓ Calling LLM for 10-dimension scoring...")
    client = LLMClient()
    engine = SRSReviewEngine(client)
    result = engine.review_srs(srs_parser, prompt_template)

    if "error" in result:
        print(f"\n❌ Review failed: {result['error']}")
        return 1

    # 5. Render and save report
    renderer = ReportRenderer(reviewer=args.reviewer, mode="Standard")
    report = renderer.render(result, srs_filename=srs_path.name)

    reviews_dir = str(project_root / "reviews")
    output_file = renderer.save(report, output_path=args.output, reviews_dir=reviews_dir)
    print(f"✓ Report saved: {output_file}")

    # 6. Console summary
    print_summary(result)
    return 0


def print_summary(result: dict) -> None:
    """Print a concise scoring summary to console."""
    total = result.get("totalScore", 0)
    verdict = result.get("verdict", "Unknown")
    recalc = result.get("recalculatedScore", total)
    valid = result.get("scoreValid", True)

    emoji = "✅" if total >= 85 else ("⚠️" if total >= 70 else "❌")

    print(f"\n{'='*60}")
    print(f"📊 REVIEW SUMMARY")
    print(f"{'='*60}")
    print(f"Total Score: {total}/100 {emoji}")
    print(f"Verdict:     {verdict}")

    if not valid:
        print(f"⚠️ Score note: LLM={total}, Recalculated={recalc}")

    sections = result.get("sections", [])
    if sections:
        print(f"\nDimension Scores:")
        for s in sections:
            title = s.get("title", "Unknown")
            score = s.get("score", 0)
            dim_emoji = "✅" if score >= 85 else ("⚠️" if score >= 70 else "❌")
            issues = len(s.get("issues", []))
            print(f"  {dim_emoji} {title}: {score}/100 ({issues} issues)")

    print(f"{'='*60}\n")


if __name__ == "__main__":
    sys.exit(main())
