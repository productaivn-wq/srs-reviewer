# Changelog

All notable changes to SRS Reviewer are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/).

---

## [2.0.0] — 2026-03-26

### ⚡ Breaking Change: ISO/IEC/IEEE 29148:2018 Upgrade

Migrated the entire scoring framework from the legacy IEEE 830 (1998) standard to the modern ISO/IEC/IEEE 29148:2018 standard. This is a major version bump because the rubric structure, dimension count, and weight distribution have all changed.

### Added
- **D11 — Requirements Engineering Process** (5%): Evaluates elicitation documentation, validation approach, change management process, and requirements baseline definition.
- **D12 — Requirement Quality Attributes** (5%): Evaluates individual requirement quality per §5.2.5 (necessary, unambiguous, singular, feasible, verifiable), set-level quality per §5.2.6, language precision, and multi-level specification awareness (BRS/StRS/SyRS/SRS layering).
- New issue types: `process_gap`, `quality_violation`.
- New mandatory section in structure validation: "Stakeholder Requirements".
- SRS template restructured with stakeholder requirements, specification level, and RE process sections.
- `VERSION` file and `CHANGELOG.md` for release tracking.

### Changed
- Rubric expanded from **10 → 12 dimensions**.
- All existing dimension weights rebalanced (D1: 10%→8%, D2: 10%→9%, D3: 15%→14%, D4: 12%→11%, D5: 10%→8%, D6: 8%→7%, D7: 12%→11%, D8: 10%→9%, D9: 8%→8%, D10: 5%→5%).
- All prompt templates (standard, strategic, alignment) rewritten with D11/D12 subcriteria and evidence rules.
- Webapp constants, Hero badge, footer, and meta description updated to reference ISO/IEC/IEEE 29148.
- SRSAnalysis skill upgraded to v2.0.0.
- SRSRewrite skill updated to reference ISO/IEC/IEEE 29148.

### Removed
- All references to "IEEE 830" as the primary standard (retained only in `best_practices.md` upgrade history and existing review artifacts).

### Files Modified (24)
| Layer | Files |
|---|---|
| Scoring | `SCORING_CRITERIA.md` |
| Core Python | `report_renderer.py`, `review_engine.py`, `structure_validator.py` |
| Prompts | `srs_review_prompt.txt`, `srs_strategic_prompt.txt`, `srs_alignment_prompt.txt` |
| CLI Scripts | `generate_prompts.py`, `review_standard.py`, `review_strategic.py` |
| Webapp | `constants.ts`, `Hero.tsx`, `App.tsx`, `index.html` |
| Skills | `SRSAnalysis/SKILL.md`, `SRSRewrite/SKILL.md` |
| Template | `SRS_Template_Standard.md` |
| Docs | `project_brief.md`, `function_list.md`, `best_practices.md` |
| Agent Rules | `.agent/rules/project-context.md` |
| Tests | `test_review_engine.py`, `test_structure_validator.py` |

---

## [1.0.0] — 2026-03-25

### Initial Release
- 10-dimension IEEE 830 / ISO 29148 scoring framework.
- Standard, Strategic, and Alignment review modes.
- Webapp with OpenRouter LLM integration.
- CLI scripts for batch review.
- SRSAnalysis and SRSRewrite skills.
