import sys


# Try to read the file and separeted into lines
def read(input):
    try:
        with open(input, "r") as file:
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


# Try to write to the output file
def write(output, items):
    try:
        with open(output, "w") as file:
            for item in items:
                file.write(get_text(item) + "\n")
    except Exception:
        print("ERROR: could not write to the file")
        sys.exit(1)


# Get the text to put in the file
def get_text(item):
    if item.category == "Error":
        return (
            "*** Error on line "
            + str(item.line)
            + " *** "
            + item.reason
            + " "
            + item.word
        )
    else:
        if item.finish is None:
            cols = " column " + str(item.start)
        else:
            cols = " columns " + str(item.start) + " to " + str(item.finish)

        if "Constant" in item.category:
            vals = " (value = " + item.word + ")"
        else:
            vals = ""

        return (
            item.word
            + " on line "
            + str(item.line)
            + cols
            + " is T_"
            + item.category
            + vals
        )
