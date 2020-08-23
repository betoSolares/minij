import sys
import os
import getopt

class Flags:

    def parse_flags(self, arg_list):
        # Try to get all the values passed to the program
        shorts = "ho:q"
        longs = ["help", "output=", "quiet"]

        try:
            opts, vals = getopt.getopt(arg_list, shorts, longs)
        except getopt.error as e:
            print("ERROR: %s" % e)
            sys.exit(1)

        # Default values
        args = {
            "input_file": None,
            "output_file": None,
            "help": False,
            "quiet": False,
        }

        # Get the input file
        if len(vals) > 1:
            print("ERROR: only one file is allowed")
            sys.exit(1)
        elif len(vals) < 1:
            print("ERROR: no file provided")
            sys.exit(1)
        args["input_file"] = vals[0]

        # Get all the options of the program
        for opt, val in opts:
            if opt in ("-h", "--help"):
                args["help"] = True
            elif opt in ("-o", "--output"):
                args["output_file"] = "%s.out" % val
            elif opt in ("-q", "--quiet"):
                args["quiet"] = True

        # Verify that the output file is set
        if args["output_file"] is None:
            args["output_file"] = os.path.splitext(args["input_file"])[0] + ".out"

        return args
