import React from 'react';
import { PIIEntity } from '../types';

interface Props {
  entities: PIIEntity[];
}

const layerColors: Record<string, string> = {
  REGEX: '#00b4d8',
  NER: '#7b2fff',
  LLM: '#ff6b35',
};

const EntityList: React.FC<Props> = ({ entities }) => {
  if (entities.length === 0) {
    return <p className="no-entities">No PII detected.</p>;
  }

  return (
    <div className="entity-list">
      {entities.map((e, i) => (
        <div key={i} className="entity-item">
          <span className="entity-type">{e.pii_type}</span>
          <span className="entity-text">"{e.text}"</span>
          <span className="entity-layer" style={{ color: layerColors[e.layer] || '#aaa' }}>
            {e.layer}
          </span>
          <span className="entity-confidence">{Math.round(e.confidence * 100)}%</span>
        </div>
      ))}
    </div>
  );
};

export default EntityList;
