"""
Cliente HTTP para comunicação com o backend Freqtrade.
"""
import requests
import logging
from urllib.parse import urljoin

logger = logging.getLogger('cli.api')

class FreqtradeAPI:
    """Cliente para a API do Freqtrade."""
    
    def __init__(self, base_url, auth_token=None):
        self.base_url = base_url
        self.auth_token = auth_token
        self.session = requests.Session()
        
        if auth_token:
            self.session.headers.update({
                'Authorization': f'Bearer {auth_token}'
            })
        
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'FreqtradeCLI/1.0'
        })
    
    def set_auth_token(self, token):
        """Define o token de autenticação."""
        self.auth_token = token
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
    
    def _request(self, method, endpoint, **kwargs):
        """Método genérico para fazer requisições."""
        url = urljoin(self.base_url, endpoint)
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            if response.content:
                return response.json()
            return {}
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erro HTTP: {e}")
            if e.response.status_code == 401:
                raise AuthError("Token de autenticação inválido ou expirado")
            if e.response.content:
                try:
                    error_data = e.response.json()
                    logger.error(f"Detalhes do erro: {error_data}")
                    raise APIError(f"{error_data.get('error', 'Erro desconhecido')}")
                except ValueError:
                    pass
            raise APIError(f"Erro na requisição: {str(e)}")
        except requests.exceptions.ConnectionError:
            raise APIError(f"Não foi possível conectar ao backend em {self.base_url}")
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            raise APIError(f"Erro inesperado: {str(e)}")
    
    # Métodos de autenticação
    def login_metamask(self, wallet_address, signature):
        """Login com MetaMask."""
        return self._request('POST', '/api/auth/login', json={
            'wallet_address': wallet_address,
            'signature': signature
        })
    
    # Métodos para backtest
    def run_backtest(self, strategy_name, timerange, pairs, stake_amount=None, exposure_level=None):
        """Executa um backtest."""
        data = {
            'strategy_name': strategy_name,
            'timerange': timerange,
            'pairs': pairs
        }
        
        if stake_amount:
            data['stake_amount'] = stake_amount
        
        if exposure_level:
            data['exposure_level'] = exposure_level
            
        return self._request('POST', '/api/backtest/run', json=data)
    
    def get_backtest_status(self, backtest_id):
        """Obtém o status de um backtest."""
        return self._request('GET', f'/api/backtest/{backtest_id}/status')
    
    def get_backtest_results(self, backtest_id):
        """Obtém os resultados de um backtest."""
        return self._request('GET', f'/api/backtest/{backtest_id}/results')
    
    # Métodos para bots
    def deploy_bot(self, strategy_name, pairs, stake_amount, exposure_level='moderate'):
        """Implanta um bot com a estratégia especificada."""
        return self._request('POST', '/api/bot/deploy', json={
            'strategy_name': strategy_name,
            'pairs': pairs,
            'stake_amount': stake_amount,
            'exposure_level': exposure_level
        })
    
    def get_bot_status(self, bot_id):
        """Obtém o status de um bot."""
        return self._request('GET', f'/api/bot/{bot_id}/status')
    
    def stop_bot(self, bot_id):
        """Para a execução de um bot."""
        return self._request('POST', f'/api/bot/{bot_id}/stop')
    
    # Métodos para estratégias
    def list_strategies(self):
        """Lista todas as estratégias disponíveis."""
        return self._request('GET', '/api/strategies')
    
    def get_strategy_details(self, strategy_name):
        """Obtém detalhes de uma estratégia."""
        return self._request('GET', f'/api/strategies/{strategy_name}')
    
    # Métodos para créditos
    def get_credits_balance(self):
        """Obtém o saldo de créditos."""
        return self._request('GET', '/api/credits/balance')
    
    def purchase_credits(self, amount):
        """Inicia o processo de compra de créditos."""
        return self._request('POST', '/api/credits/purchase', json={
            'amount': amount
        })

class APIError(Exception):
    """Erro na API."""
    pass

class AuthError(APIError):
    """Erro de autenticação."""
    pass
