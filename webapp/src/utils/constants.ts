/** Vietnamese dimension titles for the 10 IEEE 830 scoring dimensions */
export const DIMENSION_TITLES = [
  'D1 — Mục đích & Phạm vi',
  'D2 — Bên liên quan & Yêu cầu người dùng',
  'D3 — Yêu cầu chức năng',
  'D4 — Yêu cầu phi chức năng',
  'D5 — Kiến trúc hệ thống & Ràng buộc',
  'D6 — Yêu cầu dữ liệu',
  'D7 — Use Case & Kịch bản',
  'D8 — Tiêu chí nghiệm thu & Kiểm thử',
  'D9 — Truy xuất nguồn gốc & Tính nhất quán',
  'D10 — Chất lượng tài liệu & Tiêu chuẩn',
] as const;

/** Dimension weight mapping aligned with SCORING_CRITERIA.md */
export const DIMENSION_WEIGHTS: Record<string, number> = {
  D1: 0.10, D2: 0.10, D3: 0.15, D4: 0.12, D5: 0.10,
  D6: 0.08, D7: 0.12, D8: 0.10, D9: 0.08, D10: 0.05,
};

/** Model options for the config panel */
export const MODEL_OPTIONS = [
  { value: 'anthropic/claude-sonnet-4-20250514', label: 'Claude Sonnet 4 (Default)' },
  { value: 'anthropic/claude-3.5-sonnet', label: 'Claude 3.5 Sonnet' },
  { value: 'google/gemini-2.5-flash-preview', label: 'Gemini 2.5 Flash' },
  { value: 'openai/gpt-4o', label: 'GPT-4o' },
] as const;

/** System instruction sent to the LLM */
export const SYSTEM_INSTRUCTION = `You are an expert system architect and business analyst reviewing an SRS document according to IEEE 830 and ISO 29148 standards.
CRITICAL: Your ENTIRE response must be a single valid JSON object — no explanation, no markdown, no text before or after. Just pure JSON.
Each dimension MUST have at least 2 issues. Review must be in Vietnamese.
DO NOT output the template variables verbatim; you must fill them with your actual evaluation.`;

export const STORAGE_KEY = 'srs_reviewer_history';
export const MAX_HISTORY = 20;
