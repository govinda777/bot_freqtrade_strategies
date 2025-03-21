import React, { createContext, useState, useEffect, useContext, ReactNode } from 'react';
import { ethers, BrowserProvider, formatEther } from 'ethers';

interface Web3ContextType {
  isConnected: boolean;
  account: string | null;
  balance: string;
  connectWallet: () => Promise<boolean>;
  disconnectWallet: () => void;
  sendCredits: (amount: number) => Promise<boolean>;
  buyCredits: (amount: number) => Promise<boolean>;
  provider: BrowserProvider | null;
}

const Web3Context = createContext<Web3ContextType>({
  isConnected: false,
  account: null,
  balance: '0',
  connectWallet: async () => false,
  disconnectWallet: () => {},
  sendCredits: async () => false,
  buyCredits: async () => false,
  provider: null
});

interface Web3ProviderProps {
  children: ReactNode;
}

export const Web3Provider: React.FC<Web3ProviderProps> = ({ children }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [account, setAccount] = useState<string | null>(null);
  const [balance, setBalance] = useState('0');
  const [provider, setProvider] = useState<BrowserProvider | null>(null);
  
  // Check if MetaMask is installed
  const checkIfWalletIsConnected = async () => {
    try {
      if (window.ethereum) {
        // Check if we're already connected
        const accounts = await window.ethereum.request({ method: 'eth_accounts' });
        
        if (accounts.length > 0) {
          const web3Provider = new BrowserProvider(window.ethereum);
          setProvider(web3Provider);
          
          const signer = await web3Provider.getSigner();
          const address = await signer.getAddress();
          
          const balanceInWei = await web3Provider.getBalance(address);
          const balanceInEth = formatEther(balanceInWei);
          
          setAccount(address);
          setBalance(balanceInEth);
          setIsConnected(true);
        }
      } else {
        console.log('No Ethereum wallet found');
      }
    } catch (error) {
      console.error('Error checking wallet connection:', error);
    }
  };
  
  // Connect to wallet
  const connectWallet = async () => {
    try {
      if (window.ethereum) {
        await window.ethereum.request({ method: 'eth_requestAccounts' });
        
        const web3Provider = new BrowserProvider(window.ethereum);
        setProvider(web3Provider);
        
        const signer = await web3Provider.getSigner();
        const address = await signer.getAddress();
        
        const balanceInWei = await web3Provider.getBalance(address);
        const balanceInEth = formatEther(balanceInWei);
        
        setAccount(address);
        setBalance(balanceInEth);
        setIsConnected(true);
        
        // Save to localStorage
        localStorage.setItem('isAuthenticated', 'true');
        
        return true;
      } else {
        console.log('No Ethereum wallet found');
        return false;
      }
    } catch (error) {
      console.error('Error connecting to wallet:', error);
      return false;
    }
  };
  
  // Disconnect from wallet
  const disconnectWallet = () => {
    setAccount(null);
    setBalance('0');
    setIsConnected(false);
    setProvider(null);
    
    // Clear from localStorage
    localStorage.removeItem('isAuthenticated');
  };
  
  // Send credits to the bot
  const sendCredits = async (amount: number): Promise<boolean> => {
    if (!isConnected || !provider) {
      console.error('Wallet not connected');
      return false;
    }
    
    try {
      // Implement token sending logic here
      // This would typically involve calling a contract function
      
      // Simulating a successful transaction for now
      console.log(`Sending ${amount} credits to the bot`);
      
      // Update balance after sending
      const signer = await provider.getSigner();
      const address = await signer.getAddress();
      const balanceInWei = await provider.getBalance(address);
      const balanceInEth = formatEther(balanceInWei);
      setBalance(balanceInEth);
      
      return true;
    } catch (error) {
      console.error('Error sending credits:', error);
      return false;
    }
  };
  
  // Buy credits
  const buyCredits = async (amount: number): Promise<boolean> => {
    if (!isConnected || !provider) {
      console.error('Wallet not connected');
      return false;
    }
    
    try {
      // Implement token purchase logic here
      // This would typically involve a payment and receiving tokens
      
      // Simulating a successful purchase for now
      console.log(`Buying ${amount} credits`);
      
      // Update balance after purchase
      const signer = await provider.getSigner();
      const address = await signer.getAddress();
      const balanceInWei = await provider.getBalance(address);
      const balanceInEth = formatEther(balanceInWei);
      setBalance(balanceInEth);
      
      return true;
    } catch (error) {
      console.error('Error buying credits:', error);
      return false;
    }
  };
  
  // Listen for account changes
  useEffect(() => {
    if (window.ethereum) {
      window.ethereum.on('accountsChanged', (accounts: string[]) => {
        if (accounts.length > 0) {
          checkIfWalletIsConnected();
        } else {
          disconnectWallet();
        }
      });
      
      window.ethereum.on('chainChanged', () => {
        window.location.reload();
      });
    }
    
    return () => {
      if (window.ethereum) {
        window.ethereum.removeListener('accountsChanged', () => {});
        window.ethereum.removeListener('chainChanged', () => {});
      }
    };
  }, []);
  
  // Check for existing connection on load
  useEffect(() => {
    checkIfWalletIsConnected();
  }, []);
  
  return (
    <Web3Context.Provider
      value={{
        isConnected,
        account,
        balance,
        connectWallet,
        disconnectWallet,
        sendCredits,
        buyCredits,
        provider
      }}
    >
      {children}
    </Web3Context.Provider>
  );
};

// Custom hook to use the Web3 context
export const useWeb3 = () => useContext(Web3Context);

// Type declaration for window.ethereum
declare global {
  interface Window {
    ethereum: any;
  }
}