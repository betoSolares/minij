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
    # Number, Head, Body, Precedence
    def __set_rules__(self):
        return dict(
            [
                (0, ["Init", "Program", 0]),
                (1, ["Program", "Decl Program", 0]),
                (2, ["Program", "Decl", 0]),
                (3, ["DeclAdditional", "Type ident ;", 11]),
                (
                    4,
                    [
                        "DeclAdditional",
                        "FuncProtoInit ident ( Formals  ) StmtBlock",
                        9,
                    ],
                ),
                (5, ["DeclAdditional", "static ConstType ident ;", 11]),
                (6, ["Decl", "DeclAdditional", 0]),
                (7, ["Decl", "class ident Extends Implements { Field  }", 13]),
                (8, ["Decl", "interface ident { Prototype  }", 13]),
                (9, ["ConstType", "int", 14]),
                (10, ["ConstType", "double", 14]),
                (11, ["ConstType", "boolean", 14]),
                (12, ["ConstType", "string", 14]),
                (13, ["Type", "ConstType", 0]),
                (14, ["Type", "ident", 10]),
                (15, ["Type", "Type []", 9]),
                (16, ["FuncProtoInit", "Type", 0]),
                (17, ["FuncProtoInit", "void", 14]),
                (18, ["Formals", "Type ident , Formals", 12]),
                (19, ["Formals", "Type ident", 10]),
                (20, ["Extends", "extends ident", 10]),
                (21, ["Extends", "''", 10]),
                (22, ["Implements", "Implements ident ImplementsIdentPlus", 10]),
                (23, ["Implements", "''", 10]),
                (24, ["ImplementsIdentPlus", ", ident ImplementsIdentPlus", 10]),
                (25, ["ImplementsIdentPlus", "''", 11]),
                (26, ["Field", "DeclAdditional Field", 0]),
                (27, ["Field", "''", 0]),
                (
                    28,
                    [
                        "Prototype",
                        "FuncProtoInit ident ( Formals  ) ; Prototype",
                        11,
                    ],
                ),
                (29, ["Prototype", "''", 11]),
                (
                    30,
                    [
                        "StmtBlock",
                        "{ VariableDeclStar ConstDeclStar StmtStar }",
                        13,
                    ],
                ),
                (31, ["VariableDeclStar", "Type ident ; VariableDeclStar", 11]),
                (32, ["VariableDeclStar", "''", 11]),
                (
                    33,
                    [
                        "ConstDeclStar",
                        "static ConstType ident ; ConstDeclStar",
                        11,
                    ],
                ),
                (34, ["ConstDeclStar", "''", 11]),
                (35, ["StmtStar", "Stmt StmtStar", 0]),
                (36, ["StmtStar", "''", 0]),
                (37, ["Stmt", "Expr ;", 11]),
                (38, ["Stmt", ";", 11]),
                (39, ["Stmt", "if ( Expr  ) Stmt ElseStmt", 9]),
                (40, ["Stmt", "while ( Expr  ) Stmt", 9]),
                (41, ["Stmt", "for ( Expr ; Expr ; Expr  ) Stmt", 9]),
                (42, ["Stmt", "break ;", 11]),
                (43, ["Stmt", "return Expr ;", 11]),
                (
                    44,
                    [
                        "Stmt",
                        "System . out . println ( Expr PrintStmtExpr  ) ;",
                        11,
                    ],
                ),
                (45, ["Stmt", "StmtBlock", 0]),
                (46, ["ElseStmt", "else Stmt", 14]),
                (47, ["ElseStmt", "''", 14]),
                (48, ["PrintStmtExpr", ", Expr PrintStmtExpr", 12]),
                (49, ["PrintStmtExpr", "''", 0]),
                (50, ["Expr", "ident Access = ExprSubLevel1", 1]),
                (51, ["Expr", "ExprSubLevel1", 0]),
                (52, ["ExprSubLevel1", "ExprSubLevel1 || ExprSubLevel2", 2]),
                (53, ["ExprSubLevel1", "ExprSubLevel2", 0]),
                (54, ["ExprSubLevel2", "ExprSubLevel2 != ExprSubLevel3", 3]),
                (55, ["ExprSubLevel2", "ExprSubLevel3", 0]),
                (56, ["ExprSubLevel3", "ExprSubLevel3 > ExprSubLevel4", 4]),
                (57, ["ExprSubLevel3", "ExprSubLevel3 >= ExprSubLevel4", 4]),
                (58, ["ExprSubLevel3", "ExprSubLevel4", 0]),
                (59, ["ExprSubLevel4", "ExprSubLevel4 - ExprSubLevel5", 5]),
                (60, ["ExprSubLevel4", "ExprSubLevel5", 0]),
                (61, ["ExprSubLevel5", "ExprSubLevel5 / ExprSubLevel6", 6]),
                (62, ["ExprSubLevel5", "ExprSubLevel5 % ExprSubLevel6", 6]),
                (63, ["ExprSubLevel5", "ExprSubLevel6", 0]),
                (64, ["ExprSubLevel6", "New ( ident  )", 9]),
                (65, ["ExprSubLevel6", "ExprSubLevel7", 0]),
                (66, ["ExprSubLevel7", "- ExprSubLevel8", 5]),
                (67, ["ExprSubLevel7", "! ExprSubLevel8", 8]),
                (68, ["ExprSubLevel7", "ExprSubLevel8", 0]),
                (69, ["ExprSubLevel8", "( Expr )", 9]),
                (70, ["ExprSubLevel8", "this", 10]),
                (71, ["ExprSubLevel8", "intConstant", 10]),
                (72, ["ExprSubLevel8", "doubleConstant", 10]),
                (73, ["ExprSubLevel8", "booleanConstant", 10]),
                (74, ["ExprSubLevel8", "stringConstant", 10]),
                (75, ["ExprSubLevel8", "null", 10]),
                (76, ["ExprSubLevel8", "ident Access", 10]),
                (77, ["Access", ". ident Access", 10]),
                (78, ["Access", "''", 10]),
            ]
        )

    # List of terminals in the grammar
    # Terminal, Precedence
    def __set_terminals(self):
        return dict(
            [
                ("ident", 10),
                (";", 11),
                ("(", 9),
                (")", 9),
                ("static", 14),
                ("class", 14),
                ("{", 13),
                ("}", 13),
                ("interface", 14),
                ("int", 14),
                ("double", 14),
                ("boolean", 14),
                ("string", 14),
                ("[]", 9),
                ("void", 14),
                (",", 12),
                ("extends", 14),
                ("implements", 14),
                ("if", 14),
                ("while", 14),
                ("for", 14),
                ("break", 14),
                ("return", 14),
                ("System", 14),
                (".", 9),
                ("out", 14),
                ("println", 14),
                ("else", 14),
                ("=", 1),
                ("||", 2),
                ("!=", 3),
                (">", 4),
                (">=", 4),
                ("-", 5),
                ("/", 6),
                ("%", 6),
                ("New", 7),
                ("!", 8),
                ("this", 10),
                ("intConstant", 10),
                ("doubleConstant", 10),
                ("booleanConstant", 10),
                ("stringConstant", 10),
                ("null", 10),
            ]
        )

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
