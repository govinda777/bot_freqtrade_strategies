FROM freqtradeorg/freqtrade:stable

WORKDIR /freqtrade

# Copia os arquivos com permissões adequadas
COPY --chown=ftuser:ftuser config.json config.json
COPY --chown=ftuser:ftuser user_data/strategies user_data/strategies
COPY --chown=ftuser:ftuser .env .env

# Ajusta permissões e instala dependências (se necessário)
RUN chmod -R 777 /freqtrade/user_data \
    && pip install --no-cache-dir -r requirements.txt || true

# Definir variável de ambiente para a estratégia (padrão se não for especificada)
ENV FREQTRADE_STRATEGY="CombinedBinHAndCluc"

# Habilitar a interface web do Freqtrade
ENV FREQTRADE_UI="1"

# Expor a porta para a interface web
EXPOSE 8080

# Usar a variável de ambiente para definir a estratégia e iniciar o servidor web
CMD ["sh", "-c", "freqtrade trade --config /freqtrade/config.json --strategy ${FREQTRADE_STRATEGY} --enable-inotify"]