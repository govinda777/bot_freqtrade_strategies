# localstack_manager.py

import os
import subprocess
import time
import json
import requests
from threading import Lock

class LocalstackManager:
    _instance = None
    _lock = Lock()

    CONTAINER_NAME = "localstack_main"
    CONTAINER_PORT = os.getenv("CONTAINER_PORT", "4566")
    HOST_LOCALSTACK_PORT = os.getenv("HOST_LOCALSTACK_PORT", "4566")
    TERRAFORM_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "terraform"))

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LocalstackManager, cls).__new__(cls)
                cls._instance._started = False
        return cls._instance

    def start(self):
        if self._started:
            print("Localstack já iniciado.")
            return

        if not self._is_running():
            self._remove_container()
            self._start_container()
            self._wait_for_health()

        self._started = True

    def stop(self):
        subprocess.run(["docker", "stop", self.CONTAINER_NAME], check=False)
        subprocess.run(["docker", "rm", self.CONTAINER_NAME], check=False)
        self._started = False

    def init_terraform(self):
        print("Inicializando e aplicando Terraform...")
        env = os.environ.copy()
        env.update({
            "AWS_ACCESS_KEY_ID": "test",
            "AWS_SECRET_ACCESS_KEY": "test",
            "AWS_DEFAULT_REGION": "us-east-1",
            "TF_VAR_db_password": os.getenv("TF_VAR_db_password", ""),
            "LOCALSTACK_API_KEY": os.getenv("LOCALSTACK_API_KEY", "")
        })

        subprocess.run(["terraform", "-chdir=" + self.TERRAFORM_DIR, "init", "-upgrade"], check=True, env=env)
        subprocess.run(["terraform", "-chdir=" + self.TERRAFORM_DIR, "apply", "-auto-approve"], check=True, env=env)

        # Flag para evitar setups repetidos
        flag_path = os.path.join(os.path.dirname(__file__), "..", "..", "setup_done.flag")
        with open(flag_path, "w") as f:
            f.write("done")

    def _is_running(self):
        try:
            inspect = subprocess.run(["docker", "inspect", self.CONTAINER_NAME], check=True, stdout=subprocess.PIPE)
            container = json.loads(inspect.stdout.decode())[0]
            return container["State"]["Running"]
        except:
            return False

    def _remove_container(self):
        subprocess.run(["docker", "rm", "-f", self.CONTAINER_NAME], check=False)
        time.sleep(2)

    def _start_container(self):
        subprocess.run(
            ["docker", "run", "-d", "--name", self.CONTAINER_NAME,
             "-p", f"{self.HOST_LOCALSTACK_PORT}:{self.CONTAINER_PORT}",
             "-p", "4510-4559:4510-4559",
             "localstack/localstack"],
            check=True
        )
        time.sleep(5)

    def _wait_for_health(self, timeout=60):
        for _ in range(timeout):
            try:
                r = requests.get(f"http://localhost:{self.HOST_LOCALSTACK_PORT}/health")
                if r.status_code == 200:
                    print("Localstack está pronto.")
                    return
            except:
                pass
            time.sleep(1)
        raise RuntimeError("Timeout esperando Localstack.")
