from config import Config
from pathlib import Path

def test_config(mocker):
    config_file = Path(__file__).parent / "test_data" / "config.yaml"
    mocker.patch("config.config_file", return_value=config_file)

    config = Config()
    config.load()

    assert config.has_client() == True

    assert config.call("cmd") == ["bitcoin-cli", "-regtest", "cmd"]
    assert config.call("cmd", ["param1", "param2"]) == ["bitcoin-cli", "-regtest", "cmd", "param1", "param2"]
    assert config.call("cmd", ["param1 param2"]) == ["bitcoin-cli", "-regtest", "cmd", "param1 param2"]
    assert config.call("cmd2", ["param1", "param2"]) == ["curl", "--data", '{"method":"cmd2","params":["param1","param2"]}']

def test_config_no_file(mocker):
    config_file = Path("doesnotexist")
    mocker.patch("config.config_file", return_value=config_file)

    config = Config()
    config.load()

    assert config.has_client() == False

def test_set_rpc_cmd():
    config = Config()
    assert config.call("y") != ["x"]

    config.set_default_client(["x"])
    assert config.call("y") == ["x"]

    config.set_default_client(["x", "$CMD"])
    assert config.call("y") == ["x", "y"]

    config.set_default_client(["x", "$CMD", "$PARAMS"])
    assert config.call("y", ["z"]) == ["x", "y", "z"]

def test_substitutions_cmd():
    config = Config()

    config.set_default_client(['"$CMD"'])
    assert config.call("x") == ['"x"']

def test_substitutions_params_str():
    config = Config()

    config.set_default_client(['[$PARAMS_STR]'])
    assert config.call("x", ["y"]) == ['["y"]']
    assert config.call("x", ["y", "z"]) == ['["y","z"]']

def test_substitutions_cmd_params_str():
    config = Config()

    config.set_default_client(['"$CMD", [$PARAMS_STR]'])
    assert config.call("x", ["y"]) == ['"x", ["y"]']
    assert config.call("x", ["y", "z"]) == ['"x", ["y","z"]']

def test_client_version(mocker):
    config_file = Path(__file__).parent / "test_data" / "config.yaml"
    mocker.patch("config.config_file", return_value=config_file)

    config = Config()
    config.load()

    assert config.client_version("cmd") == None
    assert config.client_version("cmd2") == "0.17.1"
