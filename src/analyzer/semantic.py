from .symbol import Symbol
from .token import Token


class Semantic:
    def __init__(self):
        self.__errors__ = []
        self.__symbols__ = []
        self.__position__ = 0
        self.__input__ = []
        self.__scope__ = ["Global"]

    # Get a list with the errors
    @property
    def errors(self):
        return self.__errors__

    # Try analyze
    def analyze(self, tokens):
        self.__input__ = tokens

        while True:
            current = self.__input__[self.__position__]
            #  print(
            #      "*** Current word:",
            #      current.word,
            #      "Current category:",
            #      current.category,
            #      "***",
            #  )

            self.__position__ += 1
            if self.__position__ >= len(self.__input__):
                break

            #  print(self.__position__)


            if current.category == "Identifier":
                lookahead = self.__input__[self.__position__]
                #  print(
                #      "*** Lookahead word:",
                #      lookahead.word,
                #      "Lookahead category:",
                #      lookahead.category,
                #      "***",
                #  )

                if lookahead.category == "Identifier":
                    continue

                if self.__get_symbol__(current.word, ",".join(self.__scope__)) is None:
                    if lookahead.word == "=":
                        # Check for declared in parent scope
                        reason = "Undeclared identifier"
                        self.__errors__.append([current, reason, current.word])

                    else:
                        self.__add_symbol__(current)

                else:
                    self.__update_symbol__(current, ",".join(self.__scope__))
            else:
                # Check for escope ending
                continue

#        import pdb

#        pdb.set_trace()
        return True if len(self.__errors__) == 0 else False

    # Add new symbol to symbols table
    def __add_symbol__(self, token):
        before_previous = self.__input__[self.__position__ - 3]
        previous = self.__input__[self.__position__ - 2]
        next = self.__input__[self.__position__]

        #  print(
        #      "*** Previous word:",
        #      previous.word,
        #      "Previous category:",
        #      previous.category,
        #      "***",
        #  )
        #  print(
        #      "*** Next word:", next.word, "Next category:", next.category, "***"
        #  )

        type = ""
        category = ""
        value = ""
        scope = ",".join(self.__scope__)
        lexeme = token.word

        if before_previous.word == "static":
            type = previous.word
            category = "static"

        elif previous.word == "class":
            type = category = "class"
            self.__scope__.append(lexeme)
            # Get extends and implements

        elif previous.word == "interface":
            type = category = "interface"

        elif previous.category == "Identifier":
            type = previous.word
            category = "object"

        elif next.word == "(":
            type = previous.word
            category = "function"
            self.__scope__.append(lexeme)
            # Get params

        elif next.word == ".":

            while True:
                lexeme += next.word
                self.__position__ += 1
                next = self.__input__[self.__position__]
                if next.word == "=":
                    break

            self.__position__ += 1
            value = self.__input__[self.__position__]
            type = lexeme
            category = "object"

            symbol = Symbol(lexeme, type, category, value.word, scope)
            self.__symbols__.append(symbol)
            print("Append", symbol.lexeme, symbol.type, symbol.category, symbol.value, symbol.scope)
            return

        else:

            if previous.word == "(":
                return

            type = previous.word
            category = "variable"

        symbol = Symbol(lexeme, type, category, value, scope)
        self.__symbols__.append(symbol)
        print("Append", symbol.lexeme, symbol.type, symbol.category, symbol.value, symbol.scope)

        return

    # Return existing symbol
    def __get_symbol__(self, symbol, scope):
        value = None

        for element in self.__symbols__:
            if element.lexeme == symbol and element.scope == scope:
                value = element
                break

        return value

    # Update existing symbol
    def __update_symbol__(self, symbol, scope):
        next = self.__input__[self.__position__]
        value = ""

        if next.word == "=":

            while True:
                self.__position__ += 1
                if next.word == ";":
                    break

                next = self.__input__[self.__position__]
                # value is being stored as string until ; is found
                # should probably operate values before storing them
                # would have to make sure the types of operands are
                # compatible
                value += next.word

            # import pdb; pdb.set_trace()
            for element in self.__symbols__:
                if element.lexeme == symbol.word and element.scope == scope:
                    element.value = value
                    print("Update", element.lexeme, element.type, element.category, element.value, element.scope)
                    break

            return True

        else:
            # Class, function or interface already declared
            # add error
            return False
