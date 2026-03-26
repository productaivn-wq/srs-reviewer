---
name: SRS Rewrite
description: Lossless SRS rewriting with ISO/IEC/IEEE 29148 structure enhancement, section-level splitting, and targeted gap-filling.
version: 1.0.0
status: active
triggers:
  - "rewrite SRS"
  - "improve SRS"
  - "viết lại SRS"
  - "cải thiện SRS"
  - "upgrade SRS"
---

# SRS Rewrite Skill

Rewrite an SRS to fix issues found during analysis while maintaining **100% of the original content**. Enhances structure to follow ISO/IEC/IEEE 29148 standards.

## How to Use

When the user asks you to rewrite/improve an SRS:

1. Read the original SRS content
2. Read the analysis results (from SRSAnalysis skill output)
3. For short SRSs (≤3 sections): rewrite the entire document in one pass
4. For large SRSs (>3 sections): split into sections, rewrite each section with targeted issues, reassemble
5. Output the complete rewritten SRS in Markdown

---

## Core Principle: LOSSLESS Editing

> **You are a "LOSSLESS SRS EDITOR"**. The rewritten SRS MUST be **equal length or LONGER** than the original. You must NEVER summarize, truncate, or omit any context, reasoning, or detail from the original SRS. If a section has no issues, **copy it verbatim** into the output.

---

## Mandatory Rules (DO NOT VIOLATE)

1. **DO NOT summarize**, shorten, or skip any context, reasoning, or detail — no matter how small.
2. **PRESERVE ALL identifiers** (UC-xxx, US-xxx, FR-xxx, NFR-xxx, IDs, codes). Do NOT rename, remove, or renumber them.
3. **PRESERVE ALL tables** — do not convert tables to lists. If adding columns, keep existing rows intact. Use compact markdown tables (`|---|---|`).
4. **PRESERVE ALL detailed content** within each item, including sub-bullets, examples, notes, definitions.
5. **ABSOLUTELY NO HTML tags** — use pure Markdown syntax only.
6. Return **ONLY the Markdown content**, no explanations.
7. All content in **Vietnamese**.

---

## Heading Hierarchy Rules

The rewritten SRS MUST follow strict Markdown hierarchy:

| Level | Usage | Example |
|-------|-------|---------|
| `#` | Document title (exactly ONE) | `# Hệ thống thanh toán V2 - SRS` |
| `##` | Major sections (ISO/IEC/IEEE 29148) | `## 1. Mục đích` |
| `###` | Subsections | `### 1.1 Phạm vi sản phẩm` |
| `####` | Use Cases, Structural blocks | `#### UC-001: Đặt hàng online` |
| `#####` | Atomic items | `##### FR-001.1` |

---

## Enhancement Requirements

When rewriting, ADD the following if missing (never remove existing content):

### ISO/IEC/IEEE 29148 Structure Alignment

Ensure the document is structured following standard industry practices containing at least:
1. **Mục đích & Phạm vi (Purpose & Scope)**
2. **Tổng quan (Overall Description)**
3. **Yêu cầu chức năng (Functional Requirements)** - Structured as Features or Use Cases
4. **Yêu cầu phi chức năng (Non-Functional Requirements)** - Quantified
5. **Ràng buộc phần cứng & phần mềm (Constraints)**

### Acceptance Criteria & Quantified NFRs
- Every functional requirement must have unambiguous Given/When/Then acceptance criteria.
- Every non-functional requirement must have a measurable benchmark.
