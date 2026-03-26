import type { Section } from '../types/review';
import { DIMENSION_WEIGHTS, DIMENSION_TITLES } from './constants';

/**
 * Recalculate the weighted total score from per-dimension scores.
 * Mirrors the Python recalculate_score() in report_renderer.py.
 */
export function recalculateScore(sections: Section[]): number {
  let total = 0;
  for (const s of sections) {
    const title = s.title ?? '';
    const score = s.score ?? 0;
    let dimId = title.split('—')[0].split('–')[0].trim().toUpperCase();
    for (const key of Object.keys(DIMENSION_WEIGHTS)) {
      if (dimId.includes(key)) { dimId = key; break; }
    }
    total += score * (DIMENSION_WEIGHTS[dimId] ?? 0);
  }
  return Math.round(total * 10) / 10;
}

/**
 * Build the review prompt with SRS content injected.
 */
export function buildPrompt(srsContent: string, mode: string): string {
  const strategic = mode === 'strategic' ? `
STRATEGIC CONSIDERATIONS:
- Evaluate the product's alignment with broader technical and business strategies.
- Does the system architecture support long-term maintainability and scalability?
- Deeply scrutinize data modeling, API contracts, and integration constraints.
- Assess whether NFRs are quantified with specific thresholds (latency, uptime SLA, etc.).
- Check for hidden dependencies and vendor lock-in risks.
- Evaluate completeness of error handling and edge case documentation.
` : '';

  return `SCORING INSTRUCTIONS:
Evaluate the SRS on a scale of 0-100 based on these weighted dimensions:
1. Purpose & Scope Clarity (10%)
2. Stakeholder & User Requirements (10%)
3. Functional Requirements (15%)
4. Non-Functional Requirements (12%)
5. System Architecture & Constraints (10%)
6. Data Requirements (8%)
7. Use Cases & Scenarios (12%)
8. Acceptance Criteria & Testing (10%)
9. Traceability & Consistency (8%)
10. Document Quality & Standards (5%)
${strategic}
CALCULATION:
- Assign a score (0-100) for each dimension.
- Calculate weighted average.
- Final Score = Round(Weighted Average).

CRITICAL RULE:
- If Final Score < 85, the Overall Status MUST be "Needs Revision".
- If Final Score >= 85, the Overall Status is "Ready".
- When content is missing, specify WHICH PART of the SRS is lacking.
- Each dimension MUST have AT LEAST 2 issues. Even high-scoring dimensions must identify improvement opportunities.
- Review must be in Vietnamese. Output only JSON.

OUTPUT JSON SCHEMA:
Generate a valid JSON object matching this structure. Replace the bracketed placeholders with your actual evaluated data. DO NOT output the literal template:
{
  "totalScore": <number 0-100>,
  "verdict": "<Vietnamese verdict string>",
  "sections": [
    {
      "title": "D1 — Mục đích & Phạm vi",
      "score": <number 0-100>,
      "status": "pass|fail",
      "praise": [{"praise": "<strength>", "evidence": ["<quote>"]}],
      "issues": [{"issue": "<issue>", "severity": "critical|major|minor|nice to have", "evidence": ["<quote>"]}],
      "suggestions": ["<suggestion>"]
    }
  ]
}

DIMENSION TITLE MAPPING (use exactly):
${DIMENSION_TITLES.map(t => `- "${t}"`).join('\n')}

SRS Content:
${srsContent}`;
}
