from util import parse_cmd_line

def test_parse_example_line():
    lines = [
        ('cmd', ['cmd']),
        ('cmd arg', ['cmd', 'arg']),
        ('cmd "arg"', ['cmd', 'arg']),
        ('cmd "arg one"', ['cmd', 'arg one']),
        ('cmd "arg one" "arg two"', ['cmd', 'arg one', 'arg two']),
    ]
    for line in lines:
        assert parse_cmd_line(line[0]) == line[1]

def test_parse_example_line_quoted():
    assert parse_cmd_line('cmd 2 "[\\\"xx\\\"]"') == ['cmd', '2', '[\"xx\"]']

def test_parse_object():
    assert parse_cmd_line('cmd {\\\"rules\\\": [\\\"segwit\\\"]}') == ['cmd', '{\"rules\": [\"segwit\"]}']

def test_parse_array():
    assert parse_cmd_line("cmd '[\\\"minfeerate\\\",\\\"avgfeerate\\\"]'") == ['cmd', '[\"minfeerate\",\"avgfeerate\"]']

def test_parse_complex_array():
    assert parse_cmd_line("cmd '[{ \\\"scriptPubKey\\\": { \\\"address\\\": \\\"<my address>\\\" }}]'") == ['cmd', '[{ \"scriptPubKey\": { \"address\": \"<my address>\" }}]']

def test_parse_spacey_object():
    assert parse_cmd_line('cmd \"[{\\\"txid\\\" : \\\"mytxid\\\",\\\"vout\\\":0}]\" \"{\\\"myaddress\\\":0.01}\"') == ['cmd', '[{\"txid\" : \"mytxid\",\"vout\":0}]', '{\"myaddress\":0.01}']

def test_parse_spacey_array():
    assert parse_cmd_line('combinepsbt [\"mybase64_1\", \"mybase64_2\"]') == ['combinepsbt', '["mybase64_1", "mybase64_2"]']
