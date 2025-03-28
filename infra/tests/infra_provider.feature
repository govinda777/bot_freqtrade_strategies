# language: pt

Funcionalidade: Testar Upgrade e Downgrade do Provider AWS

  Cenário: Upgrade do Provider AWS
    Dado que o ambiente foi configurado
    Quando eu setar o provider AWS para versão "~> 5.30"
    E executar "terraform init -upgrade" e "terraform plan"
    Então o comando foi executado com sucesso

  Cenário: Downgrade do Provider AWS
    Dado que o ambiente foi configurado
    Quando eu setar o provider AWS para versão "~> 5.0"
    E executar "terraform init -upgrade" e "terraform plan"
    Então o comando foi executado com sucesso
