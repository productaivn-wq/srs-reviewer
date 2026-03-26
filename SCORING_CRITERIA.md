# SRS Scoring Formulation & Criteria

Standardized scoring rubric for Software Requirements Specifications.
Based on ISO/IEC/IEEE 29148:2018 with subcriteria, evidence requirements, MECE validation, workflow coverage, requirements engineering process, and requirement quality attributes.

---

## Scoring Overview

- **12 weighted dimensions**, each with defined subcriteria
- Final score: weighted average out of **100**
- Every subcriteria score **must include evidence** (verbatim SRS quote or explicit "not found")

### Verdict Mapping

| Total Score | Verdict |
|---|---|
| ≥ 96 | Excellent — Production-ready |
| 85–95 | Good — Solid foundation |
| 70–84 | Needs Improvement — Has gaps |
| 50–69 | Weak — Needs rewriting |
| 0–49 | Critical — Start over |

**Threshold**: Score < 85 → **"Needs Revision"**. Score ≥ 85 → **"Ready for Development"**.

---

## Dimensions & Subcriteria

### D1 — Purpose & Scope Clarity (8%)

| Sub | Criteria | Scoring Anchor |
|---|---|---|
| D1.1 | System purpose statement | Clear 1-2 sentence purpose → 100; Vague/missing → 0 |
| D1.2 | Scope boundaries (in-scope / out-of-scope) | Explicit boundaries → 100; Undefined → 0 |
| D1.3 | Business context & motivation | Business need articulated → 100 |
| D1.4 | Definitions & acronyms glossary | Complete glossary → 100; Missing → 50 |

---

### D2 — Stakeholder & User Requirements (9%)

| Sub | Criteria | Scoring Anchor |
|---|---|---|
| D2.1 | Stakeholder identification | All stakeholders listed by role → 100 |
| D2.2 | User characteristics & profiles | Personas or user types documented → 100 |
| D2.3 | User needs mapped to stakeholders | Each need traced to a stakeholder → 100 |
| D2.4 | Assumptions & dependencies | Explicitly stated → 100 |

---

### D3 — Functional Requirements (14%)

| Sub | Criteria | Scoring Anchor |
|---|---|---|
| D3.1 | Requirement atomicity | One FR per item, no compound reqs → 100 |
| D3.2 | Testability | Each FR has measurable criteria → 100 |
| D3.3 | Unique IDs & traceability tags | Every FR has an ID (e.g., FR-001) → 100 |
| D3.4 | Priority classification | MoSCoW or numbered priority → 100 |
| D3.5 | Input/output specification | Inputs, outputs, transformations defined → 100 |
| D3.6 | **MECE — Mutual Exclusivity** | No overlapping/contradicting FRs → 100; Overlaps found → deduct per overlap |
| D3.7 | **MECE — Collective Exhaustiveness** | All implied features have explicit FRs → 100; Gaps found → deduct per gap |

---

### D4 — Non-Functional Requirements (11%)

| Sub | Criteria | Scoring Anchor |
|---|---|---|
| D4.1 | Performance metrics (latency, throughput) | Quantified SLAs → 100; "should be fast" → 20 |
| D4.2 | Security requirements | Auth, encryption, RBAC specified → 100 |
| D4.3 | Reliability & availability (uptime SLA) | SLA percentage defined → 100 |
| D4.4 | Scalability constraints | Load limits, growth projections → 100 |
| D4.5 | Compliance & regulatory | Applicable standards cited → 100 |

---

### D5 — System Architecture & Constraints (8%)

| Sub | Criteria | Scoring Anchor |
|---|---|---|
| D5.1 | System interfaces (APIs, protocols) | Interface contracts documented → 100 |
| D5.2 | External system dependencies | All integrations listed → 100 |
| D5.3 | Technology constraints | Platform, language, framework constraints → 100 |
| D5.4 | Deployment topology | Environments described → 100 |

---

### D6 — Data Requirements (7%)

