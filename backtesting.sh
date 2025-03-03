#!/bin/bash

# Definir variáveis
CONTAINER_NAME="freqtrade_bot"
STRATEGY_NAME="BuyLowSellHigh"
TIMEFRAME="5m"
PAIRS="BTC/USDT"
DAYS=60
EPOCHS=50
TIMERANGE_HYPEROPT="20250201-20250301"
TIMERANGE_BACKTEST="20250102-20250301"
BACKTEST_LOG="backtest_result.log"

# 🔹 1) Parar e reiniciar o bot (sem exibir logs)
echo "🛑 Parando o bot..."
./stop_bot.sh > /dev/null 2>&1

echo "🚀 Reiniciando o bot..."
./run_bot.sh > /dev/null 2>&1

# 🔹 2) Aguardar o container iniciar completamente antes de prosseguir
echo "⏳ Aguardando o container '$CONTAINER_NAME' iniciar..."
ATTEMPTS=10
while ! docker ps | grep -q "$CONTAINER_NAME"; do
    sleep 5
    ((ATTEMPTS--))
    if [ $ATTEMPTS -le 0 ]; then
        echo "❌ Erro: O container '$CONTAINER_NAME' não iniciou corretamente."
        exit 1
    fi
done
echo "✅ Container '$CONTAINER_NAME' está rodando."

# 🔹 3) Baixar os dados mais recentes
echo "📥 Baixando dados de mercado ($DAYS dias, timeframe $TIMEFRAME)..."
docker exec $CONTAINER_NAME freqtrade download-data --days $DAYS -p $PAIRS -t $TIMEFRAME > /dev/null 2>&1

# 🔹 4) Rodar Hyperopt para otimizar parâmetros
echo "📊 Executando Hyperopt (epochs: $EPOCHS)..."
docker exec $CONTAINER_NAME freqtrade hyperopt --strategy $STRATEGY_NAME \
    --spaces roi stoploss trailing --timerange $TIMERANGE_HYPEROPT \
    --hyperopt-loss SharpeHyperOptLoss --epochs $EPOCHS --job-workers 1 > /dev/null 2>&1

# 🔹 5) Rodar Backtesting e salvar o resultado no log
echo "🔍 Executando Backtesting e salvando resultados em '$BACKTEST_LOG'..."
docker exec $CONTAINER_NAME freqtrade backtesting --strategy $STRATEGY_NAME \
    --timerange $TIMERANGE_BACKTEST --export trades > "$BACKTEST_LOG" 2>&1

echo "✅ Teste concluído! Resultados salvos em '$BACKTEST_LOG'."
