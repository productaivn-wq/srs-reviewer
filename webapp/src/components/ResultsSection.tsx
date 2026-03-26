import { useCallback } from 'react';
import type { ReviewResult } from '../types/review';
import { ScoreRing } from './ScoreRing';
import { RadarChart } from './RadarChart';
import { DimensionCard } from './DimensionCard';
import './ResultsSection.css';

interface Props {
  result: ReviewResult;
  reviewer: string;
  mode: string;
}

export function ResultsSection({ result, reviewer, mode }: Props) {
  const sections = result.sections ?? [];

  const handleDownload = useCallback(() => {
    const now = new Date().toISOString().slice(0, 16).replace('T', ' ');
    const modeLabel = mode === 'strategic' ? 'Strategic' : 'Standard';

    let md = `# SRS Review Report\n\n`;
    md += `**Reviewer**: ${reviewer}  \n`;
    md += `**Date**: ${now}  \n`;
    md += `**Mode**: ${modeLabel}  \n`;
    md += `**Total Score**: ${result.totalScore}/100  \n`;
    md += `**Verdict**: ${result.verdict}\n\n---\n\n`;

    for (const s of sections) {
      const emoji = s.score >= 85 ? '✅' : s.score >= 70 ? '⚠️' : '❌';
      md += `## ${s.title} — ${s.score}/100 ${emoji}\n\n`;

      if (s.praise?.length) {
        md += '**Strengths:**\n';
        for (const p of s.praise) md += `- ✅ ${typeof p === 'object' ? p.praise : p}\n`;
        md += '\n';
      }

      if (s.issues?.length) {
        md += '**Issues:**\n';
        for (const i of s.issues) {
          if (typeof i === 'object') md += `- [${i.severity}] ${i.issue}\n`;
          else md += `- ${i}\n`;
        }
        md += '\n';
      }

      if (s.suggestions?.length) {
        md += '**Suggestions:**\n';
        for (const sg of s.suggestions) md += `- 💡 ${sg}\n`;
        md += '\n';
      }
    }

    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `srs-review-${new Date().toISOString().slice(0, 10)}.md`;
    a.click();
    URL.revokeObjectURL(url);
  }, [result, reviewer, mode, sections]);

  return (
    <section className="results-section" id="resultsSection">
      <div className="results-header">
        <h2>📊 Review Results</h2>
        <button className="dim-toggle download-btn" onClick={handleDownload}>
          ⬇️ Download Report
        </button>
      </div>

      <ScoreRing score={result.totalScore} verdict={result.verdict} />
      <RadarChart sections={sections} />

      <div className="dimensions-grid" id="dimensionsGrid">
        {sections.map((section, i) => (
          <DimensionCard key={i} section={section} />
        ))}
      </div>
    </section>
  );
}
