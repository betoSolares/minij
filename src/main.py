#!/usr/bin/env python3
import sys

from helpers import IO
from core import Lexer

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("ERROR: only one file is allowed")
        sys.exit(1)
    elif len(sys.argv) < 2:
        print("ERROR: no file provided")
        sys.exit(1)

    input_file = sys.argv[1]
    io = IO(input_file, input_file)
    lines = io.read()
    lex = Lexer()
    lexemes = lex.get_lexemes(lines)
    print(lexemes)
