/** TypeScript interfaces for SRS Review data structures */

export interface PraiseItem {
  praise: string;
  evidence?: string[];
}

export interface Issue {
  issue: string;
  severity: 'critical' | 'major' | 'minor' | 'nice to have';
  issueType?: string;
  evidence?: string[];
}

export interface Section {
  title: string;
  score: number;
  status: 'pass' | 'fail';
  subcriteria?: SubCriterion[];
  praise: PraiseItem[];
  issues: Issue[];
  suggestions: string[];
}

export interface SubCriterion {
  id: string;
  name: string;
  score: number;
  comment: string;
  deductionReason?: string;
  evidence?: string[];
}

export interface AlignmentItem {
  prdItem?: string;
  srsItem?: string;
  prdIntent?: string;
  srsInterpretation?: string;
  evidence?: string;
  severity: 'critical' | 'major' | 'minor';
}

export interface AlignmentResult {
  summary: string;
  missingFromPRD: AlignmentItem[];
  scopeCreep: AlignmentItem[];
  intentMismatch: AlignmentItem[];
  signOffGaps: string[];
}

export interface ReviewResult {
  totalScore: number;
  verdict: string;
  sections: Section[];
  alignment?: AlignmentResult;
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
