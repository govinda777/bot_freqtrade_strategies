FROM freqtradeorg/freqtrade:stable

WORKDIR /freqtrade

# Copia os arquivos com permissões adequadas
COPY --chown=ftuser:ftuser config.json config.json
COPY --chown=ftuser:ftuser user_data/strategies user_data/strategies
COPY --chown=ftuser:ftuser .env .env

# Ajusta permissões e instala dependências (se necessário)
RUN chmod -R 777 /freqtrade/user_data \
    && pip install --no-cache-dir -r requirements.txt || true

# Definir o comando padrão no Dockerfile
CMD ["trade", "--config", "/freqtrade/config.json", "--strategy", "CombinedBinHAndCluc"]
