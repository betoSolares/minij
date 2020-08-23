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

        self.__keywords__ = [
                "void",
                "int",
                "double",
                "boolean",
                "string",
                "class",
                "const",
                "interface",
                "null",
                "this",
                "extends",
                "implements",
                "for",
                "while",
                "if",
                "else",
                "return",
                "break",
                "New",
                "System",
                "out",
                "printin",
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
                        print(word)
                        word = ""
                elif char in self.__symbols__:
                    if len(word) > 0:
                        # Do something with the word
                        print(word)
                        word = ""
                        print(char)
                    else:
                        print(char+" is a symbol")
                else:
                    word += char
                    if word in self.__keywords__:
                        print(word+" is a keyword")
                        word = ""
