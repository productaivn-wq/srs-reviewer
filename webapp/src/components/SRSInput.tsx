import { useRef, useCallback, type DragEvent } from 'react';
import './SRSInput.css';

interface Props {
  content: string;
  onChange: (v: string) => void;
}

export function SRSInput({ content, onChange }: Props) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = useCallback((file: File | undefined) => {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = e => {
      onChange(e.target?.result as string);
    };
    reader.readAsText(file);
  }, [onChange]);

  const handleDrop = useCallback((e: DragEvent) => {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
    handleFile(e.dataTransfer.files[0]);
  }, [handleFile]);

  return (
    <section className="glass srs-input-section" id="srsInputSection">
      <h2>📄 SRS Document</h2>

      <div
        className="drop-zone"
        id="dropZone"
        onClick={() => fileInputRef.current?.click()}
        onDragOver={e => { e.preventDefault(); e.currentTarget.classList.add('dragover'); }}
        onDragLeave={e => e.currentTarget.classList.remove('dragover')}
        onDrop={handleDrop}
      >
        <div className="drop-zone-icon">📁</div>
        <p>Drop your .md or .txt file here</p>
        <small>or click to browse</small>
      </div>
      <input
        ref={fileInputRef}
        type="file"
        className="file-input"
        accept=".md,.txt,.markdown"
        onChange={e => handleFile(e.target.files?.[0])}
      />

      <textarea
        className="srs-textarea"
        id="srsContent"
        placeholder={'Or paste your SRS content here in Markdown format...\n\n# 1. Introduction\n## 1.1 Purpose\n...'}
        value={content}
        onChange={e => onChange(e.target.value)}
      />
    </section>
  );
}
