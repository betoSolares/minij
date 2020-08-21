import sys


class Lexer:
    def __init__(self):
        self.__symbols__ = [
            "+",
            "-",
            "*",
            "/",
            "%",
            "<",
            "=",
            ">",
            "!",
            "&",
            "|",
            ";",
            ",",
            ".",
            "[",
            "]",
            "(",
            ")",
            "{",
            "}",
        ]
        self.__single_operator = [
            "+",
            "-",
            "*",
            "/",
            "%",
            "<",
            ">",
            "=",
            "!",
            ";",
            ",",
            ".",
            "[",
            "]",
            "(",
            ")",
            "{",
            "}",
        ]
        self.__double_operator__ = [
            "<=",
            ">=",
            "==",
            "!=",
            "&&",
            "||",
            "[]",
            "()",
            "{}",
        ]

    def get_lexemes(self, lines):
        # Check if the file is empty
        if len(lines) == 0:
            print("There is nothing to do, the file is empty")
            sys.exit(1)

        # Get all the words in the file
        word = ""
        symbol_found = False

        for line_number, text in lines.items():
            for char in text:

                if char.isspace():
                    if len(word) > 0:
                        # Do something with the word
                        word = ""
                        symbol_found = False

                elif char in self.__symbols__:
                    # Check if word and symbol are together
                    # Something like Main. or String[]
                    if len(word) > 0 and not symbol_found:
                        # Do something with the word
                        word = ""

                    # Verify if is the first or the second symbol
                    if not symbol_found:
                        symbol_found = True
                        word += char
                    else:
                        # Recognize double operator
                        if word + char in self.__double_operator__:
                            # Do something with the word
                            symbol_found = False
                            word = ""
                        else:
                            # Do something with the word
                            symbol_found = True
                            word = char

                else:

                    if symbol_found:
                        # Do something with the word
                        word = ""

                    word += char
                    symbol_found = False
