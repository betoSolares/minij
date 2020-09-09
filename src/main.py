#!/usr/bin/env python3
import sys

import helpers
from analyzer import Lexer, Parser


def main(args):
    files = helpers.parse_flags(args)
    lines = helpers.read(files["input"])
    lexer = Lexer()
    parser = Parser()

    # No lexical errors on file
    if lexer.try_tokenize(lines):
        # No syntactical errors
        if parser.try_parse(lexer.get_tokens()):
            print("The file is fine, no error was found")

        # Print syntactical errors on screen
        else:
            print(parser.get_errors(), sep="\n")

    # Print lexical errors on screen and write to the file
    else:
        for err in lexer.get_errors():
            print("*** ERROR on line", err.line, "***", err.reason, err.word)

        helpers.write(files["output"], lexer.get_all())
        print("\nCheck the file", files["output"], "for more information")

    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
