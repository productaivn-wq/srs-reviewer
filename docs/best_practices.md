# Best Practices for SRS Review

## SRS Evaluation Patterns
1. **Praise is as important as Critique**: Always balance the feedback. Pointing out what a product manager did well reinforces good documentation habits.
2. **Context-Aware Deductions**: If an SRS omits a feature because the architecture clearly states it is out of scope, do not penalize it.
3. **Evidence-based Scoring**: Any point deductions MUST be backed by an exact quote showing the ambiguity or flaw in the source document.

## Common Pitfalls
- **Missing Traceability**: Requirements often lack a backward trace to business goals. 
- **Unquantified NFRs**: Statements like "the system must be fast" are unacceptable. Expect exact metrics (e.g., "P99 < 200ms").
- **Structural Inconsistency**: Omitting standard sections like 'Overall Description' causes parsing errors.

## LLM Prompt Engineering Lessons
- **Template Echoing Control**: When providing JSON schemas, do NOT use phrasing like "Return EXACTLY this JSON structure". Claude may interpret this literally and echo the schema variables back without generating content. Instead, explicitly instruct the model to "generate a valid JSON object matching this structure" and "replace the bracketed placeholders with your actual evaluated data".
- **Tool Restriction**: Explicitly forbid tool usage (`DO NOT use any tools. DO NOT attempt to write files`) in system instructions when you only want raw JSON output, otherwise the agent may try to perform actions instead of returning the required generation.

*Ensure all bug-fixes related to parsing updates are appended here.*
