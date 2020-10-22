import os
import sys

import pyexcel as pe
import pyexcel_xls


class Grammar:
    def __init__(self):
        self.__rules__ = self.__set_rules__()
        self.__terminals__ = self.__set_terminals()
        self.__nonterminals__ = self.__set_nonterminals__()
        self.__table__ = self.__set_table__()

    @property
    def rules(self):
        return self.__rules__

    @property
    def terminals(self):
        return self.__terminals__

    @property
    def nonterminals(self):
        return self.__nonterminals__

    @property
    def table(self):
        return self.__table__

    # Set the rules of the grammar
    def __set_rules__(self):
        return dict(
            [
                (0, ["Init", "Program"]),
                (1, ["Program", "Decl Program"]),
                (2, ["Program", "Decl"]),
                (3, ["DeclAdditional", "Type ident ;"]),
                (
                    4,
                    [
                        "DeclAdditional",
                        "FuncProtoInit ident ( Formals  ) StmtBlock",
                    ],
                ),
                (5, ["DeclAdditional", "static ConstType ident ;"]),
                (6, ["Decl", "DeclAdditional"]),
                (7, ["Decl", "class ident Extends Implements { Field  }"]),
                (8, ["Decl", "interface ident { Prototype  }"]),
                (9, ["ConstType", "int"]),
                (10, ["ConstType", "double"]),
                (11, ["ConstType", "boolean"]),
                (12, ["ConstType", "string"]),
                (13, ["Type", "ConstType"]),
                (14, ["Type", "ident"]),
                (15, ["Type", "Type []"]),
                (16, ["FuncProtoInit", "Type"]),
                (17, ["FuncProtoInit", "void"]),
                (18, ["Formals", "Type ident , Formals"]),
                (19, ["Formals", "Type ident"]),
                (20, ["Extends", "extends ident"]),
                (21, ["Extends", "''"]),
                (22, ["Implements", "Implements ident ImplementsIdentPlus"]),
                (23, ["Implements", "''"]),
                (24, ["ImplementsIdentPlus", ", ident ImplementsIdentPlus"]),
                (25, ["ImplementsIdentPlus", "''"]),
                (26, ["Field", "DeclAdditional Field"]),
                (27, ["Field", "''"]),
                (
                    28,
                    [
                        "Prototype",
                        "FuncProtoInit ident ( Formals  ) ; Prototype",
                    ],
                ),
                (29, ["Prototype", "''"]),
                (
                    30,
                    ["StmtBlock", "{ VariableDeclStar ConstDeclStar StmtStar }"],
                ),
                (31, ["VariableDeclStar", "Type ident ; VariableDeclStar"]),
                (32, ["VariableDeclStar", "''"]),
                (
                    33,
                    ["ConstDeclStar", "static ConstType ident ; ConstDeclStar"],
                ),
                (34, ["ConstDeclStar", "''"]),
                (35, ["StmtStar", "Stmt StmtStar"]),
                (36, ["StmtStar", "''"]),
                (37, ["Stmt", "Expr ;"]),
                (38, ["Stmt", ";"]),
                (39, ["Stmt", "if ( Expr  ) Stmt ElseStmt"]),
                (40, ["Stmt", "while ( Expr  ) Stmt"]),
                (41, ["Stmt", "for ( Expr ; Expr ; Expr  ) Stmt"]),
                (42, ["Stmt", "break ;"]),
                (43, ["Stmt", "return Expr ;"]),
                (
                    44,
                    ["Stmt", "System . out . println ( Expr PrintStmtExpr  ) ;"],
                ),
                (45, ["Stmt", "StmtBlock"]),
                (46, ["ElseStmt", "else Stmt"]),
                (47, ["ElseStmt", "''"]),
                (48, ["PrintStmtExpr", ", Expr PrintStmtExpr"]),
                (49, ["PrintStmtExpr", "''"]),
                (50, ["Expr", "ident Access = ExprSubLevel1"]),
                (51, ["Expr", "ExprSubLevel1"]),
                (52, ["ExprSubLevel1", "ExprSubLevel1 || ExprSubLevel2"]),
                (53, ["ExprSubLevel1", "ExprSubLevel2"]),
                (54, ["ExprSubLevel2", "ExprSubLevel2 != ExprSubLevel3"]),
                (55, ["ExprSubLevel2", "ExprSubLevel3"]),
                (56, ["ExprSubLevel3", "ExprSubLevel3 > ExprSubLevel4"]),
                (57, ["ExprSubLevel3", "ExprSubLevel3 >= ExprSubLevel4"]),
                (58, ["ExprSubLevel3", "ExprSubLevel4"]),
                (59, ["ExprSubLevel4", "ExprSubLevel5 - ExprSubLevel6"]),
                (60, ["ExprSubLevel4", "ExprSubLevel5"]),
                (61, ["ExprSubLevel5", "ExprSubLevel5 / ExprSubLevel6"]),
                (62, ["ExprSubLevel5", "ExprSubLevel5 % ExprSubLevel6"]),
                (63, ["ExprSubLevel5", "ExprSubLevel6"]),
                (64, ["ExprSubLevel6", "New ( ident  )"]),
                (65, ["ExprSubLevel6", "ExprSubLevel7"]),
                (66, ["ExprSubLevel7", "- ExprSubLevel8"]),
                (67, ["ExprSubLevel7", "! ExprSubLevel8"]),
                (68, ["ExprSubLevel7", "ExprSubLevel8"]),
                (69, ["ExprSubLevel8", "( Expr )"]),
                (70, ["ExprSubLevel8", "this"]),
                (71, ["ExprSubLevel8", "intConstant"]),
                (72, ["ExprSubLevel8", "doubleConstant"]),
                (73, ["ExprSubLevel8", "booleanConstant"]),
                (74, ["ExprSubLevel8", "stringConstant"]),
                (75, ["ExprSubLevel8", "null"]),
                (76, ["ExprSubLevel8", "ident Access"]),
                (77, ["Access", ". ident Access"]),
                (78, ["Access", "''"]),
            ]
        )

    # List of terminals in the grammar
    def __set_terminals(self):
        return [
            "ident",
            ";",
            "(",
            ")",
            "static",
            "class",
            "{",
            "}",
            "interface",
            "int",
            "double",
            "boolean",
            "string",
            "[]",
            "void",
            ",",
            "extends",
            "if",
            "while",
            "for",
            "break",
            "return",
            "System",
            ".",
            "out",
            "println",
            "else",
            "=",
            "||",
            "!=",
            ">",
            ">=",
            "-",
            "/",
            "%",
            "New",
            "!",
            "this",
            "intConstant",
            "doubleConstant",
            "booleanConstant",
            "stringConstant",
            "null",
        ]

    # List of non terminals in the grammar
    def __set_nonterminals__(self):
        return [
            "Init",
            "Program",
            "DeclAdditional",
            "Decl",
            "ConstType",
            "Type",
            "FuncProtoInit",
            "Formals",
            "Extends",
            "Implements",
            "ImplementsIdentPlus",
            "Field",
            "Prototype",
            "StmtBlock",
            "VariableDeclStar",
            "ConstDeclStar",
            "StmtStar",
            "Stmt",
            "ElseStmt",
            "PrintStmtExpr",
            "Expr",
            "ExprSubLevel1",
            "ExprSubLevel2",
            "ExprSubLevel3",
            "ExprSubLevel4",
            "ExprSubLevel5",
            "ExprSubLevel6",
            "ExprSubLevel7",
            "ExprSubLevel8",
            "Access",
        ]

    # The parsing table
    def __set_table__(self):
        return pe.get_array(
            file_name=self.__resource_path__("docs/ParsingTable.xlsx")
        )

    # Get the path to the resources, works for dev and PyInstaller
    def __resource_path__(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
