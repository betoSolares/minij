import getopt
import os
import sys


# Help message to show
def help_message():
    print("usage: minij [OPTIONS] [FILE]\n")
    print("OPTIONS:")
    print("  -h, --help      Show help for the command")
    print("  -o, --output    Specify the output file")


# Try to get all the values passed to the program
def parse_flags(args_list):
    shorts = "ho:"
    longs = ["help", "output="]

    try:
        opts, vals = getopt.getopt(args_list, shorts, longs)
    except getopt.error as e:
        print("ERROR: %s" % e)
        print("Try doing minij -h or minij --help to get more information")
        sys.exit(1)

    # Default values
    args = {
        "input": None,
        "output": None,
    }

    for opt, val in opts:
        # Print help message
        if opt in ("-h", "--help"):
            args["help"] = True
            help_message()
            sys.exit(0)

        # Get specific output file
        elif opt in ("-o", "--output"):
            if os.path.isdir(val):
                print("ERROR: The output file is a directory")
                sys.exit(1)

            args["output"] = val

    # Get the input file
    if len(vals) > 1:
        print("ERROR: only one file is allowed")
        sys.exit(1)

    elif len(vals) < 1:
        print("ERROR: no file provided")
        sys.exit(1)

    args["input"] = vals[0]

    # Set the output if not specified
    if args["output"] is None:
        filename = os.path.splitext(os.path.basename(args["input"]))[0]
        output = filename
        count = 0

        while os.path.isfile(output + ".table"):
            count += 1
            output = filename + "(" + str(count) + ")"

        args["output"] = output + ".table"

    return args
