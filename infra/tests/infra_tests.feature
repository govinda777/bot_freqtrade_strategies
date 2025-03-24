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