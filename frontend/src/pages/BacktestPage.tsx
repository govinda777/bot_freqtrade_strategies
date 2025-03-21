import React from 'react';

interface BacktestPageProps {
  isDeveloper?: boolean;
}

const BacktestPage: React.FC<BacktestPageProps> = ({ isDeveloper = false }) => {
  return (
    <div>
      <h1>Backtest Page</h1>
      <h2>{isDeveloper ? 'Developer Backtest Interface' : 'Client Backtest Interface'}</h2>
      <p>This is a placeholder component for the Backtest Page</p>
    </div>
  );
};

export default BacktestPage;