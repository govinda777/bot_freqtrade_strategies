"""
Comandos relacionados ao gerenciamento de bots.
"""
import click
import logging
import time
from tabulate import tabulate

from ..api import FreqtradeAPI, AuthError, APIError
from ..utils import format_date, format_currency

logger = logging.getLogger('cli.bot')

@click.group(name='bot')
def bot():
    """Gerenciar bots de trading."""
    pass

@bot.command(name='deploy')
@click.argument('strategy', required=True)
@click.option('--pairs', '-p', required=True, multiple=True, help='Pares de moedas para operar (ex: BTC/USDT)')
@click.option('--stake-amount', '-s', type=float, required=True, help='Valor em stake currency para cada trade')
@click.option('--exposure', '-e', type=click.Choice(['conservador', 'moderado', 'ousado']), default='moderado', 
              help='Nível de exposição ao risco')
@click.option('--confirm', is_flag=True, help='Confirmar implantação sem pedir confirmação adicional')
@click.pass_context
def deploy_bot(ctx, strategy, pairs, stake_amount, exposure, confirm):
    """Implanta um bot com a estratégia especificada."""
    config = ctx.obj['config']
    
    if not config.get('auth_token'):
        click.echo("Você precisa estar autenticado para implantar bots. Use 'cli auth login'.")
        return
    
    # Resumo da implantação
    click.echo("\n=== RESUMO DA IMPLANTAÇÃO DO BOT ===")
    click.echo(f"Estratégia: {strategy}")
    click.echo(f"Pares: {', '.join(pairs)}")
    click.echo(f"Valor por trade: {stake_amount}")
    click.echo(f"Nível de exposição: {exposure}")
    
    # Confirmação
    if not confirm and not click.confirm("\nConfirma a implantação do bot?"):
        click.echo("Implantação cancelada.")
        return
    
    api = FreqtradeAPI(config['backend_url'], config['auth_token'])
    
    try:
        # Verifica saldo de créditos
        credits = api.get_credits_balance()
        if credits.get('balance', 0) <= 0:
            click.echo("Erro: Você não possui créditos suficientes para implantar um bot.")
            if click.confirm("Deseja comprar créditos agora?"):
                ctx.invoke(ctx.parent.parent.commands['credits'].commands['buy'])
            return
        
        # Implanta o bot
        click.echo("\nImplantando bot...")
        result = api.deploy_bot(
            strategy_name=strategy,
            pairs=list(pairs),
            stake_amount=stake_amount,
            exposure_level=exposure
        )
        
        bot_id = result.get('bot_id')
        if not bot_id:
            click.echo("Erro: Resposta do servidor não contém ID do bot")
            return
            
        click.echo(f"\nBot implantado com sucesso! ID: {bot_id}")
        click.echo("O bot começará a operar em instantes.")
        
    except AuthError:
        click.echo("Erro de autenticação: Token inválido ou expirado. Por favor, faça login novamente.")
    except APIError as e:
        click.echo(f"Erro na API: {str(e)}")
    except Exception as e:
        click.echo(f"Erro inesperado: {str(e)}")
        logger.exception("Erro ao implantar bot")

@bot.command(name='list')
@click.pass_context
def list_bots(ctx):
    """Lista todos os bots implantados."""
    config = ctx.obj['config']
    
    if not config.get('auth_token'):
        click.echo("Você precisa estar autenticado. Use 'cli auth login'.")
        return
    
    api = FreqtradeAPI(config['backend_url'], config['auth_token'])
    
    try:
        bots = api._request('GET', '/api/bot')
        
        if not bots:
            click.echo("Nenhum bot encontrado.")
            return
            
        # Formatar dados para exibição
        data = []
        for bot_item in bots:
            data.append([
                bot_item.get('id'),
                bot_item.get('strategy_name'),
                ', '.join(bot_item.get('pairs', [])),
                format_currency(bot_item.get('stake_amount')),
                bot_item.get('status'),
                f"{bot_item.get('profit_percent', 0):.2f}%"
            ])
        
        headers = ["ID", "Estratégia", "Pares", "Stake", "Status", "Lucro"]
        click.echo(tabulate(data, headers=headers, tablefmt="grid"))
        
    except AuthError:
        click.echo("Erro de autenticação: Token inválido ou expirado. Por favor, faça login novamente.")
    except APIError as e:
        click.echo(f"Erro na API: {str(e)}")
    except Exception as e:
        click.echo(f"Erro inesperado: {str(e)}")
        logger.exception("Erro ao listar bots")

