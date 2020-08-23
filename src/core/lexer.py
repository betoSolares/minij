import sys

from .lexeme import Lexeme


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
        self.__single_operator__ = [
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
        symbol_found = False
        string_found = False
        single_line_comment = False
        single_line_number = 0
        multiline_comment = False
        lexemes = []

        for line_number, text in lines.items():
            if string_found:
                # Unfinished string error
                word = ""
                string_found = False

            for col in range(len(text)):
                char = text[col]

                if char.isspace():
                    # Ignore everything after the comment
                    if single_line_comment:
                        if single_line_number == line_number:
                            continue
                        else:
                            single_line_comment = False

                    if multiline_comment:
                        word = ""
                        continue

                    if string_found:
                        word += char
                        continue

                    if len(word) > 0:
<<<<<<< HEAD
                        lexemes.append(self.create_word(word, line_number, col))
||||||| parent of 2f779f7... Changes before pulling
                        # Do something with the word
=======
                        # Do something with the word
                        print(word)
>>>>>>> 2f779f7... Changes before pulling
                        word = ""
                        symbol_found = False

                elif char in self.__symbols__:
<<<<<<< HEAD
                    # Ignore everything after the comment
                    if single_line_comment:
                        if single_line_number == line_number:
                            continue
                        else:
                            single_line_comment = False

                    if string_found:
                        word += char
                        continue

                    # Check if word and symbol are together
                    # Something like Main. or String[]
                    if len(word) > 0 and not symbol_found:
                        if word.isdigit() and char == ".":
                            word += char
                            continue

                        if len(word) > 2 and char == "+" or char == "-":
                            if (
                                word[-1] == "E"
                                or word[-1] == "e"
                                and word[-2].isdigit()
                            ):
                                word += char
                                continue

                        lexemes.append(self.create_word(word, line_number, col))
||||||| parent of 2f779f7... Changes before pulling
                    if len(word) > 0:
                        # Do something with the word
=======
                    if len(word) > 0:
                        # Do something with the word
                        print(word)
>>>>>>> 2f779f7... Changes before pulling
                        word = ""
<<<<<<< HEAD

                    # Verify if is the first or the second symbol
                    if not symbol_found:
                        symbol_found = True
                        word += char
                    else:
                        # Recognize double operator
                        if word + char in self.__double_operator__:
                            if multiline_comment:
                                continue

                            lexemes.append(
                                self.create_word(
                                    word + char, line_number, col + 1
                                )
                            )
                            symbol_found = False
                            word = ""
                        elif word + char == "//":
                            if multiline_comment:
                                continue
                            symbol_found = False
                            single_line_comment = True
                            single_line_number = line_number
                            word = ""
                        elif word + char == "/*":
                            if multiline_comment:
                                continue
                            symbol_found = False
                            multiline_comment = True
                            word = ""
                        elif word + char == "*/":
                            symbol_found = False
                            multiline_comment = False
                            word = ""
                        else:
                            if not multiline_comment:
                                lexemes.append(
                                    self.create_word(word, line_number, col)
                                )
                            symbol_found = True
                            word = char

||||||| parent of 2f779f7... Changes before pulling
=======
                        print(char)
                    else:
                        print(char+" is a symbol")
>>>>>>> 2f779f7... Changes before pulling
                else:
                    # Ignore everything after the comment
                    if single_line_comment:
                        if single_line_number == line_number:
                            continue
                        else:
                            single_line_comment = False

                    if multiline_comment:
                        word = ""
                        continue

                    # Check if there is a symbol in the lexeme
                    if symbol_found:
                        if word == "." and char.isdigit():
                            word += char
                            symbol_found = False
                            continue

                        lexemes.append(self.create_word(word, line_number, col))
                        word = ""
                        symbol_found = False

                    # Check for start or end of a string
                    if char == '"':
                        if len(word) > 0 and not string_found:
                            lexemes.append(
                                self.create_word(word, line_number, col)
                            )
                            word = ""

                        if string_found:
                            string_found = False
                            lexemes.append(
                                self.create_word(
                                    word + char, line_number, col + 1
                                )
                            )
                            word = ""
                        else:
                            string_found = True
                            word = char
                        continue

                    word += char
        return lexemes

    def create_word(self, word, line, col):
        if len(word) > 1:
            return Lexeme(word, line, col - len(word) + 1, col)
        else:
            return Lexeme(word, line, col, None)
