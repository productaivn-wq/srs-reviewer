import { useEffect, useRef } from 'react';
import type { Section } from '../types/review';
import './RadarChart.css';

interface Props {
  sections: Section[];
}

export function RadarChart({ sections }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    canvas.width = 500 * dpr;
    canvas.height = 500 * dpr;
    canvas.style.width = '500px';
    canvas.style.height = '500px';
    ctx.scale(dpr, dpr);

    const cx = 250, cy = 250, maxR = 180;
    const n = sections.length || 10;
    const angleStep = (Math.PI * 2) / n;

    ctx.clearRect(0, 0, 500, 500);

    // Grid circles
    for (let i = 1; i <= 5; i++) {
      const r = (maxR / 5) * i;
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(255,255,255,0.06)';
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    // Grid lines
    for (let i = 0; i < n; i++) {
      const angle = angleStep * i - Math.PI / 2;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx + Math.cos(angle) * maxR, cy + Math.sin(angle) * maxR);
      ctx.strokeStyle = 'rgba(255,255,255,0.06)';
      ctx.stroke();
    }

    // Data polygon
    const scores = sections.map(s => s.score || 0);
    ctx.beginPath();
    for (let i = 0; i < n; i++) {
      const angle = angleStep * i - Math.PI / 2;
      const r = (scores[i] / 100) * maxR;
      const x = cx + Math.cos(angle) * r;
      const y = cy + Math.sin(angle) * r;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.fillStyle = 'rgba(99, 102, 241, 0.15)';
    ctx.fill();
    ctx.strokeStyle = 'rgba(99, 102, 241, 0.7)';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Data points + labels
    for (let i = 0; i < n; i++) {
      const angle = angleStep * i - Math.PI / 2;
      const r = (scores[i] / 100) * maxR;
      const x = cx + Math.cos(angle) * r;
      const y = cy + Math.sin(angle) * r;

      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fillStyle = '#6366f1';
      ctx.fill();

      // Label
      const labelR = maxR + 24;
      const lx = cx + Math.cos(angle) * labelR;
      const ly = cy + Math.sin(angle) * labelR;
      ctx.fillStyle = '#94a3b8';
      ctx.font = '11px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(`D${i + 1}`, lx, ly);

      // Score value
      const scoreR = maxR + 38;
      const sx = cx + Math.cos(angle) * scoreR;
      const sy = cy + Math.sin(angle) * scoreR;
      ctx.fillStyle = scores[i] >= 85 ? '#10b981' : scores[i] >= 70 ? '#f59e0b' : '#ef4444';
      ctx.font = 'bold 12px Inter, sans-serif';
      ctx.fillText(String(scores[i]), sx, sy);
    }
  }, [sections]);

  return (
    <div className="chart-container">
      <canvas ref={canvasRef} width={500} height={500} />
    </div>
  );
}
