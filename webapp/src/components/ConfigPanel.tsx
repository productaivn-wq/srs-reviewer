import { MODEL_OPTIONS } from '../utils/constants';
import './ConfigPanel.css';

interface Props {
  apiKey: string;
  mode: string;
  model: string;
  reviewer: string;
  onApiKeyChange: (v: string) => void;
  onModeChange: (v: string) => void;
  onModelChange: (v: string) => void;
  onReviewerChange: (v: string) => void;
}

export function ConfigPanel({
  apiKey, mode, model, reviewer,
  onApiKeyChange, onModeChange, onModelChange, onReviewerChange,
}: Props) {
  return (
    <section className="glass section-spacing" id="configPanel">
      <div className="config-grid">
        <div className="form-group">
          <label htmlFor="apiKey">🔑 OpenRouter API Key</label>
          <input
            type="password"
            id="apiKey"
            placeholder="sk-or-v1-..."
            autoComplete="off"
            value={apiKey}
            onChange={e => onApiKeyChange(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label htmlFor="reviewMode">📋 Review Mode</label>
          <select
            id="reviewMode"
            value={mode}
            onChange={e => onModeChange(e.target.value)}
          >
            <option value="standard">Standard — Quick quality check</option>
            <option value="strategic">Strategic — Deep architectural scrutiny</option>
          </select>
        </div>
        <div className="form-group">
          <label htmlFor="modelSelect">🤖 Model</label>
          <select
            id="modelSelect"
            value={model}
            onChange={e => onModelChange(e.target.value)}
          >
            {MODEL_OPTIONS.map(opt => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label htmlFor="reviewerName">👤 Reviewer Name</label>
          <input
            type="text"
            id="reviewerName"
            placeholder="SRS Review AI"
            value={reviewer}
            onChange={e => onReviewerChange(e.target.value)}
          />
        </div>
      </div>
    </section>
  );
}
