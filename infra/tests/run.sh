#!/bin/bash
# =============================================================================
# Responsavel por configurar o ambiente de teste
# Responsavel por rodar os testes
# Responsavel por limpar o ambiente de teste
#
# /integration tests --> Testes baseados em BDD onde iremos interagir com a nossa infra apos ela subir no localstack container 
# /security tests    --> Testes de segurança onde iremos testar a segurança da nossa infra usando `checkov`
# =============================================================================

set -e

setup_env() {
    echo "=================================="
    echo "Configurando o ambiente de teste..."
    echo "=================================="
    echo "Subindo o container localstack via docker-compose..."
    docker-compose -f ../docker-compose.yml up -d localstack
    echo "Aguardando a inicialização do Localstack..."
    sleep 10
}

run_integration_tests() {
    echo "=================================="
    echo "Executando testes de integração (BDD)..."
    echo "=================================="
    # Se o behave estiver instalado e configurado, executa os testes BDD
    if command -v behave &amp;> /dev/null &amp;&amp; [ -f "integration/behave.ini" ]; then
        behave integration
    else
        echo "BDD não detectado, executando testes com pytest..."
        pytest integration
    fi
}

run_security_tests() {
    echo "=================================="
    echo "Executando testes de segurança com checkov..."
    echo "=================================="
    checkov -d ../terraform
}

cleanup_env() {
    echo "=================================="
    echo "Limpando o ambiente de teste..."
    echo "=================================="
    docker-compose -f ../docker-compose.yml down
}

# Execução das etapas de teste
setup_env
run_integration_tests
run_security_tests
cleanup_env

echo "Testes concluídos com sucesso!"