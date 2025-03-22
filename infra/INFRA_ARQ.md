
# Infraestrutura do Projeto bot_freqtrade_strategies

Este documento descreve a arquitetura, os componentes e os fluxos operacionais da infraestrutura do projeto. Ele serve como guia para criar, destruir e gerenciar a plataforma multi-tenant de bots Freqtrade usando AWS EKS, Terraform, RDS, GitHub Actions, GitHub Pages, Rancher, ArgoCD e Helm.

---

## 1. Arquitetura Geral

```mermaid
graph TD
    Client[Cliente Web/Mobile] --> FacadeAPI[Facade API]
    FacadeAPI --> GitRepo[GitHub Repository]
    FacadeAPI --> Blockchain[Blockchain Events]
    
    GitRepo --> ArgoCD
    ArgoCD --> K8S[AWS EKS Kubernetes]
    
    K8S --> PodTrade[POD_FREQTRADE_TRADE]
    K8S --> PodTest[POD_FREQTRADE_BACK_TEST]
    
    PodTrade --> RDS[(PostgreSQL RDS)]
    PodTest --> RDS
    
    subgraph "AWS Cloud"
        K8S
        RDS
    end
    
    subgraph "CI/CD Pipeline"
        GitRepo
        ArgoCD
    end
    
    class Client,Blockchain,FacadeAPI external
    class K8S,RDS,PodTrade,PodTest aws
    class GitRepo,ArgoCD cicd
    
    classDef external fill:#f9f,stroke:#333,stroke-width:2px
    classDef aws fill:#ff9900,stroke:#333,stroke-width:1px,color:white
    classDef cicd fill:#0072ce,stroke:#333,stroke-width:1px,color:white
```

### Stack Tecnológica

- **EKS**: Cluster Kubernetes gerenciado na AWS para orquestração dos Pods.
- **Terraform**: Provisionamento da infraestrutura na AWS (EKS, VPC, subnets, RDS, IAM, etc.).
- **RDS (PostgreSQL)**: Banco de dados central, utilizando multi-schema para isolamento dos dados de cada cliente.  
  Cada cliente terá seu schema dedicado, por exemplo: `/client_id_db` (schema: `cliente_001`, `cliente_002`, etc.).
- **GitHub Actions**: Pipeline CI/CD para build, testes e deploy das imagens Docker e atualizações dos valores (values.yaml).
- **GitHub Pages**: Documentação e dashboards públicos (se necessário).

### Serviços e Plugins

- **Rancher**: Interface de gerenciamento dos clusters Kubernetes.
- **ArgoCD**: GitOps para sincronização automática dos deployments a partir do repositório Git.
- **Helm**: Gerenciamento dos templates Kubernetes para implantação dos bots (charts).

### Templates de Deployment

- **POD_FREQTRADE_TRADE**: Template para Pods que executam o Freqtrade em modo trade.
- **POD_FREQTRADE_BACK_TEST**: Template para Pods que executam backtests (e hyperopt).

### API da Plataforma

A aplicação expõe endpoints para gerenciar os bots:

- **`/trade`**: Inicia um novo bot de trading (executa `freqtrade trade`).
- **`/backtest`**: Inicia um novo Pod para backtesting.
- **`/strategies`**: Permite listar, atualizar ou consultar estratégias configuradas.

---

## 2. Fluxos Operacionais

### 2.1 Criação do Banco de Dados

- **Multi-Schema no RDS:**  
  O RDS é configurado para ter um único banco de dados, onde cada cliente terá um schema exclusivo.  
  - O esquema será criado dinamicamente pelo script `init-schema.sh` contido na imagem Docker (ou via um job de inicialização).
  - O usuário de conexão é configurado para ter acesso somente ao seu schema via parâmetro `search_path`.
  - Exemplo de URL:
    ```
    postgresql://user_cliente:senha@rds-endpoint:5432/freqtrade_multi?search_path=cliente_001
    ```

### 2.2 Gatilho para Iniciar um Command

