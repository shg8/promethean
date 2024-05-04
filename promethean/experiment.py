import os
import re

import yaml
import jsonschema
import paramiko

from .utils import schema, slugify


def _format_step_name(param: dict) -> str:
    name = ""
    for key, value in param.items():
        # ensure value is filename safe
        key = slugify(key)
        value = slugify(value)
        name += f"{key}_{value}_"
    return name[:-1]


def _generate_values(knob) -> list:
    if knob['type'] == 'int':
        return list(range(knob['min'], knob['max'], knob['interval']))
    elif knob['type'] == 'float':
        return [knob['min'] + i * knob['interval'] for i in
                range(int((knob['max'] - knob['min']) / knob['interval']))]
    elif knob['type'] == 'bool':
        return [True, False]
    elif knob['type'] == 'string':
        return knob['values']

    raise ValueError(f"Invalid knob type: {knob['type']}")


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
        # create output directory if not exists
        output = self.config['output']
        if not os.path.exists(output):
            os.makedirs(output)

        self._start_ssh()
        self._run_procedure()

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

    def _run_procedure(self):
        self._run_matrix(self.config['matrix'], depth=0, params={})

    def _run_step(self, step, param):
        step_folder = self._get_step_folder(step, param)

        for node in self.config['nodes']:
            vars = node['variables'].copy()
            vars.update(param)

            print(f"Running step {step['name']} on {node['name']}...")
            client = self.clients[node['name']]
            if "script" in step:
                stdin, stdout, stderr = client.exec_command(self._parse(vars, step['script']))
                out = stdout.read().decode()
                err = stderr.read().decode()
                exit_status = stdout.channel.recv_exit_status()

                with open(os.path.join(step_folder, "stdout.txt"), 'w') as f:
                    f.write(out)
                with open(os.path.join(step_folder, "stderr.txt"), 'w') as f:
                    f.write(err)
                with open(os.path.join(step_folder, "exit_status.txt"), 'w') as f:
                    f.write(str(exit_status))
            elif "file" in step:
                files = {}
                if isinstance(step['file'], str):
                    fn = self._parse(node['variables'], step['file'])
                    files[slugify(fn)] = fn
                else:
                    for f in step['file']:
                        files[slugify(f['alias'])] = self._parse(vars, f['path'])

                for alias, remote_path in files.items():
                    remote_path = self._parse(vars, remote_path)
                    sftp = client.open_sftp()
                    try:
                        sftp.get(remote_path, os.path.join(step_folder, alias))
                    except IOError:
                        print(f"File {remote_path} not found.")
                    sftp.close()

        print(f"Step {step['name']} completed.")

    def _run_matrix(self, matrix: list, depth: int, params: dict):
        if depth == len(matrix):
            for step in self.config['steps']:
                print(f"Running step {step['name']}...")
                self._run_step(step, params)
            return

        knob_id = matrix[depth]
        knob = next(k for k in self.config['knobs'] if k['name'] == knob_id)
        knob_name = knob['name']
        if "values" in knob:
            values = knob['values']
        else:
            values = _generate_values(knob)

        for value in values:
            params[knob_name] = value
            self._run_matrix(matrix, depth + 1, params)

    def _get_step_folder(self, step, param) -> str:
        folder = os.path.join(str(self.config['output']), slugify(step['name']), _format_step_name(param))
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder

    def _parse(self, variables: dict, str_to_format: str) -> str:
        # replace {{variable}} with value
        for key, value in variables.items():
            str_to_format = re.sub(rf"{{{{\s*{key}\s*}}}}", str(value), str_to_format)
        return str_to_format
