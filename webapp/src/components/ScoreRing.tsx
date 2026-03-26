import { useEffect, useRef } from 'react';
import './ScoreRing.css';

interface Props {
  score: number;
  verdict: string;
}

export function ScoreRing({ score, verdict }: Props) {
  const circleRef = useRef<SVGCircleElement>(null);
  const numberRef = useRef<HTMLSpanElement>(null);

  const circumference = 2 * Math.PI * 78;

  useEffect(() => {
    // Animate the ring
    const offset = circumference - (score / 100) * circumference;
    if (circleRef.current) {
      // Reset first
      circleRef.current.style.strokeDashoffset = `${circumference}`;
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          if (circleRef.current) {
            circleRef.current.style.strokeDashoffset = `${offset}`;
          }
        });
      });
    }

    // Animate the number
    if (numberRef.current) {
      const el = numberRef.current;
      const start = performance.now();
      const duration = 1200;
      function update(now: number) {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = String(Math.round(score * eased));
        if (progress < 1) requestAnimationFrame(update);
      }
      requestAnimationFrame(update);
    }
  }, [score, circumference]);

  const strokeColor = score >= 85 ? 'var(--success)' : score >= 70 ? 'var(--warning)' : 'var(--danger)';
  const verdictClass = score >= 85 ? 'verdict-ready' : score >= 50 ? 'verdict-needs-revision' : 'verdict-weak';

  return (
    <div className="glass" style={{ textAlign: 'center' }}>
      <div className="score-ring-container">
        <div className="score-ring">
          <svg viewBox="0 0 180 180">
            <circle className="bg-circle" cx="90" cy="90" r="78" />
            <circle
              ref={circleRef}
              className="progress-circle"
              cx="90" cy="90" r="78"
              style={{
                stroke: strokeColor,
                strokeDasharray: circumference,
                strokeDashoffset: circumference,
              }}
            />
          </svg>
          <div className="score-value">
            <span ref={numberRef} className="score-number">0</span>
            <span className="score-label">/ 100</span>
          </div>
        </div>
        <div className={`verdict-badge ${verdictClass}`}>{verdict || '—'}</div>
      </div>
    </div>
  );
}
