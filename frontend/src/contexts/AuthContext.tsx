import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useWeb3 } from './Web3Context';

type UserType = 'client' | 'developer' | null;

interface AuthContextType {
  isAuthenticated: boolean;
  userType: UserType;
  login: (type: UserType) => Promise<boolean>;
  logout: () => void;
  userCredits: number;
  updateUserCredits: (amount: number) => void;
}

const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  userType: null,
  login: async () => false,
  logout: () => {},
  userCredits: 0,
  updateUserCredits: () => {}
});

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const { isConnected, connectWallet, disconnectWallet } = useWeb3();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userType, setUserType] = useState<UserType>(null);
  const [userCredits, setUserCredits] = useState(0);

  // Check if user is already authenticated from localStorage
  useEffect(() => {
    const storedIsAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
    const storedUserType = localStorage.getItem('userType') as UserType;
    const storedCredits = Number(localStorage.getItem('userCredits')) || 0;
    
    if (storedIsAuthenticated && storedUserType) {
      setIsAuthenticated(storedIsAuthenticated);
      setUserType(storedUserType);
      setUserCredits(storedCredits);
    }
  }, []);

  // Update authentication state when wallet connection changes
  useEffect(() => {
    if (!isConnected) {
      setIsAuthenticated(false);
    }
  }, [isConnected]);

  // Login function
  const login = async (type: UserType): Promise<boolean> => {
    try {
      // First connect wallet
      const connected = await connectWallet();
      
      if (connected) {
        setIsAuthenticated(true);
        setUserType(type);
        
        // Save to localStorage
        localStorage.setItem('isAuthenticated', 'true');
        localStorage.setItem('userType', type || '');
        
        return true;
      }
      
      return false;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };

  // Logout function
  const logout = () => {
    disconnectWallet();
    setIsAuthenticated(false);
    setUserType(null);
    
    // Clear from localStorage
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('userType');
  };
  
  // Update user credits
  const updateUserCredits = (amount: number) => {
    const newBalance = amount;
    setUserCredits(newBalance);
    localStorage.setItem('userCredits', newBalance.toString());
  };
  
  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        userType,
        login,
        logout,
        userCredits,
        updateUserCredits
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the Auth context
export const useAuth = () => useContext(AuthContext);