/** TypeScript interfaces for SRS Review data structures */

export interface PraiseItem {
  praise: string;
  evidence?: string[];
}

export interface Issue {
  issue: string;
  severity: 'critical' | 'major' | 'minor' | 'nice to have';
  evidence?: string[];
}

export interface Section {
  title: string;
  score: number;
  status: 'pass' | 'fail';
  praise: PraiseItem[];
  issues: Issue[];
  suggestions: string[];
}

export interface ReviewResult {
  totalScore: number;
  verdict: string;
  sections: Section[];
  recalculatedScore?: number;
  scoreValid?: boolean;
  dimensionCount?: number;
}

export interface HistoryEntry {
  filename: string;
  mode: string;
  model: string;
  totalScore: number;
  verdict: string;
  result: ReviewResult;
  timestamp: string;
}
