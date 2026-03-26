import type { HistoryEntry, ReviewResult } from '../types/review';
import './ReviewHistory.css';

interface Props {
  history: HistoryEntry[];
  onLoad: (result: ReviewResult) => void;
}

export function ReviewHistory({ history, onLoad }: Props) {
  return (
    <section className="history-section" id="historySection">
      <h3>🕐 Review History</h3>
      <div className="history-list" id="historyList">
        {history.length === 0 ? (
          <div className="no-history">No reviews yet. Run your first review above!</div>
        ) : (
          history.map((h, i) => {
            const score = h.totalScore ?? 0;
            const scoreClass = score >= 85 ? 'score-high' : score >= 70 ? 'score-mid' : 'score-low';
            const date = new Date(h.timestamp).toLocaleDateString('vi-VN', {
              day: '2-digit', month: '2-digit', year: 'numeric',
              hour: '2-digit', minute: '2-digit',
            });
            return (
              <div key={i} className="history-item" onClick={() => onLoad(h.result)}>
                <span className="history-name">{h.filename || 'SRS Review'}</span>
                <div className="history-meta">
                  <span className="history-mode">{h.mode}</span>
                  <span className={`history-score ${scoreClass}`}>{score}/100</span>
                  <span className="history-date">{date}</span>
                </div>
              </div>
            );
          })
        )}
      </div>
    </section>
  );
}
