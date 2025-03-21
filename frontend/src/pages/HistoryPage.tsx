import React from 'react';

interface HistoryPageProps {
  isDeveloper?: boolean;
}

const HistoryPage: React.FC<HistoryPageProps> = ({ isDeveloper = false }) => {
  return (
    <div>
      <h1>History Page</h1>
      <h2>{isDeveloper ? 'Developer Transaction History' : 'Client Transaction History'}</h2>
      <p>This is a placeholder component for the History Page</p>
      
      <div>
        <h3>Transactions</h3>
        <p>This section would display the transaction history.</p>
        
        {isDeveloper && (
          <div>
            <h3>Developer Earnings History</h3>
            <p>This section would show history of developer earnings and strategy usage.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default HistoryPage;