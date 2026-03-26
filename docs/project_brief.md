# SRS Reviewer Project Brief

## Project Purpose
To provide an automated, AI-driven quality assessment and rewrite service for Software Requirements Specification (SRS) documents based on IEEE 830 and ISO 29148 standards.

## Scope
- Analyze SRS documents across 10 defined quality dimensions.
- Output detailed, structured JSON scores highlighting praise, issues, and deductions.
- Enable lossless rewriting of SRS documents to enhance structure and ensure completeness.

## Key Components
1. **SRS Analysis Skill**: The core framework for 10-dimension evaluation.
2. **SRS Rewrite Skill**: The framework for lossless restructuring.
3. **Core Engine**: Python libraries linking the skills to LLM clients, enabling both standard and strategic reviews.
