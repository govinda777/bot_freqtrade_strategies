import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { useAuth } from '../contexts/AuthContext';

const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasMetaMask, setHasMetaMask] = useState(true);

  // Check if MetaMask is installed
  useEffect(() => {
    const checkMetaMask = () => {
      if (typeof window.ethereum === 'undefined') {
        setHasMetaMask(false);
      }
    };
    checkMetaMask();
  }, []);

  const handleConnect = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Always login as client user
      const success = await login('client');
      
      if (success) {
        // Redirect to client dashboard
        navigate('/');
      } else {
        setError('Failed to connect to MetaMask. Please make sure MetaMask is unlocked.');
      }
    } catch (err) {
      setError('An error occurred while connecting to MetaMask.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <LoginContainer>
      <LoginCard>
        <Logo>
          <h1>FreqTrade</h1>
          <span>Bot Interface</span>
        </Logo>

        <Description>
          Connect your MetaMask wallet to access the FreqTrade Bot Interface. This platform allows you to manage trading strategies, perform backtests, and execute live trading.
        </Description>

        {!hasMetaMask ? (
          <MetaMaskMissing>
            <h3>MetaMask Not Detected</h3>
            <p>
              MetaMask is required to use this application. Please install MetaMask browser extension to continue.
            </p>
            <InstallMetaMaskButton 
              href="https://metamask.io/download/" 
              target="_blank" 
              rel="noopener noreferrer"
            >
              Install MetaMask
            </InstallMetaMaskButton>
          </MetaMaskMissing>
        ) : (
          <>
            <ClientInfo>
              <ClientIconWrapper>
                <ClientIcon />
              </ClientIconWrapper>
              <ClientDetails>
                <h3>Client Access</h3>
                <p>Login to explore and use trading strategies for your crypto investments</p>
              </ClientDetails>
            </ClientInfo>

            {error && <ErrorMessage>{error}</ErrorMessage>}

            <ConnectButton 
              onClick={handleConnect} 
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Spinner /> Connecting...
                </>
              ) : (
                <>
                  <MetaMaskIcon /> Connect with MetaMask
                </>
              )}
            </ConnectButton>
          </>
        )}
      </LoginCard>
    </LoginContainer>
  );
};

// Styled components
const LoginContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, ${props => props.theme.colors.primary} 0%, #2c387e 100%);
  padding: 1rem;
`;

const LoginCard = styled.div`
  background-color: ${props => props.theme.colors.background.paper};
  border-radius: ${props => props.theme.borderRadius.medium};
  box-shadow: ${props => props.theme.shadows[3]};
  padding: 2rem;
  width: 100%;
  max-width: 480px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const Logo = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1rem;
  
  h1 {
    color: ${props => props.theme.colors.primary};
    margin: 0;
  }
  
  span {
    font-size: 1rem;
    color: ${props => props.theme.colors.text.secondary};
  }
`;

const Description = styled.p`
  color: ${props => props.theme.colors.text.secondary};
  text-align: center;
  margin: 0 0 1rem;
  line-height: 1.5;
`;

// Client section styling
const ClientInfo = styled.div`
  display: flex;
  align-items: center;
  padding: 1.25rem;
  border-radius: ${props => props.theme.borderRadius.small};
  border: 1px solid ${props => props.theme.colors.divider};
  background-color: rgba(63, 81, 181, 0.05);
`;

const ClientIconWrapper = styled.div`
  width: 48px;
  height: 48px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: ${props => props.theme.colors.primary};
  border-radius: 50%;
  color: white;
  margin-right: 1rem;
`;

const ClientIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0-6c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zm0 7c-2.67 0-8 1.34-8 4v3h16v-3c0-2.66-5.33-4-8-4zm6 5H6v-.99c.2-.72 3.3-2.01 6-2.01s5.8 1.29 6 2v1z" />
  </svg>
);

const ClientDetails = styled.div`
  flex: 1;
  
  h3 {
    margin: 0 0 0.5rem;
    font-size: 1.1rem;
    color: ${props => props.theme.colors.text.primary};
  }
  
  p {
    margin: 0;
    font-size: 0.9rem;
    color: ${props => props.theme.colors.text.secondary};
    line-height: 1.4;
  }
`;

// MetaMask missing section
const MetaMaskMissing = styled.div`
  text-align: center;
  padding: 1.5rem;
  border-radius: ${props => props.theme.borderRadius.small};
  border: 1px solid ${props => props.theme.colors.warning};
  background-color: rgba(255, 193, 7, 0.08);
  
  h3 {
    margin: 0 0 1rem;
    color: ${props => props.theme.colors.warning};
  }
  
  p {
    margin: 0 0 1.5rem;
    color: ${props => props.theme.colors.text.secondary};
  }
`;

const InstallMetaMaskButton = styled.a`
  display: inline-block;
  background-color: ${props => props.theme.colors.warning};
  color: #744210;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border-radius: ${props => props.theme.borderRadius.small};
  font-weight: 500;
  transition: background-color 0.3s;
  
  &:hover {
    background-color: #F9A825;
    text-decoration: none;
  }
`;

const ConnectButton = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.75rem;
  background-color: ${props => props.theme.colors.primary};
  color: white;
  border: none;
  border-radius: ${props => props.theme.borderRadius.small};
  padding: 1rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  
  &:hover:not(:disabled) {
    background-color: #303f9f;
  }
  
  &:disabled {
    background-color: #bdbdbd;
    cursor: not-allowed;
  }
`;

// MetaMask icon component
const MetaMaskIcon = () => (
  <svg width="20" height="20" viewBox="0 0 35 33" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M30.8 1L19.07 10.87L21.5 5.01L30.8 1Z" fill="#E2761B" stroke="#E2761B" strokeWidth="0.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M4.19 1L15.83 10.96L13.5 5.01L4.19 1Z" fill="#E4761B" stroke="#E4761B" strokeWidth="0.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M26.4 23.42L23.1 28.78L30.21 30.87L32.23 23.53L26.4 23.42Z" fill="#E4761B" stroke="#E4761B" strokeWidth="0.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M2.78 23.53L4.79 30.87L11.9 28.78L8.6 23.42L2.78 23.53Z" fill="#E4761B" stroke="#E4761B" strokeWidth="0.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M11.42 14.47L9.33 17.61L16.38 17.92L16.1 10.33L11.42 14.47Z" fill="#E4761B" stroke="#E4761B" strokeWidth="0.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M23.57 14.47L18.83 10.24L18.62 17.92L25.66 17.61L23.57 14.47Z" fill="#E4761B" stroke="#E4761B" strokeWidth="0.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M11.9 28.78L15.9 26.61L12.39 23.58L11.9 28.78Z" fill="#E4761B" stroke="#E4761B" strokeWidth="0.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M19.1 26.61L23.1 28.78L22.61 23.58L19.1 26.61Z" fill="#E4761B" stroke="#E4761B" strokeWidth="0.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Loading spinner
const Spinner = styled.div`
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
`;

const ErrorMessage = styled.div`
  color: ${props => props.theme.colors.error};
  background-color: rgba(244, 67, 54, 0.1);
  padding: 0.75rem;
  border-radius: ${props => props.theme.borderRadius.small};
  font-size: 0.9rem;
`;

export default LoginPage;