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
 * When prdContent is provided and mode is 'alignment', includes PRD alignment instructions.
 */
export function buildPrompt(srsContent: string, mode: string, prdContent?: string): string {
  const hasAlignment = mode === 'alignment' && prdContent && prdContent.trim().length > 0;

  const strategic = mode === 'strategic' ? `
STRATEGIC CONSIDERATIONS:
- Evaluate the product's alignment with broader technical and business strategies.
- Does the system architecture support long-term maintainability and scalability?
- Deeply scrutinize data modeling, API contracts, and integration constraints.
- Assess whether NFRs are quantified with specific thresholds (latency, uptime SLA, etc.).
- Check for hidden dependencies and vendor lock-in risks.
- Evaluate completeness of error handling and edge case documentation.
` : '';

  const alignmentInstructions = hasAlignment ? `
ALIGNMENT INSTRUCTIONS:
You are provided with BOTH the SRS and a REFERENCE DOCUMENT (PRD / User Story / Acceptance Criteria).
In addition to the standard 12-dimension scoring, you MUST perform alignment checks:

1. MISSING FROM PRD: List items in the PRD/US/AC that are NOT covered in the SRS.
2. SCOPE CREEP: List items in the SRS that go BEYOND what the PRD/US/AC specifies.
3. INTENT MISMATCH: List items where the SRS misinterprets or distorts the meaning of the PRD/US/AC.
4. SIGN-OFF GAPS: List conditions required for PM sign-off that are not addressed in the SRS.

The JSON output MUST include an additional top-level "alignment" field:
"alignment": {
  "summary": "<overall alignment assessment>",
  "missingFromPRD": [{"prdItem": "<what's missing>", "evidence": "<PRD quote>", "severity": "critical|major|minor"}],
  "scopeCreep": [{"srsItem": "<what exceeds PRD>", "evidence": "<SRS quote>", "severity": "critical|major|minor"}],
  "intentMismatch": [{"prdIntent": "<original intent>", "srsInterpretation": "<how SRS interpreted it>", "severity": "critical|major|minor"}],
  "signOffGaps": ["<gap description>"]
}
` : '';

  const prdSection = hasAlignment ? `

REFERENCE DOCUMENT (PRD):
${prdContent}

---

` : '';

  return `SCORING INSTRUCTIONS:
Evaluate the SRS on a scale of 0-100 based on these weighted dimensions:
1. Purpose & Scope Clarity (8%)
2. Stakeholder & User Requirements (9%)
3. Functional Requirements (14%)
4. Non-Functional Requirements (11%)
5. System Architecture & Constraints (8%)
6. Data Requirements (7%)
7. Use Cases & Scenarios (11%)
8. Acceptance Criteria & Testing (9%)
9. Traceability & Consistency (8%)
10. Document Quality & Standards (5%)
11. Requirements Engineering Process (5%)
12. Requirement Quality Attributes (5%)
${strategic}${alignmentInstructions}
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
  "verdict": "<Vietnamese verdict string>",${hasAlignment ? '\n  "alignment": { ... as described above ... },' : ''}
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
${prdSection}
SRS Content:
${srsContent}`;
}
