docker run --rm -it --entrypoint /bin/sh bot_freqtrade_strategies-freqtrade

# 🤖 Freqtrade - Estratégias de Trading Automatizado

[![Freqtrade](https://img.shields.io/badge/Freqtrade-Oficial-blue)](https://www.freqtrade.io/en/stable/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)

Este repositório fornece um **framework completo para trading automatizado** de criptomoedas, utilizando diversas estratégias incluindo a **"Buy Low, Sell High"**. O bot é baseado no [Freqtrade](https://www.freqtrade.io/) e roda dentro de um **container Docker**, facilitando a instalação, configuração e execução.

## 📋 Índice

- [🚀 Recursos do Bot](#-recursos-do-bot)
- [🧠 Estratégias Disponíveis](#-estratégias-disponíveis)
- [⚙️ Pré-requisitos](#️-pré-requisitos)
- [📂 Estrutura do Projeto](#-estrutura-do-projeto)
- [🛠️ Instalação e Configuração](#️-instalação-e-configuração)
- [▶️ Como Rodar o Bot](#️-como-rodar-o-bot)
- [📊 Monitoramento e Dashboard](#-monitoramento-e-dashboard)
- [🔍 Testando Estratégias com Backtesting](#-testando-estratégias-com-backtesting)
- [💡 Otimização de Estratégias](#-otimização-de-estratégias)
- [⚠️ Solução de Problemas Comuns](#️-solução-de-problemas-comuns)
- [🛡️ Medidas de Segurança](#️-medidas-de-segurança)
- [📚 Documentação Adicional](#-documentação-adicional)
- [📌 Contribuindo](#-contribuindo)

## 🚀 Recursos do Bot

✅ **Automatiza compras e vendas** com base em estratégias de trading configuráveis  
✅ **Rodando em Docker**, sem necessidade de instalar dependências manualmente  
✅ **Suporte a Paper Trading** (modo simulação), permitindo testar a estratégia sem arriscar dinheiro real  
✅ **Backtesting** para testar o desempenho histórico da estratégia com dados passados  
✅ **Configuração flexível**, com arquivos JSON e variáveis de ambiente  
✅ **Múltiplas estratégias disponíveis**, incluindo estratégias baseadas em indicadores técnicos e IA  
✅ **Escalabilidade** para trabalhar com múltiplos pares de moedas simultaneamente  
✅ **Segurança** com keys de API limitadas a trading, sem permitir retiradas  

## 🧠 Estratégias Disponíveis

### CombinedBinHAndCluc

Esta estratégia é uma combinação de duas estratégias populares: BinHV45 e ClucMay72018.

- **Timeframe**: 5 minutos
- **ROI Mínimo**: 5%
- **Stop Loss**: -5%
- **Lógica de Entrada**:
  - Utiliza Bollinger Bands, EMA e análise de volume
  - Compra quando o preço cai abaixo da banda inferior de Bollinger ou quando satisfaz condições específicas de volume e preço
- **Lógica de Saída**:
  - Vende quando o preço cruza acima da banda média de Bollinger

> 📈 Esta estratégia funciona bem em mercados voláteis com tendências definidas. Para mais estratégias e detalhes, consulte o arquivo [STRATEGIES.md](STRATEGIES.md).

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de ter:

- **Docker** e **Docker Compose** instalados
- Uma **conta na Binance** ou outra exchange suportada
- Conhecimento básico de criptomoedas e trading
- Pelo menos 20 USDT (ou equivalente) na sua conta para começar a operar
- Sistema operacional: Linux, macOS, ou Windows com WSL2

## 📂 Estrutura do Projeto

```
bot_freqtrade_strategies/
│── docker-compose.yml       # Configuração do Docker
│── Dockerfile               # Definição da imagem Docker
│── config.json              # Configuração do bot
│── .env                     # Armazena credenciais de forma segura
│── run_bot.sh               # Script para iniciar o bot
│── stop_bot.sh              # Script para parar o bot
│── backtesting.sh           # Script para realizar backtesting
│── user_data/               # Pasta com dados do usuário
│   ├── strategies/          # Pasta com as estratégias
│   │   ├── CombinedBinHAndCluc.py  # Estratégia combinada
│   ├── backtest_results/    # Resultados de backtests
│   ├── hyperopt_results/    # Resultados de otimizações
│── README.md                # Este arquivo com as instruções
│── STRATEGIES.md            # Documentação detalhada sobre estratégias
│── Backtesting.md           # Guia de backtesting
│── CONFIG.md                # Guia de configuração detalhada
```

## 🛠️ Instalação e Configuração

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seu-usuario/bot_freqtrade_strategies.git
cd bot_freqtrade_strategies
```

### 2️⃣ Configurar o ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```bash
cp .env.example .env
```

Abra o arquivo `.env` e adicione suas credenciais:

```ini
BINANCE_API_KEY=SUA_API_KEY
BINANCE_SECRET_KEY=SUA_SECRET_KEY
```

### 3️⃣ Criando e Configurando a API Key na Binance

Para que o bot possa operar, você precisa gerar uma **API Key** e uma **Secret Key** na Binance. Siga os passos abaixo:

#### **Gerar a API Key na Binance**
1. Acesse sua conta na Binance e vá para [Gerenciamento de API](https://www.binance.com/pt-BR/my/settings/api-management).
2. Clique em **Criar API** e escolha **Gerada pelo sistema**.
3. Dê um nome para a API, como `bot_freqtrade` e clique em **Próximo**.
4. **Habilite apenas as seguintes permissões:**
   - ✅ *Habilitar Leitura*
   - ✅ *Ativar Trading Spot e de Margem*
   - ❌ **Não habilite retiradas!** Isso mantém seus fundos seguros.
5. **Configure a restrição de IP**:
   - ✅ **Recomendado**: Escolha **Restringir o acesso apenas a IPs confiáveis** e insira o IP da sua máquina ou servidor.
   - ⚠ **Se você estiver rodando na sua máquina local**, descubra seu IP em [https://www.whatismyip.com/](https://www.whatismyip.com/) e adicione na Binance.
   - ⚠ **Se estiver rodando em um VPS**, insira o IP fixo do servidor.
6. Confirme a criação da API seguindo as etapas de segurança da Binance.
7. **Copie a API Key e a Secret Key** e guarde em um local seguro (a Secret Key só será exibida uma vez!).

### 4️⃣ Configurar o bot

Abra o arquivo `config.json` e ajuste as configurações conforme necessário:

```json
{
    "max_open_trades": 2,
    "stake_currency": "USDT",
    "stake_amount": 20,
    "tradable_balance_ratio": 0.99,
    "dry_run": true,
    "dry_run_wallet": 100,
    "bid_strategy": {
        "price_side": "bid",
        "ask_last_balance": 0.0,
        "use_order_book": false,
        "order_book_top": 1
    },
    "exchange": {
        "name": "binance",
        "key": "${BINANCE_API_KEY}",
        "secret": "${BINANCE_SECRET_KEY}",
        "pair_whitelist": [
            "BTC/USDT", "ETH/USDT", "ADA/USDT", "SOL/USDT",
            "DOT/USDT", "AVAX/USDT", "MATIC/USDT", "LINK/USDT"
        ],
        "ccxt_config": {"enableRateLimit": true},
        "ccxt_async_config": {"enableRateLimit": true}
    }
}
```

> 🔹 O `dry_run` está ativado por padrão para evitar perdas. Para operar no modo real, altere `"dry_run": false`.

## ▶️ Como Rodar o Bot

### **Iniciar o bot em modo simulação (Paper Trading)**

```bash
./run_bot.sh
```

Ou usando Docker Compose diretamente:

```bash
docker-compose up -d
```

### **Parar o bot**

```bash
./stop_bot.sh
```

Ou usando Docker Compose diretamente:

```bash
docker-compose down
```

### **Verificar os logs do bot**

```bash
docker logs -f freqtrade_bot
```

## 📊 Monitoramento e Dashboard

O Freqtrade inclui uma API REST que permite monitorar o desempenho do bot através de um dashboard web.

### **Acessar o Dashboard**

Por padrão, o dashboard está disponível em:

```
http://localhost:8080
```

Credenciais padrão:
- **Usuário**: freqtrader
- **Senha**: freqtrader

> ⚠️ É altamente recomendado alterar as credenciais padrão se você acessar o dashboard pela internet.

### **Comandos Úteis para Monitoramento**

```bash
# Ver status do bot e trades ativos
docker exec -it freqtrade_bot freqtrade status

# Ver balanço da carteira
docker exec -it freqtrade_bot freqtrade balance

# Ver lista de pares em análise
docker exec -it freqtrade_bot freqtrade whitelist
```

## 🔍 Testando Estratégias com Backtesting

Antes de operar com dinheiro real, é essencial testar suas estratégias com dados históricos.

### **Executar backtesting com script**

```bash
./backtesting.sh CombinedBinHAndCluc BTC/USDT ETH/USDT 2023-01-01 2023-06-30
```

Este comando executa um backtest da estratégia CombinedBinHAndCluc nos pares BTC/USDT e ETH/USDT para o período especificado.

### **Executar backtesting manualmente**

```bash
docker run --rm -v $(pwd):/freqtrade freqtradeorg/freqtrade:stable \
    backtesting \
    --strategy CombinedBinHAndCluc \
    --config config.json \
    --timerange 20230101-20230630 \
    --pairs BTC/USDT ETH/USDT
```

### **Analisando os Resultados**

Os resultados do backtesting mostrarão:
- Retorno total da estratégia
- Número de trades executados
- Percentual de trades lucrativos
- Drawdown máximo (risco de perda)
- Duração média dos trades

Para uma análise detalhada dos resultados, consulte [Backtesting.md](Backtesting.md).

## 💡 Otimização de Estratégias

O Freqtrade oferece uma funcionalidade chamada "Hyperopt" que permite otimizar os parâmetros da sua estratégia:

```bash
docker run --rm -v $(pwd):/freqtrade freqtradeorg/freqtrade:stable \
    hyperopt \
    --hyperopt-loss SharpeHyperOptLoss \
    --strategy CombinedBinHAndCluc \
    --config config.json \
    --timerange 20230101-20230630 \
    --epochs 100 \
    --spaces buy sell roi stoploss
```

Este comando executará 100 iterações de otimização, buscando os melhores parâmetros para entrada, saída, ROI e stoploss.

## ⚠️ Solução de Problemas Comuns

### 1. Bot não consegue conectar à exchange
- Verifique se suas API keys estão corretas no arquivo `.env`
- Confirme se você habilitou as permissões para trading
- Verifique se o IP do seu servidor está na lista de IPs permitidos na Binance

### 2. Muitas requisições (429 Too Many Requests)
- Adicione `"enableRateLimit": true` no `ccxt_config` do seu arquivo `config.json`
- Reduza o número de pares de moedas na sua `pair_whitelist`

### 3. O bot inicia mas não faz trades
- Verifique se o mercado está em condições favoráveis para sua estratégia
- Confirme se você tem saldo suficiente na sua conta
- Verifique se o `minimal_roi` e `stoploss` estão configurados adequadamente

### 4. Erros de Docker
- Verifique se o Docker e Docker Compose estão instalados corretamente
- Tente reconstruir a imagem: `docker-compose build --no-cache`

Para mais soluções de problemas, consulte [CONFIG.md](CONFIG.md).

## 🛡️ Medidas de Segurança

🔒 **Nunca ative retiradas na API Key** – Isso impede que fundos sejam roubados caso sua chave vaze.  
💰 **Use stop-loss e trailing stop** – Para limitar perdas e proteger lucros.  
🛠️ **Teste sempre em modo Paper Trading primeiro** – Antes de usar dinheiro real.  
📊 **Acompanhe os resultados e faça ajustes** – O mercado muda, e sua estratégia pode precisar ser otimizada.  
🔑 **Armazene suas chaves API de forma segura** – Use o arquivo `.env` e nunca compartilhe suas chaves.  
⚡ **Configure alertas** – Para ser notificado sobre trades ou problemas com o bot.  

## 📚 Documentação Adicional

Este repositório inclui documentação detalhada sobre vários aspectos do bot:

- [STRATEGIES.md](STRATEGIES.md) - Descrição detalhada das estratégias disponíveis
- [CONFIG.md](CONFIG.md) - Guia completo de configuração do bot
- [Backtesting.md](Backtesting.md) - Instruções detalhadas para backtesting
- [CombinedBinHAndCluc.md](CombinedBinHAndCluc.md) - Documentação específica sobre a estratégia CombinedBinHAndCluc

Para a documentação oficial do Freqtrade, visite:
- [Documentação do Freqtrade](https://www.freqtrade.io/en/stable/)
- [Wiki do Freqtrade no GitHub](https://github.com/freqtrade/freqtrade/wiki)

## 📌 Contribuindo

Se quiser sugerir melhorias ou relatar bugs, abra um **issue** ou envie um **pull request**.

### Como contribuir:

1. Faça um fork do repositório
2. Crie uma branch para sua feature: `git checkout -b minha-nova-feature`
3. Commit suas mudanças: `git commit -am 'Adicionar nova feature'`
4. Push para a branch: `git push origin minha-nova-feature`
5. Envie um Pull Request

---

## 📊 Aviso de Risco

Os bots de trading funcionam seguindo regras algorítmicas e não garantem lucro. O mercado de criptomoedas é extremamente volátil e imprevisível. **Nunca invista mais do que você pode perder**.

---

📈 **Bons trades e sucesso nos investimentos! 🚀**

