# language: pt

Funcionalidade: Validação da Infraestrutura
  Como administrador do ambiente
  Quero garantir que a infraestrutura está configurada corretamente através de testes BDD

  Cenário: Verificação da configuração do ambiente
    Dado que o script "./setup_environment.sh" foi executado com sucesso
    Quando o ambiente está configurado
    Então a saída deve conter "Ambiente configurado com sucesso"

  Cenário: Verificação dos arquivos essenciais
    Dado que o ambiente foi configurado
    Então os seguintes arquivos devem existir:
      | caminho                             |
      | infra/terraform/iam.tf              |
      | infra/terraform/main.tf             |
      | infra/terraform/outputs.tf          |

  Cenário: Verificação dos arquivos complementares
    Dado que o ambiente foi configurado
    Então os seguintes arquivos devem existir:
      | caminho                             |
      | infra/terraform/variables.tf        |
      | infra/terraform/providers.tf        |
      | infra/terraform/eks-cluster.tf      |
      | infra/docker-compose.yml            |

  Cenário: Validação do Terraform Plan
    Dado que o ambiente foi configurado
    Quando executar o comando "terraform plan" na pasta "infra/terraform"
    Então o comando foi executado com sucesso

  Cenário: Execução do Terraform Apply
    Dado que o ambiente foi configurado
    Quando executar o comando "terraform apply" na pasta "infra/terraform" com aprovação automática
    Então a saída do terraform apply deve conter "Apply complete! Resources:"
