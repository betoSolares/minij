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

    created = item.lexeme + " -> "

    if item.type is not None:
        created += "[type = " + item.type + "] "

    if item.category is not None:
        created += "[category = " + item.category + "] "

    if item.value is not None:
        created += "[value = " + item.value + "] "
    elif item.category == "variable" or item.category == "static":
        created += "[value = undefined] "

    if item.scope is not None:
        created += "[scope = " + item.scope + "] "

    if item.extends is not None:
        created += "[extends = " + item.extends + "] "

    if item.implements is not None:
        created += "[implements = " + item.implements + "] "

    if item.params is not None:
        created += "[params = " + item.params + "] "

    return created.strip()
