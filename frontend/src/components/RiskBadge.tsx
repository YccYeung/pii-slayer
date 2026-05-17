import React from 'react';
import { RiskScore } from '../types';

interface Props {
  score: RiskScore;
  recommendation: string | null;
}

const riskConfig = {
  LOW: { label: 'LOW RISK', color: '#00ff88', bg: 'rgba(0,255,136,0.08)' },
  MEDIUM: { label: 'MEDIUM RISK', color: '#ffb800', bg: 'rgba(255,184,0,0.08)' },
  HIGH: { label: 'HIGH RISK', color: '#ff4444', bg: 'rgba(255,68,68,0.08)' },
  CRITICAL: { label: 'CRITICAL', color: '#ff0000', bg: 'rgba(255,0,0,0.12)' },
};

const RiskBadge: React.FC<Props> = ({ score, recommendation }) => {
  const config = riskConfig[score] || riskConfig.LOW;
  return (
    <div className="risk-badge" style={{ borderColor: config.color, background: config.bg }}>
      <div className="risk-header">
        <span className="risk-dot" style={{ background: config.color }} />
        <span className="risk-label" style={{ color: config.color }}>{config.label}</span>
      </div>
      {recommendation && <p className="risk-recommendation">{recommendation}</p>}
    </div>
  );
};

export default RiskBadge;
