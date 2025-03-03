#!/bin/bash

# Nome do container
CONTAINER_NAME="freqtrade_bot"

# Caminhos esperados dentro do container
CONFIG_FILE="/freqtrade/config.json"
STRATEGY_FILE="/freqtrade/user_data/strategies/BuyLowSellHigh.py"

# 🚀 Passo 1: Parar o container se estiver rodando
echo "🔄 Parando o container existente..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# 🚀 Passo 2: Exportar variáveis de ambiente
echo "🔍 Exportando variáveis de ambiente..."
export $(grep -v '^#' .env | xargs)

# 🔍 Verificação de variáveis críticas
if [[ -z "$BINANCE_API_KEY" || -z "$BINANCE_SECRET_KEY" || -z "$FREQTRADE_USERNAME" || -z "$FREQTRADE_PASSWORD" || -z "$JWT_SECRET_KEY" ]]; then
    echo "❌ ERRO: Algumas variáveis de ambiente não estão definidas! Verifique o arquivo .env."
    exit 1
else
    echo "✅ Variáveis de ambiente carregadas corretamente."
fi

# 🚀 Passo 3: Construir a imagem novamente
echo "⚙️  Construindo a imagem Docker..."
docker-compose build --no-cache

# 🚀 Passo 4: Identificar o nome correto da imagem gerada
IMAGE_NAME=$(docker images --format "{{.Repository}}" | grep 'bot_freqtrade_strategies' | head -n 1)

if [ -z "$IMAGE_NAME" ]; then
    echo "❌ ERRO: A imagem Docker 'bot_freqtrade_strategies' nao foi encontrada. Algo deu errado no build."
    echo "🔎 Imagens disponiveis:"
    docker images
    exit 1
fi

echo "✅ Imagem Docker encontrada: $IMAGE_NAME"

# 🚀 Passo 5: Iniciar o container temporário para validação
echo "🚀 Iniciando o container temporário para validação..."
docker run --name temp_freqtrade -d $IMAGE_NAME /bin/sh -c "while true; do sleep 30; done"

# 🔎 Validando arquivos dentro do Docker
echo "🔎 Validando arquivos dentro do Docker..."
docker exec temp_freqtrade ls -l $CONFIG_FILE $STRATEGY_FILE

echo "🔍 Exibindo permissões e dono do arquivo de estratégia..."
docker exec temp_freqtrade ls -lah /freqtrade/user_data/strategies/

echo "🔍 Ajustando permissões no container..."
docker exec temp_freqtrade sh -c "chown -R ftuser:ftuser /freqtrade/user_data/strategies && chmod -R 777 /freqtrade/user_data/strategies"

echo "🔍 Testando permissões de leitura e escrita..."
docker exec temp_freqtrade sh -c "touch /freqtrade/user_data/strategies/testfile && rm /freqtrade/user_data/strategies/testfile" \
    && echo "✅ Permissão de escrita OK" || echo "❌ ERRO: Sem permissão de escrita em /freqtrade/user_data/strategies"

if docker exec temp_freqtrade test -f $CONFIG_FILE; then
    echo "✅ Configuração encontrada: $CONFIG_FILE"
else
    echo "❌ ERRO: Arquivo de configuração não encontrado: $CONFIG_FILE"
    docker stop temp_freqtrade && docker rm temp_freqtrade
    exit 1
fi

if docker exec temp_freqtrade test -f $STRATEGY_FILE; then
    echo "✅ Estratégia encontrada: $STRATEGY_FILE"
else
    echo "❌ ERRO: Arquivo da estratégia não encontrado: $STRATEGY_FILE"
    docker stop temp_freqtrade && docker rm temp_freqtrade
    exit 1
fi

# 🚀 Passo 6: Removendo container temporário
echo "🪚 Removendo container temporário..."
docker stop temp_freqtrade && docker rm temp_freqtrade

# 🚀 Passo 7: Iniciar o bot
echo "🚀 Iniciando o bot Freqtrade..."
docker-compose up -d

echo "✅ Bot iniciado com sucesso!"

echo "🔎 Validando permissões finais..."
if docker exec -it freqtrade_bot ls -lah /freqtrade/user_data/strategies; then
    echo "✅ Permissões listadas corretamente."
else
    echo "❌ ERRO: Falha ao listar permissões."
fi

if docker exec -it freqtrade_bot touch /freqtrade/user_data/strategies/testfile; then
    echo "✅ Teste de escrita bem-sucedido."
else
    echo "❌ ERRO: Sem permissão de escrita no container."
fi

echo "🔍 Exibindo conteúdo de /freqtrade/config.json dentro do container:"
docker exec -it freqtrade_bot cat /freqtrade/config.json

echo "🔎 Verificando a configuração carregada pelo Freqtrade..."
docker exec -it freqtrade_bot freqtrade show-config

echo "📂 Listando arquivos dentro de /freqtrade/ para garantir que tudo foi copiado corretamente:"
docker exec -it freqtrade_bot ls -lah /freqtrade/
docker exec -it freqtrade_bot ls -lah /freqtrade/user_data/
docker exec -it freqtrade_bot ls -lah /freqtrade/user_data/strategies/

echo "📌 Para verificar os logs, execute: docker logs -f freqtrade_bot"

echo "✅ Verificação concluída!"
