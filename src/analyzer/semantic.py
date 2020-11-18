from .token import Token
from .symbol import Symbol


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

    def analyze(self,tokens):
        self.__input__ = tokens
        pass

    # Add new symbol to symbols table
    def __add_symbol__(self, token):

        # Pendig validation of symbols already declared

        previous = self.__input__[self.__position__ - 1].word
        next = self.__input__[self.__position__ + 1].word

        if previous == "Class" or previous == "class":
            next = "Class"

        elif previous == "Interface" or previous == "interface":
            next = "Interface"

        elif previous == "Static" or previous == "static":
            next = "Static"

        elif next == "(":
            next = "Function"

        else:
            next = "Variable"

        self.__symbols__[token.word] = Symbol(previous,next)

        return

    # Return existing symbol
    def __get_symbol__(self, symbol):
        return self.__symbols__[symbol]
