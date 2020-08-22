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

        for line_number, text in lines.items():
            for char in text:

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
                        # Do something with the word
                        word = ""
                        symbol_found = False

                elif char in self.__symbols__:
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
                        # Do something with the word
                        word = ""

                    # Verify if is the first or the second symbol
                    if not symbol_found:
                        symbol_found = True
                        word += char
                    else:
                        # Recognize double operator
                        if word + char in self.__double_operator__:
                            if multiline_comment:
                                continue
                            # Do something with the word
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
                                # Do something with the word
                            symbol_found = True
                            word = char

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
                        # Do something with the word
                        word = ""
                        symbol_found = False

                    # Check for start or end of a string
                    if char == '"':
                        if len(word) > 0 and not string_found:
                            # Do something with the word
                            word = ""

                        if string_found:
                            string_found = False
                            word += char
                            # Do something with the word
                            word = ""
                        else:
                            string_found = True
                            word = char
                        continue

                    word += char
