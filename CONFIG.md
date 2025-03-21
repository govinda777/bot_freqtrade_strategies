
# How to Configure Freqtrade

## 1. Parâmetros Gerais

- **"$schema"**  
  Define a URL do schema JSON que valida a configuração. Isso ajuda a garantir que o arquivo siga o formato esperado pela ferramenta.  
  **Exemplo:**  
  ```json
  "$schema": "https://schema.freqtrade.io/schema.json"
  ```

- **"max_open_trades"**  
  Limita o número máximo de operações simultâneas que o bot pode manter abertas. Um valor de 3 significa que o bot só pode ter três posições abertas ao mesmo tempo.  
  **Exemplo de utilização:**  
  Se você deseja reduzir o risco em mercados voláteis, pode diminuir esse valor para 1 ou 2.

- **"stake_currency"**  
  Define a moeda que será usada para realizar os trades, por exemplo, "USDT".  
  **Exemplo de utilização:**  
  ```json
  "stake_currency": "USDT"
  ```

- **"stake_amount"**  
  Especifica o valor (em stake_currency) a ser utilizado em cada operação. No exemplo, 10 USDT por trade.  
  **Exemplo de utilização:**  
  Se você quiser investir mais por trade, pode aumentar esse valor (ex.: 20 ou 50).

- **"tradable_balance_ratio"**  
  Representa a fração do saldo disponível que será considerada para realizar trades. Um valor de 0.99 indica que 99% do saldo pode ser utilizado.  
  **Exemplo de utilização:**  
  Para reduzir riscos, você pode diminuir esse valor para, por exemplo, 0.95.

- **"fiat_display_currency"**  
  Define a moeda fiat que será usada para exibir os resultados (ex.: "USD").  
  **Exemplo de utilização:**  
  Caso você queira visualizar os resultados em Euro, altere para "EUR".

- **"timeframe"**  
  Determina o período dos candles utilizados na estratégia. Aqui está configurado como "5m" (5 minutos).  
  **Exemplo de utilização:**  
  Para estratégias de curto prazo, pode ser "1m" ou "15m". Para longos prazos, "1h" ou "4h".

- **"dry_run"**  
  Quando definido como `true`, o bot opera em modo simulação (paper trading), sem executar ordens reais.  
  **Exemplo de utilização:**  
  Durante testes e otimizações, mantenha `"dry_run": true` e, para operar no mercado real, altere para `false`.

- **"cancel_open_orders_on_exit"**  
  Se `true`, o bot cancela ordens abertas quando sai (útil para evitar ordens pendentes em situações inesperadas). No exemplo, está definido como `false`.

- **"strategy"**  
  Nome da estratégia a ser utilizada, neste caso, `"CombinedBinHAndCluc"`.  
  **Exemplo de utilização:**  
  Você pode ter diversas estratégias (cada uma em um arquivo Python) e escolher qual executar modificando esse parâmetro.

---

## 2. Configuração de Timeouts e Precificação

- **"unfilledtimeout"**  
  Define o tempo limite para que ordens de entrada ou saída não preenchidas sejam canceladas.  
  - **"entry" e "exit"**: Tempo (em unidades definidas) antes de cancelar uma ordem de entrada ou saída.  
  - **"exit_timeout_count"**: Número de vezes que um timeout de saída pode ocorrer antes de uma ação extra (como forçar a saída).  
  - **"unit"**: Unidade de tempo utilizada (aqui, "minutes").  
  **Exemplo de utilização:**  
  Se o mercado estiver muito volátil, você pode aumentar o tempo limite para 15 minutos.

- **"entry_pricing"** e **"exit_pricing"**  
  Configuram como o bot define o preço de entrada e saída das operações.  
  - **"price_side"**: Define se o preço será "same" (mesmo do mercado) ou pode haver ajustes (como melhor preço ou pior preço).  
  - **"use_order_book"**: Indica se o bot deve utilizar dados do livro de ofertas para definir o preço.  
  - **"order_book_top"**: Quantidade de níveis do order book a serem considerados.  
  - **"price_last_balance"**: Pode ser utilizado para ajustar o preço com base no último saldo (geralmente 0.0 para não alterar).  
  - **"check_depth_of_market"**: Parâmetros adicionais para checar a profundidade do mercado, como a diferença entre bids e asks.  
  **Exemplo de utilização (entrada):**  
  Se você deseja confirmar o preço de entrada com base nos primeiros 5 níveis do order book, defina `"order_book_top": 5` e altere `"use_order_book": true` se for apropriado.  
  **Exemplo de utilização (saída):**  
  Para ter um preço de saída mais preciso, pode usar `"use_order_book": true` e considerar somente o primeiro nível (`"order_book_top": 1`).

---

## 3. Configuração da Exchange

Dentro da seção **"exchange"**:

- **"name"**  
  Nome da exchange utilizada, por exemplo, `"binance"`.  
- **"key" e "secret"**  
  Chaves de API que são carregadas de variáveis de ambiente (exemplo: `${BINANCE_API_KEY}`).  
