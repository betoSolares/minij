#!/usr/bin/env python3
import sys

from helpers import IO, Flags


def help_message():
    print("usage: minij [OPTIONS] [FILE]\n")
    print("OPTIONS:")
    print("  -h, --help      Show help for the command")
    print("  -o, --output    Specify the oruput file")
    print("  -q, --quiet     Don't print anything")


if __name__ == "__main__":
    flags = Flags()
    args = flags.parse_flags(sys.argv[1:])

    if args["help"]:
        help_message()
        sys.exit(0)

    io = IO(args["input_file"], args["output_file"])
    lines = io.read()
