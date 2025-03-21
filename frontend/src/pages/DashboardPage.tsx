import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { useAuth } from '../contexts/AuthContext';
import { useWeb3 } from '../contexts/Web3Context';

interface DashboardPageProps {
  isDeveloper?: boolean;
}

const DashboardPage: React.FC<DashboardPageProps> = ({ isDeveloper = false }) => {
  const { userType, userCredits } = useAuth();
  const { account } = useWeb3();
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    activeStrategies: 0,
    totalInvestment: 0,
    totalProfit: 0,
    backtestsRun: 0,
    publishedStrategies: 0
  });

  // Simulate fetching dashboard data
  useEffect(() => {
    // This would normally be an API call to fetch user data
    const fetchDashboardData = async () => {
      // Mock data for demonstration
      if (isDeveloper) {
        setStats({
          activeStrategies: 3,
          totalInvestment: 2500,
          totalProfit: 350,
          backtestsRun: 27,
          publishedStrategies: 2
        });
      } else {
        setStats({
          activeStrategies: 2,
          totalInvestment: 5000,
          totalProfit: 750,
          backtestsRun: 12,
          publishedStrategies: 0
        });
      }
    };

    fetchDashboardData();
  }, [isDeveloper]);

  // Helper function for quick actions based on user type
  const getQuickActions = () => {
    if (isDeveloper) {
      return [
        { 
          title: 'Create Strategy', 
          description: 'Develop a new trading strategy', 
          action: () => navigate('/developer/create-strategy'),
          color: 'primary'
        },
        { 
          title: 'Run Backtest', 
          description: 'Test your strategies with historical data', 
          action: () => navigate('/developer/configure-backtest'),
          color: 'info'
        },
        { 
          title: 'Publish Strategy', 
          description: 'Share your strategy with clients', 
          action: () => navigate('/developer/publish-strategy'),
          color: 'success'
        },
        { 
          title: 'Promote Strategy', 
          description: 'Increase your strategy visibility', 
          action: () => navigate('/developer/promote-strategy'),
          color: 'secondary'
        }
      ];
    } else {
      return [
        { 
          title: 'Select Strategy', 
          description: 'Choose a trading strategy to invest in', 
          action: () => navigate('/strategies'),
          color: 'primary'
        },
        { 
          title: 'Buy Credits', 
          description: 'Purchase credits for trading and backtesting', 
          action: () => navigate('/buy-credits'),
          color: 'info'
        },
        { 
          title: 'View Results', 
          description: 'Check your investment performance', 
          action: () => navigate('/investment-results'),
          color: 'success'
        },
        { 
          title: 'Withdraw Profit', 
          description: 'Withdraw your earnings', 
          action: () => navigate('/withdraw'),
          color: 'secondary'
        }
      ];
    }
  };

  return (
    <DashboardContainer>
      <WelcomeSection>
        <h1>Welcome to FreqTrade</h1>
        <p>
          {isDeveloper 
            ? 'Your developer dashboard is ready. Create, test, and promote your trading strategies.' 
            : 'Your trading dashboard is ready. Select strategies and monitor your investments.'}
        </p>
      </WelcomeSection>

      <StatsSection>
        <StatCard>
          <StatTitle>Credits</StatTitle>
          <StatValue data-testid="user-credits">{userCredits}</StatValue>
          <StatDescription>Available for trading & backtesting</StatDescription>
        </StatCard>

        <StatCard>
          <StatTitle>Active {isDeveloper ? 'Published' : 'Selected'} Strategies</StatTitle>
          <StatValue>{stats.activeStrategies}</StatValue>
          <StatDescription>{isDeveloper ? 'Strategies available for clients' : 'Strategies you are using'}</StatDescription>
        </StatCard>

        <StatCard>
          <StatTitle>Total {isDeveloper ? 'Revenue' : 'Investment'}</StatTitle>
          <StatValue>${stats.totalInvestment.toLocaleString()}</StatValue>
          <StatDescription>{isDeveloper ? 'From strategy sales' : 'Current funds deployed'}</StatDescription>
        </StatCard>

        <StatCard>
          <StatTitle>Total Profit</StatTitle>
          <StatValue>${stats.totalProfit.toLocaleString()}</StatValue>
          <StatDescription>Your {isDeveloper ? 'commission' : 'investment'} earnings</StatDescription>
        </StatCard>
      </StatsSection>

      <ActionsSection>
        <SectionTitle>Quick Actions</SectionTitle>
        <ActionsGrid>
          {getQuickActions().map((action, index) => (
            <ActionCard key={index} onClick={action.action} color={action.color as 'primary' | 'secondary' | 'success' | 'info' | 'warning' | 'error'}>
              <ActionTitle>{action.title}</ActionTitle>
              <ActionDescription>{action.description}</ActionDescription>
            </ActionCard>
          ))}
        </ActionsGrid>
      </ActionsSection>

      {isDeveloper && (
        <BacktestSection>
          <SectionTitle>Recent Backtests</SectionTitle>
          <p>You have run {stats.backtestsRun} backtests recently.</p>
          <BacktestButton onClick={() => navigate('/developer/backtest-results')}>
            View Backtest Results
          </BacktestButton>
        </BacktestSection>
      )}

      {!isDeveloper && (
        <PerformanceSection>
          <SectionTitle>Investment Performance</SectionTitle>
          <p>Monitor your active investments and their performance over time.</p>
          <PerformanceButton onClick={() => navigate('/investment-results')}>
            View Detailed Performance
          </PerformanceButton>
        </PerformanceSection>
      )}
    </DashboardContainer>
  );
};

