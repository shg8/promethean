import yaml
import jsonschema
import paramiko

from .utils import schema


class Experiment:
    def __init__(self, yaml_path: str):
        self.clients = {}
        self.yaml_path = yaml_path
        self.config = self._load_yaml()

    def _load_yaml(self):
        with open(self.yaml_path, 'r') as f:
            config = yaml.safe_load(f)

        jsonschema.validate(config, schema)
        return config

    def run(self):
        self._start_ssh()

    def _start_ssh(self):
        for node in self.config['nodes']:
            print(f"Starting ssh to {node['name']}...")

            host = node['ssh']['host']
            port = node['ssh']['port']
            username = node['ssh']['username']
            password = node['ssh']['password']

            # test ssh connection
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host, port=port, username=username, password=password)
            self.clients[node['name']] = client