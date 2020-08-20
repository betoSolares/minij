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

    def get_lexemes(self, lines):
        # Check if the file is empty
        if len(lines) == 0:
            print("There is nothing to do, the file is empty")
            sys.exit(1)

        # Get all the words in the file
        word = ""

        for line_number, text in lines.items():
            for char in text:
                if char.isspace():
                    if len(word) > 0:
                        # Do something with the word
                        word = ""
                elif char in self.__symbols__:
                    if len(word) > 0:
                        # Do something with the word
                        word = ""
                else:
                    word += char
