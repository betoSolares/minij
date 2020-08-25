import os
import sys


class Writter:
    def __init__(self, token_list, input):
        self.token_list = token_list
        self.input = os.path.splitext(input)[0]
        self.output = "../out" + os.path.splitext(input)[0] + ".out"

    def write(self, token_obj, lexeme_list):
        # Try to write to a new output file
        try:
            if os.path.isfile(self.output):
                cont = 1
                new_output = self.input + "(" + cont + ")"

                while not os.path.isfile(self.output):
                    cont += 1
                    new_output = self.input + "(" + cont + ")"

                self.output = "../out" + new_output + ".out"

            with open(self.output, "w") as file:
                # write file
                if not token_obj.errors:
                    for token in self.token_list:
                        file.write(
                            "{} line {} cols {}-{} is {}".format(
                                token.lexeme,
                                token.line,
                                token.col_start,
                                token.col_finish,
                                token.category,
                            )
                        )

                else:
                    for lexeme in lexeme_list:
                        for error in token_obj.errors:
                            if error.endswith(lexeme.word):
                                file.write(
                                    "*** Error line {} *** {}".format(
                                        lexeme.line, error
                                    )
                                )

                        for token in self.token_list:
                            if lexeme.word == token.lexeme:
                                file.write(
                                    "{} line {} cols {}-{} is {}".format(
                                        token.lexeme,
                                        token.line,
                                        token.col_start,
                                        token.col_finish,
                                        token.category,
                                    )
                                )

        except Exception:
            print("ERROR: could not create file")
            sys.exit(1)
