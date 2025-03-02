# Usar a imagem oficial do Freqtrade
FROM freqtradeorg/freqtrade:stable

# Define o diretório de trabalho dentro do container
WORKDIR /freqtrade

# Copia os arquivos de configuração e estratégia para o container
COPY config.json /freqtrade/config.json
COPY user_data/strategies/BuyLowSellHigh.py /freqtrade/user_data/strategies/BuyLowSellHigh.py
COPY .env /freqtrade/.env

# Instala dependências adicionais, se necessário
RUN pip install --no-cache-dir -r /freqtrade/requirements.txt || true

# Carregar variáveis de ambiente e rodar o bot
CMD ["sh", "-c", "export $(grep -v '^#' .env | xargs) && freqtrade trade --config config.json --strategy BuyLowSellHigh"]
