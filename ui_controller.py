from renderer_html import RendererHtml
from cli_caller import CliCaller
from cli_bitcoin import CliBitcoin
from help_parser import HelpParser
import pprint

def parse_args(response):
    index = 0
    args = []
    while(True):
        arg_name = "arg-" + str(index)
        if arg_name in response:
            arg_value = response[arg_name]
            if arg_value:
                args.append(arg_value)
            index += 1
        else:
            break
    return args

class UiController:
    def __init__(self):
        self.renderer = RendererHtml()
        self.cli = CliCaller(CliBitcoin())
        help_output = self.cli.help()
        command_list = HelpParser().parse_help_overview(help_output)
        self.renderer.command_list = command_list

    def index(self):
        return self.renderer.render_index()

    def cmd(self, command, response=None):
        command_output = self.cli.help(command)
        help_data = HelpParser().parse_help_command(command_output)
        pprint.pprint(help_data)
        if response:
            cmd_args = [response.get("cmd")] + parse_args(response)
            print("ARGS", cmd_args)
            result_cmd = " ".join(cmd_args)
            result_out = self.cli.call(cmd_args)
        else:
            result_out = None
            result_cmd = None
        return self.renderer.render_command(command, help_data, result_out, result_cmd)
