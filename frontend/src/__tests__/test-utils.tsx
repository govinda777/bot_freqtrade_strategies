import React, { ReactElement, createContext, useContext } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import { AuthProvider } from '../contexts/AuthContext';
import { Web3Provider } from '../contexts/Web3Context';
import theme from '../theme';

// Custom render with providers
const AllProviders: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <AuthProvider>
          <Web3Provider>
            {children}
          </Web3Provider>
        </AuthProvider>
      </BrowserRouter>
    </ThemeProvider>
  );
};

// Define types for our contexts
type UserType = 'client' | 'developer' | null;

interface AuthContextType {
  isAuthenticated: boolean;
  userType: UserType;
  userCredits: number;
  login: (type: UserType) => Promise<boolean>;
  logout: () => void;
  updateUserCredits: (amount: number) => void;
}

interface Web3ContextType {
  isConnected: boolean;
  account: string | null;
  balance: string;
  connectWallet: () => Promise<boolean>;
  disconnectWallet: () => void;
}

// Create contexts for testing
export const TestAuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  userType: null,
  userCredits: 0,
  login: async () => false,
  logout: () => {},
  updateUserCredits: () => {}
});

export const TestWeb3Context = createContext<Web3ContextType>({
  isConnected: false,
  account: null,
  balance: '0',
  connectWallet: async () => false,
  disconnectWallet: () => {}
});

// Setup testing renderer
const customRender = (ui: ReactElement, options?: any) => {
  const renderer = require('@testing-library/react').render;
  return renderer(ui, { wrapper: AllProviders, ...options });
};

// Mock Auth Provider with specific values
interface MockAuthContextProps {
  userType?: 'client' | 'developer';
  userCredits?: number;
  children: React.ReactNode;
}

export const MockAuthProvider: React.FC<MockAuthContextProps> = ({ 
  userType = 'client',
  userCredits = 1000, 
  children 
}) => {
  const mockFn = () => jest.fn();
  
  const mockAuthContext: AuthContextType = {
    isAuthenticated: true,
    userType,
    userCredits,
    login: mockFn() as any,
    logout: mockFn() as any,
    updateUserCredits: mockFn() as any
  };

  return (
    <TestAuthContext.Provider value={mockAuthContext}>
      {children}
    </TestAuthContext.Provider>
  );
};

// Mock Web3 Provider with specific values
interface MockWeb3ContextProps {
  connected?: boolean;
  account?: string;
  children: React.ReactNode;
}

export const MockWeb3Provider: React.FC<MockWeb3ContextProps> = ({ 
  connected = true,
  account = '0x123456789abcdef', 
  children 
}) => {
  const mockFn = () => jest.fn();
  
  const mockWeb3Context: Web3ContextType = {
    isConnected: connected,
    account,
    balance: '1.5',
    connectWallet: mockFn() as any,
    disconnectWallet: mockFn() as any
  };

  return (
    <TestWeb3Context.Provider value={mockWeb3Context}>
      {children}
    </TestWeb3Context.Provider>
  );
};

// Custom render with mocked auth and web3 contexts
// Override useAuth hook for testing
export const useAuth = () => useContext(TestAuthContext);

export const renderWithMocks = (
  ui: ReactElement,
  {
    userType = 'client' as 'client' | 'developer',
    userCredits = 1000,
    web3Connected = true,
    web3Account = '0x123456789abcdef',
    ...renderOptions
  } = {}
) => {
  const Wrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    return (
      <ThemeProvider theme={theme}>
        <BrowserRouter>
          <MockAuthProvider userType={userType} userCredits={userCredits}>
            <MockWeb3Provider connected={web3Connected} account={web3Account}>
              {children}
            </MockWeb3Provider>
          </MockAuthProvider>
        </BrowserRouter>
      </ThemeProvider>
    );
  };
  
  const renderer = require('@testing-library/react').render;
  return renderer(ui, { wrapper: Wrapper, ...renderOptions });
};

// Define Jest globals for TypeScript
declare global {
  namespace jest {
    interface MockInstance<T = any, Y extends any[] = any[]> {
      mockImplementation(...args: Y): MockInstance<T, Y>;
      mockReturnValue(value: T): MockInstance<T, Y>;
    }
    
    function fn(): MockInstance;
  }
}

// Re-export needed testing utilities
const testingLib = require('@testing-library/react');
export const screen = testingLib.screen;
export const fireEvent = testingLib.fireEvent;
export const waitFor = testingLib.waitFor;
export { customRender as render };