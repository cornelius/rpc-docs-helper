import yaml
from pathlib import Path
import sys

def config_file():
    return Path.home() / ".rpc_docs_helper.yaml"

class Config:
    def __init__(self):
        self.__data = {
            "clients": {
                "default": {
                    "call": []
                }
            },
            "default_client": "default"
        }
        self.client_map = {}

    def load(self):
        try:
            with open(config_file()) as stream:
                self.__data = yaml.safe_load(stream)
                clients = self.__data["clients"]
                for client in clients:
                    if "commands" in clients[client]:
                        for command in clients[client]["commands"]:
                            self.client_map[command] = client
        except FileNotFoundError:
            print("Config file '%s' not found" % config_file(), file=sys.stderr)

    def has_client(self):
        if not "clients" in self.__data:
            return False
        return self.client_call("") != []

    def set_default_client(self, value):
        self.__data["clients"][self.__data["default_client"]]["call"] = value

    def client(self, cmd, client=None):
        if client is None:
            if cmd in self.client_map:
                client = self.client_map[cmd]
            else:
                client = self.__data["default_client"]
        return self.__data["clients"][client]

    def client_call(self, cmd, client=None):
        return self.client(cmd, client=client)["call"]

    def call(self, cmd, params=[], client=None):
        full_cmd = []
        for arg in self.client_call(cmd, client=client):
            if arg == "$PARAMS":
                if params:
                    full_cmd += params
            else:
                full_arg = arg.replace("$CMD", cmd)
                if "$PARAMS_STR" in full_arg:
                    params_list = []
                    for param in params:
                        params_list.append('"' + param + '"')
                    params_str = ",".join(params_list)
                    full_arg = full_arg.replace("$PARAMS_STR", params_str)
                full_cmd.append(full_arg)
        return full_cmd

    def client_version(self, cmd):
        print("CV", cmd)
        client = self.client(cmd)
        if "version" in client:
            return client["version"]
        else:
            return None
