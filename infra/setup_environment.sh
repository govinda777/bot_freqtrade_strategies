#!/bin/bash
set -e

# Nome do container do LocalStack
CONTAINER_NAME="localstack_main"

# Caminho para os arquivos Terraform
TERRAFORM_DIR="$(dirname "$0")/terraform"

# Verifica se o container já existe e está rodando
if [ "$(docker ps -q -f name=^/${CONTAINER_NAME}$)" ]; then
  echo "Container '$CONTAINER_NAME' já está em execução."
else
  # Se existir parado, remove
  if [ "$(docker ps -a -q -f name=^/${CONTAINER_NAME}$)" ]; then
    echo "Removendo container parado '$CONTAINER_NAME'..."
    docker rm $CONTAINER_NAME >/dev/null
  fi

  echo "Iniciando o container LocalStack em segundo plano..."
  docker run -d --name $CONTAINER_NAME \
    -p 4566:4566 -p 4510-4559:4510-4559 \
    localstack/localstack
fi

echo "Aguardando o LocalStack iniciar..."
sleep 10

# Configura variáveis de ambiente para o Terraform utilizar o LocalStack como endpoint AWS
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1

# Passa variáveis sensíveis
export TF_VAR_db_password=$TF_VAR_db_password
export LOCALSTACK_API_KEY=$LOCALSTACK_API_KEY

echo "Executando 'terraform init'..."
terraform -chdir="$TERRAFORM_DIR" init -upgrade

echo "Executando 'terraform apply'..."
terraform -chdir="$TERRAFORM_DIR" apply -auto-approve

echo "Ambiente configurado com sucesso"
echo "Exibindo os últimos logs do container:"
logs=$(docker logs --tail 5 $CONTAINER_NAME || true)
if [ -n "$logs" ]; then
  echo "$logs"
else
  echo "Nenhum log disponível"
fi