| Sub | Criteria | Scoring Anchor |
|---|---|---|
| D6.1 | Data entities & relationships | ER diagram or entity list → 100 |
| D6.2 | Data flows | Input→processing→output flows → 100 |
| D6.3 | Data retention & lifecycle | Retention policy defined → 100 |
| D6.4 | Data privacy & classification | PII/PHI identified, handling rules → 100 |

---

### D7 — Use Cases & Scenarios (11%)

| Sub | Criteria | Scoring Anchor |
|---|---|---|
| D7.1 | Actor identification | Primary + secondary actors listed → 100 |
| D7.2 | Main flow completeness | Step-by-step happy path → 100 |
| D7.3 | Alternative & exception flows | Alt/exception paths documented → 100 |
| D7.4 | Pre/post conditions | Both specified per UC → 100 |
| D7.5 | UC-to-FR traceability | Each UC maps to FR IDs → 100 |
| D7.6 | **Orphaned UC detection** | All UCs linked to ≥1 FR and ≥1 business goal → 100; Orphans found → deduct per orphan |
| D7.7 | **Business workflow coverage** | Key business processes modeled as UC sequences → 100; Missing workflows → deduct |
| D7.8 | **State transitions** | Lifecycle/state machines documented where applicable → 100 |

---

### D8 — Acceptance Criteria & Testing (9%)

| Sub | Criteria | Scoring Anchor |
|---|---|---|
| D8.1 | Measurable acceptance criteria | SMART criteria per feature → 100 |
| D8.2 | Test strategy/plan reference | E2E, integration, UAT strategy → 100 |
| D8.3 | Test data requirements | Test datasets specified → 100 |
| D8.4 | Sign-off process | Approval roles defined → 100 |

---

### D9 — Traceability & Consistency (8%)

| Sub | Criteria | Scoring Anchor |
|---|---|---|
| D9.1 | Requirements Traceability Matrix (RTM) | Forward + backward traceability → 100 |
| D9.2 | Internal consistency | No contradictions between sections → 100 |
| D9.3 | Version control & change history | Revision table present → 100 |
| D9.4 | Cross-reference integrity | All section references valid → 100 |
| D9.5 | **Bidirectional completeness** | Every FR has ≥1 UC, every UC has ≥1 FR, every BRD has ≥1 FR → 100 |
| D9.6 | **Workflow-to-UC mapping** | Business processes decomposed into traceable UCs → 100 |

---

### D10 — Document Quality & Standards (5%)

| Sub | Criteria | Scoring Anchor |
|---|---|---|
| D10.1 | ISO/IEC/IEEE 29148 structure compliance | All mandatory sections present → 100 |
| D10.2 | Writing quality (clarity, no ambiguity) | Precise language, no weasel words → 100 |
| D10.3 | Formatting consistency | Consistent heading numbering → 100 |

---

### D11 — Requirements Engineering Process (5%)

| Sub | Criteria | Scoring Anchor |
|---|---|---|
| D11.1 | Elicitation process documented | Sources, techniques, stakeholder sessions referenced → 100; Not mentioned → 0 |
| D11.2 | Validation & verification approach | How requirements were validated (reviews, prototypes, etc.) → 100 |
| D11.3 | Change management process | Change request workflow, impact analysis process → 100; Missing → 0 |
| D11.4 | Requirements baseline defined | Baseline version identified, approval gate documented → 100 |

---

### D12 — Requirement Quality Attributes (5%)

| Sub | Criteria | Scoring Anchor |
|---|---|---|
| D12.1 | Individual requirement quality | Each requirement is necessary, unambiguous, singular, feasible, verifiable per §5.2.5 → 100; Violations found → deduct per violation |
| D12.2 | Set-level quality | Requirement set is complete, consistent, affordable, bounded per §5.2.6 → 100 |
| D12.3 | Requirement language precision | No vague terms ("should", "might", "etc.", "appropriate", "as needed") → 100; Violations → deduct |
| D12.4 | Multi-level specification awareness | Document identifies its specification level (BRS/StRS/SyRS/SRS) and relationship to other levels → 100; Not mentioned → 50 |

