#!/bin/bash
set -e

AWS_VERSION=$1

if [ -z "$AWS_VERSION" ]; then
    echo "Uso: $0 <versao_do_provider> (ex: ~> 5.0)"
    exit 1
fi

# Define os valores padrão se não estiverem definidos
AWS_PROVIDER_VERSION="$AWS_VERSION"
KUBERNETES_PROVIDER_VERSION="${KUBERNETES_PROVIDER_VERSION:-~> 2.20}"
HELM_PROVIDER_VERSION="${HELM_PROVIDER_VERSION:-~> 2.10}"
TLS_PROVIDER_VERSION="${TLS_PROVIDER_VERSION:-~> 4.0}"
CLOUDINIT_PROVIDER_VERSION="${CLOUDINIT_PROVIDER_VERSION:-~> 2.3}"

export AWS_PROVIDER_VERSION
export KUBERNETES_PROVIDER_VERSION
export HELM_PROVIDER_VERSION
export TLS_PROVIDER_VERSION
export CLOUDINIT_PROVIDER_VERSION

TEMPLATE_DIR="$(dirname "$0")/../terraform"
TEMPLATE_FILE="${TEMPLATE_DIR}/providers.tf.template"
OUTPUT_FILE="${TEMPLATE_DIR}/providers.tf"

echo "Gerando providers.tf"
echo "  AWS            = ${AWS_PROVIDER_VERSION}"
echo "  Kubernetes     = ${KUBERNETES_PROVIDER_VERSION}"
echo "  Helm           = ${HELM_PROVIDER_VERSION}"
echo "  TLS            = ${TLS_PROVIDER_VERSION}"
echo "  CloudInit      = ${CLOUDINIT_PROVIDER_VERSION}"

envsubst < "$TEMPLATE_FILE" > "$OUTPUT_FILE"

echo "Arquivo ${OUTPUT_FILE} gerado com sucesso."
