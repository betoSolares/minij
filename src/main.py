#!/usr/bin/env python3
import sys

import helpers
from analyzer import Analyzer


def main(args):
    files = helpers.parse_flags(args)
    analyzer = Analyzer(helpers.read(files["input"]))

    if analyzer.try_analyze():
        for warning in analyzer.warnings:
            print(warning)

        print("The file is fine, no error was found")
        print("\nCheck the", files["output"], "file for more information.")
        helpers.write(files["output"], analyzer.symbols)
        sys.exit(0)

    else:
        for warning in analyzer.warnings:
            print(warning)

        for error in analyzer.errors:
            print(error)

        if analyzer.failedAt == "Semantic":
            print("\nCheck the", files["output"], "file for more information.")
            helpers.write(files["output"], analyzer.symbols)

        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
