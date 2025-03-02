FROM freqtradeorg/freqtrade:stable

WORKDIR /freqtrade

COPY --chown=ftuser:ftuser config.json config.json
COPY --chown=ftuser:ftuser user_data/strategies user_data/strategies
COPY --chown=ftuser:ftuser .env .env

RUN chmod -R 777 /freqtrade/user_data \
    && pip install --no-cache-dir -r requirements.txt || true

# A imagem base já faz ENTRYPOINT ["freqtrade"]
# Então precisamos passar APENAS o subcomando no CMD:
CMD ["trade", "--config", "/freqtrade/config.json", "--strategy", "BuyLowSellHigh"]
