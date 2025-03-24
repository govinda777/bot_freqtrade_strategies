"""
Arquivo de configuração do Behave para gerenciamento do container Localstack nos testes BDD.
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from infra.tests.helpers import localstack_manager
from infra.tests.helpers.localstack_manager import LocalstackManager

def before_all(context):
    """
    Inicia o container Localstack antes de todos os testes.
    """
    manager = LocalstackManager()
    manager.start()
    manager.init_terraform()
    context.localstack = manager

def after_all(context):
    """
    Finaliza e remove o container Localstack após a execução de todos os testes.
    """
    localstack_manager.stop_localstack_container()