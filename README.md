docker run --rm -it --entrypoint /bin/sh bot_freqtrade_strategies-freqtrade

# 🤖 Freqtrade - Buy Low Sell High Bot

Este repositório fornece um **bot de trading automático** para negociação de criptomoedas, utilizando a estratégia **"Buy Low, Sell High"**. O bot é baseado no [Freqtrade](https://www.freqtrade.io/) e roda dentro de um **container Docker**, facilitando a instalação e execução.

## 🚀 Recursos do Bot

✅ **Automatiza compras e vendas** com base na estratégia "Buy Low, Sell High".\
✅ **Rodando em Docker**, sem necessidade de instalar dependências manualmente.\
✅ **Suporte a Paper Trading**, permitindo testar a estratégia sem arriscar dinheiro real.\
✅ **Backtesting** para testar o desempenho histórico da estratégia.\
✅ **Configuração fácil**, com um arquivo `config.json` pronto para uso.

---

## 📂 Estrutura do Projeto

```
freqtrade-buy-low-sell-high/
│── docker-compose.yml   # Arquivo de configuração do Docker
│── Dockerfile           # Arquivo que define a imagem Docker
│── install.sh           # Script de instalação automatizada
│── .env                 # Arquivo para armazenar credenciais de forma segura
│── config.json          # Configuração do bot
│── user_data/           # Pasta com dados do bot
│   ├── strategies/      # Pasta com as estratégias
│   │   ├── BuyLowSellHigh.py  # Arquivo com a estratégia do bot
│── README.md            # Este arquivo com as instruções detalhadas
```

---

## 🛠️ Instalação e Configuração

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seu-usuario/freqtrade-buy-low-sell-high.git
cd freqtrade-buy-low-sell-high
```

### 2️⃣ Executar o script de instalação

Este script instalará **Docker e Docker Compose**, criará a imagem do bot e iniciará o container automaticamente.

```bash
bash install.sh
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

#### **Configurar a API Key no Bot Usando .env**
Para manter suas credenciais seguras, crie um arquivo chamado `.env` na raiz do projeto e adicione suas chaves:

```ini
BINANCE_API_KEY=SUA_API_KEY
BINANCE_SECRET_KEY=SUA_SECRET_KEY
```

Depois, edite o arquivo `config.json` para carregar essas variáveis em tempo de execução:

```json
{
    "exchange": {
        "name": "binance",
        "key": "${BINANCE_API_KEY}",
        "secret": "${BINANCE_SECRET_KEY}",
        "pair_whitelist": ["BTC/USDT"]
    },
    "dry_run": true
}
```

> 🔹 O `dry_run` está ativado por padrão para evitar perdas. Para operar no modo real, altere `"dry_run": false`.

Agora, antes de rodar o bot, **carregue as variáveis do .env** com o seguinte comando:

```bash
export $(grep -v '^#' .env | xargs)
```

Isso garantirá que as credenciais sejam carregadas corretamente sem ficarem expostas no código-fonte.

---

## ▶️ Como Rodar o Bot

### **Rodar o bot em modo simulação (Paper Trading)**

```bash
docker-compose up -d
```

### **Rodar o bot no modo real** (após configurar a API Key)

```bash
docker-compose up -d
```

### **Verificar os logs do bot**

```bash
docker logs -f freqtrade_bot
```

### **Parar o bot**

```bash
docker-compose down
```

---

## 🔍 Testando a Estratégia com Backtesting

Antes de operar com dinheiro real, é essencial testar a estratégia com dados históricos. Para isso, rode:

```bash
docker run --rm -v $(pwd):/freqtrade freqtradeorg/freqtrade:stable backtest --strategy BuyLowSellHigh --config config.json --datadir user_data/data/
```

Isso gerará um relatório mostrando:

- Retorno total da estratégia
- Número de trades executados
- Percentual de trades lucrativos
- Drawdown máximo (risco de perda)

> 🧠 **Dica**: Se os resultados forem ruins, tente ajustar os parâmetros da estratégia.

---

## 🛡️ Medidas de Segurança

🔒 **Nunca ative retiradas na API Key** – Isso impede que fundos sejam roubados caso sua chave vaze.\
💰 **Use stop-loss e trailing stop** – Para limitar perdas e proteger lucros.\
🛠️ **Teste sempre em modo Paper Trading primeiro** – Antes de usar dinheiro real.\
📊 **Acompanhe os resultados e faça ajustes** – O mercado muda, e sua estratégia pode precisar ser otimizada.

---

## 📌 Contribuindo

Se quiser sugerir melhorias ou relatar bugs, abra um **issue** ou envie um **pull request**.

---

## 🎯 Conclusão

Este projeto facilita o uso do **Freqtrade** para implementar a estratégia "Buy Low, Sell High", com instalação automatizada via Docker e configurações prontas.

📈 **Bons trades e sucesso nos investimentos! 🚀**

