import React, { useEffect, useState } from 'react';
import './App.css';

interface ContentGap {
  id: number;
  title: string;
  demand_score: number;
  sources: string[];
}

function App() {
  const [contentGaps, setContentGaps] = useState<ContentGap[]>([]);

  useEffect(() => {
    fetch('/api/content-gaps')
      .then(response => response.json())
      .then(data => setContentGaps(data))
      .catch(error => console.error('Error fetching content gaps:', error));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>The Observatory</h1>
        <p>Top 10 Most Profitable Content Gaps</p>
      </header>
      <div className="content-gaps-container">
        <ul className="content-gaps-list">
          {contentGaps.map(gap => (
            <li key={gap.id} className="content-gap-item">
              <h2>{gap.title}</h2>
              <p>Demand Score: {gap.demand_score}</p>
              <div className="sources">
                {gap.sources.map(source => (
                  <span key={source} className={`source-icon ${source}`}>{source}</span>
                ))}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;