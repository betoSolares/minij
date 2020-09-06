class Parser:
    def __init__(self, tokens):
        self.__tokens__ = tokens

    # Get the next token in the list
    def __get_next_token__(self):
        if len(self.__tokens__) > 0:
            return self.__tokens__.pop(0)
        else:
            return None
