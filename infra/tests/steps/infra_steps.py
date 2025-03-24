import os
import subprocess
from behave import given, when, then

@given(u'que o script "./setup_environment.sh" foi executado com sucesso')
def step_executa_setup(context):
    # Calcula o caminho absoluto para o script "setup_environment.sh" relativo ao diretório de steps
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "setup_environment.sh"))
    try:
        result = subprocess.run(["bash", script_path], check=True, capture_output=True, text=True)
        context.output = result.stdout
        print("Logs do setup_environment.sh:")
        print(result.stdout)
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
    # Reexecuta o setup para garantir que o ambiente esteja configurado
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "setup_environment.sh"))
    try:
        result = subprocess.run(["bash", script_path], check=True, capture_output=True, text=True)
        context.output = result.stdout
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