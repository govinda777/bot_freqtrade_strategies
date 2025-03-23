# Teste Local da Infraestrutura com LocalStack

Esta documentação explica, de forma didática, como você pode testar toda a infraestrutura do projeto **bot_freqtrade_strategies** localmente utilizando o **LocalStack**. Dessa forma, é possível simular os serviços AWS (como S3, RDS, EKS, etc.) sem necessidade de deploy real na AWS, facilitando testes e desenvolvimento.

---

## 1. Visão Geral

A infraestrutura do projeto é provisionada com **Terraform** e gerenciada via **Helm/ArgoCD** para deploy no cluster Kubernetes (AWS EKS em produção). No ambiente local, usamos o **LocalStack** para emular os serviços AWS. O estado do Terraform (tfstate) será armazenado em um bucket S3 simulado no LocalStack e o lock será feito via tabela DynamoDB também emulado.

---

## 2. Pré-requisitos

- **Docker:** Para rodar o LocalStack.
- **Terraform:** Instalação e configuração local.
- **kubectl:** Para interagir com um cluster Kubernetes local (pode ser minikube, Kind ou outro).
- **Helm:** Para testar os charts do Kubernetes.
- **Git:** Para versionar a infraestrutura e os arquivos de deploy.
- **LocalStack CLI (opcional):** Pode ajudar na verificação dos serviços emulado.

---

## 3. Configurando o LocalStack

### 3.1. Iniciando o LocalStack

Para simular os serviços AWS localmente, execute o seguinte comando:

```bash
docker run --rm -d --name localstack_main \
  -p 4566:4566 -p 4510-4559:4510-4559 \
  localstack/localstack
```

Este comando inicia o LocalStack, expondo:
- Porta **4566**: Usada como endpoint para a maioria dos serviços AWS (S3, EKS, RDS, etc.).
- Portas adicionais **4510-4559**: Para outros serviços, se necessário.

### 3.2. Verificando o LocalStack

Você pode usar o CLI do LocalStack ou o `aws` CLI configurado para apontar para o LocalStack. Por exemplo, para listar buckets S3:

```bash
aws --endpoint-url=http://localhost:4566 s3 ls
```

---

## 4. Configurando o Terraform para LocalStack

### 4.1. Provider do Terraform

No arquivo `terraform/provider.tf` (ou equivalente), configure o provider AWS para apontar aos endpoints do LocalStack:

```hcl
provider "aws" {
  region                      = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  endpoints {
    s3  = "http://localhost:4566"
    eks = "http://localhost:4566"
    rds = "http://localhost:4566"
  }
}
```

> Essa configuração permite que o Terraform se conecte ao LocalStack para provisionar os recursos simulados.

### 4.2. Backend do Terraform

Configure o backend para armazenar o tfstate no LocalStack:

```hcl
terraform {
  backend "s3" {
    bucket         = "meu-bucket-tfstate"
    key            = "tfstate/infra.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

> Certifique-se de que o bucket S3 e a tabela DynamoDB existam no LocalStack. Você pode criá-los manualmente ou deixar o Terraform criar.

---

## 5. Testando a Infraestrutura

### 5.1. Executando os Scripts

Na pasta `/infra`, utilize os scripts de gerenciamento para provisionar ou destruir a infraestrutura.

#### Inicialização e Provisionamento

```bash
./aws.sh init   # Inicializa o Terraform
./aws.sh plan   # Mostra o plano de execução
./aws.sh apply  # Provisiona os recursos (EKS, RDS, S3, etc.) no LocalStack
```

#### Verificação dos Outputs

```bash
./aws.sh output  # Visualiza os outputs, como endpoints e IDs dos recursos provisionados
```

### 5.2. Deploy dos Bots com Helm/ArgoCD

- Utilize o cluster Kubernetes local (minikube, Kind ou similar) para testar os Helm charts.
- Certifique-se de que o provider do Terraform esteja configurado para o LocalStack.
- Faça o deploy do Helm chart:
  ```bash
  helm install bot-cliente-001 ./charts/freqtrade -f clientes/cliente-001/values.yaml --namespace freqtrade
  ```
- O chart irá criar o Deployment do bot, o Service para expor a API e montar os scripts necessários (como `init-schema.sh`).

### 5.3. Verificando os Pods e Serviços

Use o script `cluster.sh` para listar nós, Pods e acessar logs:

```bash
./cluster.sh nodes
./cluster.sh pods
./cluster.sh logs <nome-do-pod>
```

Você pode também verificar o endpoint de health check do bot (por exemplo, acessando `http://localhost:8080/api/v1/ping`).

---

## 6. Fluxo de Teste de Novo Trade

1. **Recepção do Comando:**  
   Simule um comando on-chain manualmente ou via sua Facade API.
2. **Montagem do values.yaml:**  
   O arquivo de configuração específico para o cliente é gerado (com as variáveis necessárias, inclusive o `DATABASE_URL` com `search_path`).
3. **Commit e Deploy via GitOps:**  
   Para teste, você pode simular o commit no repositório e forçar uma sincronização do ArgoCD (ou aplicar o Helm chart manualmente).
4. **Inicialização do Pod:**  
   O Pod é criado e, ao iniciar, executa o script `init-schema.sh` para criar o schema no RDS (simulado no LocalStack) e inicia o bot.
5. **Monitoramento e Logs:**  
   Verifique os logs e endpoints para confirmar que o bot está rodando corretamente.

---

## 7. Limpeza

Para destruir a infraestrutura provisionada localmente:

```bash
./aws.sh destroy
```

Este comando remove todos os recursos provisionados (EKS, RDS, S3 bucket e tabela DynamoDB) no LocalStack.

---

## 8. Considerações Finais

- **Simulação Local:**  
  O uso do LocalStack permite testar todo o fluxo de provisionamento da infraestrutura AWS localmente, garantindo que os mesmos arquivos Terraform e Helm charts possam ser usados tanto no ambiente de testes quanto na AWS real, com a simples alteração do provider.

- **tfstate Centralizado:**  
  O estado do Terraform é salvo no bucket S3 (simulado pelo LocalStack), permitindo versionamento e controle de locks via DynamoDB.

- **Migração para AWS:**  
  Quando estiver pronto para o deploy real, basta alterar as configurações do provider no Terraform (remover os endpoints do LocalStack) e utilizar as credenciais reais da AWS.

Esta documentação serve como um guia para testar e validar toda a infraestrutura do projeto **bot_freqtrade_strategies** de forma local, utilizando o LocalStack. Se houver dúvidas ou necessidades de ajustes, consulte os arquivos de configuração ou entre em contato com a equipe de DevOps.
