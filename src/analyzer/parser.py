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
        symbols = []
        position = 0

        while True:
            state = int(stack[-1])
            token = input_stream[position]

            # Check if the word is a terminal
            if self.__get_equivalent__(token) in self.__grammar__.table[0]:
                actions = self.__get_action__(token, state)

                # Actions
                if len(actions) == 1:
                    if actions[0][0] == "Shift":
                        stack.append(str(actions[0][1]))
                        symbols.append(token.word)
                        position += 1

                    elif actions[0][0] == "Reduce":
                        rule = self.__grammar__.rules.get(int(actions[0][1]))
                        length = 0 if rule[1] == "''" else len(rule[1].split())
                        stack = stack[:len(stack)-length]
                        symbols = symbols[:len(symbols)-length]
                        symbols.append(rule[0])
                        state = int(stack[-1])
                        index = self.__grammar__.table[0].index(rule[0])
                        goto = str(self.__grammar__.table[state + 1][index])
                        stack.append(str(goto))

                    else:
                        break

                # Conflicts
                else:
                    print("Error Conflicts")
                    break

            # Error not word in terminals
            else:
                print("Error not terminal")
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
            else:
                actions.append(("Accept", -1))

        return actions
