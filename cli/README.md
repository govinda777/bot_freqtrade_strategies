
# Documentação da CLI Freqtrade

## Sumário

- [Introdução](#introdução)
- [Instalação](#instalação)
- [Configuração Inicial](#configuração-inicial)
- [Autenticação](#autenticação)
- [Gerenciamento de Backtests](#gerenciamento-de-backtests)
- [Implantação e Monitoramento de Bots](#implantação-e-monitoramento-de-bots)
- [Gerenciamento de Créditos](#gerenciamento-de-créditos)
- [Estratégias](#estratégias)
- [Exemplos de Uso](#exemplos-de-uso)
- [Solução de Problemas](#solução-de-problemas)

## Introdução

A CLI Freqtrade é uma ferramenta de linha de comando que permite interagir com o backend Freqtrade hospedado no Render. Com esta CLI, você pode executar backtests, implantar bots com estratégias personalizadas, gerenciar créditos e monitorar o desempenho dos seus bots de trading de criptomoedas, tudo a partir do terminal.

### Recursos Principais

- Autenticação via MetaMask ou navegador
- Execução e análise de backtests
- Implantação e monitoramento de bots de trading
- Gerenciamento de créditos para utilização da plataforma
- Acesso a diversas estratégias de trading disponíveis

## Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Conexão à internet para comunicação com o backend

### Método de Instalação

Instale a CLI utilizando pip:

```bash
pip install freqtrade-cli
```

Ou, para instalar diretamente do repositório:

```bash
git clone https://github.com/seu-usuario/cli
cd cli
pip install -e .
```

Após a instalação, você poderá usar o comando `cli` em seu terminal.

## Configuração Inicial

Antes de começar a usar a CLI, configure a URL do backend:

```bash
cli config --url https://freqtrade-bot.onrender.com
```

Verifique suas configurações atuais:

```bash
cli config
```

## Autenticação

A CLI suporta autenticação via carteira Ethereum (MetaMask) ou interface web.

### Login via Navegador

```bash
cli auth login
```

Este comando abrirá seu navegador para completar o processo de autenticação com MetaMask. Após a conclusão, copie o token gerado para o terminal.

### Login via Linha de Comando (Para desenvolvimento)

```bash
cli auth login --wallet 0xYourEthereumWalletAddress --private-key YourPrivateKey
```

**Nota:** Use este método apenas para desenvolvimento/testes, nunca compartilhe sua chave privada.

### Verificar Status de Autenticação

```bash
cli auth status
```

### Logout

```bash
cli auth logout
```

## Gerenciamento de Backtests

Os backtests permitem testar estratégias com dados históricos antes de usar capital real.

### Executar um Backtest

```bash
cli backtest run MinhaEstrategia --timerange 20230101-20230301 --pairs BTC/USDT ETH/USDT --stake-amount 100 --exposure moderado
```

Parâmetros:
- `run <estrategia>`: Nome da estratégia a ser testada
- `--timerange`: Período para o backtest no formato YYYYMMDD-YYYYMMDD
- `--pairs` ou `-p`: Um ou mais pares de criptomoedas
- `--stake-amount` ou `-s`: Valor por trade (opcional)
- `--exposure` ou `-e`: Nível de exposição (conservador, moderado, ousado)
- `--wait/--no-wait`: Aguardar ou não a conclusão do backtest

### Listar Backtests

```bash
cli backtest list
```

### Ver Resultados de um Backtest

```bash
cli backtest show <backtest_id>
```

## Implantação e Monitoramento de Bots

### Implantar um Bot

```bash
cli bot deploy MinhaEstrategia --pairs BTC/USDT ETH/USDT --stake-amount 100 --exposure moderado
```

Parâmetros:
- `deploy <estrategia>`: Nome da estratégia a ser utilizada
- `--pairs` ou `-p`: Um ou mais pares de criptomoedas
- `--stake-amount` ou `-s`: Valor por trade
- `--exposure` ou `-e`: Nível de exposição (conservador, moderado, ousado)
- `--confirm`: Implantar sem solicitar confirmação adicional

### Listar Bots Ativos

```bash
cli bot list
```

### Verificar Status de um Bot

```bash
cli bot status <bot_id>
```

### Parar um Bot

```bash
cli bot stop <bot_id>
```

## Gerenciamento de Créditos

Créditos são necessários para utilizar os serviços de backtest e operação de bots.

### Verificar Saldo de Créditos

```bash
cli credits balance
```

### Comprar Créditos

```bash
cli credits buy --amount 100
```

### Ver Histórico de Transações

```bash
cli credits history
```

## Estratégias

### Listar Estratégias Disponíveis

```bash
cli strategies list
```

### Ver Detalhes de uma Estratégia

```bash
cli strategies show MinhaEstrategia
```

## Exemplos de Uso

### Fluxo Completo para Testar e Implantar uma Estratégia

```bash
# Login
cli auth login

# Verificar estratégias disponíveis
cli strategies list

# Executar backtest
cli backtest run CombinedBinHAndCluc --timerange 20230101-20230301 --pairs BTC/USDT ETH/USDT --exposure moderado

# Verificar resultados do backtest
cli backtest show 12345

# Comprar créditos se necessário
cli credits buy --amount 50

# Implantar bot com a estratégia
cli bot deploy CombinedBinHAndCluc --pairs BTC/USDT ETH/USDT --stake-amount 100 --exposure moderado

# Monitorar status
cli bot status 67890
```

### Backtest Rápido de Múltiplas Estratégias

```bash
# Testar 3 estratégias com os mesmos parâmetros
for estrategia in "CombinedBinHAndCluc" "NostalgiaForInfinityX" "BBRSIOptimizedStrategy"; do
    cli backtest run $estrategia --timerange 20230101-20230301 --pairs BTC/USDT --exposure moderado --no-wait
done

# Listar todos os backtests
cli backtest list
```

## Solução de Problemas

### Erro de Autenticação

Se receber erros de autenticação:

```bash
cli auth logout
cli auth login
```

### Conectividade com o Backend

Para verificar se a CLI está se comunicando corretamente com o backend:

```bash
cli config
```

Confirme se a URL está correta. Se necessário, atualize:

```bash
cli config --url https://freqtrade-bot.onrender.com
```

### Logs Detalhados

Para obter logs mais detalhados durante a execução de comandos:

```bash
cli --debug backtest run MinhaEstrategia --timerange 20230101-20230301 --pairs BTC/USDT
```

### Reiniciar a Configuração

Se necessário, você pode excluir o arquivo de configuração e reiniciar:

```bash
rm ~/.freqtrade-cli.json
cli config --url https://freqtrade-bot.onrender.com
```

---

Para mais informações ou suporte, visite a documentação online em [https://freqtrade-bot.onrender.com/docs](https://freqtrade-bot.onrender.com/docs) ou entre em contato com a equipe de suporte.