```mermaid
sequenceDiagram
    participant BC as Blockchain
    participant API as Facade API
    participant Git as GitHub Repo
    participant Argo as ArgoCD
    participant K8s as Kubernetes
    participant Pod as FreqTrade Pod
    participant RDS as PostgreSQL

    BC->>API: Emite evento (EncryptedCommand)
    API->>API: Descriptografa comando
    API->>Git: Gera e commita values.yaml
    Git->>Argo: Detecta alteração
    Argo->>K8s: Aplica Helm chart
    K8s->>Pod: Cria Pod (trade ou backtest)
    Pod->>RDS: Executa init-schema.sh
    Pod->>Pod: Inicia Freqtrade
    Pod->>API: Retorna status
    API->>BC: Confirma transação
```

- **Evento na Blockchain / Smart Contract Transaction:**  
  A Facade API da plataforma escuta eventos da blockchain (por exemplo, um smart contract emite um comando criptografado).
  - **Passo 1:** A API detecta e descriptografa a mensagem.
  - **Passo 2:** A API monta os valores necessários (como API keys, estratégia, schema, etc.) e gera um arquivo `values.yaml` específico para o cliente.
  - **Passo 3:** A API comita essa configuração no repositório Git (estrutura de arquivos em `/clientes/<client_id>/values.yaml`).
  - **Passo 4:** ArgoCD detecta a alteração no Git e, via Helm, implanta um novo Pod usando o template adequado (POD_FREQTRADE_TRADE ou POD_FREQTRADE_BACK_TEST).
  - **Passo 5:** Durante a inicialização, o Pod executa o script `init-schema.sh` para criar o schema (caso não exista) e, em seguida, inicia o bot com os parâmetros configurados.

### 2.3 Solicitação de Dados (GET)

- **Endpoints da API:**  
  A Facade API também expõe endpoints para consulta dos status e históricos dos bots:
  - **`/trade`**: Consulta o status dos bots de trading em execução.
  - **`/backtest`**: Lista resultados e relatórios dos backtests realizados.
  - **`/strategies`**: Retorna as estratégias configuradas e os históricos de operações.
- **Monitoramento:**  
  Cada Pod expõe um endpoint de health check (ex.: `/api/v1/ping`), e os logs e métricas são coletados e centralizados para monitoramento (via ferramentas como Prometheus, Grafana, ou soluções integradas no Rancher).

---

## 3. Componentes e Arquivos da Infraestrutura

```mermaid
graph TD
    subgraph "EKS Cluster"
        Pods[FreqTrade Pods]
        Services[K8s Services]
        ConfigMaps[ConfigMaps]
        Secrets[Secrets]
    end
    
    subgraph "Terraform Resources"
        EKS[EKS Cluster]
        VPC[VPC & Subnets]
        RDS[PostgreSQL RDS]
        IAM[IAM Roles & Policies]
    end
    
    subgraph "Helm Charts"
        Chart[Chart.yaml]
        Values[values.yaml]
        Templates[Deployment Templates]
        Scripts[Init Scripts]
    end
    
    subgraph "CI/CD"
        GitHub[GitHub Actions]
        ArgoCD[ArgoCD Application]
        DockerHub[Docker Images]
    end
    
    Terraform --> EKS
    Terraform --> VPC
    Terraform --> RDS
    Terraform --> IAM
    
    GitHub --> DockerHub
    GitHub --> ArgoCD
    
    ArgoCD --> Chart
    Chart --> Templates
    Values --> Templates
    Templates --> Pods
    Scripts --> Pods
    
    Pods --> RDS
    Services --> Pods

    class EKS,VPC,RDS,IAM terraform
    class Chart,Values,Templates,Scripts helm
    class GitHub,ArgoCD,DockerHub cicd
    class Pods,Services,ConfigMaps,Secrets kubernetes
    
    classDef terraform fill:#844FBA,stroke:#333,stroke-width:1px,color:white
    classDef helm fill:#0F1689,stroke:#333,stroke-width:1px,color:white
    classDef cicd fill:#2088FF,stroke:#333,stroke-width:1px,color:white
    classDef kubernetes fill:#326CE5,stroke:#333,stroke-width:1px,color:white
```

### 3.1 Terraform

Responsável por provisionar a infraestrutura AWS.

- **eks-cluster.tf**: Cria o cluster EKS e configura a rede.
- **rds.tf**: Provisiona a instância PostgreSQL RDS para o banco multi-tenant.
- **iam.tf**: Configura roles e policies necessárias.
- **variables.tf & outputs.tf**: Define variáveis e outputs para integração.

### 3.2 Kubernetes / Helm

