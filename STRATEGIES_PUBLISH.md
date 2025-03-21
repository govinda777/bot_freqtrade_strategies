# Documentação do Projeto Bot Freqtrade Strategies

Esta documentação descreve o fluxo completo de criação, teste, publicação e gerenciamento de estratégias no bot Freqtrade. Ela abrange os seguintes tópicos:

- Como configurar uma estratégia
- Realização de back tests (incluindo geração de relatórios e sugestões de mudança)
- Publicação da estratégia (ex.: como transformar em um NFT)
- Validação da estratégia (performance e lucratividade)
- Sugestões de melhorias na estratégia
- Execução do bot (seleção de estratégia e entrada de dados via formulário)
- Geração de reports (rendimento, ordens em execução, vitórias, derrotas, etc.)
- Back office (gestão e escalabilidade do bot)

Cada seção a seguir explica como os passos são realizados, os arquivos e scripts envolvidos e como você pode acessá-los e configurá-los.

---

## 1. Configuração da Estratégia

### Como configurar uma estratégia

- **Localização e Estrutura:**  
  As estratégias estão armazenadas na pasta `user_data/strategies`. Cada estratégia é implementada em um arquivo Python (por exemplo, `CombinedBinHAndCluc.py`) e deve seguir a interface definida pelo Freqtrade (usando a classe `IStrategy`).  
  > No arquivo [CombinedBinHAndCluc.py](citeturn0file9) você encontra a implementação da estratégia que utiliza indicadores como Bollinger Bands e EMA para gerar sinais de entrada e saída.

- **Configuração no arquivo config.json:**  
  No arquivo `config.json` você define qual estratégia o bot deve usar, através do parâmetro `"strategy"`. Por exemplo:
  ```json
  "strategy": "CombinedBinHAndCluc"
  ```
  Essa configuração permite que, ao iniciar o bot, a estratégia especificada seja carregada.

- **Personalização dos Parâmetros:**  
  Parâmetros específicos (como stoploss, minimal_roi, timeframes e indicadores) são definidos diretamente no código da estratégia. Para modificá-los, basta editar o arquivo da estratégia conforme o seu perfil de risco e a lógica desejada.

---

## 2. Back Tests

### Realizando Back Tests e Gerando Relatórios

- **Scripts de Backtesting:**  
  O script `backtesting.sh` é responsável por:
  - Parar o bot (usando `stop_bot.sh`)
  - Reiniciar o bot (usando `run_bot.sh`)
  - Baixar dados históricos (com o comando `freqtrade download-data`)
  - Executar a otimização (Hyperopt) e o backtesting propriamente dito
  - Exportar os resultados para um arquivo de log
  > Veja o conteúdo do [backtesting.sh](citeturn0file5) para entender a sequência de comandos.

- **Relatórios e Sugestões de Mudanças:**  
  Ao executar os comandos de backtesting, o Freqtrade gera relatórios que contêm:
  - Total de trades, ROI, drawdown e outras métricas
  - O Hyperopt pode ser usado para sugerir ajustes nos parâmetros (como ROI, stoploss e trailing stop) a partir de um período de teste configurado (exemplo, timerange).
  > As configurações de timerange e parâmetros do Hyperopt estão definidas no script, permitindo ajustes finos para melhor desempenho.

---

## 3. Publicação da Estratégia (New NFT)

### Como publicar essa estratégia

- **Conceito de NFT para Estratégias:**  
  Em alguns projetos inovadores, estratégias podem ser publicadas como NFTs para registrar sua autoria e performance. No nosso projeto, a publicação pode envolver:
  - Gerar um pacote contendo o código da estratégia e os resultados históricos de backtest
  - Registrar essa estratégia em uma plataforma de NFT (ex.: mintagem via smart contract)
  - Compartilhar o NFT com investidores interessados, que podem acessar os resultados e a lógica da estratégia

- **Passos para Publicação:**
  1. **Preparar a Documentação:** Reúna os relatórios de backtest, sugestões de mudanças e a implementação da estratégia.
  2. **Criar o NFT:** Utilize uma plataforma compatível com NFTs para criar um token que representa a estratégia (incluir metadados como performance e data de publicação).
  3. **Divulgar e Comercializar:** Publique o NFT em marketplaces e compartilhe com a comunidade de investidores.
  
> Essa etapa pode variar conforme a plataforma e as regras do projeto. Não há um script específico no repositório, mas os dados gerados (por exemplo, os relatórios de backtest) servem como base para a documentação e validação.

---

## 4. Validação da Estratégia

### Como essa estratégia é validada (Performance / Lucratividade)

- **Backtesting e Hyperopt:**  
  A validação inicial é feita através de backtests usando dados históricos. Métricas avaliadas incluem:
  - Taxa de vitória (win rate)
  - ROI (Retorno sobre Investimento)
  - Drawdown (máxima queda)
  - Número total de trades e sua distribuição (vitórias x derrotas)
  > Os resultados são gerados pelos comandos do Freqtrade executados no script de backtesting ([backtesting.sh](citeturn0file5)).

- **Monitoramento em Tempo Real:**  
  Após a validação com dados históricos, a estratégia pode ser testada em modo Paper Trading (dry_run = true) para verificar sua performance em condições reais de mercado.
  
- **Critérios de Validação:**  
  A estratégia deve apresentar consistência, performance positiva e gerenciamento de riscos adequado. Se esses critérios não forem atendidos, são sugeridas alterações (revisão de parâmetros ou ajustes na lógica de entrada/saída).

---

