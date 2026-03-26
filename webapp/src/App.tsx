import { useState, useCallback, useEffect } from 'react';
import { Hero } from './components/Hero';
import { ConfigPanel } from './components/ConfigPanel';
import { DocumentInput } from './components/DocumentInput';
import { ReviewButton } from './components/ReviewButton';
import { ResultsSection } from './components/ResultsSection';
import { ReviewHistory } from './components/ReviewHistory';
import { callOpenRouter } from './services/openrouter';
import { recalculateScore } from './utils/scoring';
import { useHistory } from './hooks/useHistory';
import { MODEL_OPTIONS, REVIEW_MODES } from './utils/constants';
import type { ReviewResult } from './types/review';
import './App.css';

export default function App() {
  // Config state
  const [apiKey, setApiKey] = useState(() => localStorage.getItem('srs_openrouter_key') ?? '');
  const [mode, setMode] = useState('standard');
  const [model, setModel] = useState<string>(MODEL_OPTIONS[0].value);
  const [reviewer, setReviewer] = useState('SRS Review AI');

  // Content state
  const [srsContent, setSrsContent] = useState('');
  const [prdContent, setPrdContent] = useState('');

  // Review state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<ReviewResult | null>(null);

  // History
  const { history, addEntry } = useHistory();

  // Persist API key
  useEffect(() => {
    localStorage.setItem('srs_openrouter_key', apiKey);
  }, [apiKey]);

  const selectedMode = REVIEW_MODES.find(m => m.value === mode);
  const needsPrd = selectedMode?.requiresPrd && prdContent.trim().length === 0;
  const canReview = apiKey.trim().length > 0 && srsContent.trim().length > 0 && !needsPrd;

  const handleReview = useCallback(async () => {
    if (!canReview || loading) return;

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const reviewResult = await callOpenRouter({
        apiKey: apiKey.trim(),
        model,
        mode,
        srsContent: srsContent.trim(),
        prdContent: prdContent.trim() || undefined,
      });

      // Validate & enrich
      const recalc = recalculateScore(reviewResult.sections ?? []);
      reviewResult.recalculatedScore = recalc;
      reviewResult.scoreValid = Math.abs(recalc - (reviewResult.totalScore ?? 0)) <= 2;

      setResult(reviewResult);

      // Save to history
      addEntry({
        filename: 'SRS Review',
        mode,
        model,
        totalScore: reviewResult.totalScore,
        verdict: reviewResult.verdict,
        result: reviewResult,
        timestamp: new Date().toISOString(),
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  }, [canReview, loading, apiKey, model, mode, srsContent, prdContent, addEntry]);

  const handleLoadHistory = useCallback((historyResult: ReviewResult) => {
    setResult(historyResult);
  }, []);

  return (
    <div className="container">
      <Hero />

      <ConfigPanel
        apiKey={apiKey} mode={mode} model={model} reviewer={reviewer}
        hasPrd={prdContent.trim().length > 0}
        onApiKeyChange={setApiKey} onModeChange={setMode}
        onModelChange={setModel} onReviewerChange={setReviewer}
      />

      <section className="glass section-spacing" id="documentsSection">
        <h2>📄 Documents</h2>
        <div className="doc-inputs-row">
          <DocumentInput
            id="srsContent"
            title="SRS Document"
            icon="📋"
            content={srsContent}
            onChange={setSrsContent}
            placeholder={'Paste your SRS content here in Markdown format...\n\n# 1. Introduction\n## 1.1 Purpose\n...'}
          />
          <DocumentInput
            id="prdContent"
            title="PRD / Reference Document"
            icon="📑"
            content={prdContent}
            onChange={setPrdContent}
            placeholder={'Paste your PRD, User Stories, or Acceptance Criteria here...\n\nUsed for alignment analysis.'}
            optional
          />
        </div>
      </section>

      {error && (
        <div className="error-banner" id="errorBanner">❌ {error}</div>
      )}

      <ReviewButton
        disabled={!canReview}
        loading={loading}
        onClick={handleReview}
      />

      {result && (
        <ResultsSection result={result} reviewer={reviewer} mode={mode} />
      )}

      <ReviewHistory history={history} onLoad={handleLoadHistory} />

      <footer className="footer">
        <p>
          SRS Reviewer — Powered by{' '}
          <a href="https://openrouter.ai" target="_blank" rel="noopener noreferrer">OpenRouter</a>
          {' '}· ISO/IEC/IEEE 29148
        </p>
      </footer>
    </div>
  );
}
