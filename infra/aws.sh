#!/bin/bash
# infra/aws.sh
# Script para gerenciar a infraestrutura AWS via Terraform, com opção de configuração para LocalStack ou AWS.
# Comandos: init, plan, apply, destroy, output, configure

set -e

TERRAFORM_DIR="./terraform"

usage() {
  echo "Usage: $0 {init|plan|apply|destroy|output|configure}"
  exit 1
}

if [ "$#" -ne 1 ]; then
  usage
fi

COMMAND=$1

case $COMMAND in
  init|plan|apply|destroy|output)
    cd "$TERRAFORM_DIR"
    case $COMMAND in
      init)
        echo "Inicializando o Terraform..."
        terraform init
        ;;
      plan)
        echo "Executando o plano do Terraform..."
        terraform plan
        ;;
      apply)
        echo "Aplicando as mudanças (terraform apply)..."
        terraform apply -auto-approve
        ;;
      destroy)
        echo "Destruindo a infraestrutura (terraform destroy)..."
        terraform destroy -auto-approve
        ;;
      output)
        echo "Mostrando outputs do Terraform..."
        terraform output
        ;;
    esac
    ;;
  configure)
    echo "Configuração do provider:"
    echo "Digite 'local' para usar o LocalStack ou 'aws' para utilizar a AWS real:"
    read -r PROVIDER
    case "$PROVIDER" in
      local)
        echo "Configurando para LocalStack..."
        # Verifica se o container LocalStack já está rodando
        if docker ps | grep -q "localstack_main"; then
          echo "LocalStack já está rodando."
        else
          echo "Iniciando LocalStack (porta 4566 para serviços AWS)..."
          docker run --rm -d --name localstack_main -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack
          echo "LocalStack iniciado."
        fi
        echo "Atualize seu provider no Terraform para usar os endpoints do LocalStack."
        echo "Exemplo de provider no terraform/provider.tf:"
        echo 'provider "aws" {'
        echo '  region                      = "us-east-1"'
        echo '  access_key                  = "test"'
        echo '  secret_key                  = "test"'
        echo '  skip_credentials_validation = true'
        echo '  skip_metadata_api_check     = true'
        echo '  endpoints {'
        echo '    s3  = "http://localhost:4566"'
        echo '    eks = "http://localhost:4566"'
        echo '    rds = "http://localhost:4566"'
        echo '  }'
        echo '}'
        ;;
      aws)
        echo "Configurando para AWS real..."
        echo "Certifique-se de que as credenciais AWS estão configuradas corretamente no ambiente."
        ;;
      *)
        echo "Opção inválida. Use 'local' ou 'aws'."
        exit 1
        ;;
    esac
    ;;
  *)
    usage
    ;;
esac
