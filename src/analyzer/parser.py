class Parser:
    def __init__(self):
        self.__tokens__ = None
        self.__errors__ = []

    # Try to parse the tokens list, true if no errors
    def try_parse(self, tokens):
        self.__tokens__ = iter(tokens)
        # Parse method
        return len(self.__errors__) == 0

    # Get all the errors
    def get_errors(self):
        return self.__errors__

    # Add a new error to the list
    def __add_error__(self, token, expect):
        exp = self.__multiple_expected__(expect) if len(expect) > 0 else expect
        self.__errors__.append(
            "*** Syntax Error *** on line "
            + str(token.line)
            + " "
            + exp
            + " was expected and got "
            + token.word
        )

    # Get the next token in the list
    def __get_next_token__(self):
        return next(self.__tokens__, None)

    # Concatenate all the expected in a single string
    def __multiple_expected__(self, expected):
        return " or ".join(expected)
