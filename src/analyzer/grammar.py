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
                (0, "Program"),
                (1, "Decl Program"),
                (2, "Decl"),
                (3, "Type ident ;"),
                (4, "FuncProtoInit ident ( Formals  ) StmtBlock"),
                (5, "static ConstType ident ;"),
                (6, "DeclAdditional"),
                (7, "class ident Extends Implements { Field  }"),
                (8, "interface ident { Prototype  }"),
                (9, "int"),
                (10, "double"),
                (11, "boolean"),
                (12, "string"),
                (13, "ConstType"),
                (14, "ident"),
                (15, "Type []"),
                (16, "Type"),
                (17, "void"),
                (18, "Type ident , Formals"),
                (19, "Type ident"),
                (20, "extends ident"),
                (21, "''"),
                (22, "Implements ident ImplementsIdentPlus"),
                (23, "''"),
                (24, ", ident ImplementsIdentPlus"),
                (25, "''"),
                (26, "DeclAdditional Field"),
                (27, "''"),
                (28, "FuncProtoInit ident ( Formals  ) ; Prototype"),
                (29, "''"),
                (30, "{ VariableDeclStar ConstDeclStar StmtStar }"),
                (31, "Type ident ; VariableDeclStar"),
                (32, "''"),
                (33, "static ConstType ident ; ConstDeclStar"),
                (34, "''"),
                (35, "Stmt StmtStar"),
                (36, "''"),
                (37, "Expr ;"),
                (38, ";"),
                (39, "if ( Expr  ) Stmt ElseStmt"),
                (40, "while ( Expr  ) Stmt"),
                (41, "for ( Expr ; Expr ; Expr  ) Stmt"),
                (42, "break ;"),
                (43, "return Expr ;"),
                (44, "System . out . println ( Expr PrintStmtExpr  ) ;"),
                (45, "StmtBlock"),
                (46, "else Stmt"),
                (47, "''"),
                (48, ", Expr PrintStmtExpr"),
                (49, "''"),
                (50, "ident Access = ExprSubLevel1"),
                (51, "ExprSubLevel1"),
                (52, "ExprSubLevel1 || ExprSubLevel2"),
                (53, "ExprSubLevel2"),
                (54, "ExprSubLevel2 != ExprSubLevel3"),
                (55, "ExprSubLevel3"),
                (56, "ExprSubLevel3 > ExprSubLevel4"),
                (57, "ExprSubLevel3 >= ExprSubLevel4"),
                (58, "ExprSubLevel4"),
                (59, "ExprSubLevel5 - ExprSubLevel6"),
                (60, "ExprSubLevel5"),
                (61, "ExprSubLevel5 / ExprSubLevel6"),
                (62, "ExprSubLevel5 % ExprSubLevel6"),
                (63, "ExprSubLevel6"),
                (64, "New ( ident  )"),
                (65, "ExprSubLevel7"),
                (66, "- ExprSubLevel8"),
                (67, "! ExprSubLevel8"),
                (68, "ExprSubLevel8"),
                (69, "( Expr )"),
                (70, "this"),
                (71, "intConstant"),
                (72, "doubleConstant"),
                (73, "booleanConstant"),
                (74, "stringConstant"),
                (75, "null"),
                (76, "ident Access"),
                (77, ". ident Access"),
                (78, "''"),
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
