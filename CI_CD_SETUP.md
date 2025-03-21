# CI/CD Setup para o Projeto Freqtrade Bot

Este documento descreve como configurar o pipeline de CI/CD usando GitHub Actions e a plataforma Render.com para o projeto Freqtrade Bot.

## Visão Geral

O pipeline de CI/CD configurado realiza as seguintes ações:

1. **Build e teste do frontend**: Compila e testa a aplicação React
2. **Build e push da imagem Docker**: Cria a imagem Docker do bot e a publica no Docker Hub
3. **Deploy no Render.com**: Implanta a aplicação no Render.com

## Requisitos

- Conta no GitHub
- Conta no Docker Hub
- Conta no Render.com

## Configuração do GitHub

### Secrets do GitHub

Você precisa configurar os seguintes secrets no seu repositório GitHub:

1. Vá para seu repositório > Settings > Secrets and variables > Actions
2. Adicione os seguintes secrets:

| Nome do Secret | Descrição |
|---------------|-----------|
| `DOCKER_USERNAME` | Seu nome de usuário do Docker Hub |
| `DOCKER_TOKEN` | Token de acesso pessoal do Docker Hub |
| `RENDER_API_KEY` | API Key do Render.com (obtida no dashboard do Render) |
| `RENDER_SERVICE_ID` | ID do serviço criado no Render.com |

> **Nota sobre autenticação do Docker Hub**: Este projeto utiliza autenticação com Docker Hub via tokens de acesso pessoal para maior segurança. Para detalhes sobre como configurar, consulte [DOCKER_HUB_AUTH.md](DOCKER_HUB_AUTH.md).

## Configuração do Render.com

### Criar uma Conta e um Serviço

1. Registre-se em [Render.com](https://render.com) se ainda não tiver uma conta
2. No dashboard do Render, clique em "New" e selecione "Web Service"
3. Conecte seu repositório GitHub (você precisará autorizar o Render a acessar seus repositórios)
4. Configure o serviço:
   - Nome: `freqtrade-bot` (ou outro nome de sua preferência)
   - Ambiente: `Docker`
   - Plano: Escolha o plano adequado às suas necessidades
   - Região: Escolha a região mais próxima de você
   - Branch: `main` (ou a branch principal do seu repositório)

### Configurar Variáveis de Ambiente

No Render.com, adicione as seguintes variáveis de ambiente ao seu serviço:

| Variável | Descrição |
|----------|-----------|
| `FREQTRADE_STRATEGY` | Nome da estratégia a ser executada (default: CombinedBinHAndCluc) |
| `BINANCE_API_KEY` | Sua chave de API da Binance |
| `BINANCE_SECRET_KEY` | Sua chave secreta da Binance |
| `FREQTRADE_USERNAME` | Nome de usuário para o Freqtrade |
| `FREQTRADE_PASSWORD` | Senha para o Freqtrade |
| `JWT_SECRET_KEY` | Chave secreta para geração de JWT |

### Obter o Service ID e API Key

1. **Service ID**: Após criar o serviço, o ID do serviço será parte da URL quando você estiver na página de configuração do serviço. Geralmente tem o formato `srv-xxxxxxxxxxxx`.
2. **API Key**: Vá para o dashboard do Render.com > Account Settings > API Keys > Create API Key.

## Como Funciona o Pipeline

### GitHub Actions

O arquivo `.github/workflows/main.yml` define o fluxo de CI/CD:

1. Quando há um push para a branch principal ou um pull request, o fluxo é iniciado
2. O frontend é compilado e testado
3. A imagem Docker é construída
4. Se for um push para a branch principal (não um PR), a imagem é enviada para o Docker Hub
5. Em seguida, o deploy é acionado no Render.com

### Render.com

O arquivo `render.yaml` define a configuração do serviço no Render.com:

1. Tipo de serviço: web
2. Ambiente: Docker
3. Configurações do serviço, como região, plano, etc.
4. Comando Docker a ser executado
5. Variáveis de ambiente necessárias
6. Configuração de disco para os dados do bot

## Observações Importantes

- O deploy automático só acontece em pushes para a branch principal, não em pull requests
- As variáveis de ambiente sensíveis (chaves de API, senhas) são mantidas como secrets para segurança
- O arquivo `.env` não é versionado (está no .gitignore) para proteger informações sensíveis
- Um volume de disco é configurado no Render.com para persistir os dados do bot entre restarts

## Solução de Problemas

Se o deploy falhar, verifique:

1. Se todos os secrets foram configurados corretamente no GitHub
2. Se o serviço foi configurado corretamente no Render.com
3. Os logs de build no GitHub Actions
4. Os logs de deploy no dashboard do Render.com

## Executando Localmente

Você ainda pode executar o bot localmente usando o script `run_bot.sh`. O pipeline de CI/CD não afeta a execução local.