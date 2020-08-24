import re

from .token import Token


class Tokenizer:
    def __init__(self):

        self.__deci_pattern__ = r"^[0-9]+$"
        self.__hexa_pattern__ = r"^0[x|X][0-9a-fA-F]+$"
        self.__double_pattern__ = r"^[0-9]+.[0-9]*([e|E][+|-]?[0-9]+)?$"
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
            "printin",
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

    def categorize(self, lexeme_list):
        # Match all lexems with their category
        tokens = []
        category = ""

        for lexeme in lexeme_list:

            curr_word = lexeme.word()
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
                category = "T_Identifier"

            else:
                category = "ERROR"

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

    def create_token(self, lexeme, line, col_start, col_finish, category):
        return Token(lexeme, line, col_start, col_finish, category)
