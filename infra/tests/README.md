# Testes de Infraestrutura

Este documento descreve as definições e diretrizes para a execução dos testes de infraestrutura do projeto "bot_freqtrade_strategies". Aqui, detalhamos como a infraestrutura funciona e os passos necessários para testar e validar este ambiente.

## Definições de Infraestrutura

1. **Cluster Kubernetes (AWS EKS)**  
   - Ambiente onde são executados os pods contendo os bots e serviços internos.
   - Gerenciado via Terraform, com namespaces distintos para "freqtrade" (bots) e "infra" (ferramentas de gerenciamento).

2. **Banco de Dados (AWS RDS - PostgreSQL)**  
   - Instância única de Postgres com um schema dedicado para cada cliente, garantindo isolamento de dados.
   - Utiliza o parâmetro "search_path" para direcionar conexões ao schema correto.

3. **Deploy GitOps com Helm e ArgoCD**  
   - Configurações de deploy versionadas no Git e aplicadas automaticamente via ArgoCD.
   - Helm permite templates parametrizáveis para implantações dinâmicas.

4. **CI/CD com GitHub Actions**  
   - Pipelines automatizados que constroem imagens Docker, atualizam arquivos de configuração (como <code>values.yaml</code>) e realizam deploy contínuo.
   - Integração com ArgoCD para atualizações imediatas no cluster.

5. **Facade API**  
   - Ponto central para o processamento de comandos criptografados vindos da blockchain.
   - Gerencia a configuração dos bots, monitora a saúde dos serviços (por meio de endpoints como <code>/api/v1/ping</code>) e executa operações de approve/rollback conforme necessário.

## Como Testar e Validar a Infraestrutura

- **Provisionamento com Terraform**  
  - Execute os scripts (ex.: <code>eks.tf</code>, <code>rds.tf</code>, <code>iam.tf</code>, etc.) para provisionar ou atualizar os recursos na AWS.

- **Monitoramento dos Deployments (ArgoCD)**  
  - Verifique a interface do ArgoCD para confirmar a sincronização dos deployments e o estado dos pods.

- **Execução dos Pipelines CI/CD**  
  - Acompanhe os workflows do GitHub Actions para validar a construção das imagens Docker e a atualização dos arquivos de configuração.

- **Testes Automatizados**  
  - Utilize os scripts e testes automatizados contidos neste diretório (como <code>run.sh</code> e demais testes) para simular cenários de deploy e garantir a integridade do ambiente.

## Conclusão

A integração entre Terraform, Helm, ArgoCD e os pipelines CI/CD proporciona um ambiente escalável, seguro e auditável. Estas definições e procedimentos asseguram que a infraestrutura do projeto seja mantida e evolua de forma eficiente.

## Próximos Passos

- Implementar verificação das IAC Policies com Checkov para garantir a conformidade com as melhores práticas de segurança na AWS e Terraform.
- Desenvolver casos de testes para validar upgrade e downgrade de versões do provider AWS e Terraform, assegurando compatibilidade e reversibilidade dos deployments.
- Integrar esses testes ao pipeline de CI/CD para execução contínua e feedback imediato.