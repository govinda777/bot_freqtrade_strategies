#!/bin/bash

echo "🛑 Parando o bot Freqtrade..."

# Verifica se o container do bot está rodando
if docker ps | grep -q "freqtrade_bot"; then
    docker-compose down
    echo "✅ Bot parado com sucesso!"
else
    echo "⚠️  O bot não está em execução."
fi
