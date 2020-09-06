class Parser:
    def __init__(self, tokens):
        self.__tokens__ = iter(tokens)

    # Get the next token in the list
    def __get_next_token__(self):
        return next(self.__tokens__, None)
