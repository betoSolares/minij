import re

from .token import Token


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
        self.__reserved_words__ = [
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
            "println",
            "Print",
        ]
        self.__analysis__ = []
        self.__has_errors__ = False

    # Try to tokenize the text, true if has no errors
    def try_tokenize(self, lines):
        self.__tokenization__(lines)
        return not self.__has_errors__

    # Get a list with all the errors
    def get_errors(self):
        return [x for x in self.__analysis__ if x.category == "Error"]

    # Get a list with all the tokens
    def get_tokens(self):
        return [x for x in self.__analysis__ if x.category != "Error"]

    # Get a list with all the errors and tokens
    def get_all(self):
        return self.__analysis__

    # Get all the words of the file and categorize them
    def __tokenization__(self, lines):
        word = ""
        symbol = False
        string = False
        single = False
        single_number = 0
        multiline = False

        for line, text in lines.items():
            # Verify that no string is open
            if string:
                self.__add_error__("", line - 1, len(word), "Unfinished string")
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
                        self.__categorize__(word, line, col)
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
                        if len(word) >= 2 and (char == "+" or char == "-"):
                            if (word[-1] == "E" or word[-1] == "e") and (
                                word[-2].isdigit() or word[-2] == "."
                            ):
                                word += char
                                continue

                        self.__categorize__(word, line, col)
                        word = ""

                    # If it's the second ocurrence of a symbol
                    if symbol:
                        # Recognize double operator
                        if word + char in self.__double_operator__:
                            if multiline:
                                continue

                            self.__categorize__(word + char, line, col + 1)
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
                            if not multiline:
                                self.__add_error__(
                                    word + char,
                                    line,
                                    col,
                                    "Comment without match",
                                )

                            symbol = False
                            multiline = False
                            word = ""

                        # Two differentes symbols
                        else:
                            if not multiline:
                                self.__categorize__(word, line, col)

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
                        self.__categorize__(word, line, col)
                        word = ""
                        symbol = False

                    # Check for start or end of a string
                    if char == '"':
                        # Word before string start
                        if len(word) > 0 and not string:
                            self.__categorize__(word, line, col)
                            word = ""

                        # String end
                        if string:
                            string = False
                            self.__categorize__(word + char, line, col + 1)
                            word = ""

                        # String start
                        else:
                            string = True
                            word = char

                        continue

                    word += char

        # EOF errors
        if string:
            self.__add_error__("", len(lines), None, "EOF in string")

        if multiline:
            self.__add_error__("", len(lines), None, "EOF in comment")

    # Match the word with their category
    def __categorize__(self, word, line, col):
        # Recognize reserverd words
        if word in self.__reserved_words__:
            self.__add_token__(word, line, col, word.lower().capitalize())

        # Recognize int base 10 number
        elif re.search(r"^[0-9]+$", word):
            self.__add_token__(word, line, col, "IntConstant_Decimal")

        # Recognize int base 16 number
        elif re.search(r"^0[x|X][0-9a-fA-F]+$", word):
            self.__add_token__(word, line, col, "IntConstant_Hexadecimal")

        # Recognize double number
        elif re.search(r"^[0-9]+\.?[0-9]*([e|E][+|-]?[0-9]+)?$", word):
            self.__add_token__(word, line, col, "DoubleConstant")

        # Recognize string
        elif re.search(r"^\".*\"$", word):
            if "\0" in word:
                self.__add_error__(word, line, col, "String with NULL char")
            else:
                self.__add_token__(word, line, col, "StringConstant")

        # Recognize boolean
        elif word == "true" or word == "false":
            self.__add_token__(word, line, col, "BooleanConstant")

        # Recognize double operator
        elif word in self.__double_operator__:
            self.__add_token__(word, line, col, "DoubleOperator")

        # Recognize single operator
        elif word in self.__single_operator__:
            self.__add_token__(word, line, col, "SingleOperator")

        # Recognize identifier
        elif re.search(r"^[a-zA-Z\$][0-9a-zA-Z\$]*$", word):
            # The identifier can't be greater than 31 chars length
            if len(word) > 31:
                self.__add_error__(word, line, col, "Identifier to long")
                self.__add_token__(word[:31], line, col, "Identifier")
            else:
                self.__add_token__(word, line, col, "Identifier")

        # Recognize error
        else:
            self.__handle_error__(word, line, col)

    # Handle all the errors in the categorization
    def __handle_error__(self, word, line, col):
        # Not a recognized character
        if len(word) == 1:
            self.__add_error__(word, line, col, "Not a recognized char")

        # Double number error
        elif re.search(r"^[0-9]*\.?[0-9]*([e|E][+|-]?[0-9]*)?$", word):
            self.__add_error__(word, line, col, "Not a valid double number")

        # Identifier error
        elif re.search(r"^[0-9][0-9a-zA-Z\$]+$", word):
            self.__add_error__(word, line, col, "Not a valid identifier")

        # Iterate through the word to find know lexemes
        else:
            recognized = ""

            for sub_col in range(len(word)):
                char = word[sub_col]

                # Know character
                if (
                    char.isdigit()
                    or char.isalpha()
                    or char in self.__symbols__
                    or char == "$"
                ):
                    recognized += char

                # Unrecognized character
                else:
                    if len(recognized) > 0:
                        n = col - len(word) + sub_col
                        self.__categorize__(recognized, line, n)
                        recognized = ""

                    n = col - len(word) + sub_col + 1
                    self.__add_error__(char, line, n, "Not a recognized char")

            if len(recognized) > 0:
                self.__categorize__(recognized, line, col)
                recognized = ""

    # Add a new token to the list of analysis
    def __add_token__(self, word, line, col, category):
        if len(word) > 1:
            token = Token(word, line, col - len(word) + 1, col, category)
        else:
            token = Token(word, line, col, None, category)

        self.__analysis__.append(token)

    # Add a new error to the list of analysis
    def __add_error__(self, word, line, col, reason):
        self.__has_errors__ = True

        if len(word) > 1:
            error = Token(word, line, col - len(word) + 1, col, "Error", reason)
        else:
            error = Token(word, line, col, None, "Error", reason)

        self.__analysis__.append(error)
