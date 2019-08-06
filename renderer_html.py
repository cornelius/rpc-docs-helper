from bottle import template
from pathlib import Path
from help_parser import CommandList
import json

class RendererHtml:
    def __init__(self):
        self.command_list = CommandList()
        self.html_nav = ""

    def render_page(self, content, template_file="layout.html"):
        template_path = Path(__file__).parent / "templates" / template_file
        with template_path.open() as f:
            return template(f.read(), nav=self.render_nav(), content=content)

    def render_index(self):
        return self.render_page(self.content_index())

    def content_index(self):
        return "CONTENT"

    def render_nav(self):
        if not self.html_nav:
            o = ""
            for group in self.command_list.grouped():
                o += "<h2>" + group + "</h2>\n"
                o += "<ul>\n"
                for command in self.command_list.grouped()[group]:
                    cmd = command.split()[0]
                    o += "<li><a href='/cmd/" + cmd + "'>" + cmd + "</a></li>\n"
                o += "</ul>\n"
            self.html_nav = o
        return self.html_nav

    def render_command(self, command, help_data, result_out=None, result_cmd=None):
        return self.render_page(self.content_cmd(command, help_data, result_out, result_cmd))

    def format_result(self, result):
        if result.startswith("[") or result.startswith("{"):
            json_data = json.loads(result)
            return json.dumps(json_data, indent=2)
        else:
            return result

    def render_table(self, table):
        o = "<table>\n"
        o += "<tr><th>Name</th><th>Type</th><th>Description</th></tr>\n"
        for row in table:
            o += f"<tr><td>{row['name']}</td><td>{row['type']}</td><td>{row['description']}</td></tr>\n"
        o += "</table>\n"
        return o

    def content_cmd(self, command, help_data, result_out, result_cmd):
        o = "<h2>" + command + "</h2>\n"

        o += "<p><em>" + help_data["command"] + "</em></p>\n"

        o += "<p>" + help_data["description"] + "</p>\n"

        arguments = help_data["arguments"]
        if arguments:
            o += "<h3>Arguments</h3>\n"
            o += self.render_table(arguments)

        results = help_data["results"]
        if results:
            for result in results:
                o += "<h3>Result " + result["title_extension"] + "</h4>\n"
                if result["format"] == "literal":
                    o += "<pre>\n" + result["text"] + "</pre>\n"
                elif result["format"] == "table":
                    o += "<table>\n"
                    o += "<tr><th>Name</th><th>Type</th><th>Description</th></tr>\n"
                    o += f"<tr><td>{result['name']}</td><td>{result['type']}</td><td>{result['description']}</td></tr>\n"
                    o += "</table>\n"

        examples = help_data["examples"]
        if examples:
            o += "<h3>Examples</h3>"
            for example in examples:
                if not example.startswith("> curl"):
                    o += "<p>" + example + "</p>\n"

        o += "<hr/>"

        o += "<form action='/cmd/" + command + "' method='post'>\n"
        o += f"<input type='hidden' name='cmd' value='{command}'>\n"
        for index, argument in enumerate(arguments):
            o += argument["name"] + " (" + argument["description"] + ")"
            if "required" in argument["type"]:
                o += " <b>(required)</b>"
            o += "<br>\n"
            o += "<input type='text' name='arg-" + str(index) + "'"
            if "required" in argument["type"]:
                o += " required"
            o += "><br>\n"
        o += "<input type='submit' value='Run Command'>\n"
        o += "</form>\n"

        if result_out:
            o += "<h3>Result</h3>\n"
            o += "<p>" + result_cmd + "</p>"
            o += "<pre>\n"
            o += self.format_result(result_out) + "\n"
            o += "</pre>\n"

        return o
