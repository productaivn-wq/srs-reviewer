# SRS Reviewer — Function List

All code functions, classes, and methods grouped by component.
Consistent with [system_architect.md](system_architect.md).

---

## 1. Core Library (`core/lib/`)

### `srs_parser.py` — SRS Document Parser

| Entity | Type | Signature | Description |
|---|---|---|---|
| `SRSParser` | class | `__init__(srs_path: str)` | Parse SRS markdown files and extract structured content |
| | method | `_load_content() -> str` | Load SRS file content from disk |
| | method | `_parse_sections() -> Dict[str, str]` | Parse markdown sections based on heading hierarchy |
| | method | `get_section(section_name: str) -> Optional[str]` | Get section content by name (case-insensitive fuzzy match) |
| | method | `get_all_sections() -> Dict[str, str]` | Return all parsed sections |
| | method | `get_section_list() -> List[str]` | Return list of section names |

### `structure_validator.py` — IEEE 830 Structure Gate Check

| Entity | Type | Signature | Description |
|---|---|---|---|
| `MANDATORY_SECTIONS` | const | `List[str]` | Required sections: Introduction, Overall Description, Specific Requirements |
| `normalize_section_name` | func | `(name: str) -> str` | Clean and lowercase a section name for matching |
| `validate_structure` | func | `(srs_parser, strict=False) -> Tuple[bool, List, List]` | Validate SRS has mandatory structural sections |

### `llm_client.py` — OpenRouter API Client

| Entity | Type | Signature | Description |
|---|---|---|---|
| `DEFAULT_MODEL` | const | `str` | Default model: `anthropic/claude-sonnet-4-20250514` |
| `DEFAULT_BASE_URL` | const | `str` | `https://openrouter.ai/api/v1` |
| `_extract_json` | func | `(text: str) -> str` | Extract JSON from LLM markdown-fenced responses |
| `LLMClient` | class | `__init__(api_key=None, model=DEFAULT_MODEL, base_url=DEFAULT_BASE_URL)` | OpenRouter LLM client using httpx |
| | method | `generate_content(prompt, system_instruction=None, timeout=300) -> str` | Send prompt to OpenRouter chat completions, return extracted JSON |
| | method | `close() -> None` | No-op (kept for interface compatibility) |

### `review_engine.py` — 10-Dimension Scoring Engine

| Entity | Type | Signature | Description |
|---|---|---|---|
| `SYSTEM_INSTRUCTION` | const | `str` | System-level instruction for the LLM |
| `SRSReviewEngine` | class | `__init__(llm_client: LLMClient)` | Orchestrate SRS review with LLM |
| | method | `review_srs(srs_parser, prompt_template) -> Dict` | Execute review and return validated result |
| | method | `_validate_and_enrich(result: Dict) -> Dict` | Validate LLM score against recalculation and enrich output |
| | static | `get_dimension_weights() -> Dict` | Return canonical dimension weight mapping |

### `report_renderer.py` — Markdown Report Generator

| Entity | Type | Signature | Description |
|---|---|---|---|
| `DIMENSION_WEIGHTS` | const | `Dict[str, Dict]` | 10-dimension weight mapping (D1-D10) |
| `VERDICT_MAP` | const | `List[Tuple]` | Score-to-verdict threshold mapping |
| `get_verdict` | func | `(score: float) -> str` | Map score to verdict string |
| `get_status_emoji` | func | `(score: float) -> str` | Return emoji indicator for score |
| `recalculate_score` | func | `(sections: list) -> float` | Recalculate weighted total from per-dimension scores |
| `ReportRenderer` | class | `__init__(reviewer="SRS Review AI", mode="Standard")` | Render ReviewResult into markdown |
| | method | `render(review_result, srs_filename) -> str` | Render full markdown report string |
| | method | `save(report, output_path, reviews_dir) -> Path` | Save report to file |
| | method | `_executive_summary(total_score, sections) -> str` | Generate executive summary paragraph |
| | method | `_render_dimension(section: Dict) -> str` | Render single dimension breakdown |
| | method | `_render_error(result, srs_filename) -> str` | Render error report |

---

## 2. CLI Scripts (`core/scripts/`)

### `review_standard.py` — Standard Review CLI

| Entity | Type | Signature | Description |
|---|---|---|---|
| `main` | func | `() -> int` | Entry point for standard review mode |
| `print_summary` | func | `(result: dict) -> None` | Print console scoring summary with emoji |

### `review_strategic.py` — Strategic Review CLI

| Entity | Type | Signature | Description |
|---|---|---|---|
| `main` | func | `() -> int` | Entry point for deep strategic review mode |
| `print_summary` | func | `(result: dict) -> None` | Print console scoring summary with emoji |

---

## 3. Web App (`webapp/src/`) — Phase 2 React SPA

### Components

| Entity | Type | File | Description |
|---|---|---|---|
| `App` | component | `App.tsx` | Root app with state management and layout |
| `Hero` | component | `Hero.tsx` | Landing hero with gradient title and badge |
| `ConfigPanel` | component | `ConfigPanel.tsx` | API key, model, mode, reviewer inputs |
| `SRSInput` | component | `SRSInput.tsx` | File drop zone + textarea for SRS content |
| `ReviewButton` | component | `ReviewButton.tsx` | Submit button with spinner loading state |
| `ResultsSection` | component | `ResultsSection.tsx` | Composite results view |
| `ScoreRing` | component | `ScoreRing.tsx` | SVG animated score circle |
| `RadarChart` | component | `RadarChart.tsx` | Canvas-based 10-dimension radar chart |
| `DimensionCard` | component | `DimensionCard.tsx` | Expandable card with praise/issues/suggestions |
| `ReviewHistory` | component | `ReviewHistory.tsx` | localStorage-backed review history list |

### Services & Utilities

| Entity | Type | File | Description |
|---|---|---|---|
| `callOpenRouter` | func | `services/openrouter.ts` | Send review prompt to OpenRouter API |
| `useHistory` | hook | `hooks/useHistory.ts` | React hook for localStorage review history |
| `recalculateScore` | func | `utils/scoring.ts` | Weighted score recalculation |
| `buildPrompt` | func | `utils/scoring.ts` | Build review prompt with SRS content |
| `DIMENSION_WEIGHTS` | const | `utils/constants.ts` | D1-D10 weight mapping |
| `DIMENSION_TITLES` | const | `utils/constants.ts` | Vietnamese dimension title labels |
| `ReviewResult` | type | `types/review.ts` | TypeScript interface for review JSON |
| `Section` | type | `types/review.ts` | TypeScript interface for dimension section |
| `Issue` | type | `types/review.ts` | TypeScript interface for issue item |
