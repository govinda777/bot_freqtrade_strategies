# Configuração de Deploy Frontend / Backend

Este documento explica as configurações para executar o frontend e o backend separadamente, permitindo o deploy do frontend no GitHub Pages.

## Estrutura do Projeto

O projeto agora possui duas configurações Docker separadas:

1. **Backend (Freqtrade)**: `Dockerfile.backend`
2. **Frontend (React)**: `Dockerfile.frontend`

Esta separação permite uma maior flexibilidade no deploy e desenvolvimento.

## Executando com Docker Compose

Para executar localmente os dois serviços juntos:

```bash
docker-compose up
```

Isso iniciará:
- Backend na porta 8080
- Frontend na porta 80

## Deploy do Frontend no GitHub Pages

### Configuração Automática (CI/CD)

O pipeline CI/CD foi configurado para automáticamente:

1. Testar o frontend
2. Construir o frontend com configurações para GitHub Pages
3. Fazer o deploy para o branch `gh-pages` (que é automaticamente publicado pelo GitHub)

Nenhuma ação manual é necessária, basta fazer push para o branch principal.

### Deploy Manual

Para fazer o deploy manual do frontend para GitHub Pages:

```bash
cd frontend
npm install
npm run deploy
```

Este comando irá:
1. Construir o aplicativo
2. Fazer o deploy para o branch `gh-pages`

## Configuração de API

A comunicação entre o frontend no GitHub Pages e o backend no Render.com é gerenciada automaticamente:

- O arquivo `frontend/src/config.ts` detecta o ambiente atual
- Quando executado no GitHub Pages, ele usa a URL do backend no Render.com
- Quando executado localmente, ele usa o proxy configurado no webpack

### Modificando a URL do Backend

Se você precisar atualizar a URL do backend, edite o arquivo `frontend/src/config.ts`:

```typescript
if (isGitHubPages) {
  // Atualize esta URL para apontar para o seu backend no Render.com
  API_BASE_URL = 'https://freqtrade-backend.onrender.com';
}
```

## Desenvolvimento Local

### Frontend

Para desenvolver apenas o frontend:

```bash
cd frontend
npm install
npm start
```

O servidor de desenvolvimento utilizará um proxy para o backend na porta 8080.

### Backend

Para executar apenas o backend:

```bash
docker build -f Dockerfile.backend -t freqtrade-backend .
docker run -p 8080:8080 freqtrade-backend
```

## Modificações nos Arquivos

Os seguintes arquivos foram modificados ou criados:

1. `Dockerfile.backend` - Contém apenas a configuração do backend Freqtrade
2. `Dockerfile.frontend` - Configuração para o frontend React com Nginx
3. `docker-compose.yml` - Atualizado para usar ambos os serviços
4. `.github/workflows/main.yml` - Atualizado para incluir deploy no GitHub Pages
5. `frontend/package.json` - Adicionado suporte para GitHub Pages
6. `frontend/webpack.config.js` - Configurado para usar caminhos relativos
7. `frontend/src/config.ts` - Configuração de API para diferentes ambientes

## Considerações importantes

1. Ao fazer o deploy do frontend no GitHub Pages, ele estará em um domínio diferente do backend, então é importante que o backend tenha CORS configurado corretamente.

2. Ajuste as variáveis de ambiente e secrets no GitHub para o deploy funcionar corretamente.

3. Caso precise atualizar as URLs da API ou outros parâmetros da aplicação, o arquivo `config.ts` centraliza essas configurações.