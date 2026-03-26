---
trigger: always_on
---

# SRSReviewer Architecture Rules

## 1. Directory Structure

```text
projects/
└── SRSReviewer/
    ├── .agent/                    # [POLICY] Local agent rules and workflows
    ├── extracted_skills/          # [LOCAL SKILLS] SRSAnalysis and SRSRewrite
    ├── core/                      # [LOGIC] Review engine, LLM client, parsers, CLI scripts
    ├── docs/                      # [CONTEXT] Architecture, Best Practices, Project Brief
    ├── templates/                 # [STANDARDS] SRS definition templates (e.g. IEEE 830)
    ├── srs_docs/                  # [DATA] Input SRS files
    ├── reviews/                   # [DATA] Output review artifacts
    └── tracking/                  # [MEMORY] Task status and history logs
```

## 2. Constraints
- **Separation of Concerns**: `core/` contains Python logic, detached from `extracted_skills/`. Skills invoke `core/scripts`.
- **Stateless Execution**: Reviews must be reproducible based on `srs_docs/` input and the chosen LLM configuration.
