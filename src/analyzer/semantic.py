from .symbol import Symbol
from .token import Token


class Semantic:
    def __init__(self):
        self.__errors__ = []
        self.__symbols__ = dict()
        self.__position__ = 0
        self.__input__ = []

    # Get a list with the errors
    @property
    def errors(self):
        return self.__errors__

    def analyze(self, tokens):
        self.__input__ = tokens

        while True:

            if self.__position__ >= len(self.__input__):
                break

            current = self.__input__[self.__position__]
            self.__position__ += 1

            if current.category == "Identifier":
                if self.__get_symbol__(current) is None:
                    self.__add_symbol__(current)
                else:
                    self.__update_symbol__(current)
            else:
                continue

        return True if len(self.__errors__) == 0 else False

    # Add new symbol to symbols table
    def __add_symbol__(self, token):

        previous = self.__input__[self.__position__ - 1].word
        next = self.__input__[self.__position__ + 1].word

        if previous == "class":
            next = "Class"

        elif previous == "interface":
            next = "Interface"

        elif previous == "static":
            next = "Static"

        elif next == "(":
            next = "Function"

        else:
            next = "Variable"

        self.__symbols__[token.word] = Symbol(previous, next)

        return

    # Return existing symbol
    def __get_symbol__(self, symbol):
        return self.__symbols__.get(symbol.word, default=None)

    # Update existing symbol
    def __update_symbol__(self, symbol):
        next = self.__input__[self.__position__ + 1].word

        if next == "=":
            value = self.__input__[self.__position__ + 2].word
            self.__symbols__[symbol].value = value
            # current = self.__symbols__[symbol]
            # current.value = value
            # self.__symbols__[symbol] = current
            return True
        else:
            # Class, function or interface already declared
            # add error
            return False
