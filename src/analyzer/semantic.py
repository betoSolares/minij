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

    # Try analyze
    def analyze(self, tokens):
        import pdb

        pdb.set_trace()
        self.__input__ = tokens

        while True:

            if self.__position__ >= len(self.__input__):
                break

            current = self.__input__[self.__position__]
            print(
                "*** Current word:",
                current.word,
                "Current category:",
                current.category,
                "***",
            )
            self.__position__ += 1
            print(self.__position__)

            if current.category == "Identifier":
                lookahead = self.__input__[self.__position__]
                print(
                    "*** Lookahead word:",
                    lookahead.word,
                    "Lookahead category:",
                    lookahead.category,
                    "***",
                )

                if lookahead.category == "Identifier":
                    continue

                if self.__get_symbol__(current) is None:
                    self.__add_symbol__(current)

                else:
                    self.__update_symbol__(current)
            else:
                continue

        return True if len(self.__errors__) == 0 else False

    # Add new symbol to symbols table
    def __add_symbol__(self, token):

        previous = self.__input__[self.__position__ - 2]
        next = self.__input__[self.__position__]
        print(
            "*** Previous word:",
            previous.word,
            "Previous category:",
            previous.category,
            "***",
        )
        print(
            "*** Next word:", next.word, "Next category:", next.category, "***"
        )
        type = ""
        category = ""

        if previous.word == "class":
            type = category = "class"

        elif previous.word == "interface":
            type = category = "interface"

        elif previous.word == "static":
            type = category = "static"

        elif previous.category == "Identifier":
            type = previous.word
            category = "object"

        elif next.word == "(":
            type = previous.word
            category = "function"

        else:
            type = previous.word
            category = "variable"

        self.__symbols__[token.word] = Symbol(type, category)

        return

    # Return existing symbol
    def __get_symbol__(self, symbol):
        return self.__symbols__.get(symbol.word, None)

    # Update existing symbol
    def __update_symbol__(self, symbol):
        next = self.__input__[self.__position__].word

        if next == "=":
            value = self.__input__[self.__position__].word
            self.__symbols__[symbol].value = value
            # current = self.__symbols__[symbol]
            # current.value = value
            # self.__symbols__[symbol] = current
            return True
        else:
            # Class, function or interface already declared
            # add error
            return False
