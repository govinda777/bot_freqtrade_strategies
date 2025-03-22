"""
Comandos relacionados a backtesting de estratégias.
"""
import click
import logging
import time
import json
from tabulate import tabulate

from ..api import FreqtradeAPI, AuthError, APIError
from ..utils import format_date, save_json, parse_timerange

logger = logging.getLogger('cli.backtest')

@click.group(name='backtest')
def backtest():
    """Gerenciar backtests de estratégias."""
    pass

@backtest.command(name='run')
@click.argument('strategy', required=True)
@click.option('--timerange', '-t', required=True, help='Período para backtest (formato: YYYYMMDD-YYYYMMDD)')
@click.option('--pairs', '-p', required=True, multiple=True, help='Pares de moedas para testar (ex: BTC/USDT)')
@click.option('--stake-amount', '-s', type=float, default=None, help='Valor em stake currency para cada trade')
@click.option('--exposure', '-e', type=click.Choice(['conservador', 'moderado', 'ousado']), default='moderado', help='Nível de exposição')
@click.option('--wait/--no-wait', default=True, help='Aguardar a conclusão do backtest')
@click.pass_context
def run_backtest(ctx, strategy, timerange, pairs, stake_amount, exposure, wait):
    """Executa um backtest com a estratégia especificada."""
    config = ctx.obj['config']
    
    if not config.get('auth_token'):
        click.echo("Você precisa estar autenticado para executar backtests. Use 'cli auth login'.")
        return
    
    # Validar e formatar o timerange
    try:
        timerange = parse_timerange(timerange)
    except ValueError as e:
        click.echo(f"Erro: {str(e)}")
        return
    
    api = FreqtradeAPI(config['backend_url'], config['auth_token'])
    
    try:
        # Inicia o backtest
        click.echo(f"Iniciando backtest da estratégia '{strategy}'...")
        result = api.run_backtest(
            strategy_name=strategy,
            timerange=timerange,
            pairs=list(pairs),
            stake_amount=stake_amount,
            exposure_level=exposure
        )
        
        backtest_id = result.get('backtest_id')
        if not backtest_id:
            click.echo("Erro: Resposta do servidor não contém ID do backtest")
            return
            
        click.echo(f"Backtest iniciado com ID: {backtest_id}")
        
        if wait:
            # Aguarda a conclusão do backtest
            click.echo("Aguardando conclusão do backtest...")
            status = "pending"
            progress = 0
            
            with click.progressbar(length=100) as bar:
                while status in ["pending", "running"]:
                    time.sleep(2)  # Espera 2 segundos entre as verificações
                    
                    try:
                        status_data = api.get_backtest_status(backtest_id)
                        status = status_data.get('status', 'unknown')
                        new_progress = status_data.get('progress', 0)
                        
                        # Atualiza a barra de progresso
                        if new_progress > progress:
                            bar.update(new_progress - progress)
                            progress = new_progress
                    except Exception as e:
                        click.echo(f"\nErro ao verificar status: {str(e)}")
                        break
                
                if status == "completed":
                    click.echo("\nBacktest concluído com sucesso!")
                    results = api.get_backtest_results(backtest_id)
                    display_backtest_results(results)
                elif status == "failed":
                    click.echo("\nBacktest falhou!")
                    status_data = api.get_backtest_status(backtest_id)
                    click.echo(f"Erro: {status_data.get('error', 'Desconhecido')}")
                else:
                    click.echo(f"\nStatus do backtest: {status}")
        
    except AuthError:
        click.echo("Erro de autenticação: Token inválido ou expirado. Por favor, faça login novamente.")
    except APIError as e:
        click.echo(f"Erro na API: {str(e)}")
    except Exception as e:
        click.echo(f"Erro inesperado: {str(e)}")
        logger.exception("Erro ao executar backtest")

