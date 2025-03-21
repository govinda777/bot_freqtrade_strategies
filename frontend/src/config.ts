/**
 * Configuração para diferentes ambientes (desenvolvimento local e GitHub Pages)
 */

// Determina se estamos rodando em produção (GitHub Pages)
const isProduction = process.env.NODE_ENV === 'production';

// Determina se estamos rodando no GitHub Pages
const isGitHubPages = window.location.hostname.includes('github.io');

// URLs para diferentes ambientes
let API_BASE_URL = '';

if (isGitHubPages) {
  // Quando rodando no GitHub Pages, utilizamos a URL do backend no Render
  // Este valor deve ser atualizado para apontar para a URL real do backend após o deploy
  API_BASE_URL = 'https://freqtrade-backend.onrender.com';
} else if (isProduction) {
  // Em produção (mas não no GitHub Pages), usamos o backend local
  API_BASE_URL = window.location.origin;
} else {
  // Em desenvolvimento, usamos o proxy configurado no webpack
  API_BASE_URL = '';
}

export default {
  API_BASE_URL,
  
  // Endpoints específicos da API
  ENDPOINTS: {
    LOGIN: '/api/v1/token/login',
    LOGOUT: '/api/v1/token/logout',
    TRADES: '/api/v1/trades',
    BALANCE: '/api/v1/balance',
    STRATEGIES: '/api/v1/strategies',
    BACKTEST: '/api/v1/backtest',
  }
};