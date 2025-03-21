import React from 'react';

interface BacktestResultsPageProps {
  isDeveloper?: boolean;
  performanceView?: boolean;
}

const BacktestResultsPage: React.FC<BacktestResultsPageProps> = ({ 
  isDeveloper = false,
  performanceView = false
}) => {
  let pageTitle = 'Backtest Results';
  
  if (isDeveloper && performanceView) {
    pageTitle = 'Developer Performance View';
  } else if (isDeveloper) {
    pageTitle = 'Developer Backtest Results';
  }

  return (
    <div>
      <h1>{pageTitle}</h1>
      <p>This is a placeholder component for the Backtest Results Page</p>
      {performanceView && (
        <div>
          <h2>Performance Metrics</h2>
          <p>This section would display detailed performance metrics</p>
        </div>
      )}
    </div>
  );
};

export default BacktestResultsPage;