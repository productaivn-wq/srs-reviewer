---
description: Review an SRS document using the SRS Reviewer project skills
---

# SRS Review Workflow (Local)

// turbo-all

Unified workflow for reviewing Software Requirement Specification documents based on IEEE 830 and ISO 29148.

## Prerequisites
- Python 3.10+ with `httpx` installed (`pip install httpx`)
- OpenRouter API key set as `OPENROUTER_API_KEY` environment variable
- Default model: `anthropic/claude-sonnet-4-20250514` (Claude via OpenRouter)

## Mode Selection

| Mode | When to Use |
|---|---|
| **Standard** | Routine reviews, first-pass quality check |
| **Strategic** | High-stakes SRS, architectural decisions, GTM |

---

## Mode 1: Standard Review

```bash
python "core/scripts/review_standard.py" "<path/to/srs.md>" --output "<output.md>" --reviewer "Name"
```

## Mode 2: Deep Strategic Review

```bash
python "core/scripts/review_strategic.py" "<path/to/srs.md>" --output "<output.md>" --reviewer "Name"
```

---

## CLI Reference

| Argument | Description | Default |
|---|---|---|
| `file` | Path to SRS markdown file (required) | — |
| `--output` | Custom output file path | `reviews/review-YYYY-MM-DD-HHmm.md` |
| `--reviewer` | Reviewer name in report header | `SRS Review AI` |

## Running Tests

```bash
python -m pytest tests/ -v
```
