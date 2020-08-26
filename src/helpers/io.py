import sys


class IO:
    def __init__(self, input, output):
        self.input = input
        self.output = output

    def read(self):
        # Try to read the file and separeted into lines
        try:
            with open(self.input, "r") as file:
                lines = {}

                for i, l in enumerate(file):
                    lines[i + 1] = l

            # Check if the file is empty
            if len(lines) == 0:
                print("There is nothing to do, the file is empty")
                sys.exit(0)

            return lines
        except Exception:
            print("ERROR: could not load file")
            sys.exit(1)
