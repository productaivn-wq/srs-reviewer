import type { ReviewResult } from '../types/review';
import { SYSTEM_INSTRUCTION } from '../utils/constants';
import { buildPrompt } from '../utils/scoring';

const OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions';

/**
 * Extract JSON from an LLM response, stripping markdown fences.
 */
function extractJson(text: string): string {
  const fenceMatch = text.match(/```(?:json)?\s*\n?(.*?)\n?```/s);
  if (fenceMatch) return fenceMatch[1].trim();

  const trimmed = text.trim();
  const start = trimmed.indexOf('{');
  const end = trimmed.lastIndexOf('}');
  if (start !== -1 && end > start) return trimmed.slice(start, end + 1);

  return trimmed;
}

export interface ReviewRequest {
  apiKey: string;
  model: string;
  mode: string;
  srsContent: string;
  prdContent?: string;
}

/**
 * Call OpenRouter and return parsed ReviewResult.
 * Throws on API errors.
 */
export async function callOpenRouter(req: ReviewRequest): Promise<ReviewResult> {
  const prompt = buildPrompt(req.srsContent, req.mode, req.prdContent);

  const response = await fetch(OPENROUTER_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${req.apiKey}`,
      'Content-Type': 'application/json',
      'HTTP-Referer': 'https://srs-reviewer.pages.dev',
      'X-Title': 'SRS Reviewer',
    },
    body: JSON.stringify({
      model: req.model,
      messages: [
        { role: 'system', content: SYSTEM_INSTRUCTION },
        { role: 'user', content: prompt },
      ],
      temperature: 0,
      max_tokens: 16384,
    }),
  });

  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`API Error (${response.status}): ${errText.slice(0, 200)}`);
  }

  const data = await response.json();
  const rawContent = data.choices[0].message.content;
  const jsonStr = extractJson(rawContent);
  const result: ReviewResult = JSON.parse(jsonStr);

  return result;
}
