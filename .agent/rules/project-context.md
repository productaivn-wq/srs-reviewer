---
trigger: always_on
description: Context Filtering Rule — Binds SRSReviewer Project to Specific Skills
---

# Project Context Rules for SRSReviewer

## 1. Active Skills
| Skill | Status | Description |
|---|---|---|
| SRSAnalysis | active | 12-dimension ISO/IEC/IEEE 29148 based SRS scoring framework |
| SRSRewrite | active | Lossless SRS rewriting and structural enhancement |
| DocumentControl | active | AI-powered document organization |
| TaskManager | active | Task sync between Markdown and Jira |

## 2. Dynamic Rules
*   **When user mentions "SRS Reviewer" or "SRS Review"**:
    *   Focus on `projects/SRSReviewer/`
    *   Use `SRSAnalysis`, `DocumentControl`.
