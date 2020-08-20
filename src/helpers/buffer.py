import sys


class IO:
    def __init__(self, input, output):
        self.input = input
        self.output = output

    def read(self):
        # Try to read the file
        try:
            with open(self.input, "r") as file:
                print(file.read())
        except:
            print("ERROR: could not load file")
            exit(1)
