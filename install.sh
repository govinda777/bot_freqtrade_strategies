#!/bin/bash

echo "📥 Instalando Docker e Docker Compose..."

# Verifica e instala o Docker se não estiver presente
if ! command -v docker &> /dev/null
then
    echo "🔧 Instalando Docker..."
    curl -fsSL https://get.docker.com | bash
fi

# Verifica e instala o Docker Compose se não estiver presente
if ! command -v docker-compose &> /dev/null
then
    echo "🔧 Instalando Docker Compose..."
    sudo apt install docker-compose -y
fi

# Verifica se o arquivo .env existe
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado! Criando um modelo..."
    cat <<EOT >> .env
BINANCE_API_KEY=SUA_API_KEY
BINANCE_SECRET_KEY=SUA_SECRET_KEY
EOT
    echo "⚠️  Atualize o arquivo .env com suas credenciais antes de iniciar o bot!"
    exit 1
fi

echo "🚀 Construindo a imagem do bot..."
docker-compose build

echo "📂 Criando container e rodando o bot..."
docker-compose up -d

echo "✅ Instalação completa! O bot está rodando no Docker."

echo "📌 Para verificar os logs do bot, execute:"
echo "   docker logs -f freqtrade_bot"
