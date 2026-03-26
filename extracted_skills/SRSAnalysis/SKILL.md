---
name: SRS Analysis
description: 10-dimension SRS quality scoring framework based on IEEE 830 / ISO 29148 standards, with weighted subcriteria, PRD alignment checking, domain safety profiles, issue type classification, and annotated SRS output.
version: 1.1.0
status: active
triggers:
  - "review SRS"
  - "analyze SRS"
  - "score SRS"
  - "SRS quality"
  - "đánh giá SRS"
  - "PRD alignment"
  - "SRS alignment"
  - "domain safety"
---

# SRS Analysis Skill

Perform a comprehensive, evidence-based quality assessment of a Software Requirements Specification (SRS) using a 10-dimension scoring framework. Each dimension is scored independently with weighted subcriteria, producing a structured JSON result with a total weighted score and verdict.

## How to Use

When the user asks you to analyze/review/score an SRS:

1. Read the SRS content (from file, URL, or pasted text)
2. Run **Structure Validation** first (gate check)
3. Score all **10 dimensions** in one pass
4. Calculate the **weighted total score**
5. Return structured results in the JSON output format below

---

## Step 1: Structure Validation (Gate Check)

Verify the SRS contains the expected core structural elements. Ensure the SRS follows a logical flow covering these essentials (keyword match, supports English/Vietnamese):

| Required Section | Keywords to Match |
|-----------------|-------------------|
| Purpose & Scope | `purpose`, `mục đích`, `scope`, `phạm vi` |
| Overall Description | `overall description`, `tổng quan`, `user characteristics`, `đặc điểm người dùng`, `constraints`, `ràng buộc` |
| Specific Requirements | `specific requirements`, `yêu cầu cụ thể`, `functional requirements`, `yêu cầu chức năng`, `non-functional`, `phi chức năng` |

If missing critical elements → return `{ structureFailed: true, missingSections: [...] }` and STOP.

---

## Step 2: Score All 10 Dimensions

### Dimension Definitions

Each dimension has an ID, title, weight (% of total), and core question. Default all subcriteria within a dimension equally unless specified.

#### D1 — Purpose & Scope Clarity · Weight: 10%
**Core question:** Is the system purpose, scope, and context clearly defined?

#### D2 — Stakeholder & User Requirements · Weight: 10%
**Core question:** Are all stakeholders identified with their needs documented?

#### D3 — Functional Requirements · Weight: 15%
**Core question:** Are functional requirements specific, testable, and traceable?

#### D4 — Non-Functional Requirements · Weight: 12%
**Core question:** Are NFRs (performance, security, reliability, etc.) quantified?

#### D5 — System Architecture & Constraints · Weight: 10%
**Core question:** Are system interfaces, constraints, and dependencies documented?

#### D6 — Data Requirements · Weight: 8%
**Core question:** Are data models, flows, and storage requirements specified?

#### D7 — Use Cases & Scenarios · Weight: 12%
**Core question:** Are use cases complete with actors, flows, and exceptions?

#### D8 — Acceptance Criteria & Testing · Weight: 10%
**Core question:** Are acceptance criteria measurable and test plans defined?

#### D9 — Traceability & Consistency · Weight: 8%
**Core question:** Are requirements traceable to business goals and internally consistent?

#### D10 — Document Quality & Standards · Weight: 5%
**Core question:** Does the document follow IEEE 830/ISO 29148 structure?

---

## Step 3: Scoring Rules

### Scoring Rubric (per subcriteria)
- **96–100**: Xuất sắc (Excellent — Production-ready)
- **85–95**: Tốt (Good — Solid foundation)
- **70–84**: Cần cải thiện (Needs Improvement — Has gaps)
- **50–69**: Yếu (Weak — Needs rewriting)
- **0–49**: Nghiêm trọng (Critical — Start over)

### Calculation Formula
```
Score = Σ (DimensionScore × Weight)
```

**CRITICAL RULE:**
- If Final Score < 85, the Overall Status MUST be "Needs Revision".
- If Final Score >= 85, the Overall Status is "Ready".

---

## Step 4: Output Format

All output MUST be in **Vietnamese**. Return the following JSON structure:

```json
{
  "totalScore": 75,
  "verdict": "Cần cải thiện — Có lỗ hổng",
  "sections": [
    {
      "title": "D1 — Mục đích & Phạm vi",
      "score": 72,
      "status": "pass",
      "subcriteria": [
        {
          "id": "D1.1",
          "name": "Tên tiêu chí con",
          "score": 80,
          "comment": "Nhận xét ngắn gọn",
          "deductionReason": "Lý do",
          "wbs": "1.2.3",
          "evidence": ["Trích dẫn"]
        }
      ],
      "praise": [
        {
          "praise": "Điểm tốt",
          "evidence": ["Trích dẫn"]
        }
      ],
      "issues": [
        {
          "issue": "Vấn đề",
          "severity": "critical | major | minor | nice to have",
          "wbs": "1.2.3",
          "evidence": ["Trích dẫn"]
        }
      ],
      "suggestions": ["Gợi ý"]
    }
  ]
}
```

### Output Rules
- All content MUST be in Vietnamese.
- Each praise/issue MUST include an `evidence` array with verbatim quotes from the SRS.
- Score FAIRLY: acknowledge both strengths and weaknesses.
- Each dimension MUST have AT LEAST 2 issues.
