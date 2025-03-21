import axios from 'axios';
import '@testing-library/jest-dom';

// Create a helper function to check if server is running
const checkServerStatus = async (url: string): Promise<boolean> => {
  try {
    const response = await axios.get(url, { timeout: 5000 });
    return response.status === 200;
  } catch (error) {
    console.error('Server check failed:', error);
    return false;
  }
};

// Create a helper to check if app HTML contains expected elements
const hasExpectedElements = async (url: string): Promise<boolean> => {
  try {
    const response = await axios.get(url, { timeout: 5000 });
    const html = response.data;
    
    // Check for root element where React mounts
    const hasRootElement = html.includes('id="root"');
    
    // Check for common app elements in the HTML
    const hasAppElements = html.includes('React') || 
                          html.includes('app') || 
                          html.includes('bundle');
    
    return hasRootElement && hasAppElements;
  } catch (error) {
    console.error('Element check failed:', error);
    return false;
  }
};

describe('Server Startup Tests', () => {
  // Base URL for testing - default development server
  const baseUrl = process.env.SERVER_URL || 'http://localhost:3000';
  
  // Skip tests if explicitly marked to skip server tests
  const skipTests = process.env.SKIP_SERVER_TESTS === 'true';
  
  // Conditional test that checks if server is running
  (skipTests ? describe.skip : describe)('Server availability', () => {
    test('server is running and accessible', async () => {
      const isServerRunning = await checkServerStatus(baseUrl);
      expect(isServerRunning).toBe(true);
    }, 10000); // Allow up to 10 seconds for server check
    
    test('server returns page with required elements', async () => {
      const hasElements = await hasExpectedElements(baseUrl);
      expect(hasElements).toBe(true);
    }, 10000); // Allow up to 10 seconds for content check
  });
  
  // Basic connectivity tests that don't require actual server
  describe('Server connection simulation', () => {
    // Mock axios for this test group
    beforeEach(() => {
      jest.mock('axios');
      const mockedAxios = axios as jest.Mocked<typeof axios>;
      
      // Mock successful response
      mockedAxios.get.mockImplementation(async () => {
        return {
          status: 200,
          data: `
            <!DOCTYPE html>
            <html>
              <head>
                <title>FreqTrade UI</title>
              </head>
              <body>
                <div id="root"></div>
                <script src="bundle.js"></script>
              </body>
            </html>
          `
        };
      });
    });
    
    afterEach(() => {
      jest.resetAllMocks();
    });
    
    test('can simulate successful server connection', async () => {
      const isServerRunning = await checkServerStatus(baseUrl);
      expect(isServerRunning).toBe(true);
    });
    
    test('can simulate page with required elements', async () => {
      const hasElements = await hasExpectedElements(baseUrl);
      expect(hasElements).toBe(true);
    });
  });
  
  // Test server error handling
  describe('Server error handling', () => {
    // Mock axios for this test group
    beforeEach(() => {
      jest.mock('axios');
      const mockedAxios = axios as jest.Mocked<typeof axios>;
      
      // Mock error response
      mockedAxios.get.mockRejectedValue(new Error('Connection refused'));
    });
    
    afterEach(() => {
      jest.resetAllMocks();
    });
    
    test('handles server connection failures gracefully', async () => {
      const isServerRunning = await checkServerStatus(baseUrl);
      expect(isServerRunning).toBe(false);
    });
  });
});