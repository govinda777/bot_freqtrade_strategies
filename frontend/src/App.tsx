import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import { Web3Provider } from '@/contexts/Web3Context';
import { AuthProvider } from '@/contexts/AuthContext';

// Layout components
import MainLayout from '@/layouts/MainLayout';

// Pages
import LoginPage from '@/pages/LoginPage';
import DashboardPage from '@/pages/DashboardPage';
import StrategySelectionPage from '@/pages/StrategySelectionPage';
import StrategyFormPage from '@/pages/StrategyFormPage';
import BacktestPage from '@/pages/BacktestPage';
import BacktestResultsPage from '@/pages/BacktestResultsPage';
import TermsAndConditionsPage from '@/pages/TermsAndConditionsPage';
import InvestmentPage from '@/pages/InvestmentPage';
import InvestmentResultsPage from '@/pages/InvestmentResultsPage';
import WithdrawPage from '@/pages/WithdrawPage';
import BalancePage from '@/pages/BalancePage';
import HistoryPage from '@/pages/HistoryPage';
import CreateStrategyPage from '@/pages/CreateStrategyPage';
import ConfigureBacktestPage from '@/pages/ConfigureBacktestPage';
import PublishStrategyPage from '@/pages/PublishStrategyPage';
import PromoteStrategyPage from '@/pages/PromoteStrategyPage';

// Theme
import theme from '@/theme';

// Private route component
const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <Web3Provider>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            
            {/* Client routes */}
            <Route path="/" element={
              <PrivateRoute>
                <MainLayout userType="client" />
              </PrivateRoute>
            }>
              <Route index element={<DashboardPage />} />
              <Route path="strategies" element={<StrategySelectionPage />} />
              <Route path="strategy-form/:id" element={<StrategyFormPage />} />
              <Route path="exposure-level" element={<StrategyFormPage exposureStep={true} />} />
              <Route path="send-credits" element={<StrategyFormPage creditsStep={true} />} />
              <Route path="buy-credits" element={<StrategyFormPage buyCreditsStep={true} />} />
              <Route path="backtest" element={<BacktestPage />} />
              <Route path="backtest-results" element={<BacktestResultsPage />} />
              <Route path="terms" element={<TermsAndConditionsPage userType="client" />} />
              <Route path="investment" element={<InvestmentPage />} />
              <Route path="investment-results" element={<InvestmentResultsPage />} />
              <Route path="withdraw" element={<WithdrawPage />} />
              <Route path="balance" element={<BalancePage />} />
              <Route path="history" element={<HistoryPage />} />
            </Route>
            
            {/* Developer routes */}
            <Route path="/developer" element={
              <PrivateRoute>
                <MainLayout userType="developer" />
              </PrivateRoute>
            }>
              <Route index element={<DashboardPage isDeveloper={true} />} />
              <Route path="create-strategy" element={<CreateStrategyPage />} />
              <Route path="configure-backtest" element={<ConfigureBacktestPage />} />
              <Route path="backtest-results" element={<BacktestResultsPage isDeveloper={true} />} />
              <Route path="buy-credits" element={<StrategyFormPage buyCreditsStep={true} />} />
              <Route path="send-credits" element={<StrategyFormPage creditsStep={true} />} />
              <Route path="backtest" element={<BacktestPage isDeveloper={true} />} />
              <Route path="performance" element={<BacktestResultsPage performanceView={true} />} />
              <Route path="terms" element={<TermsAndConditionsPage userType="developer" />} />
              <Route path="publish-strategy" element={<PublishStrategyPage />} />
              <Route path="balance" element={<BalancePage isDeveloper={true} />} />
              <Route path="history" element={<HistoryPage isDeveloper={true} />} />
              <Route path="promote-strategy" element={<PromoteStrategyPage />} />
            </Route>
            
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </Web3Provider>
    </ThemeProvider>
  );
};

export default App;