@bot.command(name='status')
@click.argument('bot_id', required=True)
@click.pass_context
def bot_status(ctx, bot_id):
    """Verifica o status de um bot específico."""
    config = ctx.obj['config']
    
    if not config.get('auth_token'):
        click.echo("Você precisa estar autenticado. Use 'cli auth login'.")
        return
    
    api = FreqtradeAPI(config['backend_url'], config['auth_token'])
    
    try:
        status = api.get_bot_status(bot_id)
        
        click.echo("\n=== STATUS DO BOT ===")
        click.echo(f"ID: {status.get('id')}")
        click.echo(f"Estratégia: {status.get('strategy_name')}")
        click.echo(f"Status: {status.get('status')}")
        click.echo(f"Uptime: {status.get('uptime', 'N/A')}")
        click.echo(f"Lucro atual: {status.get('profit_percent', 0):.2f}%")
        
        # Exibir trades ativos
        active_trades = status.get('active_trades', [])
        if active_trades:
            click.echo("\n--- Trades Ativos ---")
            trade_data = []
            for trade in active_trades:
                trade_data.append([
                    trade.get('id'),
                    trade.get('pair'),
                    trade.get('amount'),
                    trade.get('open_rate'),
                    trade.get('current_rate'),
                    f"{trade.get('profit_percent', 0):.2f}%",
                    format_date(trade.get('open_date'))
                ])
            
            trade_headers = ["ID", "Par", "Qtd", "Preço Entrada", "Preço Atual", "Lucro", "Abertura"]
            click.echo(tabulate(trade_data, headers=trade_headers, tablefmt="grid"))
        else:
            click.echo("\nNenhum trade ativo no momento.")
            
        # Exibir trades concluídos
        closed_trades = status.get('closed_trades', [])
        if closed_trades:
            click.echo("\n--- Últimos Trades Concluídos ---")
            closed_data = []
            for trade in closed_trades[:5]:  # Exibir apenas os 5 últimos
                closed_data.append([
                    trade.get('id'),
                    trade.get('pair'),
                    f"{trade.get('profit_percent', 0):.2f}%",
                    format_date(trade.get('close_date'))
                ])
            
            closed_headers = ["ID", "Par", "Lucro", "Fechamento"]
            click.echo(tabulate(closed_data, headers=closed_headers, tablefmt="grid"))
        
    except AuthError:
        click.echo("Erro de autenticação: Token inválido ou expirado. Por favor, faça login novamente.")
    except APIError as e:
        click.echo(f"Erro na API: {str(e)}")
    except Exception as e:
        click.echo(f"Erro inesperado: {str(e)}")
        logger.exception("Erro ao verificar status do bot")

@bot.command(name='stop')
@click.argument('bot_id', required=True)
@click.pass_context
def stop_bot(ctx, bot_id):
    """Para a execução de um bot específico."""
    config = ctx.obj['config']
    
    if not config.get('auth_token'):
        click.echo("Você precisa estar autenticado para parar bots. Use 'cli auth login'.")
        return
    
    api = FreqtradeAPI(config['backend_url'], config['auth_token'])
    
    try:
        click.echo(f"Parando bot com ID: {bot_id}...")
        result = api.stop_bot(bot_id)
        
        if result.get('status') == 'stopped':
            click.echo("Bot parado com sucesso!")
        else:
            click.echo("Erro ao parar o bot: resposta inesperada do servidor")
    except AuthError:
        click.echo("Erro de autenticação: Token inválido ou expirado. Por favor, faça login novamente.")
    except APIError as e:
        click.echo(f"Erro na API: {str(e)}")
    except Exception as e:
        click.echo(f"Erro inesperado: {str(e)}")
        logger.exception("Erro ao parar bot")
