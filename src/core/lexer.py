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
        self.errors = []

    def get_lexeme(self, lines):
        word = ""
        symbol = False
        string = False
        single = False
        single_number = 0
        multiline = False
        lexemes = []

        for line, text in lines.items():
            # Verify that no string is open
            if string:
                self.errors.append("Unfinished string on line" + str(line - 1))
                word = ""
                string = False

            for col in range(len(text)):
                char = text[col]

                # Character is a whitespace
                if char.isspace():
                    # Ignore everything if it's a comment
                    if single and single_number < line:
                        single = False
                    elif single:
                        continue

                    if multiline:
                        word = ""
                        continue

                    # Append the character if it's a string
                    if string:
                        word += char
                        continue

                    # A word was found
                    if len(word) > 0:
                        lexemes.append(self.create_word(word, line, col))
                        word = ""
                        symbol = False

                # Character is a know symbol
                elif char in self.__symbols__:
                    # Ignore everything if it's a comment
                    if single and single_number < line:
                        single = False
                    elif single:
                        continue

                    # Append the character if it's a string
                    if string:
                        word += char
                        continue

                    # If it's the first ocurrence of a symbol
                    if len(word) > 0 and not symbol:
                        # Check if it's the firts point of the number
                        if word.isdigit() and char == ".":
                            word += char
                            continue

                        # Check for exponential part of a number
                        if len(word) > 2 and char == "+" or char == "-":
                            if (word[-1] == "E" or word[-1] == "e" and word[-2].isdigit()):
                                word += char
                                continue

                        lexemes.append(self.create_word(word, line, col))
                        word = ""

                    # If it's the second ocurrence of a symbol
                    if symbol:
                        # Recognize double operator
                        if word + char in self.__double_operator__:
                            if multiline:
                                continue

                            lexemes.append(self.create_word(word + char, line, col + 1))
                            symbol = False
                            word = ""

                        # Single comment starts
                        elif word + char == "//":
                            if multiline:
                                continue

                            symbol = False
                            single = True
                            single_number = line
                            word = ""

                        # Multiline comment starts
                        elif word + char == "/*":
                            if multiline:
                                continue

                            symbol = False
                            multiline = True
                            word = ""

                        # Multiline comment ends
                        elif word + char == "*/":
                            # comment without match
                            if not multiline:
                                self.errors.append("Comment without match on line " + str(line))

                            symbol = False
                            multiline = False
                            word = ""

                        # Two differentes symbols
                        else:
                            if not multiline:
                                lexemes.append(self.create_word(word, line, col))

                            symbol = True
                            word = char

                    # First ocurrence of a symbol
                    else:
                        symbol = True
                        word += char

                # Character is anything else
                else:
                    # Ignore everything if it's a comment
                    if single and single_number < line:
                        single = False
                    elif single:
                        continue

                    if multiline:
                        word = ""
                        continue

                    # If it's double number
                    if symbol and word == "." and char.isdigit():
                        word += char
                        symbol = False
                        continue

                    # Check if there is a symbol in the lexeme
                    elif symbol:
                        lexemes.append(self.create_word(word, line, col))
                        word = ""
                        symbol = False

                    # Check for start or end of a string
                    if char == '"':
                        # Word before string start
                        if len(word) > 0 and not string:
                            lexemes.append(self.create_word(word, line, col))
                            word = ""

                        # String end
                        if string:
                            string = False
                            lexemes.append(self.create_word(word + char, line, col + 1))
                            word = ""

                        # String start
                        else:
                            string = True
                            word = char

                        continue

                    word += char

        # EOF errors
        if string:
            self.errors.append("End of file on string")

        if multiline:
            self.errors.append("End of file on comment")

        return lexemes

    def create_word(self, word, line, col):
        if len(word) > 1:
            return Lexeme(word, line, col - len(word) + 1, col)
        else:
            return Lexeme(word, line, col, None)
