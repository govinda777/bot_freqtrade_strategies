# language: pt

Funcionalidade: Testar Upgrade e Downgrade do Provider AWS

  Cenário: Upgrade do Provider AWS
    Dado que o ambiente foi configurado
    Quando eu setar o provider AWS para versão "~> 5.30"
    E executar "terraform init -upgrade" e "terraform plan"
    Então o terraform plan foi executado com sucesso
    Quando executar "terraform apply" com aprovação automática
    Então o terraform apply foi executado com sucesso
    Quando executar "terraform providers"
    Então a saída do terraform providers deve conter "provider[registry.terraform.io/hashicorp/aws] ~> 5.30"

  Cenário: Downgrade do Provider AWS
    Dado que o ambiente foi configurado
    Quando eu setar o provider AWS para versão "~> 5.0"
    E executar "terraform init -upgrade" e "terraform plan"
    Então o terraform plan foi executado com sucesso
    Quando executar "terraform apply" com aprovação automática
    Então o terraform apply foi executado com sucesso
    Quando executar "terraform providers"
    Então a saída do terraform providers deve conter "provider[registry.terraform.io/hashicorp/aws] ~> 5.0"
