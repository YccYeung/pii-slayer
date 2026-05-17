import React, { useState } from 'react';
import axios from 'axios';
import { DetectionResponse, RedactionMode } from '../types';
import RiskBadge from './RiskBadge';
import EntityList from './EntityList';

const API = 'http://localhost:8000/api/v1';

const TextMode: React.FC = () => {
  const [text, setText] = useState('');
  const [mode, setMode] = useState<RedactionMode>('REDACT');
  const [result, setResult] = useState<DetectionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const handleSubmit = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await axios.post(`${API}/detect/text`, { text, mode });
      setResult(res.data);
    } catch (e) {
      setError('Detection failed. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (result?.redacted_text) {
      navigator.clipboard.writeText(result.redacted_text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="text-mode">
      <div className="input-section">
        <div className="section-header">
          <span className="section-label">INPUT</span>
          <div className="mode-select">
            <button
              className={`small-btn ${mode === 'REDACT' ? 'active' : ''}`}
              onClick={() => setMode('REDACT')}
            >REDACT</button>
            <button
              className={`small-btn ${mode === 'ANONYMISE' ? 'active' : ''}`}
              onClick={() => setMode('ANONYMISE')}
            >ANONYMISE</button>
          </div>
        </div>
        <textarea
          className="text-input"
          value={text}
          onChange={e => setText(e.target.value)}
          placeholder="Paste text here to detect and redact PII..."
          rows={8}
        />
        <button
          className="submit-btn"
          onClick={handleSubmit}
          disabled={loading || !text.trim()}
        >
          {loading ? (
            <><span className="spinner" /> PROCESSING...</>
          ) : (
            '▶ DETECT & REDACT'
          )}
        </button>
        {error && <p className="error">{error}</p>}
      </div>

      {result && (
        <div className="results-section">
          <div className="stats-row">
            <div className="stat">
              <span className="stat-value">{result.entity_count}</span>
              <span className="stat-label">ENTITIES FOUND</span>
            </div>
            <div className="stat">
              <span className="stat-value" style={{ color: '#7b2fff' }}>
                {result.entities.filter(e => e.layer === 'NER').length}
              </span>
              <span className="stat-label">NER</span>
            </div>
            <div className="stat">
              <span className="stat-value" style={{ color: '#00b4d8' }}>
                {result.entities.filter(e => e.layer === 'REGEX').length}
              </span>
              <span className="stat-label">REGEX</span>
            </div>
            <div className="stat">
              <span className="stat-value" style={{ color: '#ff6b35' }}>
                {result.entities.filter(e => e.layer === 'LLM').length}
              </span>
              <span className="stat-label">LLM</span>
            </div>
          </div>

          {result.risk_score && (
            <RiskBadge score={result.risk_score} recommendation={result.recommendation} />
          )}

          <div className="output-section">
            <div className="section-header">
              <span className="section-label">REDACTED OUTPUT</span>
              <button className="copy-btn" onClick={handleCopy}>
                {copied ? '✓ COPIED' : 'COPY'}
              </button>
            </div>
            <div className="text-output">{result.redacted_text}</div>
          </div>

          <div className="entities-section">
            <div className="section-header">
              <span className="section-label">DETECTED ENTITIES</span>
            </div>
            <EntityList entities={result.entities} />
          </div>
        </div>
      )}
    </div>
  );
};

export default TextMode;
