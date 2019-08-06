from renderer_html import RendererHtml

from renderer_rst import RendererRst
from help_parser import HelpParser, CommandList
from pathlib import Path
import os

test_data_dir = Path(os.path.dirname(__file__)) / "test_data"


def command_list():
    commands = CommandList()
    commands.add("Blockchain", "getblock")
    commands.add("Blockchain", "getblockhash")
    commands.add("Control", "getrpcinfo")
    return commands


def test_render_nav():
    renderer = RendererHtml()
    renderer.command_list = command_list()

    html = renderer.render_nav()
    assert "Blockchain" in html
    assert "getblock" in html


def test_render_command():
    renderer = RendererHtml()
    renderer.command_list = command_list()

    cmd = "getblockstats"
    with open(str(test_data_dir / cmd)) as file:
        input = file.read()
        help_data = HelpParser().parse_help_command(input)
    with open(str(test_data_dir / "html" / (cmd + ".html"))) as file:
        expected_output = file.read()
    html = renderer.render_command(cmd, help_data)
    print(html)
    assert html == expected_output


def test_render_page():
    expected = '''<html>
  dummy
</html>
'''
    html = RendererHtml().render_page("dummy", template_file="test.html")
    assert html == expected
