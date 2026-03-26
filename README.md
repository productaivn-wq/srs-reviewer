# SRS Reviewer

AI-powered quality assessment for Software Requirements Specifications (SRS).
Scores across **10 dimensions** with **49 subcriteria** based on IEEE 830 / ISO 29148 standards.

## Features

- 🔍 **10-Dimension Scoring** — Purpose, Stakeholders, Functional Reqs, NFRs, Architecture, Data, Use Cases, Acceptance, Traceability, Document Quality
- 📐 **MECE Validation** — Detects overlapping and missing requirements
- 🔗 **Orphaned UC Detection** — Flags use cases not linked to any FR or business goal
- 🔄 **Workflow Coverage** — Checks business processes are modeled as UC sequences
- 📝 **Evidence-Based** — Every score backed by verbatim SRS quotes
- 🌐 **Web App** — Modern React SPA with OpenRouter integration
- 💻 **CLI** — Python scripts for Standard and Strategic review modes

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ (for webapp)
- [OpenRouter](https://openrouter.ai) API key

### CLI Usage

```bash
# Install Python dependencies
pip install -r requirements.txt

# Set your OpenRouter API key
export OPENROUTER_API_KEY="sk-or-v1-..."

# Standard Review (quick quality check)
python core/scripts/review_standard.py "srs_docs/sample_project_srs.md" --reviewer "Your Name"

# Deep Strategic Review (architecture + business alignment)
python core/scripts/review_strategic.py "srs_docs/sample_project_srs.md" --reviewer "Your Name"
```

### Web App

```bash
cd webapp
npm install
npm run dev
# Open http://localhost:5173
```

Enter your OpenRouter API key in the UI, paste/upload an SRS document, and click **Review SRS**.

## Scoring Dimensions

| # | Dimension | Weight | Key Checks |
|---|---|---|---|
| D1 | Purpose & Scope | 10% | Purpose statement, scope boundaries, glossary |
| D2 | Stakeholders | 10% | Roles, profiles, needs mapping |
| D3 | Functional Reqs | 15% | Atomicity, testability, IDs, **MECE** |
| D4 | Non-Functional Reqs | 12% | Quantified NFRs (SLAs, security, compliance) |
| D5 | Architecture | 10% | Interfaces, dependencies, constraints |
| D6 | Data Requirements | 8% | Entities, flows, retention, privacy |
| D7 | Use Cases | 12% | Completeness, **orphan detection**, **workflow coverage** |
| D8 | Acceptance & Testing | 10% | SMART criteria, test strategy |
| D9 | Traceability | 8% | RTM, consistency, **bidirectional completeness** |
| D10 | Document Quality | 5% | IEEE 830 compliance, writing quality |

See [SCORING_CRITERIA.md](SCORING_CRITERIA.md) for the full 49-subcriteria rubric.

## Architecture

```
CLI Mode:      SRS File → SRSParser → StructureValidator → LLMClient (OpenRouter) → ReviewEngine → ReportRenderer → Markdown
Web App Mode:  Browser → React SPA → OpenRouter API → JSON → ScoreRing + RadarChart + DimensionCards
```

- **Backend**: Python 3.10+, `httpx` for HTTP
- **LLM Provider**: OpenRouter (supports Claude, GPT-4o, Gemini)
- **Frontend**: Vite + React + TypeScript, dark glassmorphism design
- **Hosting**: Cloudflare Pages (static SPA)

## Running Tests

```bash
python -m pytest tests/ -v
# Expected: 56 tests pass
```

## Deployment

```bash
cd webapp
npm run deploy  # Builds and deploys to Cloudflare Pages
```

## License

MIT
