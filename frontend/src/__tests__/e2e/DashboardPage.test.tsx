import React from 'react';
import { screen, fireEvent, waitFor, renderWithMocks } from '../test-utils';
import DashboardPage from '../../pages/DashboardPage';
import { BrowserRouter, useNavigate } from 'react-router-dom';
import '@testing-library/jest-dom';

// Use global Jest types
type MockedNavigate = jest.Mock<ReturnType<typeof useNavigate>>;

// Mock the useNavigate hook
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: jest.fn()
}));

describe('DashboardPage E2E Tests', () => {
  const mockNavigate = jest.fn();
  
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
    (useNavigate as MockedNavigate).mockImplementation(() => mockNavigate);
  });

  describe('Client User View', () => {
    beforeEach(() => {
      renderWithMocks(<DashboardPage />, {
        userType: 'client',
        userCredits: 500
      });
    });

    test('renders welcome section with client message', () => {
      expect(screen.getByText('Welcome to FreqTrade')).toBeInTheDocument();
      expect(screen.getByText(/Your trading dashboard is ready/)).toBeInTheDocument();
    });

    test('displays correct stats for client', () => {
      expect(screen.getByText('Credits')).toBeInTheDocument();
      expect(screen.getByTestId('user-credits')).toHaveTextContent('500');
      expect(screen.getByText('Selected Strategies')).toBeInTheDocument();
      expect(screen.getByText('Investment')).toBeInTheDocument();
      expect(screen.getByText('Total Profit')).toBeInTheDocument();
    });

    test('shows client-specific quick actions', () => {
      expect(screen.getByText('Select Strategy')).toBeInTheDocument();
      expect(screen.getByText('Buy Credits')).toBeInTheDocument();
      expect(screen.getByText('View Results')).toBeInTheDocument();
      expect(screen.getByText('Withdraw Profit')).toBeInTheDocument();
    });

    test('shows investment performance section', () => {
      expect(screen.getByText('Investment Performance')).toBeInTheDocument();
      expect(screen.getByText('View Detailed Performance')).toBeInTheDocument();
    });

    test('clicking actions triggers navigation', async () => {
      // Click the Select Strategy card
      fireEvent.click(screen.getByText('Select Strategy'));
      expect(mockNavigate).toHaveBeenCalledWith('/strategies');

      // Click the Performance button
      fireEvent.click(screen.getByText('View Detailed Performance'));
      expect(mockNavigate).toHaveBeenCalledWith('/investment-results');
    });
  });

  describe('Developer User View', () => {
    beforeEach(() => {
      renderWithMocks(<DashboardPage isDeveloper={true} />, {
        userType: 'developer',
        userCredits: 300
      });
    });

    test('renders welcome section with developer message', () => {
      expect(screen.getByText('Welcome to FreqTrade')).toBeInTheDocument();
      expect(screen.getByText(/Your developer dashboard is ready/)).toBeInTheDocument();
    });

    test('displays correct stats for developer', () => {
      expect(screen.getByText('Credits')).toBeInTheDocument();
      expect(screen.getByTestId('user-credits')).toHaveTextContent('300');
      expect(screen.getByText('Published Strategies')).toBeInTheDocument();
      expect(screen.getByText('Revenue')).toBeInTheDocument();
      expect(screen.getByText('Total Profit')).toBeInTheDocument();
    });

    test('shows developer-specific quick actions', () => {
      expect(screen.getByText('Create Strategy')).toBeInTheDocument();
      expect(screen.getByText('Run Backtest')).toBeInTheDocument();
      expect(screen.getByText('Publish Strategy')).toBeInTheDocument();
      expect(screen.getByText('Promote Strategy')).toBeInTheDocument();
    });

    test('shows backtest section', () => {
      expect(screen.getByText('Recent Backtests')).toBeInTheDocument();
      expect(screen.getByText('View Backtest Results')).toBeInTheDocument();
    });

    test('clicking actions triggers navigation', async () => {
      // Click the Create Strategy card
      fireEvent.click(screen.getByText('Create Strategy'));
      expect(mockNavigate).toHaveBeenCalledWith('/developer/create-strategy');

      // Click the Backtest button
      fireEvent.click(screen.getByText('View Backtest Results'));
      expect(mockNavigate).toHaveBeenCalledWith('/developer/backtest-results');
    });
  });

  // Test responsive behavior
  describe('Responsive Behavior', () => {
    test('dashboard adapts to different screen sizes', async () => {
      // This would typically test responsive layouts
      // For demonstration, we'd mock window resize events and verify layout changes
      // However, actual implementation depends on how the responsiveness is implemented
      
      // Mock example (simplified):
      // global.innerWidth = 480; // Mobile width
      // fireEvent(window, new Event('resize'));
      // expect(...mobile specific assertions...);
      
      // global.innerWidth = 1024; // Desktop width
      // fireEvent(window, new Event('resize'));
      // expect(...desktop specific assertions...);
    });
  });
});