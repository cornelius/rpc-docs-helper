import json
import subprocess

from help_parser import HelpParser
from cli_caller import CliCaller
from util import parse_cmd_line

class Examples:
    def __init__(self, filename):
        self.filename = filename
        self.examples = {}

    def parse_example_line(self, line):
        return parse_cmd_line(line)

    def extract_examples(self, help_data):
        prefix = "> bitcoin-cli"
        examples = []
        for line in help_data["examples"]:
            example = {"text": line}
            if line.startswith(prefix):
                example["cmd"] = self.parse_example_line(line[len(prefix)+1:])
            examples.append(example)
        return examples

    def parse_example(self, cli, command):
        command_output = cli.help(command)
        help_data = HelpParser().parse_help_command(command_output)
        return self.extract_examples(help_data)

    def load(self):
        with open(self.filename) as file:
            self.examples = json.load(file)

    def save(self):
        with open(self.filename, "w") as file:
            file.write(json.dumps(self.examples, indent=2, sort_keys=True))

    def update_examples(self, cli, cmd=None):
        try:
            self.load()
        except FileNotFoundError:
            print(f"Creating examples file '{self.filename}'")

        if cmd:
            self.examples[cmd] = self.parse_example(cli, cmd)
        else:
            help_output = cli.help()
            command_list = HelpParser().parse_help_overview(help_output)
            for command in command_list.flat():
                self.examples[command] = self.parse_example(cli, command)

        self.save()

    def run_example(self, command, cli_caller, update=False):
        print(f"Run examples for command {command}")
        if command == "encryptwallet":
            print("  Warning: skipping command '%s'" % command)
            return self.examples[command]
        example = self.examples[command]
        processed_example = []
        for line in example:
            if "cmd" in line:
                result = {}
                print("  CMD", line["cmd"])
                try:
                    cmd_result = cli_caller.call(line["cmd"])
                    result["exit_code"] = 0
                    if len(cmd_result) > 500:
                        print("  Warning: truncating output")
                        cmd_result = cmd_result[:500] + " ..."
                    result["output"] = cmd_result
                except CliCaller.Error as e:
                    result["exit_code"] = e.exit_code
                    result["output"] = e.message
                if cli_caller.client_version(command):
                    result["client_version"] = cli_caller.client_version(line["cmd"][0])
                line["result"] = result
                processed_example.append(line)
            else:
                processed_example.append(line)
        if update:
            self.examples[command] = processed_example
        return processed_example

    def print_example_statistics(self):
        print(f"Total commands: {len(self.examples)}")
        exit_codes = {}
        for command in self.examples:
            for line in self.examples[command]:
                if "result" in line:
                    exit_code = line["result"]["exit_code"]
                    if exit_code in exit_codes:
                        exit_codes[exit_code] += 1
                    else:
                        exit_codes[exit_code] = 1
        print("Exit codes:")
        for exit_code in sorted(exit_codes):
            print(f"  {exit_code}: {exit_codes[exit_code]}")
