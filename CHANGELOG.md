# Changelog

All notable changes to SRS Reviewer are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2026-03-26

### 🎉 First Release — ISO/IEC/IEEE 29148:2018

First public release of the SRS Reviewer, an AI-driven quality assessment tool for Software Requirements Specification documents based on the **ISO/IEC/IEEE 29148:2018** standard.

### Features
- **12-dimension scoring rubric** aligned with ISO/IEC/IEEE 29148:2018:
  - D1 — Purpose & Scope (8%)
  - D2 — Stakeholders & User Needs (9%)
  - D3 — Functional Requirements (14%)
  - D4 — Non-Functional Requirements (11%)
  - D5 — System Architecture & Constraints (8%)
  - D6 — Data Requirements (7%)
  - D7 — Use Cases & Scenarios (11%)
  - D8 — Acceptance Criteria & Testing (9%)
  - D9 — Traceability & Consistency (8%)
  - D10 — Document Quality & Standards (5%)
  - D11 — Requirements Engineering Process (5%)
  - D12 — Requirement Quality Attributes (5%)
- **3 review modes**: Standard, Strategic (with PRD alignment), and Alignment-only.
- **Webapp** with OpenRouter LLM integration for browser-based reviews.
- **CLI scripts** for batch review (`review_standard.py`, `review_strategic.py`).
- **Structure validator** with 4 mandatory ISO/IEC/IEEE 29148 sections.
- **SRS template** following ISO/IEC/IEEE 29148 recommended outline.
- **SRSAnalysis** and **SRSRewrite** extracted skills.
- Issue types: `missing_logic`, `ambiguous_wording`, `missing_edge_case`, `missing_validation`, `domain_safety`, `process_gap`, `quality_violation`.
