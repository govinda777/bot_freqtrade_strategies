#!/bin/bash
# infra/cluster.sh
# Script para gerenciar e interagir com o cluster Kubernetes

set -e

usage() {
  echo "Usage: $0 {kubeconfig|nodes|pods|logs|exec <pod> <command>}"
  echo "  kubeconfig          - Gera/atualiza o kubeconfig para o cluster EKS."
  echo "  nodes               - Lista os nós do cluster."
  echo "  pods                - Lista os Pods no namespace 'freqtrade'."
  echo "  logs <pod>          - Mostra os logs do Pod especificado."
  echo "  exec <pod> <command> - Executa um comando interativo no Pod especificado."
  exit 1
}

if [ "$#" -lt 1 ]; then
  usage
fi

COMMAND=$1
NAMESPACE="freqtrade"  # Ajuste o namespace conforme necessário

case $COMMAND in
  kubeconfig)
    echo "Atualizando o kubeconfig para o cluster EKS..."
    # Substitua <cluster_name> pela sua variável ou nome do cluster
    aws eks update-kubeconfig --name <cluster_name>
    ;;
  nodes)
    echo "Listando nós do cluster..."
    kubectl get nodes
    ;;
  pods)
    echo "Listando Pods no namespace ${NAMESPACE}..."
    kubectl get pods -n ${NAMESPACE}
    ;;
  logs)
    if [ "$#" -ne 2 ]; then
      usage
    fi
    POD_NAME=$2
    echo "Exibindo logs do Pod ${POD_NAME} no namespace ${NAMESPACE}..."
    kubectl logs -n ${NAMESPACE} ${POD_NAME} --tail=100
    ;;
  exec)
    if [ "$#" -lt 3 ]; then
      usage
    fi
    POD_NAME=$2
    shift 2
    echo "Executando comando no Pod ${POD_NAME} no namespace ${NAMESPACE}..."
    kubectl exec -it -n ${NAMESPACE} ${POD_NAME} -- "$@"
    ;;
  *)
    usage
    ;;
esac
