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

            return lines
        except:
            print("ERROR: could not load file")
            exit(1)
