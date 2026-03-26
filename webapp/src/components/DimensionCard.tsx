import { useState } from 'react';
import type { Section, PraiseItem, Issue } from '../types/review';
import './DimensionCard.css';

interface Props {
  section: Section;
}

export function DimensionCard({ section }: Props) {
  const [expanded, setExpanded] = useState(false);
  const score = section.score ?? 0;
  const scoreClass = score >= 85 ? 'score-high' : score >= 70 ? 'score-mid' : 'score-low';
  const barColor = score >= 85 ? 'var(--success)' : score >= 70 ? 'var(--warning)' : 'var(--danger)';

  return (
    <div className={`dim-card ${expanded ? 'expanded' : ''}`}>
      <div className="dim-header">
        <span className="dim-title">{section.title || 'Unknown'}</span>
        <span className={`dim-score ${scoreClass}`}>{score}</span>
      </div>
      <div className="dim-bar">
        <div className="dim-bar-fill" style={{ width: `${score}%`, background: barColor }} />
      </div>
      <button className="dim-toggle" onClick={() => setExpanded(!expanded)}>
        {expanded ? 'Hide details ▴' : 'Show details ▾'}
      </button>
      {expanded && (
        <div className="dim-details">
          <PraiseList items={section.praise} />
          <IssueList items={section.issues} />
          <SuggestionList items={section.suggestions} />
        </div>
      )}
    </div>
  );
}

function PraiseList({ items }: { items?: PraiseItem[] }) {
  if (!items?.length) return null;
  return (
    <div className="detail-section">
      <h4>✅ Strengths</h4>
      {items.map((p, i) => (
        <div key={i} className="detail-item">
          {typeof p === 'object' ? p.praise : String(p)}
        </div>
      ))}
    </div>
  );
}

function IssueList({ items }: { items?: Issue[] }) {
  if (!items?.length) return null;
  return (
    <div className="detail-section">
      <h4>⚠️ Issues</h4>
      {items.map((issue, i) => {
        if (typeof issue === 'object') {
          const sevClass = issue.severity === 'critical' ? 'sev-critical' : issue.severity === 'major' ? 'sev-major' : 'sev-minor';
          return (
            <div key={i} className="detail-item">
              <span className={`severity-badge ${sevClass}`}>{issue.severity}</span>
              {issue.issue}
            </div>
          );
        }
        return <div key={i} className="detail-item">{String(issue)}</div>;
      })}
    </div>
  );
}

function SuggestionList({ items }: { items?: string[] }) {
  if (!items?.length) return null;
  return (
    <div className="detail-section">
      <h4>💡 Suggestions</h4>
      {items.map((s, i) => (
        <div key={i} className="detail-item">→ {s}</div>
      ))}
    </div>
  );
}
