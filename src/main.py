#!/usr/bin/env python3
import sys

from helpers import Flags, IO

if __name__ == "__main__":
    flags = Flags()
    args = flags.parse_flags(sys.argv[1:])
    io = IO(args["input_file"], args["output_file"])
    lines = io.read()
