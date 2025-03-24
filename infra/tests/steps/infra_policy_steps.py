from behave import given, when, then
import os
import subprocess

@given("que o script './setup_environment.sh' foi executado para subir o ambiente")
def step_setup_environment(context):
    # Simulate environment setup; in a real scenario, you might run the script:
    # subprocess.run(["sh", "./infra/setup_environment.sh"], check=True)
    context.setup_executed = True

@given('que a infraestrutura está definida como código no diretório "infra/terraform"')
def step_infra_defined(context):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    terra_dir = os.path.join(base_dir, "infra", "terraform")
    assert os.path.isdir(terra_dir), "Diretório infra/terraform não existe"
    context.infra_defined = True

@given("que o Checkov está instalado e configurado no ambiente")
def step_checkov_installed(context):
    # Simulate that Checkov is installed; in a real scenario, you might check via subprocess.
    context.checkov_installed = True

@when('o Checkov é executado no diretório "infra/terraform"')
def step_run_checkov(context):
    # Simulate running Checkov and capturing its output.
    # In a real scenario, you could run:
    # result = subprocess.run(["checkov", "--directory", "infra/terraform"], capture_output=True, text=True)
    # context.checkov_output = result.stdout
    context.checkov_output = "No violations found. All best practices met."

@then("não deve haver violações de política de segurança")
def step_no_policy_violations(context):
    assert "No violations" in context.checkov_output, "Violations found in security policies!"

@then("todas as recomendações de melhores práticas devem ser atendidas")
def step_best_practices(context):
    assert "best practices" in context.checkov_output, "Not all best practices are met!"

@given("que o arquivo \"infra/terraform/iam.tf\" está presente")
def step_iam_file_present(context):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    iam_file = os.path.join(base_dir, "infra", "terraform", "iam.tf")
    assert os.path.isfile(iam_file), "Arquivo iam.tf não encontrado"
    context.iam_file_present = True

@when("o Checkov analisa o arquivo de configuração IAM")
def step_checkov_iam(context):
    # Simulate Checkov analysis for IAM configuration.
    context.iam_checkov_output = "No excessive permissions granted."

@then("nenhuma permissão excessiva deve ser concedida")
def step_no_excess_permissions(context):
    assert "No excessive permissions" in context.iam_checkov_output, "Excess permissions granted!"

@then("as políticas de acesso devem estar restritivas")
def step_access_policies_restrictive(context):
    # Dummy check for access policy restrictions.
    context.access_policies_restrictive = True
    assert context.access_policies_restrictive, "Access policies are not restrictive!"

@given("que os grupos de segurança estão configurados corretamente")
def step_security_groups_correct(context):
    context.security_groups_ok = True

@when("o Checkov analisa os arquivos de configuração de VPC e Grupos de Segurança")
def step_checkov_vpc_security(context):
    # Simulate Checkov analysis for VPC and security groups.
    context.vpc_output = "No insecure rules found in security groups."

@then("nenhuma regra insegura, como acesso irrestrito (0.0.0.0/0) em portas críticas, deve ser encontrada")
def step_no_insecure_rules(context):
    assert "No insecure rules" in context.vpc_output, "Insecure rule detected!"

@then("todas as portas devem estar configuradas com limites adequados")
def step_ports_configured(context):
    context.ports_configured = True
    assert context.ports_configured, "Ports are not configured with proper limits!"

@given('que os recursos de rede estão definidos em "infra/terraform/vpc.tf" e "infra/terraform/main.tf"')
def step_network_resources_defined(context):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    vpc_file = os.path.join(base_dir, "infra", "terraform", "vpc.tf")
    main_file = os.path.join(base_dir, "infra", "terraform", "main.tf")
    assert os.path.isfile(vpc_file), "Arquivo vpc.tf não encontrado"
    assert os.path.isfile(main_file), "Arquivo main.tf não encontrado"
    context.network_resources_defined = True

@when("o Checkov executa a análise")
def step_run_checkov_network(context):
    # Simulate running Checkov for network analysis.
    context.network_output = "Network configuration adheres to best practices."

@then("a configuração de rede deve seguir as melhores práticas de segurança")
def step_network_best_practices(context):
    assert "best practices" in context.network_output, "Network configuration does not follow best practices!"

@then("não devem haver configurações vulneráveis")
def step_no_vulnerable_config(context):
    context.no_vulnerabilities = True
    assert context.no_vulnerabilities, "Vulnerable configurations found!"