// Styled components
const DashboardContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const WelcomeSection = styled.div`
  margin-bottom: 1rem;
  
  h1 {
    color: ${props => props.theme.colors.text.primary};
    margin-bottom: 0.5rem;
  }
  
  p {
    color: ${props => props.theme.colors.text.secondary};
    font-size: 1.1rem;
  }
`;

const StatsSection = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
`;

const StatCard = styled.div`
  background-color: ${props => props.theme.colors.background.paper};
  padding: 1.5rem;
  border-radius: ${props => props.theme.borderRadius.medium};
  box-shadow: ${props => props.theme.shadows[1]};
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
`;

const StatTitle = styled.h3`
  margin: 0 0 0.5rem;
  color: ${props => props.theme.colors.text.secondary};
  font-size: 0.9rem;
  font-weight: 500;
  text-transform: uppercase;
`;

const StatValue = styled.div`
  font-size: 2rem;
  font-weight: 700;
  color: ${props => props.theme.colors.primary};
  margin-bottom: 0.5rem;
`;

const StatDescription = styled.div`
  font-size: 0.85rem;
  color: ${props => props.theme.colors.text.secondary};
`;

const ActionsSection = styled.div`
  margin-bottom: 2rem;
`;

const SectionTitle = styled.h2`
  margin: 0 0 1.5rem;
  color: ${props => props.theme.colors.text.primary};
  font-size: 1.5rem;
`;

const ActionsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
`;

interface ActionCardProps {
  color?: 'primary' | 'secondary' | 'success' | 'info' | 'warning' | 'error';
}

const getColorForType = (color: string = 'primary', theme: any) => {
  switch (color) {
    case 'primary': return theme.colors.primary;
    case 'secondary': return theme.colors.secondary;
    case 'success': return theme.colors.success;
    case 'info': return theme.colors.info;
    case 'warning': return theme.colors.warning;
    case 'error': return theme.colors.error;
    default: return theme.colors.primary;
  }
};

const ActionCard = styled.div<ActionCardProps>`
  background-color: ${props => props.theme.colors.background.paper};
  padding: 2rem;
  border-radius: ${props => props.theme.borderRadius.medium};
  box-shadow: ${props => props.theme.shadows[1]};
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  border-top: 5px solid ${props => getColorForType(props.color, props.theme)};
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: ${props => props.theme.shadows[2]};
  }
`;

const ActionTitle = styled.h3`
  margin: 0 0 0.5rem;
  color: ${props => props.theme.colors.text.primary};
`;

const ActionDescription = styled.p`
  margin: 0;
  color: ${props => props.theme.colors.text.secondary};
  font-size: 0.9rem;
`;

const BacktestSection = styled.div`
  background-color: ${props => props.theme.colors.background.paper};
  padding: 2rem;
  border-radius: ${props => props.theme.borderRadius.medium};
  box-shadow: ${props => props.theme.shadows[1]};
  margin-bottom: 2rem;
  
  p {
    margin-bottom: 1.5rem;
    color: ${props => props.theme.colors.text.secondary};
  }
`;

const BacktestButton = styled.button`
  background-color: ${props => props.theme.colors.info};
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: ${props => props.theme.borderRadius.small};
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  
  &:hover {
    background-color: #1976d2;
  }
`;

const PerformanceSection = styled.div`
  background-color: ${props => props.theme.colors.background.paper};
  padding: 2rem;
  border-radius: ${props => props.theme.borderRadius.medium};
  box-shadow: ${props => props.theme.shadows[1]};
  margin-bottom: 2rem;
  
  p {
    margin-bottom: 1.5rem;
    color: ${props => props.theme.colors.text.secondary};
  }
`;

const PerformanceButton = styled.button`
  background-color: ${props => props.theme.colors.success};
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: ${props => props.theme.borderRadius.small};
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  
  &:hover {
    background-color: #388e3c;
  }
`;

export default DashboardPage;