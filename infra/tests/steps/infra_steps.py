import os
import subprocess
from behave import given, when, then
setup_executed_globally = False

@given(u'que o script "./setup_environment.sh" foi executado com sucesso')
def step_executa_setup(context):
    if hasattr(context, 'setup_executed') and context.setup_executed:
        return
    # Calcula o caminho absoluto para o script "setup_environment.sh" relativo ao diretório de steps
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "setup_environment.sh"))
    try:
        result = subprocess.run(["bash", script_path], check=True, capture_output=True, text=True)
        context.output = result.stdout
        print("Logs do setup_environment.sh:")
        print(result.stdout)
        context.setup_executed = True
    except subprocess.CalledProcessError as e:
        assert False, f"Erro ao executar setup_environment.sh: {e.stderr.strip()}"

@when(u'o ambiente está configurado')
def step_ambiente_configurado(context):
    # Verifica se o ambiente foi configurado a partir do output do script
    assert hasattr(context, "output") and context.output, "O ambiente não foi configurado."

@then(u'a saída deve conter "Ambiente configurado com sucesso"')
def step_verifica_saida(context):
    expected = "Ambiente configurado com sucesso"
    assert expected in context.output, f"A saída não contém a mensagem esperada. Saída: {context.output}"

@given(u'que o ambiente foi configurado')
def step_ambiente_configurado_given(context):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    setup_flag = os.path.join(base_dir, "setup_done.flag")
    if os.path.exists(setup_flag):
        with open(setup_flag, "r") as f:
            context.output = f.read()
        context.setup_executed = True
        print("Setup already executed, reading cached output.")
        return
    script_path = os.path.join(base_dir, "setup_environment.sh")
    try:
        result = subprocess.run(["bash", script_path], check=True, capture_output=True, text=True)
        context.output = result.stdout
        with open(setup_flag, "w") as f:
            f.write(result.stdout)
        print("Logs do setup_environment.sh:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        assert False, "O ambiente não foi configurado."

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