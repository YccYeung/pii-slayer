import React, { useState } from 'react';
import './App.css';
import TextMode from './components/TextMode';
import FileMode from './components/FileMode';
import pii_slayer_logo from './pii_slayer_logo.svg'

type Mode = 'text' | 'file';

function App() {
  const [mode, setMode] = useState<Mode>('text');

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
        <img src={pii_slayer_logo} alt="PII Slayer" height="55" />
        </div>
      </header>

      <main className="main">
        <div className="mode-toggle">
          <button className={`mode-btn ${mode === 'text' ? 'active' : ''}`} onClick={() => setMode('text')}>
            Text
          </button>
          <button className={`mode-btn ${mode === 'file' ? 'active' : ''}`} onClick={() => setMode('file')}>
            File
          </button>
        </div>
        <div className="content">
          {mode === 'text' ? <TextMode /> : <FileMode />}
        </div>
      </main>

      <footer className="footer">
        <span>PII Slayer v1.0</span>
      </footer>
    </div>
  );
}

export default App;
