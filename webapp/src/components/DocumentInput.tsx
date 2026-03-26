import { useRef, useCallback, type DragEvent } from 'react';
import './DocumentInput.css';

interface Props {
  id: string;
  title: string;
  icon: string;
  content: string;
  onChange: (v: string) => void;
  placeholder: string;
  accept?: string;
  optional?: boolean;
}

export function DocumentInput({
  id, title, icon, content, onChange, placeholder, accept = '.md,.txt,.markdown', optional,
}: Props) {
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
    <div className="doc-input-panel" id={`${id}Section`}>
      <h3>
        {icon} {title}
        {optional && <span className="optional-badge">Optional</span>}
      </h3>

      <div
        className="drop-zone"
        id={`${id}DropZone`}
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
        accept={accept}
        onChange={e => handleFile(e.target.files?.[0])}
      />

      <textarea
        className="doc-textarea"
        id={id}
        placeholder={placeholder}
        value={content}
        onChange={e => onChange(e.target.value)}
      />

      {content.length > 0 && (
        <div className="doc-status">
          <span className="doc-status-dot" />
          {Math.round(content.length / 1000)}k chars loaded
          <button className="clear-btn" onClick={() => onChange('')}>✕ Clear</button>
        </div>
      )}
    </div>
  );
}
