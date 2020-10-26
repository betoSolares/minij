from .grammar import Grammar
from .token import Token


class Parser:
    def __init__(self):
        self.__errors__ = []
        self.__grammar__ = Grammar()

    # Try analyze
    def Analyze(self, tokens):
        input_stream = tokens + [Token("$", "-1", "-1", "-1", "EndInputStream")]
        stack = ["0"]
        position = 0

        while True:
            state = int(stack[-1])
            token = input_stream[position]
            actions = self.__get_action__(token, state)

            if actions != -1:
                if len(actions) == 1:
                    print(state, token.word, token.category, actions[0][0], actions[0][1])

                # Conflicts
                else:
                    print("Error")

            # Error not word in terminals
            else:
                break

            if position < len(input_stream) - 1:
                position += 1
            else:
                break

    # Get the equivalent terminal for the category of the token
    def __get_equivalent__(self, token):
        if (
            token.category == "IntConstant_Decimal"
            or token.category == "IntConstant_Hexadecimal"
        ):
            return "intConstant"

        elif token.category == "DoubleConstant":
            return "doubleConstant"

        elif token.category == "StringConstant":
            return "stringConstant"

        elif token.category == "BooleanConstant":
            return "booleanConstant"

        elif (
            token.category == "DoubleOperator"
            or token.category == "SingleOperator"
        ):
            return token.word

        elif token.category == "Identifier":
            return "ident"

        else:
            return token.word

    # Get the action to make
    def __get_action__(self, token, state):
        terminal = self.__get_equivalent__(token)
        if terminal not in self.__grammar__.table[0]:
            return -1

        actions = []
        index = self.__grammar__.table[0].index(terminal)
        raw = str(self.__grammar__.table[state + 1][index]).split("/")

        for item in raw:
            if not item:
                continue

            if item.startswith("s"):
                actions.append(("Shift", int(item[1:])))
            elif item.startswith("r"):
                actions.append(("Reduce", int(item[1:])))
            elif item == "acc":
                actions.append(("Accept", -1))
            else:
                actions.append(("Goto", int(item)))

        return actions