---

## Evidence Requirements

Every subcriteria evaluation **must** include:

```json
{
  "id": "D3.6",
  "name": "MECE — Mutual Exclusivity",
  "score": 60,
  "comment": "Found 2 overlapping requirements between FR-012 and FR-018",
  "deductionReason": "Functional overlap: both FRs define user notification behavior",
  "evidence": ["FR-012: 'Hệ thống gửi thông báo khi...'", "FR-018: 'Gửi notification cho user khi...'"]
}
```

If the SRS lacks content for a criteria:
- `evidence`: `["Không tìm thấy nội dung liên quan trong tài liệu"]`
- `score`: reflects the absence (typically 0–20)

---

## Calculation Formula

$$Score = \sum_{i=1}^{12} (DimensionScore_i \times Weight_i)$$

Each dimension score = average of its subcriteria scores.

---

## Prompt Instruction Block

All AI prompts must include:

```text
SCORING INSTRUCTIONS:
Evaluate the SRS on a scale of 0-100 based on these weighted dimensions:
1. Purpose & Scope Clarity (8%) — 4 subcriteria
2. Stakeholder & User Requirements (9%) — 4 subcriteria
3. Functional Requirements (14%) — 7 subcriteria incl. MECE checks
4. Non-Functional Requirements (11%) — 5 subcriteria
5. System Architecture & Constraints (8%) — 4 subcriteria
6. Data Requirements (7%) — 4 subcriteria
7. Use Cases & Scenarios (11%) — 8 subcriteria incl. orphan detection & workflow coverage
8. Acceptance Criteria & Testing (9%) — 4 subcriteria
9. Traceability & Consistency (8%) — 6 subcriteria incl. bidirectional completeness
10. Document Quality & Standards (5%) — 3 subcriteria
11. Requirements Engineering Process (5%) — 4 subcriteria incl. elicitation & change mgmt
12. Requirement Quality Attributes (5%) — 4 subcriteria incl. language precision & spec-level awareness

EVIDENCE RULE:
- Every subcriteria MUST include verbatim evidence from the SRS.
- If content is missing, state "Không tìm thấy nội dung liên quan" and score accordingly.

MECE RULE:
- D3.6: Flag any FRs that overlap or contradict each other.
- D3.7: Flag any implied features that lack explicit FR coverage.

ORPHAN DETECTION RULE:
- D7.6: Flag any UC not linked to at least one FR and one business goal.
- D9.5: Flag any FR without a UC, any UC without an FR, any BRD without an FR.

WORKFLOW RULE:
- D7.7: Identify key business processes and check each is modeled as a UC sequence.
- D7.8: Check for state machines / lifecycle flows where applicable.

REQUIREMENTS ENGINEERING PROCESS RULE:
- D11.1: Check if elicitation sources and techniques are documented.
- D11.2: Check if validation approach (reviews, prototypes) is referenced.
- D11.3: Check if change management process is defined.
- D11.4: Check if requirements baseline version and approval gate are identified.

REQUIREMENT QUALITY ATTRIBUTES RULE (per ISO/IEC/IEEE 29148 §5.2.5–§5.2.6):
- D12.1: Sample individual requirements and check: necessary, unambiguous, singular, feasible, verifiable.
- D12.2: Evaluate requirement set: complete, consistent, affordable, bounded.
- D12.3: Flag vague language: "should", "might", "etc.", "appropriate", "as needed", "TBD".
- D12.4: Check if the document identifies its specification level (SRS/SyRS/StRS/BRS).

CALCULATION:
- Score each subcriteria (0-100) with evidence.
- Dimension score = average of subcriteria scores.
- Final Score = Round(weighted average of dimension scores).

CRITICAL:
- Final Score < 85 → "Needs Revision"
- Final Score >= 85 → "Ready for Development"
- Each dimension MUST have AT LEAST 2 issues with evidence.
```