- **"ccxt_config" e "ccxt_async_config"**  
  Permitem configurações específicas para a biblioteca CCXT, que o Freqtrade utiliza para interagir com a exchange.  
- **"pair_whitelist"**  
  Lista de pares que o bot está autorizado a negociar, por exemplo, ["BTC/USDT", "ETH/USDT", ...].  
- **"pair_blacklist"**  
  Permite excluir determinados pares (usando regex), por exemplo, excluir todos os pares que começam com "BNB/".  
  **Exemplo de utilização:**  
  Se você deseja negociar apenas pares estáveis, pode configurar a whitelist com os ativos desejados e usar a blacklist para excluir aqueles com baixa liquidez.

---

## 4. Outras Configurações

- **"pairlists"**  
  Define o método de seleção dos pares. No exemplo, é utilizado o método `"StaticPairList"`, que usa uma lista fixa.  
  **Exemplo de utilização:**  
  Você pode usar outros métodos, como `"VolumePairList"`, se quiser selecionar os pares com maior volume.

- **"telegram"**  
  Configuração para integração com o Telegram.  
  - **"enabled"**: Se o envio de alertas pelo Telegram está ativado (aqui está `false`).  
  - **"token" e "chat_id"**: Dados necessários para a autenticação e envio de mensagens.  
  **Exemplo de utilização:**  
  Para receber notificações dos trades, ative o Telegram definindo `"enabled": true` e configure os valores corretos para `"token"` e `"chat_id"`.

- **"api_server"**  
  Configuração do servidor de API para monitoramento e controle do bot.  
  - **"enabled"**: Se o servidor está ativo.  
  - **"listen_ip_address" e "listen_port"**: IP e porta para acesso à API.  
  - **"verbosity"**: Nível de verbosidade dos logs (aqui, "error" para somente erros).  
  - **"jwt_secret_key"**: Chave para autenticação JWT.  
  - **"CORS_origins"**: Lista de origens permitidas para CORS.  
  - **"username" e "password"**: Credenciais para acessar a API.  
  **Exemplo de utilização:**  
  Se você deseja que a API esteja acessível apenas na sua rede local, pode restringir o `"listen_ip_address"` para "127.0.0.1".

- **"bot_name"**  
  Nome dado ao bot, útil para identificação em logs e monitoramento.

- **"initial_state"**  
  Estado inicial do bot ao ser iniciado (ex.: `"running"`).

- **"force_entry_enable"**  
  Permite forçar a entrada mesmo que não haja sinal conforme outros filtros (aqui, está `false`).

- **"internals"**  
  Configurações internas, como o `"process_throttle_secs"`, que define quantos segundos o bot espera entre execuções de processos internos.  
  **Exemplo de utilização:**  
  Se o seu ambiente for mais lento, você pode aumentar esse valor para evitar sobrecarga.

---

## Exemplo Completo de Uso

Imagine que você queira testar sua estratégia com papel trading e apenas operar nos pares "BTC/USDT" e "ETH/USDT". Sua configuração poderia ser ajustada da seguinte forma:

```json
{
    "$schema": "https://schema.freqtrade.io/schema.json",
    "max_open_trades": 2,
    "stake_currency": "USDT",
    "stake_amount": 20,
    "tradable_balance_ratio": 0.95,
    "fiat_display_currency": "USD",
    "timeframe": "5m",
    "dry_run": true,
    "cancel_open_orders_on_exit": true,
    "strategy": "CombinedBinHAndCluc",
    "unfilledtimeout": {
        "entry": 15,
        "exit": 15,
        "exit_timeout_count": 0,
        "unit": "minutes"
    },
    "entry_pricing": {
        "price_side": "same",
        "use_order_book": true,
        "order_book_top": 3,
        "price_last_balance": 0.0,
        "check_depth_of_market": {
            "enabled": false,
            "bids_to_ask_delta": 1
        }
    },
    "exit_pricing": {
        "price_side": "same",
        "use_order_book": true,
        "order_book_top": 1
    },
    "exchange": {
        "name": "binance",
        "key": "${BINANCE_API_KEY}",
        "secret": "${BINANCE_SECRET_KEY}",
        "ccxt_config": {},
        "ccxt_async_config": {},
        "pair_whitelist": [
            "BTC/USDT", "ETH/USDT"
        ],
        "pair_blacklist": []
    },
    "pairlists": [
        {"method": "StaticPairList"}
    ],
    "telegram": {
        "enabled": true,
        "token": "seu_token_telegram",
        "chat_id": "seu_chat_id"
    },
    "api_server": {
        "enabled": true,
        "listen_ip_address": "127.0.0.1",
        "listen_port": 8080,
        "verbosity": "error",
        "jwt_secret_key": "sua_chave_secreta_jwt",
        "CORS_origins": ["*"],
        "username": "usuario",
        "password": "senha"
    },
    "bot_name": "freqtrade",
    "initial_state": "running",
    "force_entry_enable": false,
    "internals": {
        "process_throttle_secs": 5
    }
}
```

