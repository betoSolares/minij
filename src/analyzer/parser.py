class Parser:
    def __init__(self, tokens):
        self.__tokens__ = None
        self.__analysis__ = []
        self.__has_errors__ = False

    # Try to parse the tokens list
    def try_parse(self, tokens):
        self.__tokens__ = iter(tokens)
        # Parse method
        return not self.__has_errors__

    # Get the next token in the list
    def __get_next_token__(self):
        return next(self.__tokens__, None)

    # Concatenate all the expected words in a single string
    def __multiple_expected__(self, expected):
        new_expected = ""

        for expect in expected:
            new_expected += expect + "or "

        return new_expected
