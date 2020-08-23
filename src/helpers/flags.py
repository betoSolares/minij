import getopt
import os
import sys


class Flags:
    def parse_flags(self, arg_list):
        # Try to get all the values passed to the program
        shorts = "ho:q"
        longs = ["help", "output=", "quiet"]

        try:
            opts, vals = getopt.getopt(arg_list, shorts, longs)
        except getopt.error as e:
            print("ERROR: %s" % e)
            print("Try doing minij -h or minij --help to get more information")
            sys.exit(1)

        # Default values
        args = {
            "input_file": None,
            "output_file": None,
            "help": False,
            "quiet": False,
        }

        # Get all the options of the program
        for opt, val in opts:
            if opt in ("-h", "--help"):
                args["help"] = True
            elif opt in ("-o", "--output"):
                args["output_file"] = "%s.out" % val
            elif opt in ("-q", "--quiet"):
                args["quiet"] = True

        # Get the input file
        if not args["help"]:
            if len(vals) > 1:
                print("ERROR: only one file is allowed")
                sys.exit(1)
            elif len(vals) < 1:
                print("ERROR: no file provided")
                sys.exit(1)
            args["input_file"] = vals[0]

        # Verify that the output file is set
        if not args["help"] and args["output_file"] is None:
            args["output_file"] = (
                os.path.splitext(args["input_file"])[0] + ".out"
            )

        return args