Neste exemplo, reduzimos o número máximo de trades para 2, aumentamos o stake_amount para 20 USDT por trade, e ajustamos os timeouts para 15 minutos. Também ativamos notificações pelo Telegram e restringimos a API para a máquina local.


## Nível de Exposição

### Parâmetros que Afetam o Nível de Exposição

A exposição (nível de risco) do bot pode ser ajustada por diversos parâmetros na configuração. Abaixo estão alguns dos principais parâmetros que afetam esse nível, com exemplos para três perfis de exposição: **Conservador**, **Moderado** e **Ousado**.

---

### Parâmetros que Afetam o Nível de Exposição

1. **max_open_trades**  
   - **Impacto:** Define o número máximo de trades simultâneos.  
   - **Peso:** Mais trades abertos podem aumentar a exposição e o risco agregado, pois múltiplas operações estão sujeitas a oscilações do mercado.

2. **stake_amount**  
   - **Impacto:** Valor investido por trade.  
   - **Peso:** Um valor maior implica um risco financeiro mais elevado por operação.

3. **tradable_balance_ratio**  
   - **Impacto:** Proporção do saldo total utilizado para trading.  
   - **Peso:** Quanto maior o ratio, maior a parte do capital está exposta ao mercado.

4. **stoploss (definido na estratégia)**  
   - **Impacto:** Percentual máximo de perda permitida por trade.  
   - **Peso:** Um stoploss mais apertado protege contra grandes perdas, mas pode gerar saídas prematuras; um stoploss mais largo pode aumentar o risco.

---

### Exemplos de Configurações de Exposição

#### 1. Perfil Conservador

```json
{
    // Limita a exposição: somente uma operação de cada vez
    "max_open_trades": 1, // Apenas 1 trade simultâneo reduz o risco agregado.
    // Valor menor investido por operação, minimizando perdas em caso de erro.
    "stake_amount": 5, // Investindo 5 USDT por trade, o risco financeiro individual é menor.
    // Utiliza uma fração menor do saldo total para evitar sobreposição de riscos.
    "tradable_balance_ratio": 0.5, // Somente 50% do saldo total é usado, garantindo reserva.
    // Na estratégia, um stoploss mais apertado para limitar perdas
    // (Exemplo na estratégia: stoploss de -0.02)
    "strategy_stoploss": -0.02
}
```

> **Comentário:**  
> Essa configuração é indicada para investidores que preferem segurança e menor volatilidade. Com apenas um trade ativo e investimentos menores, o risco total fica reduzido mesmo em caso de movimentos adversos no mercado.

---

#### 2. Perfil Moderado

```json
{
    // Permite duas operações simultâneas, aumentando a exposição de forma controlada.
    "max_open_trades": 2, // A duplicação das trades permite aproveitar mais oportunidades, mas com risco controlado.
    // Valor moderado investido por operação.
    "stake_amount": 10, // 10 USDT por trade, equilíbrio entre potencial de lucro e risco.
    // Maior proporção do saldo é utilizada, mas ainda mantendo uma reserva.
    "tradable_balance_ratio": 0.75, // Utiliza 75% do saldo, aumentando a exposição sem comprometer totalmente o capital.
    // Stoploss moderado, permitindo uma certa oscilação sem sair rapidamente do trade.
    "strategy_stoploss": -0.05
}
```

> **Comentário:**  
> Configuração ideal para quem busca um equilíbrio entre segurança e rentabilidade. Aumenta a exposição comparada ao perfil conservador, mas mantém limites para controlar as perdas.

---

#### 3. Perfil Ousado

```json
{
    // Permite até três operações simultâneas, maximizando a exposição.
    "max_open_trades": 3, // Maior número de trades permite capturar mais oportunidades, mas eleva o risco total.
    // Investimento maior por operação para maximizar os lucros potenciais.
    "stake_amount": 15, // 15 USDT por trade, visando maior retorno, com risco proporcional.
    // Quase todo o saldo disponível é utilizado, sem muita reserva.
    "tradable_balance_ratio": 0.99, // Quase 100% do saldo é utilizado, aumentando significativamente a exposição.
    // Stoploss mais amplo para permitir maior oscilação de mercado sem fechar o trade, mas com risco elevado.
    "strategy_stoploss": -0.08
}
```

> **Comentário:**  
> Esta configuração é para investidores com alta tolerância a riscos e que buscam potencializar os ganhos, mesmo sabendo que as perdas podem ser maiores. O maior número de trades e o alto stake aumentam a exposição, assim como a utilização quase total do saldo.

---

### Conclusão

Cada um desses parâmetros (max_open_trades, stake_amount, tradable_balance_ratio e stoploss) possui um peso importante na definição do risco total do bot. Ao ajustar esses valores, o investidor pode calibrar seu nível de exposição de acordo com seu perfil:
- **Conservador:** Menor número de operações e investimentos menores para minimizar riscos.
- **Moderado:** Exposição intermediária, equilibrando riscos e oportunidades.
- **Ousado:** Maior exposição com potencial de altos ganhos, mas com risco elevado.