Estrutura de arquivos em `/infra/charts/freqtrade`:

- **Chart.yaml**: Metadados do chart.
- **values.yaml**: Valores padrão para a implantação (ex.: ambiente, endpoints, variáveis).
- **templates/**:
  - **deployment.yaml**: Define o Deployment do bot (template para POD_FREQTRADE_TRADE ou POD_FREQTRADE_BACK_TEST).
  - **service.yaml**: Exposição da API (porta 8080).
  - **_helpers.tpl**: Funções auxiliares para nomeação.
- **scripts/**:
  - **init-schema.sh**: Script de inicialização que cria o schema no banco se necessário.

### 3.3 ArgoCD

Arquivo de configuração para sincronização GitOps:

- **argocd-application.yaml**: Define a aplicação ArgoCD para implantar o chart Helm no namespace designado (ex.: `freqtrade`).

### 3.4 Docker Images

- **freqtrade-platform**: Imagem Docker customizada baseada em `freqtradeorg/freqtrade:stable` com:
  - Configuração (config.json, strategies).
  - Scripts de inicialização (init-schema.sh).
  - Variáveis configuráveis para API keys, estratégia, etc.

---

## 4. Fluxo Completo de uma Nova Trade

```mermaid
flowchart TD
    A[Evento na Blockchain] --> B{Facade API}
    B -->|Descriptografa| C[Gera configuração]
    C --> D[Commit no Git]
    D --> E[ArgoCD detecta mudança]
    E --> F[Implanta Helm Chart]
    F --> G[Cria Pod no EKS]
    G --> H{Inicializa Pod}
    H -->|init-schema.sh| I[Verifica/Cria Schema]
    I --> J[Inicia Freqtrade Trade]
    J --> K[Monitora Status]
    K -->|Sucesso| L[Aprova Transação]
    K -->|Falha| M[Rollback]
    
    style A fill:#f9a,stroke:#333,stroke-width:2px
    style B fill:#ad9,stroke:#333,stroke-width:2px
    style J fill:#9cf,stroke:#333,stroke-width:2px
    style L fill:#9f9,stroke:#333,stroke-width:2px
    style M fill:#f99,stroke:#333,stroke-width:2px
```

1. **Recebimento do Comando:**
   - A blockchain emite um evento `EncryptedCommand`.
   - A Facade API escuta esse evento e descriptografa a mensagem.

2. **Montagem dos Valores:**
   - A API monta os parâmetros para o novo bot: API keys, estratégia, e configurações específicas.
   - Preenche um template `values.yaml` com:
     - `BINANCE_API_KEY`
     - `BINANCE_SECRET_KEY`
     - `FREQTRADE_STRATEGY`
     - `FREQTRADE_SCHEMA` (ex.: `cliente_001`)
     - `DATABASE_URL` com `?search_path=cliente_001`

3. **Commit no Repositório:**
   - O arquivo `values.yaml` para o cliente é commitado no repositório Git (pasta `/clientes/cliente_001/values.yaml`).

4. **Deploy via ArgoCD e Helm:**
   - ArgoCD detecta o commit e aplica o Helm chart, gerando um novo Deployment no EKS.
   - O template do Deployment utiliza os valores do arquivo para configurar o Pod.

5. **Inicialização do Pod:**
   - O Pod executa o script `init-schema.sh`:
     - Conecta ao RDS e verifica se o schema `cliente_001` existe.
     - Se não existir, o schema é criado.
   - Em seguida, o comando `freqtrade trade` é iniciado com as variáveis de ambiente configuradas.

6. **Monitoramento e Feedback:**
   - A Facade API monitora os health checks do Pod (endpoint `/api/v1/ping`) e os logs.
   - Com base na resposta, a API emite um comando de **approve** (se o bot estiver funcionando) ou **rollback** (se ocorrer algum erro).
   - A transação é registrada e o cliente pode consultar o status via endpoints `/trade`, `/backtest` e `/strategies`.

---

## 5. Criação e Destruição da Infraestrutura

```mermaid
stateDiagram-v2
    [*] --> Terraform_Init
    Terraform_Init --> Terraform_Apply
    Terraform_Apply --> EKS_Cluster_Ready
    
    EKS_Cluster_Ready --> ArgoCD_Setup
    ArgoCD_Setup --> GitRepo_Ready
    
    GitRepo_Ready --> Values_Commit
    Values_Commit --> Pods_Running
    
    Pods_Running --> Bot_Active
    Bot_Active --> Bot_Cleanup: Remove values.yaml
    Bot_Cleanup --> Pods_Running: Add new bot
    
    Bot_Cleanup --> Terraform_Destroy: Decommission
    Terraform_Destroy --> [*]
    
    state Terraform_Apply {
        [*] --> Create_VPC
        Create_VPC --> Create_EKS
        Create_EKS --> Create_RDS
        Create_RDS --> Create_IAM
        Create_IAM --> [*]
    }
    
    state Pods_Running {
        [*] --> Trading_Pods 
        [*] --> Backtest_Pods
        Trading_Pods --> [*]
        Backtest_Pods --> [*]
    }
```

### 5.1 Criação

- **Terraform:**
  - Execute `terraform init` e `terraform apply` para provisionar o EKS, RDS e recursos associados.
- **Deploy do Helm Chart via ArgoCD:**
  - O repositório Git contém os arquivos do Helm chart e dos valores dos clientes.
  - ArgoCD sincroniza automaticamente os deployments no cluster EKS.
- **GitHub Actions:**
  - Pipeline CI/CD constrói a imagem Docker e atualiza o repositório com os arquivos de valores para novos bots.

### 5.2 Destruição

- **Terraform:**
  - Para destruir a infraestrutura AWS, execute `terraform destroy`.
- **ArgoCD / Helm:**
  - Para remover um bot específico, remova o arquivo de valores correspondente ou execute um comando de rollback via Helm.
- **Cleanup de Recursos:**
  - Remova Pods, Services e ConfigMaps associados conforme necessário.

---

## 6. Organização do Repositório (/infra)

```mermaid
graph TD
    subgraph "/infra"
        A[/infra]
        B[/charts]
        C[/terraform]
        D[/clientes]
        E[/.github]
        
        A --> B
        A --> C
        A --> D
        A --> E
        A --> ArgoApp[argocd-application.yaml]
        
        B --> Freqtrade[/freqtrade]
        Freqtrade --> ChartFile[Chart.yaml]
        Freqtrade --> ValuesFile[values.yaml]
        Freqtrade --> Templates[/templates]
        Freqtrade --> Scripts[/scripts]
        
        Templates --> DeploymentFile[deployment.yaml]
        Templates --> ServiceFile[service.yaml]
        Templates --> HelperFile[_helpers.tpl]
        
        Scripts --> InitSchema[init-schema.sh]
        
        C --> EksFile[eks-cluster.tf]
        C --> RdsFile[rds.tf]
        C --> IamFile[iam.tf]
        C --> VpcFile[vpc.tf]
        C --> VarsFile[variables.tf]
        C --> OutputsFile[outputs.tf]
        
        D --> Cliente1[/cliente-001]
        D --> Cliente2[/cliente-002]
        D --> ClienteDots[...]
        
        Cliente1 --> Values1[values.yaml]
        Cliente2 --> Values2[values.yaml]
        
        E --> Workflows[/workflows]
        Workflows --> DeployBot[deploy-bot.yml]
    end
```

```
/infra
├── charts/
│   └── freqtrade/
│       ├── Chart.yaml
│       ├── values.yaml             # Valores padrão
│       ├── templates/
│       │   ├── deployment.yaml     # Templates para POD_FREQTRADE_TRADE e POD_FREQTRADE_BACK_TEST
│       │   ├── service.yaml
│       │   └── _helpers.tpl
│       └── scripts/
│           └── init-schema.sh      # Script para criar o schema
├── argocd-application.yaml         # Configuração ArgoCD para deploy automático
├── terraform/
│   ├── eks-cluster.tf
│   ├── rds.tf
│   ├── iam.tf
│   ├── vpc.tf
│   ├── variables.tf
│   └── outputs.tf
├── clientes/
│   ├── cliente-001/
│   │   └── values.yaml           # Valores específicos do cliente 001
│   ├── cliente-002/
│   │   └── values.yaml           # Valores específicos do cliente 002
│   └── ...                       # E assim por diante
└── .github/
    └── workflows/
        └── deploy-bot.yml        # Pipeline GitHub Actions para build e deploy
```

---

## 7. API Endpoints da Plataforma

```mermaid
classDiagram
    class FacadeAPI {
        +POST /trade
        +POST /backtest
        +GET /strategies
        +GET /trade/client_id/status
        +GET /backtest/backtest_id/results
        +GET /strategies/strategy_name
    }
    
    class TradeEndpoints {
        +POST /trade
        +GET /trade/client_id/status
        +POST /trade/client_id/stop
    }
    
    class BacktestEndpoints {
        +POST /backtest
        +GET /backtest/backtest_id/status
        +GET /backtest/backtest_id/results
    }
    
    class StrategyEndpoints {
        +GET /strategies
        +GET /strategies/strategy_name
        +PUT /strategies/strategy_name/parameters
    }
    
    FacadeAPI <|-- TradeEndpoints
    FacadeAPI <|-- BacktestEndpoints
    FacadeAPI <|-- StrategyEndpoints
```

A Facade API expõe os seguintes endpoints:

- **`POST /trade`**:  
  Recebe um comando de novo trade (através de evento da blockchain) e inicia o processo descrito (monta valores, commit no Git, deploy via ArgoCD).

- **`POST /backtest`**:  
  Inicia uma instância de backtesting para o cliente.

- **`GET /strategies`**:  
  Lista as estratégias disponíveis e os históricos de trades/backtests.

- **`POST /strategies`**:  
  Adiciona cria uma NFT com a estratégia e a lista de parâmetros. Apenas o Smart Contract da plataforma consegue ler os dados que estão dentro dessa NFT.

- **`GET /trade/{client_id}/status`**:  
  Consulta o status do bot de trading de um cliente específico (através do health check e logs).

---

## 8. Fluxo de Operação Resumido

```mermaid
sequenceDiagram
    autonumber
    actor Cliente
    participant Blockchain
    participant API as Facade API
    participant Git as GitHub Repo
    participant ArgoCD
    participant EKS as AWS EKS
    participant RDS as PostgreSQL
    
    Cliente->>Blockchain: Envia transação
    Blockchain->>API: Emite evento (EncryptedCommand)
    API->>API: Descriptografa comando
    API->>Git: Monta e commita values.yaml
    Git->>ArgoCD: Alteração detectada
    ArgoCD->>EKS: Aplica Helm chart
    EKS->>EKS: Cria Pod Freqtrade
    EKS->>RDS: Executa init-schema.sh
    EKS->>EKS: Inicia bot (freqtrade trade)
    EKS->>API: Retorna status via health check
    API->>Blockchain: Aprova ou rejeita
    Cliente->>API: Consulta status via GET /trade/{id}
    API->>EKS: Solicita health check
    EKS->>API: Retorna status atual
    API->>Cliente: Mostra resultado
```

1. **Recepção do Comando On-Chain:**  
   - Blockchain emite `EncryptedCommand` → Facade API recebe e descriptografa.

2. **Preparação e Commit:**  
   - API monta o arquivo `values.yaml` para o cliente com as configurações: API keys, estratégia, `DATABASE_URL` com `search_path=<cliente_schema>`.
   - API comita o arquivo no repositório Git.

3. **Deploy Automatizado via ArgoCD:**  
   - ArgoCD detecta a alteração e aplica o Helm chart, criando o Deployment no AWS EKS.
   - Durante a inicialização, o Pod executa `init-schema.sh` para garantir que o schema exista no RDS.
   - Em seguida, o comando `freqtrade trade` inicia o bot.

4. **Monitoramento e Controle:**  
   - A Facade API monitora a saúde do bot (via `/api/v1/ping`, logs, etc.).
   - Se o bot estiver funcionando, a API aprova a transação; se não, executa rollback.

5. **Consulta de Dados:**  
   - Clientes podem consultar o status, históricos e estratégias através dos endpoints expostos.

---

## Conclusão

Esta arquitetura proporciona uma plataforma escalável, segura e automatizada para gerenciar múltiplos bots Freqtrade para diferentes clientes. Utilizando AWS EKS, RDS, Terraform, Helm, ArgoCD e GitHub Actions, a infraestrutura é definida como código e operada com GitOps, garantindo consistência e facilidade de manutenção.

Caso precise de mais detalhes ou de scripts/templates adicionais, estou à disposição para ajudar!
