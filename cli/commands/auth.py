"""
Comandos relacionados à autenticação com o backend.
"""
import click
import logging
import webbrowser
import json
import time
from eth_account.messages import encode_defunct
from web3 import Web3

from ..api import FreqtradeAPI, AuthError
from ..config import save_config

logger = logging.getLogger('cli.auth')

@click.group(name='auth')
def auth():
    """Gerenciar autenticação com o backend."""
    pass

@auth.command(name='login')
@click.option('--wallet', help='Endereço da carteira Ethereum')
@click.option('--private-key', help='Chave privada da carteira (USE APENAS PARA TESTES/DESENVOLVIMENTO)')
@click.pass_context
def login(ctx, wallet, private_key):
    """Login com carteira Ethereum (MetaMask)."""
    config = ctx.obj['config']
    api = FreqtradeAPI(config['backend_url'])
    
    if wallet is None:
        if private_key:
            # Se apenas a chave privada for fornecida, derive o endereço da carteira
            web3 = Web3()
            account = web3.eth.account.from_key(private_key)
            wallet = account.address
            click.echo(f"Usando carteira derivada da chave privada: {wallet}")
        else:
            # Inicia o processo de login via browser
            click.echo("Iniciando processo de login via navegador...")
            webbrowser.open(f"{config['backend_url']}/login?cli=true")
            click.echo("Complete o processo de login no navegador e cole o token gerado:")
            token = click.prompt("Token de autenticação", hide_input=True)
            
            # Salva o token na configuração
            config['auth_token'] = token
            save_config(ctx.obj['config_path'], config)
            click.echo("Login realizado com sucesso!")
            return
    
    # Processo de login com wallet/private_key fornecidos
    if wallet and private_key:
        # Cria mensagem para assinar
        nonce = str(int(time.time()))
        message = f"Login na Freqtrade CLI - Nonce: {nonce}"
        
        try:
            # Assina a mensagem
            web3 = Web3()
            message_encoded = encode_defunct(text=message)
            signed_message = web3.eth.account.sign_message(message_encoded, private_key=private_key)
            signature = signed_message.signature.hex()
            
            # Envia para o backend
            result = api.login_metamask(wallet, signature)
            
            if 'token' in result:
                config['auth_token'] = result['token']
                config['user_id'] = result.get('user_id')
                save_config(ctx.obj['config_path'], config)
                click.echo("Login realizado com sucesso!")
            else:
                click.echo("Falha no login: resposta inesperada do servidor")
        except AuthError as e:
            click.echo(f"Erro de autenticação: {str(e)}")
        except Exception as e:
            click.echo(f"Erro ao realizar login: {str(e)}")
    else:
        click.echo("Erro: Forneça tanto o endereço da carteira quanto a chave privada, ou nenhum dos dois para usar o navegador.")

@auth.command(name='logout')
@click.pass_context
def logout(ctx):
    """Logout da conta atual."""
    config = ctx.obj['config']
    
    if config.get('auth_token'):
        config['auth_token'] = None
        config['user_id'] = None
        save_config(ctx.obj['config_path'], config)
        click.echo("Logout realizado com sucesso!")
    else:
        click.echo("Você não está logado.")

@auth.command(name='status')
@click.pass_context
def status(ctx):
    """Verifica o status da autenticação atual."""
    config = ctx.obj['config']
    
    if config.get('auth_token'):
        try:
            api = FreqtradeAPI(config['backend_url'], config['auth_token'])
            # Tentar obter informações do usuário para validar o token
            credits = api.get_credits_balance()
            click.echo(f"Autenticado como ID: {config.get('user_id', 'Desconhecido')}")
            click.echo(f"Saldo de créditos: {credits.get('balance', 'Desconhecido')}")
        except AuthError:
            click.echo("Token de autenticação inválido ou expirado. Por favor, faça login novamente.")
            config['auth_token'] = None
            save_config(ctx.obj['config_path'], config)
        except Exception as e:
            click.echo(f"Erro ao verificar status: {str(e)}")
    else:
        click.echo("Você não está logado.") 