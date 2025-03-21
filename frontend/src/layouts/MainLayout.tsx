import React from 'react';
import { Outlet, useNavigate, Link } from 'react-router-dom';
import styled from 'styled-components';
import { useWeb3 } from '../contexts/Web3Context';
import { useAuth } from '../contexts/AuthContext';

interface MainLayoutProps {
  userType: 'client' | 'developer';
}

const MainLayout: React.FC<MainLayoutProps> = ({ userType }) => {
  const { isConnected, account, balance } = useWeb3();
  const { logout, userCredits } = useAuth();
  const navigate = useNavigate();

  // Handle logout
  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Menu items based on user type
  const getMenuItems = () => {
    if (userType === 'client') {
      return [
        { label: 'Dashboard', path: '/' },
        { label: 'Select Strategy', path: '/strategies' },
        { label: 'Backtest Results', path: '/backtest-results' },
        { label: 'Investment Results', path: '/investment-results' },
        { label: 'Balance', path: '/balance' },
        { label: 'Transaction History', path: '/history' },
      ];
    } else {
      return [
        { label: 'Dashboard', path: '/developer' },
        { label: 'Create Strategy', path: '/developer/create-strategy' },
        { label: 'Configure Backtest', path: '/developer/configure-backtest' },
        { label: 'Performance', path: '/developer/performance' },
        { label: 'Publish Strategy', path: '/developer/publish-strategy' },
        { label: 'Promote Strategy', path: '/developer/promote-strategy' },
        { label: 'Balance', path: '/developer/balance' },
        { label: 'Transaction History', path: '/developer/history' },
      ];
    }
  };

  return (
    <LayoutContainer>
      <Header>
        <Logo>
          <h1>FreqTrade</h1>
          <span>{userType === 'client' ? 'Client Portal' : 'Developer Portal'}</span>
        </Logo>
        <UserInfo>
          <div>
            <strong>Credits:</strong> {userCredits}
          </div>
          {isConnected && (
            <div>
              <strong>Wallet:</strong> {account?.substring(0, 6)}...{account?.substring(account.length - 4)}
            </div>
          )}
          <LogoutButton onClick={handleLogout}>Logout</LogoutButton>
        </UserInfo>
      </Header>

      <MainContent>
        <Sidebar>
          <Nav>
            {getMenuItems().map((item, index) => (
              <NavItem key={index}>
                <NavLink to={item.path}>{item.label}</NavLink>
              </NavItem>
            ))}
          </Nav>
        </Sidebar>

        <Content>
          <Outlet />
        </Content>
      </MainContent>

      <Footer>
        <p>© {new Date().getFullYear()} FreqTrade Bot Interface. All rights reserved.</p>
      </Footer>
    </LayoutContainer>
  );
};

// Styled Components
const LayoutContainer = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
`;

const Header = styled.header`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: ${props => props.theme.colors.primary};
  color: white;
  box-shadow: ${props => props.theme.shadows[2]};
`;

const Logo = styled.div`
  display: flex;
  flex-direction: column;
  
  h1 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: bold;
  }
  
  span {
    font-size: 0.8rem;
    opacity: 0.8;
  }
`;

const UserInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  
  div {
    font-size: 0.9rem;
  }
`;

const LogoutButton = styled.button`
  background-color: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  
  &:hover {
    background-color: rgba(255, 255, 255, 0.3);
  }
`;

const MainContent = styled.div`
  display: flex;
  flex: 1;
`;

const Sidebar = styled.aside`
  width: 250px;
  background-color: ${props => props.theme.colors.background.paper};
  box-shadow: ${props => props.theme.shadows[1]};
  overflow-y: auto;
`;

const Nav = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const NavItem = styled.li`
  margin: 0;
`;

const NavLink = styled(Link)`
  display: block;
  padding: 1rem 1.5rem;
  color: ${props => props.theme.colors.text.primary};
  text-decoration: none;
  transition: background-color 0.3s, color 0.3s;
  
  &:hover {
    background-color: rgba(0, 0, 0, 0.05);
    color: ${props => props.theme.colors.primary};
  }
  
  &.active {
    background-color: rgba(63, 81, 181, 0.1);
    color: ${props => props.theme.colors.primary};
    border-left: 4px solid ${props => props.theme.colors.primary};
  }
`;

const Content = styled.main`
  flex: 1;
  padding: 2rem;
  background-color: ${props => props.theme.colors.background.default};
  overflow-y: auto;
`;

const Footer = styled.footer`
  background-color: ${props => props.theme.colors.background.paper};
  color: ${props => props.theme.colors.text.secondary};
  text-align: center;
  padding: 1rem;
  border-top: 1px solid ${props => props.theme.colors.divider};
`;

export default MainLayout;