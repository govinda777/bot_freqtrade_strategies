import os
import subprocess
from behave import given, when, then

@when(u'eu setar o provider AWS para versão "{versao}"')
def step_set_provider_version(context, versao):
    tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    terraform_dir = os.path.abspath(os.path.join(tests_dir, "..", "terraform"))
    script_path = os.path.join(tests_dir, "set_provider_version.sh")
    
    subprocess.run(["bash", script_path, versao], cwd=terraform_dir, check=True)

@when(u'executar "terraform init -upgrade" e "terraform plan"')
def step_init_and_plan(context):
    terraform_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "infra", "terraform"))
    subprocess.run(["terraform", "init", "-upgrade"], cwd=terraform_dir, check=True)
    result = subprocess.run(["terraform", "plan"], cwd=terraform_dir, check=True, capture_output=True, text=True)
    context.terraform_plan_output = result.stdout
    print(result.stdout)
