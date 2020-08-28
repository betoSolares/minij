#!/usr/bin/env python3
import sys

import helpers
from analyzer import Lexer


def main(args):
    files = helpers.parse_flags(args)
    lines = helpers.read(files["input"])
    lexer = Lexer()

    # No errors on file
    if lexer.try_tokenize(lines):
        print("The file is fine, no error was found")

    # Print errors on screen
    else:
        for err in lexer.get_errors():
            print("*** ERROR on line", err.line, "***", err.reason, err.word)

    # Write to the file
    helpers.write(files["output"], lexer.get_all())
    print("\nCheck the file", files["output"], "for more information")

    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
