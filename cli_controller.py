# Distributed under the MIT software license, see the accompanying
# file LICENSE or https://www.opensource.org/licenses/MIT.

import os
import json
import sys

from generator import Generator
from cli_caller import CliCaller
from annotations import Annotations
from help_parser import HelpParser
from references import References
from examples import Examples
from util import parse_cmd_line

class CliController:
    def __init__(self, config):
        self.config = config

    def generate(self, renderer, command=None):
        generator = Generator(CliCaller(self.config), renderer)
        if command:
            generator.generate_command(command)
        else:
            generator.generate_overview()

    def get_help(self, command):
        print(CliCaller(self.config).help(command))

    def import_see_also(self, markdown_dir, annotations_file):
        annotations = Annotations(annotations_file)
        annotations.import_see_also(markdown_dir)

    def clean_annotations(self, annotations_file):
        annotations = Annotations(annotations_file)
        annotations.clean_annotations()

    def mark_removed(self, annotations_file, version, command):
        annotations = Annotations(annotations_file)
        annotations.mark_removed(version, command)

    def mark_added(self, annotations_file, version, command):
        annotations = Annotations(annotations_file)
        annotations.mark_added(version, command)

    def show_removed(self, markdown_dir):
        commands = HelpParser().parse_help_overview(CliCaller(self.config).help()).flat()
        removed_commands = []
        for markdown_file in os.listdir(markdown_dir):
            command = os.path.splitext(markdown_file)[0]
            if not command in commands:
                removed_commands.append(command)
        for command in sorted(removed_commands):
            print(command)

    def show_missing(self, annotations_file):
        commands = HelpParser().parse_help_overview(CliCaller(self.config).help()).flat()
        annotations = Annotations(annotations_file)
        annotations.show_missing(commands)

    def update_references(self, docs_dir):
        commands = HelpParser().parse_help_overview(CliCaller(self.config).help()).flat()
        references = References(docs_dir)
        references.update(commands)

    def update_examples(self, examples_file, cmd=None):
        Examples(examples_file).update_examples(CliCaller(self.config), cmd)

    def run_example(self, examples_file, command):
        examples = Examples(examples_file)
        examples.load()
        processed_example = examples.run_example(command, CliCaller(self.config))
        json.dump(processed_example, sys.stdout, indent=2)
        print()

    def update_example_results(self, examples_file):
        examples = Examples(examples_file)
        examples.load()
        for command in examples.examples:
            examples.run_example(command, CliCaller(self.config), update=True)
        examples.save()
        examples.print_example_statistics()

    def run_command(self, rpc_cmd, client):
        result = CliCaller(self.config).call(parse_cmd_line(rpc_cmd), client=client)
        print(result)
