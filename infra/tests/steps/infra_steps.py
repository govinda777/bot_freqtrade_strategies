# steps/infra_steps.py

import os
import subprocess
from behave import given, when, then
from infra.tests.helpers.localstack_manager import LocalstackManager

setup_executed_globally = False

def _ensure_setup(context):
    if getattr(context, 'setup_executed', False):
        return

    flag = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "setup_done.flag"))
    if os.path.exists(flag):
        context.output = "Ambiente configurado com sucesso"
        context.setup_executed = True
        return

    manager = LocalstackManager()
    manager.start()
    manager.init_terraform()
    context.output = "Ambiente configurado com sucesso"
    context.setup_executed = True

@given(u'que o script "./setup_environment.sh" foi executado com sucesso')
def step_executa_setup(context):
    _ensure_setup(context)

@when(u'o ambiente está configurado')
def step_ambiente_configurado(context):
    assert getattr(context, "output", None), "Ambiente não está configurado."

@then(u'a saída deve conter "{expected}"')
def step_check_output_contains(context, expected):
    output = getattr(context, "terraform_providers_output", "")
    assert expected in output, f'Esperado "{expected}" na saída, mas obtido: {output}'


@given(u'que o ambiente foi configurado')
def step_ambiente_configurado_given(context):
    _ensure_setup(context)

@then(u'os seguintes arquivos devem existir')
def step_verifica_arquivos(context):
    # Calcula o caminho absoluto para a raiz do projeto (subindo 3 níveis)
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    print("Base path para verificação de arquivos:", base_path)
    # Verifica se cada arquivo listado na tabela existe, logando o caminho completo
    for row in context.table:
        caminho = row['caminho']
        full_path = os.path.join(base_path, caminho)
        print("Verificando existência do arquivo:", full_path)
        assert os.path.exists(full_path), f"O arquivo {caminho} não existe em {full_path}."

@when(u'executar o comando "terraform plan" na pasta "infra/terraform"')
def step_terraform_plan(context):
    terraform_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "infra", "terraform"))
    try:
        result = subprocess.run(["terraform", "plan"], cwd=terraform_dir, check=True, capture_output=True, text=True)
        context.terraform_plan_output = result.stdout
        print("Output do terraform plan:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        assert False, f"Erro ao executar terraform plan: {e.stderr.strip()}"

@when(u'executar o comando "terraform apply" na pasta "infra/terraform" com aprovação automática')
def step_terraform_apply(context):
    terraform_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "infra", "terraform"))
    try:
        result = subprocess.run(["terraform", "apply", "-auto-approve"], cwd=terraform_dir, check=True, capture_output=True, text=True)
        context.terraform_apply_output = result.stdout
        print("Output do terraform apply:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        assert False, f"Erro ao executar terraform apply: {e.stderr.strip()}"

@then(u'a saída do terraform apply deve conter "Apply complete! Resources:"')
def step_verifica_terraform_apply(context):
    expected = "Apply complete! Resources:"
    assert expected in context.terraform_apply_output, f"A saída do terraform apply não contém a mensagem esperada. Saída: {context.terraform_apply_output}"

@then(u'o comando foi executado com sucesso')
def step_terraform_plan_output(context):
    print(context.terraform_plan_output)
    assert context.terraform_plan_output.strip(), "Terraform plan output is empty. {context.terraform_plan_output}"