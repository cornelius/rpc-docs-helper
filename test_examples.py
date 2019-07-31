import json
from pathlib import Path

from examples import Examples

def test_extract_examples():
    help_data = {
        "examples": [
            'Encrypt your wallet',
            '> bitcoin-cli encryptwallet "my pass phrase"',
            'Now lock the wallet again by removing the passphrase',
            '> bitcoin-cli walletlock ',
            'As a JSON-RPC call',
            '> curl --user myusername --data-binary \'{"jsonrpc": "1.0", "id":"curltest", "method": "encryptwallet", "params": ["my pass phrase"] }\' -H \'content-type: text/plain;\' http://127.0.0.1:8332/'
        ]
    }
    expected = [
        {
            'text': 'Encrypt your wallet',
        },
        {
            'text': '> bitcoin-cli encryptwallet "my pass phrase"',
            'cmd': ['encryptwallet', 'my pass phrase'],
        },
        {
            'text': 'Now lock the wallet again by removing the passphrase',
        },
        {
            'text': '> bitcoin-cli walletlock ',
            'cmd': ['walletlock'],
        },
        {
            'text': 'As a JSON-RPC call',
        },
        {
            'text': '> curl --user myusername --data-binary \'{"jsonrpc": "1.0", "id":"curltest", "method": "encryptwallet", "params": ["my pass phrase"] }\' -H \'content-type: text/plain;\' http://127.0.0.1:8332/'
        }
    ]
    assert Examples("").extract_examples(help_data) == expected

def test_save(tmp_path):
    examples_path = tmp_path / "examples.json"

    examples = Examples(examples_path)
    examples.examples = {
        'cmd': [
            'some line',
            '> bitcoin-cli cmd',
            '> curl xxx',
        ]
    }

    examples.save()

    assert examples_path.is_file()

    with examples_path.open() as f:
        examples_data = json.load(f)

    assert examples_data == examples.examples

def test_run_example():
    class DummyCliCaller():
        def call(self, cmd):
            return ""

        def client_version(self, cmd):
            return None

    examples_path = Path(__file__).parent / "test_data" / "examples.json"
    examples = Examples(examples_path)
    examples.load()
    result = examples.run_example("somecmd", DummyCliCaller())
    print(result)
    assert result == [
        {
            "cmd": [
                "somecmd",
                "1075"
            ],
            "result": {
                "exit_code": 0,
                "output": ""
            },
            "text": "> bitcoin-cli somecmd \"1075\""
        },
        {
            "text": "> curl ..."
        }
    ]
