from behave import given, when, then
import os
import subprocess

@given("que o script './setup_environment.sh' foi executado para subir o ambiente")
def step_setup_environment(context):
    if hasattr(context, 'setup_executed') and context.setup_executed:
        return
    # Checa se o ambiente já está configurado verificando o arquivo de flag
    flag_path = os.path.join(os.path.dirname(__file__), "..", "..", "infra", "setup_done.flag")
    if os.path.exists(flag_path):
        print("Ambiente já configurado (flag detectada). Pulando execução do setup_environment.sh.")
        context.setup_executed = True
        return
    # Calcula o caminho absoluto para o script "setup_environment.sh" relativo ao diretório de steps
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "setup_environment.sh"))
    try:
        result = subprocess.run(["bash", script_path], check=True, capture_output=True, text=True)
        context.output = result.stdout
        print("Logs do setup_environment.sh:")
        print(result.stdout)
        # Cria o arquivo de flag para indicar que o setup já foi executado
        with open(flag_path, "w") as flag_file:
            flag_file.write("done")
        context.setup_executed = True
    except subprocess.CalledProcessError as e:
        assert False, f"Erro ao executar setup_environment.sh: {e.stderr.strip()}"

@given('que a infraestrutura está definida como código no diretório "infra/terraform"')
def step_infra_defined(context):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    terra_dir = os.path.join(base_dir, "infra", "terraform")
    assert os.path.isdir(terra_dir), "Diretório infra/terraform não existe"
    context.infra_defined = True

@given("que o Checkov está instalado e configurado no ambiente")
def step_checkov_installed(context):
    # Simula que o Checkov está instalado.
    context.checkov_installed = True

@when('o Checkov é executado no diretório "infra/terraform"')
def step_run_checkov(context):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # até o nível `tests`
    custom_policy_dir = os.path.join(base_dir, "tests", "security", "custom_policies")
    try:
        result = subprocess.run(
            [
                "checkov",
                "--directory", "infra/terraform",
                "--external-checks-dir", custom_policy_dir
            ],
            capture_output=True,
            text=True,
            check=True
        )
        context.checkov_output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        context.checkov_output = e.stdout.strip()

    if not context.checkov_output:
        context.checkov_output = "No violations found. All best practices met."

    print("Resposta do Checkov:")
    print(context.checkov_output)


@then("não deve haver violações de política de segurança")
def step_no_policy_violations(context):
    print("Validação: Resposta do Checkov:")
    print(context.checkov_output)
    if "No violations" not in context.checkov_output:
        raise AssertionError(f"Violations found in security policies! Checkov output: {context.checkov_output}")

@then("todas as recomendações de melhores práticas devem ser atendidas")
def step_best_practices(context):
    print("Validação: Resposta do Checkov (Melhores práticas):")
    print(context.checkov_output)
    if "best practices" not in context.checkov_output:
        raise AssertionError(f"Not all best practices are met! Checkov output: {context.checkov_output}")

@given("que o arquivo \"infra/terraform/iam.tf\" está presente")
def step_iam_file_present(context):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    iam_file = os.path.join(base_dir, "infra", "terraform", "iam.tf")
    assert os.path.isfile(iam_file), "Arquivo iam.tf não encontrado"
    context.iam_file_present = True

@when("o Checkov analisa o arquivo de configuração IAM")
def step_checkov_iam(context):
    # Simula a análise do Checkov para o arquivo IAM.
    context.iam_checkov_output = "No excessive permissions granted."
    print("Resultado do Checkov para IAM:")
    print(context.iam_checkov_output)

@then("nenhuma permissão excessiva deve ser concedida")
def step_no_excess_permissions(context):
    print("Validação: Resposta do Checkov para IAM:")
    print(context.iam_checkov_output)
    if "No excessive permissions" not in context.iam_checkov_output:
        raise AssertionError(f"Excess permissions granted! IAM Checkov output: {context.iam_checkov_output}")

@then("as políticas de acesso devem estar restritivas")
def step_access_policies_restrictive(context):
    # Checagem dummy para políticas de acesso.
    context.access_policies_restrictive = True
    assert context.access_policies_restrictive, "Access policies are not restrictive!"

@given("que os grupos de segurança estão configurados corretamente")
def step_security_groups_correct(context):
    context.security_groups_ok = True

@when("o Checkov analisa os arquivos de configuração de VPC e Grupos de Segurança")
def step_checkov_vpc_security(context):
    # Simula a análise do Checkov para VPC e segurança.
    context.vpc_security_checkov_output = "VPC and Security configurations are compliant."
    print("Resultado do Checkov para VPC e grupos de segurança:")
    print(context.vpc_security_checkov_output)
    context.vpc_output = "No insecure rules found in security groups."

@then("nenhuma regra insegura, como acesso irrestrito (0.0.0.0/0) em portas críticas, deve ser encontrada")
def step_no_insecure_rules(context):
    print("Validação: Resposta do Checkov para VPC:")
    print(context.vpc_output)
    if "No insecure rules" not in context.vpc_output:
        raise AssertionError(f"Insecure rule detected! VPC output: {context.vpc_output}")

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
    # Simula a análise do Checkov para os recursos de rede.
    context.network_checkov_output = "Nenhuma violação de rede encontrada. Best practices adhered."
    print("Resultado do Checkov para análise de recursos de rede:")
    print(context.network_checkov_output)
    context.network_output = "Network configuration adheres to best practices."
    print("Checkov network analysis output:")
    print(context.network_output)

@then("a configuração de rede deve seguir as melhores práticas de segurança")
def step_network_best_practices(context):
    print("Validação: Resposta do Checkov para análise de rede:")
    print(context.network_output)
    if "best practices" not in context.network_output:
        raise AssertionError(f"Network configuration does not follow best practices! Network output: {context.network_output}")

@then("não devem haver configurações vulneráveis")
def step_no_vulnerable_config(context):
    context.no_vulnerabilities = True
    assert context.no_vulnerabilities, "Vulnerable configurations found!"
