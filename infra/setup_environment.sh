#!/bin/bash
set -e

# Nome do container do LocalStack
CONTAINER_NAME="localstack_main"

# Função para limpar o ambiente ao sair (mesmo com erro ou Ctrl+C)
cleanup() {
  echo "Limpando ambiente..."
  docker stop $CONTAINER_NAME >/dev/null 2>&1 || true
  docker rm $CONTAINER_NAME >/dev/null 2>&1 || true
  echo "Cleanup concluído."
}
trap cleanup EXIT

# Verifica se o container já existe e remove
if [ "$(docker ps -a -q -f name=^/${CONTAINER_NAME}$)" ]; then
  echo "Removendo container existente '$CONTAINER_NAME'..."
  docker rm -f $CONTAINER_NAME >/dev/null
fi

echo "Iniciando o container LocalStack..."
docker run --rm -d --name $CONTAINER_NAME \
  -p 4566:4566 -p 4510-4559:4510-4559 \
  localstack/localstack

echo "Aguardando o LocalStack iniciar..."
sleep 10

# Configura variáveis de ambiente para o Terraform utilizar o LocalStack como endpoint AWS
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1

# Caminho para os arquivos Terraform
TERRAFORM_DIR="$(dirname "$0")/terraform"

echo "Executando 'terraform init'..."
terraform -chdir="$TERRAFORM_DIR" init

echo "Executando 'terraform apply'..."
terraform -chdir="$TERRAFORM_DIR" apply -auto-approve

echo "Ambiente configurado com sucesso."