## 5. Sugestões de Melhorias na Estratégia

### Identificando e Implementando Melhorias

- **Análise dos Relatórios:**  
  Verifique os relatórios de backtesting para identificar pontos fracos, como:
  - Alta taxa de trades perdedores
  - Drawdown elevado
  - Desempenho inconsistente em diferentes períodos
- **Ajuste de Parâmetros:**  
  Utilize o Hyperopt para sugerir modificações nos parâmetros de ROI, stoploss, trailing stop e indicadores.  
- **Testes Incrementais:**  
  Após cada alteração, execute novos backtests e valide as mudanças. Mantenha um diário de mudanças para documentar o impacto de cada ajuste.

- **Sugestões Comuns:**
  - Revisar o período e os desvios padrão das Bollinger Bands
  - Ajustar o timeframe se a estratégia estiver muito sensível a ruídos de mercado
  - Adicionar filtros adicionais (ex.: volume mínimo ou condições de mercado) para evitar falsos sinais

---

## 6. Run Bot

### Como executar o bot com a estratégia escolhida

- **Script run_bot.sh:**  
  Este script automatiza a sequência de:
  - Parar e remover qualquer container existente
  - Exportar variáveis de ambiente (carregando as chaves e credenciais do arquivo `.env`)
  - Construir a imagem Docker novamente para garantir que todas as atualizações sejam aplicadas
  - Validar que os arquivos essenciais (config.json e o arquivo da estratégia) estão disponíveis no container
  - Iniciar o container com `docker-compose up -d`
  
  > Confira o [run_bot.sh](citeturn0file8) para ver todos os passos e como as variáveis são verificadas e utilizadas.

- **Seleção da Estratégia e Dados do Formulário:**  
  Em uma interface integrada (por exemplo, um formulário web) você pode:
  - Selecionar qual estratégia executar (alterando o parâmetro `"strategy"` no config.json ou através de uma interface de seleção)
  - Inserir dados específicos (como timeframe, stake_amount, etc.)
  
  Esses dados podem ser repassados para os scripts e a configuração do bot, permitindo uma operação dinâmica.

---

## 7. Reports

### Acompanhamento e Análise de Performance

- **Métricas Monitoradas:**
  - **Rendimento (ROI):** Retorno sobre os investimentos realizados.
  - **Quantidade de Ordens em Execução:** Monitoramento em tempo real das posições abertas.
  - **Taxa de Vitórias e Derrotas:** Número de trades vencedores versus perdedores.
  - **Outras Estatísticas:** Drawdown, número de trades, tempo médio de operação, entre outras.
  
- **Acesso aos Relatórios:**
  - **Logs e Relatórios de Backtesting:** Gerados pelos scripts (como o `backtesting.sh`) e exportados para arquivos (ex.: `backtest_result.log`).
  - **API Server:** O Freqtrade disponibiliza uma API para consulta de configurações e status do bot. Acesse os dados pela API (definida no config.json em `"api_server"`) para visualizar métricas e logs em tempo real.
  
  > Para mais detalhes, veja as configurações de API em [config.json](citeturn0file15).

---

## 8. Back Office

### Gestão e Escalabilidade do Bot

- **Gerenciamento do Bot:**
  - **Monitoramento:** Utilize a API e os logs do Docker para acompanhar a performance do bot e identificar possíveis problemas.
  - **Gestão de Múltiplas Estratégias:** Se houver diversas estratégias, crie containers separados ou use uma interface central para gerenciar e alternar entre elas.
  - **Escalabilidade:** Ajuste os parâmetros do bot (como `max_open_trades` e `process_throttle_secs`) e configure balanceamento de carga se estiver operando com múltiplos containers.
  - **Atualizações e Deploy:** Utilize o script `run_bot.sh` para atualizar o container sempre que houver alterações no código ou na configuração.

- **Ferramentas de Back Office:**
  - **Docker Compose:** Para gerenciar o ciclo de vida do bot (start, stop, reinicialização).
  - **Interface Web/API:** Para visualizar relatórios, métricas e status do bot.
  - **Logs Centralizados:** Armazene e analise logs para facilitar a manutenção e a identificação de gargalos.

---

## Conclusão

Esta documentação detalha como configurar e gerenciar todas as etapas do ciclo de vida de uma estratégia no bot Freqtrade. Desde a configuração inicial e testes (backtesting) até a publicação (como NFT) e o gerenciamento em produção, cada passo foi cuidadosamente explicado para que você possa:

- **Configurar e personalizar estratégias** conforme seu perfil de risco.
- **Realizar back tests** e utilizar os relatórios para aprimoramentos.
- **Publicar e validar** estratégias, demonstrando sua performance e lucratividade.
- **Executar o bot** com a estratégia desejada e monitorar seus resultados através de relatórios e uma API integrada.
- **Gerenciar a escalabilidade e manutenção** do bot através de ferramentas de back office.

Com esses passos, você tem uma visão completa do fluxo de desenvolvimento, validação e operação das estratégias no ambiente Freqtrade, garantindo uma melhor gestão e evolução contínua do seu projeto.

---

Esta documentação integra informações dos seguintes arquivos e scripts:
- [stop_bot.sh](citeturn0file11)
- [run_bot.sh](citeturn0file8)
- [Dockerfile](./Dockerfile)
- [backtesting.sh](citeturn0file5)
- [config.json](citeturn0file15)

Essa estrutura permite que novos usuários e colaboradores compreendam rapidamente o fluxo e possam contribuir com melhorias ou ajustes na estratégia e na infraestrutura do bot.