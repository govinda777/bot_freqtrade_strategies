"""
Gerenciamento de configuração para CLI.
"""
import os
import json
import logging

logger = logging.getLogger('cli.config')

DEFAULT_CONFIG = {
    'backend_url': 'https://freqtrade-bot.onrender.com',
    'auth_token': None,
    'user_id': None,
}

def load_config(config_path):
    """Carrega configuração de um arquivo JSON."""
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                # Verificar se há novos campos no DEFAULT_CONFIG que não estão no arquivo
                updated = False
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                        updated = True
                
                if updated:
                    save_config(config_path, config)
                    
                return config
        else:
            # Cria diretório se necessário
            directory = os.path.dirname(config_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            save_config(config_path, DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
    except Exception as e:
        logger.error(f"Erro ao carregar configuração: {str(e)}")
        return DEFAULT_CONFIG.copy()

def save_config(config_path, config):
    """Salva configuração em um arquivo JSON."""
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        logger.error(f"Erro ao salvar configuração: {str(e)}")
