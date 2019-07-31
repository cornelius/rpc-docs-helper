def parse_cmd_line(line):
    args = []
    arg = ""
    quoted_double = False
    quoted_single = False
    escaped = False
    square_bracket_level = 0
    curly_bracket_level = 0
    for char in line:
        if char == ' ':
            if quoted_single or quoted_double or square_bracket_level > 0 or curly_bracket_level > 0:
                arg += char
            else:
                args.append(arg)
                arg = ""
        elif char == '"' and not escaped:
            if quoted_double:
                quoted_double = False
            else:
                quoted_double = True
            if square_bracket_level > 0 or curly_bracket_level > 0:
                arg += char
        elif char == '\'' and not escaped:
            if quoted_single:
                quoted_single = False
            else:
                quoted_single = True
        else:
            if char == '\\':
                escaped = True
            else:
                if char == '[':
                    square_bracket_level += 1
                elif char == ']':
                    square_bracket_level -= 1
                elif char == '{':
                    curly_bracket_level += 1
                elif char == '}':
                    curly_bracket_level -= 1
                escaped = False
                arg += char
#        print("CHAR", char, "ARG", arg)
    if arg:
        args.append(arg)
    return args
