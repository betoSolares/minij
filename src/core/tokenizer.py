import sys
import re

from .token import Token
from .lexeme import Lexeme

class Tokenizer:
    def __init__(self):
        self.__reservedwords__ = [
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
        self.__deciPattern__ = r"^[0-9]+$"
        self.__hexaPattern__ = r"^0[x|X][0-9a-fA-F]+$"
        self.__doublePattern__ = r"^[0-9]+.[0-9]*([e|E][+|-]?[0-9]+)?$"
        self.__strPattern__ = r"^\"[^\"\n]*\"$"
        self.__IdPattern_ = r"^[a-zA-Z\$][0-9a-zA-Z\$]*$"

    def categorize(self, lexeme_list):
        #Match all lexems with their category
        tokens = []
        category = ""

        for lexeme in lexemes_list:

            #Recognize reserved word
            if lexeme.word in self.__reservedwords__:
                category = "T_" + lexeme.word

            #Recognize decimal whole number
            elif re.search(__deciPattern__, lexeme.word):
                category = "T_IntConstant_Decimal (value = " + lexeme.word + ")"

            #Recognize hexadecimal whole number
            elif re.search(__hexaPattern__, lexeme.word):
                category = "T_IntConstant_Hexadecimal (value =" + lexeme.word + ")"

            #Recognize double constant
            elif re.search(__doublePattern__, lexeme.word):
                category = "T_DoubleConstant (value =" + lexeme.word + ")"

            #Recognize string constant
            elif re.search(__strPattern__, lexeme.word):
                category = "T_StrConstant"

            #Recognize boolean constant
            elif lexeme.word == "true" or lexeme.word == "false":
                category = "T_BoolConstant"

            #Recognize double operator
            elif lexeme.word in self.__double_operator__:
                category = "T_DoubleOperator"

            #Recognize single operator
            elif lexeme.word in self.__single_operator__:
                category = "T_SingleOperator"
            #Recognize indentifier
            elif re.search(__IdPattern_, lexeme.word):
                category = "T_Identifier"

            else:
                category = "ERROR"

            tokens.append(self.create_token(lexeme.word, lexeme.line, lexeme.col_start, lexeme.col_finish, category))
    return tokens

    def create_token(self, lexeme, line, col_start, col_finish, category):
        return Token(lexeme, line, col_start, col_finish, category)
