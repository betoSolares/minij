import re

from .token import Token


class Tokenizer:
    def __init__(self):

        self.__deci_pattern__ = r"^[0-9]+$"
        self.__hexa_pattern__ = r"^0[x|X][0-9a-fA-F]+$"
        self.__double_pattern__ = r"^[0-9]+\.[0-9]*([e|E][+|-]?[0-9]+)?$"
        self.__str_pattern__ = r"^\"[^\"\n]*\"$"
        self.__id_pattern__ = r"^[a-zA-Z\$][0-9a-zA-Z\$]*$"

        self.__reserved_words__ = [
            "void",
            "int",
            "double",
            "boolean",
            "string",
            "class",
            "const",
            "interface",
            "null",
            "this",
            "extends",
            "implements",
            "for",
            "while",
            "if",
            "else",
            "return",
            "break",
            "New",
            "System",
            "out",
            "println",
        ]
        self.__single_operator__ = [
            "+",
            "-",
            "*",
            "/",
            "%",
            "<",
            ">",
            "=",
            "!",
            ";",
            ",",
            ".",
            "[",
            "]",
            "(",
            ")",
            "{",
            "}",
        ]
        self.__double_operator__ = [
            "<=",
            ">=",
            "==",
            "!=",
            "&&",
            "||",
            "[]",
            "()",
            "{}",
        ]
        self.errors = []

    def categorize(self, lexeme_list):
        # Match all lexems with their category
        tokens = []
        category = ""

        for lexeme in lexeme_list:

            curr_word = lexeme.word
            # Recognize reserved word
            if curr_word in self.__reserved_words__:
                category = "T_" + curr_word

            # Recognize decimal whole number
            elif re.search(self.__deci_pattern__, curr_word):
                category = "T_IntConstant_Decimal (value = " + curr_word + ")"

            # Recognize hexadecimal whole number
            elif re.search(self.__hexa_pattern__, curr_word):
                category = "T_IntConstant_Hexadecimal (value =" + curr_word + ")"

            # Recognize double constant
            elif re.search(self.__double_pattern__, curr_word):
                category = "T_DoubleConstant (value =" + curr_word + ")"

            # Recognize string constant
            elif re.search(self.__str_pattern__, curr_word):
                category = "T_StrConstant"

            # Recognize boolean constant
            elif curr_word == "true" or curr_word == "false":
                category = "T_BoolConstant"

            # Recognize double operator
            elif curr_word in self.__double_operator__:
                category = "T_DoubleOperator"

            # Recognize single operator
            elif curr_word in self.__single_operator__:
                category = "T_SingleOperator"
            # Recognize indentifier
            elif re.search(self.__id_pattern__, curr_word):
                if len(curr_word) > 31:
                    self.errors.append("Identifier to long" + curr_word)
                    continue
                category = "T_Identifier"

            else:
                self.add_error(curr_word)
                continue

            tokens.append(
                self.create_token(
                    lexeme.word,
                    lexeme.line,
                    lexeme.col_start,
                    lexeme.col_finish,
                    category,
                )
            )

        return tokens

    def add_error(self, word):
        if re.search(r"\.[0-9]+[E|e]?[+|-]?", word):
            self.errors.append("Not a valid double number" + word)
        elif len(word) == 1:
            self.errors.append("Not a recognized character" + word)
        else:
            self.errors.append("Not a valid identifier" + word)

    def create_token(self, lexeme, line, col_start, col_finish, category):
        return Token(lexeme, line, col_start, col_finish, category)
