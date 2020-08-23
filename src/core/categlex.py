import sys
import re

class Categorizer:

    def __init__(self):

        self.__symbols__ = [
            "+",
            "-",
            "*",
            "/",
            "%",
            "<",
            "=",
            ">",
            "!",
            "&",
            "|",
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

        self.__keywords__ = [
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

        deciPattern = r'[0-9]+'
        deciPattern = r"^[0-9]+$"
        hexaPattern = r"^0[x|X][0-9a-fA-F]+$"
        doublePattern = r"^[0-9]+.[0-9]*([e|E][+|-]?[0-9]+)?$"
        strPattern = r"^\"[^\"\n]*\"$"

    def categorize(self, lexemes_list):
        for word in lexemes_list.items():

        return
