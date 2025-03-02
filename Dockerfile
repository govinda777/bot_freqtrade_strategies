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

# Executar o bot corretamente
CMD ["bash", "-c", "source /freqtrade/.env && freqtrade trade --config /freqtrade/config.json --strategy BuyLowSellHigh"]
