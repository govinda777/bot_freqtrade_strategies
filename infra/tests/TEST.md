# Documentação de Testes de Infraestrutura

Este documento descreve em detalhes como realizamos os testes da nossa infraestrutura antes de ir para produção, utilizando simulações da AWS com LocalStack. Essa abordagem nos possibilitou criar uma stack de testes BDD robusta e confiável.

## Objetivo
O objetivo dos testes é garantir que todos os componentes da infraestrutura — incluindo clusters, serviços, deployment e segurança — operem conforme o esperado antes de realizarmos o deploy na AWS real.

## Por que LocalStack?
- **Simulação da AWS:** LocalStack simula os principais serviços da AWS, permitindo testes sem custos ou impacto em ambientes reais.
- **Ambiente Isolado:** Permite a execução de testes em um ambiente controlado, sem interferência de serviços externos.
- **Integração com CI/CD:** Facilita a incorporação dos testes de infraestrutura no pipeline de CI/CD, garantindo validações contínuas.

## Estrutura dos Testes
Os testes foram implementados utilizando o framework BDD, possibilitando a escrita de cenários em linguagem natural. A estrutura dos testes inclui:

- **Cenários de Deploy:** Validação dos processos de build e deploy dos containers e serviços.
- **Testes de Segurança:** Verificação dos controles de segurança e das políticas IAM simuladas.
- **Testes de Rede e Comunicação:** Confirmação da conectividade entre serviços, load balancing e health checks.
- **Testes de Backup e Recovery:** Simulação de falhas e validação dos mecanismos de backup e recuperação.

## Como Executar os Testes
1. **Preparar o Ambiente:**
   - Instale e configure o [LocalStack](https://localstack.cloud/).
   - Ajuste os arquivos de configuração conforme as orientações descritas no [README de infraestrutura](/infra/README.md).
2. **Executar os Testes:**
   - Utilize o script <code>infra/tests/run.sh</code> para iniciar a execução dos testes.
   - A execução utiliza o framework BDD, que gera um relatório detalhado dos resultados.
3. **Analisar os Resultados:**
   - Após a execução, os logs e relatórios serão disponibilizados na pasta <code>infra/tests/</code>.
   - Confirme que todos os cenários foram aprovados antes de avançar para produção.

## Integração com o Pipeline
A simulação com LocalStack e os testes BDD estão integrados ao pipeline de CI/CD, garantindo:
- Validação automática dos deploys.
- Notificações imediatas em caso de falhas.
- Execução de rollbacks automáticos diante de falhas críticas.

## Conclusão
A utilização do LocalStack para simular a AWS permitiu testar nossa infraestrutura de forma segura e eficiente. Com os cenários BDD, conseguimos validar a resiliência e confiabilidade do ambiente, minimizando riscos no deploy para produção.

## Referências
- [LocalStack Documentation](https://localstack.cloud/)
- [Documentação do BDD (Cucumber)](https://cucumber.io/)