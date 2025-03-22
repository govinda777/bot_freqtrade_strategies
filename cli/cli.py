#!/usr/bin/env python3
"""
CLI - Interface de linha de comando para interagir com o backend Freqtrade.
"""
import os
import sys
import click
import logging

from .commands.auth import auth
from .commands.backtest import backtest
from .commands.bot import bot
from .commands.credits import credits
from .commands.strategies import strategies
from .config import load_config, save_config

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('cli')

@click.group()
@click.option('--debug', is_flag=True, help='Ativa modo de depuração')
@click.option('--config', '-c', default='~/.freqtrade-cli.json', help='Caminho para o arquivo de configuração')
@click.pass_context
def cli(ctx, debug, config):
    """CLI - Ferramenta para interagir com o backend Freqtrade."""
    if debug:
        logger.setLevel(logging.DEBUG)
        click.echo('Modo de depuração ativado')
    
    # Expandir caminho ~ para home do usuário
    config_path = os.path.expanduser(config)
    
    # Carrega configuração existente ou cria uma nova
    ctx.ensure_object(dict)
    ctx.obj['config'] = load_config(config_path)
    ctx.obj['config_path'] = config_path
    
    if debug:
        click.echo(f'Configuração carregada de: {config_path}')

# Registrar grupos de comandos
cli.add_command(auth)
cli.add_command(backtest)
cli.add_command(bot)
cli.add_command(credits)
cli.add_command(strategies)

@cli.command()
@click.option('--url', help='URL da API do backend')
@click.pass_context
def config(ctx, url):
    """Configurar CLI com URLs e outras configurações."""
    if url:
        ctx.obj['config']['backend_url'] = url
        save_config(ctx.obj['config_path'], ctx.obj['config'])
        click.echo(f'URL do backend configurada para: {url}')
    else:
        # Exibir configuração atual
        for key, value in ctx.obj['config'].items():
            if key != 'auth_token':  # Não mostrar token por segurança
                click.echo(f'{key}: {value}')

def main():
    try:
        cli(obj={})
    except Exception as e:
        logger.error(f"Erro: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()