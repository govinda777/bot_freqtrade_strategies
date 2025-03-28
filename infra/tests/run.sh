#!/bin/bash
set -e
cd "$(dirname "$0")"

# Executa os testes BDD para a infraestrutura
# Considerando que o arquivo de feature está em "infra_tests.feature"
# e os step definitions estão em "steps" (diretório atual/steps)


#behave infra.feature
#behave infra_tests_policy.feature
behave infra_provider.feature