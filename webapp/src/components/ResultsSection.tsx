import { useCallback } from 'react';
import type { ReviewResult, AlignmentResult } from '../types/review';
import { ScoreRing } from './ScoreRing';
import { RadarChart } from './RadarChart';
import { DimensionCard } from './DimensionCard';
import './ResultsSection.css';

interface Props {
  result: ReviewResult;
  reviewer: string;
  mode: string;
}

function AlignmentCard({ alignment }: { alignment: AlignmentResult }) {
  return (
    <div className="glass alignment-card" id="alignmentCard">
      <h3>🔗 PRD Alignment Analysis</h3>
      <p className="alignment-summary">{alignment.summary}</p>

      {alignment.missingFromPRD?.length > 0 && (
        <div className="alignment-group">
          <h4>🚨 Missing from SRS <span className="align-count">{alignment.missingFromPRD.length}</span></h4>
          <ul>
            {alignment.missingFromPRD.map((item, i) => (
              <li key={i} className={`severity-${item.severity}`}>
                <strong>{item.prdItem}</strong>
                {item.evidence && <span className="align-evidence">"{item.evidence}"</span>}
              </li>
            ))}
          </ul>
        </div>
      )}

      {alignment.scopeCreep?.length > 0 && (
        <div className="alignment-group">
          <h4>📐 Scope Creep <span className="align-count">{alignment.scopeCreep.length}</span></h4>
          <ul>
            {alignment.scopeCreep.map((item, i) => (
              <li key={i} className={`severity-${item.severity}`}>
                <strong>{item.srsItem}</strong>
                {item.evidence && <span className="align-evidence">"{item.evidence}"</span>}
              </li>
            ))}
          </ul>
        </div>
      )}

      {alignment.intentMismatch?.length > 0 && (
        <div className="alignment-group">
          <h4>⚡ Intent Mismatches <span className="align-count">{alignment.intentMismatch.length}</span></h4>
          <ul>
            {alignment.intentMismatch.map((item, i) => (
              <li key={i} className={`severity-${item.severity}`}>
                <div><strong>PRD:</strong> {item.prdIntent}</div>
                <div><strong>SRS:</strong> {item.srsInterpretation}</div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {alignment.signOffGaps?.length > 0 && (
        <div className="alignment-group">
          <h4>📝 Sign-Off Gaps <span className="align-count">{alignment.signOffGaps.length}</span></h4>
          <ul>
            {alignment.signOffGaps.map((gap, i) => (
              <li key={i}>{gap}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export function ResultsSection({ result, reviewer, mode }: Props) {
  const sections = result.sections ?? [];

  const handleDownload = useCallback(() => {
    const now = new Date().toISOString().slice(0, 16).replace('T', ' ');
    const modeLabel = mode === 'strategic' ? 'Strategic' : mode === 'alignment' ? 'Alignment' : 'Standard';

    let md = `# SRS Review Report\n\n`;
    md += `**Reviewer**: ${reviewer}  \n`;
    md += `**Date**: ${now}  \n`;
    md += `**Mode**: ${modeLabel}  \n`;
    md += `**Total Score**: ${result.totalScore}/100  \n`;
    md += `**Verdict**: ${result.verdict}\n\n---\n\n`;

    // Alignment section
    if (result.alignment) {
      md += `## 🔗 PRD Alignment Analysis\n\n`;
      md += `${result.alignment.summary}\n\n`;

      if (result.alignment.missingFromPRD?.length) {
        md += `### 🚨 Missing from SRS\n`;
        for (const item of result.alignment.missingFromPRD) {
          md += `- [${item.severity}] ${item.prdItem}\n`;
        }
        md += '\n';
      }
      if (result.alignment.scopeCreep?.length) {
        md += `### 📐 Scope Creep\n`;
        for (const item of result.alignment.scopeCreep) {
          md += `- [${item.severity}] ${item.srsItem}\n`;
        }
        md += '\n';
      }
      if (result.alignment.intentMismatch?.length) {
        md += `### ⚡ Intent Mismatches\n`;
        for (const item of result.alignment.intentMismatch) {
          md += `- [${item.severity}] PRD: ${item.prdIntent} → SRS: ${item.srsInterpretation}\n`;
        }
        md += '\n';
      }
      if (result.alignment.signOffGaps?.length) {
        md += `### 📝 Sign-Off Gaps\n`;
        for (const gap of result.alignment.signOffGaps) {
          md += `- ${gap}\n`;
        }
        md += '\n';
      }
      md += '---\n\n';
    }

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

      {result.alignment && <AlignmentCard alignment={result.alignment} />}

      <div className="dimensions-grid" id="dimensionsGrid">
        {sections.map((section, i) => (
          <DimensionCard key={i} section={section} />
        ))}
      </div>
    </section>
  );
}
