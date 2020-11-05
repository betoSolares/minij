import os
import sys

import pyexcel as pe
import pyexcel_xls


class Grammar:
    def __init__(self):
        self.__rules__ = self.__set_rules__()
        self.__terminals__ = self.__set_terminals__()
        self.__table__ = self.__set_table__()

    @property
    def rules(self):
        return self.__rules__

    @property
    def terminals(self):
        return self.__terminals__

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
                (3, ["Decl", "VariableDecl"]),
                (4, ["Decl", "FunctionDecl"]),
                (5, ["Decl", "ConstDecl"]),
                (6, ["Decl", "ClassDecl"]),
                (7, ["Decl", "InterfaceDecl"]),
                (8, ["VariableDecl", "Variable ;"]),
                (9, ["Variable", "Type ident"]),
                (10, ["ConstDecl", "static ConstType ident ;"]),
                (11, ["ConstType", "int"]),
                (12, ["ConstType", "double"]),
                (13, ["ConstType", "boolean"]),
                (14, ["ConstType", "string"]),
                (15, ["Type", "int TypeArray"]),
                (16, ["Type", "double TypeArray"]),
                (17, ["Type", "boolean TypeArray"]),
                (18, ["Type", "string TypeArray"]),
                (19, ["Type", "ident TypeArray"]),
                (20, ["TypeArray", "[] TypeArray"]),
                (21, ["TypeArray", "''"]),
                (22, ["FunctionDecl", "Type ident ( Formals ) StmtBlock"]),
                (23, ["FunctionDecl", "void ident ( Formals ) StmtBlock"]),
                (24, ["Formals", "Variable , Formals"]),
                (25, ["Formals", "Variable"]),
                (
                    26,
                    [
                        "ClassDecl",
                        "class ident Extends Implements  { FieldStar }",
                    ],
                ),
                (27, ["Extends", "extends ident"]),
                (28, ["Extends", "''"]),
                (29, ["Implements", "implements ident ImplementsIdentPlus"]),
                (30, ["Implements", "''"]),
                (31, ["ImplementsIdentPlus", ", ident ImplementsIdentPlus"]),
                (32, ["ImplementsIdentPlus", "''"]),
                (33, ["FieldStar", "Field FieldStar"]),
                (34, ["FieldStar", "''"]),
                (35, ["Field", "VariableDecl"]),
                (36, ["Field", "FunctionDecl"]),
                (37, ["Field", "ConstDecl"]),
                (38, ["InterfaceDecl", "interface ident { PrototypeStar }"]),
                (39, ["PrototypeStar", "Prototype PrototypeStar"]),
                (40, ["PrototypeStar", "''"]),
                (41, ["Prototype", "Type ident ( Formals ) ;"]),
                (42, ["Prototype", "void ident ( Formals ) ;"]),
                (43, ["StmtBlock", "{ StmtBlockDeclStar }"]),
                (44, ["StmtBlockDeclStar", "StmtBlockDecl StmtBlockDeclStar"]),
                (45, ["StmtBlockDeclStar", "''"]),
                (46, ["StmtBlockDecl", "VariableDecl"]),
                (47, ["StmtBlockDecl", "ConstDecl"]),
                (48, ["StmtBlockDecl", "Stmt"]),
                (49, ["Stmt", "OpenStmt"]),
                (50, ["Stmt", "ClosedStmt"]),
                (51, ["OpenStmt", "if ( Expr ) Stmt"]),
                (52, ["OpenStmt", "if ( Expr ) ClosedStmt else OpenStmt"]),
                (53, ["OpenStmt", "for ( Expr ; Expr ; Expr ) OpenStmt"]),
                (54, ["OpenStmt", "while ( Expr ) OpenStmt"]),
                (55, ["ClosedStmt", "SimpleStatemet"]),
                (56, ["ClosedStmt", "if ( Expr ) ClosedStmt else ClosedStmt"]),
                (57, ["ClosedStmt", "for ( Expr ; Expr ; Expr ) ClosedStmt"]),
                (58, ["ClosedStmt", "while ( Expr ) ClosedStmt"]),
                (59, ["SimpleStatemet", "Expr ;"]),
                (60, ["SimpleStatemet", ";"]),
                (61, ["SimpleStatemet", "BreakStmt"]),
                (62, ["SimpleStatemet", "ReturnStmt"]),
                (63, ["SimpleStatemet", "PrintStmt"]),
                (64, ["SimpleStatemet", "StmtBlock"]),
                (65, ["ReturnStmt", "return Expr ;"]),
                (66, ["BreakStmt", "break ;"]),
                (67, ["PrintStmt", "System . out . println ( ExprPlus )"]),
                (68, ["ExprPlus", "Expr , ExprPlus"]),
                (69, ["ExprPlus", "Expr"]),
                (70, ["Expr", "ident Access = ExprSubLevel1"]),
                (71, ["Expr", "ExprSubLevel1"]),
                (72, ["ExprSubLevel1", "ExprSubLevel1 || ExprSubLevel2"]),
                (73, ["ExprSubLevel1", "ExprSubLevel2"]),
                (74, ["ExprSubLevel2", "ExprSubLevel2 != ExprSubLevel3"]),
                (75, ["ExprSubLevel2", "ExprSubLevel3"]),
                (76, ["ExprSubLevel3", "ExprSubLevel3 > ExprSubLevel4"]),
                (77, ["ExprSubLevel3", "ExprSubLevel3 >= ExprSubLevel4"]),
                (78, ["ExprSubLevel3", "ExprSubLevel4"]),
                (79, ["ExprSubLevel4", "ExprSubLevel4 - ExprSubLevel5"]),
                (80, ["ExprSubLevel4", "ExprSubLevel5"]),
                (81, ["ExprSubLevel5", "ExprSubLevel5 / ExprSubLevel6"]),
                (82, ["ExprSubLevel5", "ExprSubLevel5 % ExprSubLevel6"]),
                (83, ["ExprSubLevel5", "ExprSubLevel6"]),
                (84, ["ExprSubLevel6", "New ( ident )"]),
                (85, ["ExprSubLevel6", "ExprSubLevel7"]),
                (86, ["ExprSubLevel7", "- ExprSubLevel8"]),
                (87, ["ExprSubLevel7", "! ExprSubLevel8"]),
                (88, ["ExprSubLevel7", "ExprSubLevel8"]),
                (89, ["ExprSubLevel8", "( Expr )"]),
                (90, ["ExprSubLevel8", "this"]),
                (91, ["ExprSubLevel8", "intConstant"]),
                (92, ["ExprSubLevel8", "doubleConstant"]),
                (93, ["ExprSubLevel8", "booleanConstant"]),
                (94, ["ExprSubLevel8", "stringConstant"]),
                (95, ["ExprSubLevel8", "null"]),
                (96, ["ExprSubLevel8", "ident Access"]),
                (97, ["Access", ". ident Access"]),
                (98, ["Access", "''"]),
            ]
        )

    # List of terminals in the grammar
    def __set_terminals__(self):
        return [
            ";",
            "ident",
            "static",
            "int",
            "double",
            "boolean",
            "string",
            "[]",
            "(",
            ")",
            "void",
            ",",
            "class",
            "{",
            "}",
            "extends",
            "implements",
            "interface",
            "if",
            "else",
            "for",
            "while",
            "return",
            "break",
            "System",
            ".",
            "out",
            "println",
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
