from .grammar import Grammar
from .token import Token

class Parser:
    def __init__(self):
        self.__errors = []
        self.grammar = Grammar()

    # Try analyze
    def Analyze(self, tokens):
        input_stream = tokens + [Token("$", "-1", "-1", "-1", "EndInputStream")]
        stack = ["0"]
        position = 0

        #  for i in range(len(self.grammar.table)):
        #      print(i, " -> ", self.grammar.table[i])
        #      print("###################################################################3")

        while True:
            state = int(stack[-1])
            token = input_stream[position]

            print(state, token.word, token.category)


            if position < len(input_stream) - 1:
                position += 1
            else:
                break

    # Get the equivalent terminal for the category of the token
    def __get_equivalent__(self, token):
        if token.category == "IntConstant_Decimal" or token.category == "IntConstant_Hexadecimal":
            return "intConstant"

        elif token.category == "DoubleConstant":
            return "doubleConstant"

        elif token.category == "StringConstant":
            return "stringConstant"

        elif token.category == "BooleanConstant":
            return "booleanConstant"

        elif token.category == "DoubleOperator" or token.category == "SingleOperator":
            return token.word

        elif token.category == "Identifier":
            return "ident"

        else:
            return token.category