@backtest.command(name='list')
@click.pass_context
def list_backtests(ctx):
    """Lista todos os backtests executados."""
    config = ctx.obj['config']
    
    if not config.get('auth_token'):
        click.echo("Você precisa estar autenticado. Use 'cli auth login'.")
        return
    
    api = FreqtradeAPI(config['backend_url'], config['auth_token'])
    
    try:
        backtests = api._request('GET', '/api/backtest')
        
        if not backtests:
            click.echo("Nenhum backtest encontrado.")
            return
            
        # Formatar dados para exibição
        data = []
        for bt in backtests:
            data.append([
                bt.get('id'),
                bt.get('strategy_name'),
                bt.get('timerange'),
                bt.get('status'),
                format_date(bt.get('created_at')),
                f"{bt.get('profit_percent', 0):.2f}%"
            ])
        
        headers = ["ID", "Estratégia", "Período", "Status", "Data", "Lucro"]
        click.echo(tabulate(data, headers=headers, tablefmt="grid"))
        
    except AuthError:
        click.echo("Erro de autenticação: Token inválido ou expirado. Por favor, faça login novamente.")
    except APIError as e:
        click.echo(f"Erro na API: {str(e)}")
    except Exception as e:
        click.echo(f"Erro inesperado: {str(e)}")
        logger.exception("Erro ao listar backtests")

@backtest.command(name='show')
@click.argument('backtest_id', required=True)
@click.pass_context
def show_backtest(ctx, backtest_id):
    """Exibe os resultados detalhados de um backtest específico."""
    config = ctx.obj['config']
    
    if not config.get('auth_token'):
        click.echo("Você precisa estar autenticado. Use 'cli auth login'.")
        return
    
    api = FreqtradeAPI(config['backend_url'], config['auth_token'])
    
    try:
        results = api.get_backtest_results(backtest_id)
        display_backtest_results(results)
    except AuthError:
        click.echo("Erro de autenticação: Token inválido ou expirado. Por favor, faça login novamente.")
    except APIError as e:
        click.echo(f"Erro na API: {str(e)}")
    except Exception as e:
        click.echo(f"Erro inesperado: {str(e)}")
        logger.exception("Erro ao exibir backtest")

def display_backtest_results(results):
    """Exibe os resultados de um backtest de forma formatada."""
    if not results:
        click.echo("Nenhum resultado disponível.")
        return
    
    # Exibir resumo
    summary = results.get('summary', {})
    click.echo("\n=== RESUMO DO BACKTEST ===")
    click.echo(f"Estratégia: {results.get('strategy', 'N/A')}")
    click.echo(f"Período: {results.get('timerange', 'N/A')}")
    click.echo(f"Total de trades: {summary.get('total_trades', 0)}")
    click.echo(f"Lucro: {summary.get('profit_percent', 0):.2f}%")
    click.echo(f"Profit factor: {summary.get('profit_factor', 0):.2f}")
    click.echo(f"Trades vencedores: {summary.get('winning_trades', 0)} ({summary.get('win_rate', 0):.2f}%)")
    click.echo(f"Drawdown máximo: {summary.get('max_drawdown', 0):.2f}%")
    
    # Exibir métricas por par
    pair_metrics = results.get('pair_metrics', [])
    if pair_metrics:
        click.echo("\n=== MÉTRICAS POR PAR ===")
        data = []
        for pair in pair_metrics:
            data.append([
                pair.get('pair'),
                pair.get('trades'),
                f"{pair.get('profit_percent', 0):.2f}%",
                f"{pair.get('win_rate', 0):.2f}%"
            ])
        
        headers = ["Par", "Trades", "Lucro", "Win Rate"]
        click.echo(tabulate(data, headers=headers, tablefmt="grid"))
    
    # Opções para exportar resultados
    if click.confirm("\nDeseja exportar os resultados para um arquivo JSON?"):
        filename = click.prompt("Nome do arquivo", default=f"backtest_{int(time.time())}.json")
        success, result = save_json(results, filename)
        if success:
            click.echo(f"Resultados exportados para {result}")
        else:
            click.echo(f"Erro ao exportar resultados: {result}")
