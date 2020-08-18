#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("ERROR: only one file is allowed")
        exit(1)
    elif len(sys.argv) < 2:
        print("ERROR: no file provided")
        exit(1)
    else:
        input_file = sys.argv[1]
