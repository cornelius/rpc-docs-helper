from ui_controller import parse_args

def test_parse_args():
    args = {"arg-0": "one", "arg-1": "two"}
    assert parse_args(args) == ["one", "two"]

    args = {"arg-0": "one", "arg-1": ""}
    assert parse_args(args) == ["one"]
