# Distributed under the MIT software license, see the accompanying
# file LICENSE or https://www.opensource.org/licenses/MIT.

import subprocess
import sys

class CliCaller:
    class Error(Exception):
        def __init__(self, message, exit_code):
            self.message = message
            self.exit_code = exit_code

    def __init__(self, config):
        self.config = config
        if not config.has_client():
            sys.exit("RPC command is not set. Set it in ~/.rpc_doc_helper.yaml.")

    def client_version(self, cmd):
        return self.config.client_version(cmd)

    def extract_error_message(self, full_message):
        return full_message[full_message.find("\n", full_message.find("\n") + 1) + 1:]

    def call(self, rpc_cmd, client=None):
        cmd = rpc_cmd[0]
        args = rpc_cmd[1:]
        full_cmd = self.config.call(cmd, args, client=client)
        try:
            result = subprocess.check_output(full_cmd, stderr=subprocess.STDOUT)
            return result.rstrip().decode("utf-8")
        except subprocess.CalledProcessError as e:
            message = self.extract_error_message(e.output.rstrip().decode("utf-8"))
            raise CliCaller.Error(message, e.returncode)

    def help(self, cmd=None):
        arg = ["help"]
        if cmd:
            arg.append(cmd)
        return self.call(arg)
