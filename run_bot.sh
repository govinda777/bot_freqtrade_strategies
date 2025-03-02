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

# 🚀 Passo 2: Construir a imagem novamente
echo "⚙️  Construindo a imagem Docker..."
docker-compose build

# 🚀 Passo 3: Identificar o nome correto da imagem gerada
IMAGE_NAME=$(docker images --format "{{.Repository}}" | grep 'bot_freqtrade_strategies' | head -n 1)

if [ -z "$IMAGE_NAME" ]; then
    echo "❌ ERRO: A imagem Docker 'bot_freqtrade_strategies' não foi encontrada. Algo deu errado no build."
    echo "🔎 Imagens disponíveis:"
    docker images
    exit 1
fi

echo "✅ Imagem Docker encontrada: $IMAGE_NAME"

# 🚀 Passo 4: Iniciar o container temporário para validação
echo "🚀 Iniciando o container temporário para validação..."
docker run --name temp_freqtrade -d $IMAGE_NAME /bin/sh -c "while true; do sleep 30; done"

# 🚀 Passo 5: Verificar arquivos dentro do container
echo "🔎 Validando arquivos dentro do Docker..."
docker exec temp_freqtrade ls -l /freqtrade/config.json /freqtrade/user_data/strategies/BuyLowSellHigh.py

# Exibir permissões e dono do arquivo dentro do container
echo "🔍 Exibindo permissões e dono do arquivo de estratégia..."
docker exec temp_freqtrade ls -l /freqtrade/user_data/strategies/

# Testar a acessibilidade do arquivo de estratégia
echo "🔍 Testando permissões de leitura e escrita..."
docker exec temp_freqtrade sh -c "touch /freqtrade/user_data/strategies/testfile && rm /freqtrade/user_data/strategies/testfile" \
    && echo "✅ Permissão de escrita OK" || echo "❌ ERRO: Sem permissão de escrita em /freqtrade/user_data/strategies"

# Verificação individual dos arquivos esperados
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

# 🚀 Passo 6: Parar e remover o container temporário após a validação
echo "🧹 Removendo container temporário..."
docker stop temp_freqtrade && docker rm temp_freqtrade

# 🚀 Passo 7: Iniciar o container normalmente
echo "🚀 Iniciando o bot Freqtrade..."
docker-compose up -d

echo "✅ Bot iniciado com sucesso!"
echo "📌 Para verificar os logs, execute: docker logs -f freqtrade_bot"
