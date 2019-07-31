import subprocess
from pathlib import Path

def test_help():
    cmd = Path(__file__).parent / "rpc_docs_helper"
    result = subprocess.check_output([cmd, "--help"], stderr=subprocess.STDOUT).rstrip().decode("utf-8")
    assert "Usage" in result

