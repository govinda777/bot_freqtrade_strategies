import os
import subprocess
from behave import when, then

def after_scenario(context, scenario):
    if hasattr(context, "terraform_providers_output"):
        print("===== PROVIDERS FINAL =====")
        print(context.terraform_providers_output)

@when(u'eu setar o provider AWS para versão "{versao}"')
def step_set_provider_version(context, versao):
    tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    terraform_dir = os.path.abspath(os.path.join(tests_dir, "..", "terraform"))
    script_path = os.path.join(tests_dir, "set_provider_version.sh")
    subprocess.run(["bash", script_path, versao], cwd=terraform_dir, check=True)

@when(u'executar "terraform init -upgrade" e "terraform plan"')
def step_terraform_plan(context):
    terraform_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "infra", "terraform")
    )

    subprocess.run(["terraform", "init", "-upgrade"], cwd=terraform_dir, check=True)
    result = subprocess.run(
        ["terraform", "plan"],
        cwd=terraform_dir,
        check=True,
        capture_output=True,
        text=True
    )
    context.terraform_plan_output = result.stdout
    print("===== PLAN EXECUTADO =====")

@then(u'o terraform plan foi executado com sucesso')
def step_check_plan_output(context):
    assert context.terraform_plan_output.strip(), "Terraform plan output is empty."

@when(u'executar "terraform apply" com aprovação automática')
def step_terraform_apply(context):
    terraform_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "infra", "terraform")
    )
    result = subprocess.run(
        ["terraform", "apply", "-auto-approve"],
        cwd=terraform_dir,
        check=True,
        capture_output=True,
        text=True
    )
    context.terraform_apply_output = result.stdout
    print("===== APPLY EXECUTADO =====")

@then(u'o terraform apply foi executado com sucesso')
def step_check_apply_output(context):
    assert context.terraform_apply_output.strip(), "Terraform apply output is empty."

@when(u'executar "terraform providers"')
def step_terraform_providers(context):
    terraform_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "infra", "terraform")
    )
    result = subprocess.run(
        ["terraform", "providers"],
        cwd=terraform_dir,
        check=True,
        capture_output=True,
        text=True
    )
    
    output = result.stdout.strip() or result.stderr.strip()
    context.terraform_providers_output = output
    print("===== PROVIDERS EVIDÊNCIA =====")
    print(output)

@then(u'a saída do terraform providers deve conter "{expected}"')
def step_check_providers_output(context, expected):
    output = getattr(context, "terraform_providers_output", "")
    assert expected in output, f'Esperado "{expected}" na saída, mas obtido: {output}'
