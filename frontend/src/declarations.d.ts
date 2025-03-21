// This file is used to tell TypeScript about modules that don't have explicit type definitions
// It helps resolve "Cannot find module" type errors

declare module '*.svg' {
  const content: any;
  export default content;
}

declare module '*.png' {
  const content: any;
  export default content;
}

declare module '*.jpg' {
  const content: any;
  export default content;
}

// Explicitly declare problematic modules
declare module './contexts/AuthContext' {
  export const AuthProvider: React.FC<{ children: React.ReactNode }>;
  export const useAuth: () => {
    isAuthenticated: boolean;
    userType: 'client' | 'developer' | null;
    login: (type: 'client' | 'developer' | null) => Promise<boolean>;
    logout: () => void;
    userCredits: number;
    updateUserCredits: (amount: number) => void;
  };
}

declare module './theme' {
  const theme: {
    colors: any;
    typography: any;
    shadows: string[];
    spacing: (factor: number) => string;
    borderRadius: any;
    transitions: any;
    zIndex: any;
  };
  export default theme;
}

// Declare modules for all other local imports that TypeScript can't resolve
declare module './contexts/Web3Context';
declare module './layouts/MainLayout';
declare module './pages/*';