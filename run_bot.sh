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
docker-compose build --no-cache

# 🚀 Passo 3: Identificar o nome correto da imagem gerada
IMAGE_NAME=$(docker images --format "{{.Repository}}" | grep 'bot_freqtrade_strategies' | head -n 1)

if [ -z "$IMAGE_NAME" ]; then
    echo "❌ ERRO: A imagem Docker 'bot_freqtrade_strategies' nao foi encontrada. Algo deu errado no build."
    echo "🔎 Imagens disponiveis:"
    docker images
    exit 1
fi

echo "✅ Imagem Docker encontrada: $IMAGE_NAME"

# 🚀 Passo 4: Iniciar o container temporario para validacao
echo "🚀 Iniciando o container temporario para validacao..."
docker run --name temp_freqtrade -d $IMAGE_NAME /bin/sh -c "while true; do sleep 30; done"

# 🚀 Passo 5: Verificar arquivos dentro do container
echo "🔎 Validando arquivos dentro do Docker..."
docker exec temp_freqtrade ls -l $CONFIG_FILE $STRATEGY_FILE

# Exibir permissoes e dono do arquivo dentro do container
echo "🔍 Exibindo permissoes e dono do arquivo de estrategia..."
docker exec temp_freqtrade ls -lah /freqtrade/user_data/strategies/

# 🔍 Corrigindo permissoes dentro do container
echo "🔍 Ajustando permissoes no container..."
docker exec temp_freqtrade sh -c "chown -R ftuser:ftuser /freqtrade/user_data/strategies && chmod -R 777 /freqtrade/user_data/strategies"

# Testar a acessibilidade do arquivo de estrategia
echo "🔍 Testando permissoes de leitura e escrita..."
docker exec temp_freqtrade sh -c "touch /freqtrade/user_data/strategies/testfile && rm /freqtrade/user_data/strategies/testfile" \
    && echo "✅ Permissao de escrita OK" || echo "❌ ERRO: Sem permissao de escrita em /freqtrade/user_data/strategies"

# Verificacao individual dos arquivos esperados
if docker exec temp_freqtrade test -f $CONFIG_FILE; then
    echo "✅ Configuracao encontrada: $CONFIG_FILE"
else
    echo "❌ ERRO: Arquivo de configuracao nao encontrado: $CONFIG_FILE"
    docker stop temp_freqtrade && docker rm temp_freqtrade
    exit 1
fi

if docker exec temp_freqtrade test -f $STRATEGY_FILE; then
    echo "✅ Estrategia encontrada: $STRATEGY_FILE"
else
    echo "❌ ERRO: Arquivo da estrategia nao encontrado: $STRATEGY_FILE"
    docker stop temp_freqtrade && docker rm temp_freqtrade
    exit 1
fi

# 🚀 Passo 6: Parar e remover o container temporario apos a validacao
echo "🪚 Removendo container temporario..."
docker stop temp_freqtrade && docker rm temp_freqtrade

# 🚀 Passo 7: Iniciar o container normalmente
echo "🚀 Iniciando o bot Freqtrade..."
docker-compose up -d

echo "✅ Bot iniciado com sucesso!"
echo "📌 Para verificar os logs, execute: docker logs -f freqtrade_bot"

# 🔎 Validacao final de permissoes no container
echo "🔎 Validando permissoes finais..."
if docker exec -it freqtrade_bot ls -lah /freqtrade/user_data/strategies; then
    echo "✅ Permissoes listadas corretamente."
else
    echo "❌ ERRO: Falha ao listar permissoes."
fi

if docker exec -it freqtrade_bot touch /freqtrade/user_data/strategies/testfile; then
    echo "✅ Teste de escrita bem-sucedido."
else
    echo "❌ ERRO: Sem permissao de escrita no container."
fi

# 📝 Exibir conteúdo do config.json
echo "🔍 Exibindo conteúdo de /freqtrade/config.json dentro do container:"
docker exec -it freqtrade_bot cat /freqtrade/config.json

# 🔎 Verificar qual configuração o bot realmente está carregando
echo "🔎 Verificando a configuração carregada pelo Freqtrade..."
docker exec -it freqtrade_bot freqtrade show-config

# 📂 Listar **apenas** os arquivos do diretório relevante
echo "📂 Listando os arquivos dentro de /freqtrade/ para garantir que tudo foi copiado corretamente:"
docker exec -it freqtrade_bot ls -lah /freqtrade/
docker exec -it freqtrade_bot ls -lah /freqtrade/user_data/
docker exec -it freqtrade_bot ls -lah /freqtrade/user_data/strategies/


echo "✅ Verificação concluída!"
