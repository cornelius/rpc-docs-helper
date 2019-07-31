from pathlib import Path
import pytest
import subprocess

from config import Config

from cli_caller import CliCaller

def create_config():
    config = Config()
    config.set_default_client([str(Path(__file__).parent / "dummy_cli"), "$CMD", "$PARAMS"])
    return config

def test_call_pass():
    caller = CliCaller(create_config())

    result = caller.call(["z"])

    assert result == "pass"

def test_call_fail():
    caller = CliCaller(create_config())

    with pytest.raises(CliCaller.Error) as e:
        caller.call(["fail"])

    assert e.value.message == "fail"
    assert e.value.exit_code == 1

def test_extract_error_message():
    message = "error code: -8\nerror message:\nfail"
    assert CliCaller(create_config()).extract_error_message(message) == "fail"

def test_call_stubbed(mocker):
    mocker.patch("subprocess.check_output")

    config = Config()
    config.set_default_client(["dummy_cli", "$CMD", "$PARAMS"])

    cli = CliCaller(config)
    cli.call(["cmd", "arg one", "arg2"])

    subprocess.check_output.assert_called_once_with(["dummy_cli",
            "cmd", "arg one", "arg2"], stderr=subprocess.STDOUT)

def test_help(mocker):
    mocker.patch("subprocess.check_output")

    config = Config()
    config.set_default_client(["dummy_cli", "$CMD", "$PARAMS"])

    cli = CliCaller(config)
    cli.help("cmd")

    subprocess.check_output.assert_called_once_with(["dummy_cli",
            "help", "cmd"], stderr=subprocess.STDOUT)

def test_curl(mocker):
    mocker.patch("subprocess.check_output")

    config = Config()
    config.set_default_client(["curl", "--data", '{"method":"$CMD","params":[$PARAMS_STR]}'])

    cli = CliCaller(config)
    cli.call(["cmd"])

    subprocess.check_output.assert_called_once_with(["curl", "--data",
            '{"method":"cmd","params":[]}'], stderr=subprocess.STDOUT)

def test_curl_params(mocker):
    mocker.patch("subprocess.check_output")

    config = Config()
    config.set_default_client(["curl", "--data", '{"method":"$CMD","params":[$PARAMS_STR]}'])

    cli = CliCaller(config)
    cli.call(["cmd", "arg one", "arg2"])

    subprocess.check_output.assert_called_once_with(["curl", "--data",
            '{"method":"cmd","params":["arg one","arg2"]}'], stderr=subprocess.STDOUT)
