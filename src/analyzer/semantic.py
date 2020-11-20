from .symbol import Symbol
from .token import Token
import sys


class Semantic:
    def __init__(self):
        self.__errors__ = []
        self.__symbols__ = []
        self.__position__ = 0
        self.__input__ = []
        self.__scope__ = ["Global"]
        self.__loking_class__ = False
        self.__loking_func__ = False
        self.__class_open__ = False
        self.__func_open__ = False
        self.__skips__ = 0

    # Get a list with the errors
    @property
    def errors(self):
        return self.__errors__

    # Try analyze
    def analyze(self, tokens):
        self.__input__ = tokens

        while True:
            current = self.__input__[self.__position__]
            self.__position__ += 1
            if self.__position__ >= len(self.__input__):
                break

            if current.category == "Identifier":
                lookahead = self.__input__[self.__position__]

                if lookahead.category == "Identifier":
                    continue

                if self.__get_symbol__(current.word, ",".join(self.__scope__)) is None:
                    if lookahead.word == "=":
                        # Check for declared in parent scope
                        reason = "Undeclared identifier"
                        self.__errors__.append([current, reason, current.word])

                    elif lookahead.word == ".":
                        # Check if declared in parent scope
                        reason = "Undeclared identifier"
                        self.__errors__.append([current, reason, current.word])

                        while lookahead.word != ")":
                            self.__position__ += 1
                            lookahead = self.__input__[self.__position__]

                    else:
                        # Check if declared in parent scope
                        self.__add_symbol__(current)

                else:

                    # Function invoke
                    if lookahead.word == ".":
                        self.__position__ += 1
                        current = self.__input__[self.__position__]
                        self.__position__ += 1
                        self.__add_symbol__(current)


                    self.__update_symbol__(current, ",".join(self.__scope__))
            else:

                # Check for scope starting
                if current.word == "{":
                    if self.__loking_class__:
                        self.__class_open__ = True
                        self.__loking_class__ = False
                    elif self.__loking_func__:
                        self.__func_open__ = True
                        self.__loking_func__ = False
                    else:
                        self.__skips__ += 1

                # Check for scope ending
                elif current.word == "}":
                    if self.__skips__ > 0:
                        self.__skips__ -= 1
                    elif self.__func_open__:
                        self.__func_open__ = False
                        self.__scope__.pop()
                    elif self.__class_open__:
                        self.__class_open__ = False
                        self.__scope__.pop()

                else:
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
        value = None
        scope = ",".join(self.__scope__)
        lexeme = token.word
        extends = None
        implements = None
        params = None

        if before_previous.word == "static":
            type = previous.word
            category = "static"

        elif previous.word == "[]":
            type = "array of " + before_previous.word
            category = "variable"

        elif previous.word == "class":
            type = category = "class"
            self.__scope__.append(lexeme)
            self.__loking_class__ = True

            # Get extends and implements
            if next.word != "{":

                if next.word == "extends":
                    self.__position__ += 1
                    next = self.__input__[self.__position__]
                    extends = next.word
                    self.__position__ += 1
                    next = self.__input__[self.__position__]

                    if next.word == "implements":
                        implements = ""

                        while next.word != "{":
                            self.__position__ += 1
                            next = self.__input__[self.__position__]
                            implements += next.word

                        implements = implements[:len(implements) - 1]

        elif previous.word == "interface":
            type = category = "interface"

        elif previous.category == "Identifier":
            type = previous.word
            category = "object"

        # Check if funtion declaration or function call
        elif next.word == "(":
            # Function call
            if previous.word == ".":
                type = lexeme # Get actual type
                category = "function call"

                # Get params
                params = ""
                helper = self.__position__

                while next.word != ")":
                    helper += 1
                    next = self.__input__[helper]
                    params += next.word

                params = params[:len(params) - 1]

                # Check params

            # Function declaration
            else:
                type = previous.word
                category = "function declaration"
                self.__loking_func__ = True
                self.__scope__.append(lexeme)

                # Get params
                params = ""
                helper = self.__position__

                while next.word != ")":
                    helper += 1
                    next = self.__input__[helper]
                    params += next.word

                params = params[:len(params) - 1]

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

            symbol = Symbol(lexeme, type, category, value.word, scope, extends, implements, params)
            self.__symbols__.append(symbol)
            print("Append", symbol.lexeme, symbol.type, symbol.category, symbol.value, symbol.scope, symbol.extends, symbol.implements, symbol.params)
            return

        else:

            if previous.word == "(":
                return

            type = previous.word
            category = "variable"

        symbol = Symbol(lexeme, type, category, value, scope, extends, implements, params)
        self.__symbols__.append(symbol)
        print("Append", symbol.lexeme, symbol.type, symbol.category, symbol.value, symbol.scope, symbol.extends, symbol.implements, symbol.params)

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
