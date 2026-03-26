# SRS Reviewer System Architect

## Phase 1: CLI-Based Architecture (Current)
The initial release operates via local CLI using the Antigravity framework.
- **Frontend**: Local terminal via agentic workflows.
- **Backend Core**: Python 3.10+ with `httpx` for HTTP requests.
- **LLM Provider**: OpenRouter API (`https://openrouter.ai/api/v1`), OpenAI-compatible chat completions.
- **Default Model**: `anthropic/claude-sonnet-4-20250514` (configurable via constructor).
- **Skills**: `SRSAnalysis` and `SRSRewrite` configured in `.agent/rules/project-context.md`.
- **Infrastructure**: Local files — `srs_docs/` for input, `reviews/` for output.

## Phase 2: Web App (Current)
A modern React SPA that calls OpenRouter directly from the client.
- **Frontend**: Vite + React + TypeScript, dark glassmorphism design system.
- **Hosting**: Cloudflare Pages (static SPA).
- **API**: Client-side OpenRouter calls (user-supplied API key).
- **Storage**: `localStorage` for review history (up to 20 entries).

## Phase 3: Backend Services (Future)
- **Backend API**: Cloudflare Workers for server-side review orchestration.
- **Storage**: Supabase for historical review telemetry, LLM response caching, and team sharing.
