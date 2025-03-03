# 📊 Backtesting da Estratégia "Buy Low, Sell High" no Freqtrade


docker exec -it freqtrade_bot freqtrade download-data --days 60 -p BTC/USDT -t 5m

docker exec -it freqtrade_bot freqtrade hyperopt --strategy BuyLowSellHigh --spaces roi stoploss trailing --timerange 20250201-20250301 --hyperopt-loss SharpeHyperOptLoss --epochs 70 --job-workers 3

docker exec -it freqtrade_bot freqtrade backtesting --strategy BuyLowSellHigh --timerange 20250102-20250301 --export trades

---

# 📊 Backtesting da Estratégia "Buy Low, Sell High" no Freqtrade

Este guia explica como realizar um **backtesting** no Freqtrade para avaliar o desempenho da estratégia **"Buy Low, Sell High"** com dados históricos.

---

## 🛠️ **Pré-requisitos**
Antes de iniciar o backtesting, certifique-se de:

- Ter o **Freqtrade** instalado e configurado.
- Ter o bot rodando em um container Docker.
- Possuir dados históricos baixados para o par desejado.

Caso ainda não tenha os dados históricos, siga as instruções na seção [Baixando Dados Históricos](#baixando-dados-históricos).

---

## 📥 **Baixando Dados Históricos**
Para garantir que o backtesting tenha dados suficientes, execute o seguinte comando:

```bash
docker exec -it freqtrade_bot freqtrade download-data --days 60 -p BTC/USDT -t 5m
```

Esse comando baixa **60 dias** de histórico para o par **BTC/USDT** no timeframe **5m** (5 minutos).

Caso queira apagar os dados anteriores e baixar novamente:

```bash
docker exec -it freqtrade_bot freqtrade download-data --days 60 -p BTC/USDT -t 5m --erase
```

Para verificar se os dados foram baixados corretamente:

```bash
docker exec -it freqtrade_bot freqtrade list-data
```

Se os dados aparecerem na lista, você está pronto para o backtesting.

---

## 🏆 **Executando o Backtesting**
Agora que os dados históricos estão baixados, execute o seguinte comando para rodar o backtesting:

```bash

docker exec -it freqtrade_bot freqtrade hyperopt --strategy BuyLowSellHigh --spaces roi stoploss trailing --timerange 20250102-20250301 --hyperopt-loss SharpeHyperOptLoss

docker exec -it freqtrade_bot freqtrade hyperopt --strategy BuyLowSellHigh --spaces roi stoploss trailing --timerange 20250201-20250301 --hyperopt-loss SharpeHyperOptLoss --epochs 70 --job-workers 1

```

Esse comando:
- **Usa a estratégia** `BuyLowSellHigh.py` localizada em `user_data/strategies/`
- **Executa o backtesting** entre **2025-01-02** e **2025-03-01**

Caso queira testar um período menor, utilize:

```bash
docker exec -it freqtrade_bot freqtrade backtesting --strategy BuyLowSellHigh --timerange 20250201-20250301
```

Se os dados estiverem corretos, você verá um **relatório completo** com:
- Total de trades executados
- Lucro ou prejuízo percentual
- Tempo médio dos trades
- Win rate (% de trades vencedores)
- Drawdown (risco da estratégia)

---

## 📊 **Analisando os Resultados**
Depois do backtesting, o Freqtrade gera um **relatório resumido** no terminal. Para salvar os resultados e analisá-los posteriormente, execute:

```bash
docker exec -it freqtrade_bot freqtrade backtesting --strategy BuyLowSellHigh --timerange 20250102-20250301 --export trades
```

Os resultados ficarão salvos na pasta:

```
/freqtrade/user_data/backtest_results/
```

Para copiar os arquivos para sua máquina local:

```bash
docker cp freqtrade_bot:/freqtrade/user_data/backtest_results/ ./backtest_results/
```

---

## 📉 **Gerando Gráficos**
Você pode visualizar os trades executados no histórico de preços com um gráfico interativo:

```bash
docker exec -it freqtrade_bot freqtrade plot-data --timerange 20250102-20250301 --export trades
```

Ou gerar um gráfico detalhado do backtesting:

```bash
docker exec -it freqtrade_bot freqtrade plot-backtest --strategy BuyLowSellHigh --timerange 20250102-20250301
```

Os gráficos serão salvos na pasta:

```
/freqtrade/user_data/plot/
```

Para copiá-los para sua máquina local:

```bash
docker cp freqtrade_bot:/freqtrade/user_data/plot/ ./plot_results/
```

Agora você pode abrir os arquivos e analisar os trades graficamente!

---

## ✅ **Conclusão**
Com este guia, você pode:
- Baixar dados históricos 📥
- Rodar o backtesting da estratégia 🎯
- Exportar os resultados 📊
- Gerar gráficos para análise visual 📉

Caso precise ajustar a estratégia, edite o arquivo `BuyLowSellHigh.py` e rode o backtesting novamente.

Bons testes e boas operações! 🚀

