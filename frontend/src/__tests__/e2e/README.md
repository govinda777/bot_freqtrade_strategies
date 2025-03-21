# End-to-End Tests

Este diretório contém testes end-to-end (e2e) para validar o funcionamento adequado da aplicação FreqTrade UI.

## Testes de Validação da Inicialização

Os testes neste diretório verificam se a aplicação foi inicializada corretamente, incluindo:

### AppStartup.test.tsx

Testa se os componentes principais da aplicação React estão carregando corretamente:

- Renderização do componente raiz (App)
- Elementos críticos como dashboard e autenticação
- Navegação básica entre componentes

### ServerStartup.test.tsx

Testa se o servidor está respondendo adequadamente:

- Verificação de conectividade com o servidor
- Validação do conteúdo HTML retornado
- Detecção e manipulação de erros graciosamente

## Como Executar os Testes

Execute os testes usando os scripts NPM definidos no arquivo `package.json`:

```bash
# Executar todos os testes e2e
npm run test:e2e

# Executar apenas os testes de inicialização (AppStartup + ServerStartup)
npm run test:startup

# Executar testes de inicialização sem verificar servidor real
# (útil para ambiente CI/CD ou sem servidor rodando)
npm run test:startup:mock
```

## Interpretando os Resultados

Os testes verificam diferentes aspectos da aplicação:

1. **Tests passed** ✅ - A aplicação está funcionando corretamente
2. **Component tests passed, server tests failed** ⚠️ - Os componentes React estão sendo renderizados, mas o servidor não está acessível
3. **All tests failed** ❌ - Problemas graves na inicialização da aplicação

## Solução de Problemas

Se os testes de servidor falharem, mas os testes de componente passarem:
- Verifique se o servidor está rodando (`npm start`)
- Verifique se a URL do servidor está correta (padrão: http://localhost:3000)
- Verifique logs do servidor para erros específicos

Se todos os testes falharem:
- Verifique se o NodeJS e as dependências estão instalados corretamente
- Limpe cache e node_modules e reinstale (`rm -rf node_modules && npm install`)
- Verifique conflitos de versão no package.json

## Adicionando Novos Testes

Para adicionar novos testes de validação de inicialização:

1. Crie um novo arquivo `*Startup.test.tsx` neste diretório
2. Use os utilitários em `__tests__/test-utils.tsx`
3. Inclua o padrão de nome no script npm `test:startup` se necessário