import { useRef, useCallback, useState, type DragEvent } from 'react';
import * as pdfjsLib from 'pdfjs-dist';
import mammoth from 'mammoth';
import './DocumentInput.css';

// Configure PDF.js worker
pdfjsLib.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.mjs`;

interface Props {
  id: string;
  title: string;
  icon: string;
  content: string;
  onChange: (v: string) => void;
  placeholder: string;
  accept?: string;
  optional?: boolean;
  multiple?: boolean;
}

/** Extract text from a PDF file using pdf.js. */
async function extractPdfText(file: File): Promise<string> {
  const buffer = await file.arrayBuffer();
  const pdf = await pdfjsLib.getDocument({ data: buffer }).promise;
  const pages: string[] = [];

  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const content = await page.getTextContent();
    const text = content.items
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      .map((item: any) => (item.str as string) ?? '')
      .join(' ');
    pages.push(text);
  }

  return pages.join('\n\n');
}

/** Extract text from a DOCX file using mammoth. */
async function extractDocxText(file: File): Promise<string> {
  const buffer = await file.arrayBuffer();
  const result = await mammoth.extractRawText({ arrayBuffer: buffer });
  return result.value;
}

/** Determine file type and extract text accordingly. */
async function extractFileText(file: File): Promise<string> {
  const name = file.name.toLowerCase();

  if (name.endsWith('.pdf')) {
    return extractPdfText(file);
  }

  if (name.endsWith('.docx')) {
    return extractDocxText(file);
  }

  if (name.endsWith('.doc')) {
    throw new Error('Legacy .doc format is not supported. Please convert to .docx or .pdf first.');
  }

  // Plain text / markdown
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = e => resolve(e.target?.result as string);
    reader.onerror = () => reject(new Error('Failed to read file'));
    reader.readAsText(file);
  });
}

const ACCEPTED = '.md,.txt,.markdown,.pdf,.docx,.doc';

export function DocumentInput({
  id, title, icon, content, onChange,
  placeholder, accept = ACCEPTED, optional, multiple,
}: Props) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [parsing, setParsing] = useState(false);
  const [parseError, setParseError] = useState('');
  const [fileCount, setFileCount] = useState(0);

  const handleFiles = useCallback(async (files: FileList | null) => {
    if (!files || files.length === 0) return;
    setParsing(true);
    setParseError('');

    try {
      const parts: string[] = [];
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const text = await extractFileText(file);
        if (files.length > 1) {
          parts.push(`--- ${file.name} ---\n${text}`);
        } else {
          parts.push(text);
        }
      }
      setFileCount(files.length);
      onChange(parts.join('\n\n'));
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      setParseError(msg);
      console.error('File parse error:', err);
    } finally {
      setParsing(false);
    }
  }, [onChange]);

  const handleDrop = useCallback((e: DragEvent) => {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
  }, [handleFiles]);

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
        <p>{parsing ? '⏳ Reading file...' : `Drop your file${multiple ? '(s)' : ''} here (.md, .txt, .pdf, .docx)`}</p>
        <small>or click to browse</small>
      </div>
      <input
        ref={fileInputRef}
        type="file"
        className="file-input"
        accept={accept}
        multiple={multiple}
        onChange={e => handleFiles(e.target.files)}
      />

      {parseError && (
        <div className="parse-error">❌ {parseError}</div>
      )}

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
          {fileCount > 1 && <span className="file-count-badge">{fileCount} files</span>}
          <button className="clear-btn" onClick={() => { onChange(''); setFileCount(0); }}>✕ Clear</button>
        </div>
      )}
    </div>
  );
}
