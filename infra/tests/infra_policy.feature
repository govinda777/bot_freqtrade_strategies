# language: pt
# ATENÇÃO: Execute "./setup_environment.sh" para configurar o ambiente antes de executar os testes
Funcionalidade: Validação de Segurança da Infraestrutura com Checkov

  Contexto:
    Dado que o script './setup_environment.sh' foi executado para subir o ambiente
    E que a infraestrutura está definida como código no diretório "infra/terraform"
    E que o Checkov está instalado e configurado no ambiente

  Cenário: Verificar políticas de segurança gerais
    Quando o Checkov é executado no diretório "infra/terraform"
    Então não deve haver violações de política de segurança
    E todas as recomendações de melhores práticas devem ser atendidas

  Cenário: Verificar configurações de IAM
    Dado que o arquivo "infra/terraform/iam.tf" está presente
    Quando o Checkov analisa o arquivo de configuração IAM
    Então nenhuma permissão excessiva deve ser concedida
    E as políticas de acesso devem estar restritivas

  Cenário: Verificar regras de Grupos de Segurança
    Dado que os grupos de segurança estão configurados corretamente
    Quando o Checkov analisa os arquivos de configuração de VPC e Grupos de Segurança
    Então nenhuma regra insegura, como acesso irrestrito (0.0.0.0/0) em portas críticas, deve ser encontrada
    E todas as portas devem estar configuradas com limites adequados

  Cenário: Validação de recursos de rede e sub-redes
    Dado que os recursos de rede estão definidos em "infra/terraform/vpc.tf" e "infra/terraform/main.tf"
    Quando o Checkov executa a análise
    Então a configuração de rede deve seguir as melhores práticas de segurança
    E não devem haver configurações vulneráveis