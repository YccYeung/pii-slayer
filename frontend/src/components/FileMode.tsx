import React, { useState, useRef } from 'react';
import axios from 'axios';
import { FileDetectionResponse } from '../types';
import RiskBadge from './RiskBadge';
import EntityList from './EntityList';

const API = 'http://localhost:8000/api/v1';

const FileMode: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<FileDetectionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = (f: File) => {
    const ext = f.name.split('.').pop()?.toLowerCase();
    if (!['pdf', 'csv'].includes(ext || '')) {
      setError('Only PDF and CSV files are supported.');
      return;
    }
    setFile(f);
    setError(null);
    setResult(null);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const f = e.dataTransfer.files[0];
    if (f) handleFile(f);
  };

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    const ext = file.name.split('.').pop()?.toLowerCase();
    const endpoint = ext === 'pdf' ? 'detect/pdf' : 'detect/csv';
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post(`${API}/${endpoint}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(res.data);
    } catch (e) {
      setError('Processing failed. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!result) return;
    const ext = result.filename.split('.').pop()?.toLowerCase();
    const mimeType = ext === 'pdf' ? 'application/pdf' : 'text/csv';
    const bytes = atob(result.redacted_file);
    const arr = new Uint8Array(bytes.length);
    for (let i = 0; i < bytes.length; i++) arr[i] = bytes.charCodeAt(i);
    const blob = new Blob([arr], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = result.filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="file-mode">
      <div
        className={`drop-zone ${dragging ? 'dragging' : ''} ${file ? 'has-file' : ''}`}
        onDragOver={e => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.csv"
          style={{ display: 'none' }}
          onChange={e => e.target.files?.[0] && handleFile(e.target.files[0])}
        />
        {file ? (
          <div className="file-info">
            <span className="file-icon">{file.name.endsWith('.pdf') ? '⬛' : '⬜'}</span>
            <span className="file-name">{file.name}</span>
            <span className="file-size">{(file.size / 1024).toFixed(1)} KB</span>
          </div>
        ) : (
          <div className="drop-prompt">
            <span className="drop-icon">📄</span>
            <p>DROP PDF OR CSV HERE</p>
            <p className="drop-sub">or click to browse</p>
          </div>
        )}
      </div>

      {error && <p className="error">{error}</p>}

      {file && (
        <button
          className="submit-btn"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? (
            <><span className="spinner" /> PROCESSING...</>
          ) : (
            '▶ DETECT & REDACT'
          )}
        </button>
      )}

      {result && (
        <div className="results-section">
          <div className="stats-row">
            <div className="stat">
              <span className="stat-value">{result.entity_count}</span>
              <span className="stat-label">ENTITIES FOUND</span>
            </div>
          </div>

          {result.risk_score && (
            <RiskBadge score={result.risk_score} recommendation={result.recommendation} />
          )}

          <button className="download-btn" onClick={handleDownload}>
            ↓ DOWNLOAD REDACTED FILE
          </button>

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

export default FileMode;
