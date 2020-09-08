class Parser:
    def __init__(self):
        self.__tokens__ = None
        self.__errors__ = []
        self.cursor = 0
        self.saved = 0

    # Try to parse the tokens list, true if no errors
    def try_parse(self, tokens):
        # self.__tokens__ = iter(tokens)
        self.__tokens__ = tokens

        # Parse method
        return len(self.__errors__) == 0

    # Get all the errors
    def get_errors(self):
        return self.__errors__

    # Add a new error to the list
    def __add_error__(self, token, expect):
        exp = self.__multiple_expected__(expect) if len(expect) > 0 else expect
        self.__errors__.append(
            "*** Syntax Error *** on line "
            + str(token.line)
            + " "
            + exp
            + " was expected and got "
            + token.word
        )

    # Get the next token in the list
    # def __get_next_token__(self):
    #     return next(self.__tokens__, None)

    # Concatenate all the expected in a single string
    def __multiple_expected__(self, expected):
        return " or ".join(expected)

    def Program(self):
        return self.Decl and self._Program

    def _Program(self):
        if self.Program:
            return True
        else:
            return True

    def Decl(self):
        if self.VarDecl:
            return True
        elif self.FuncDeclare:
            return True
        else:
            # Backtracking
            return False

    def VarDecl(self):
        return self.Variable and self.term(";")

    def Variable(self):
        return self.Type and self.term_cat("T_Identifier")

    def Type(self):
        if self.lookahead_term == "int":
            self.save_cursor
            return self.term("int") and self._Type
        elif self.lookahead_term == "double":
            self.backtrack
            self.save_cursor
            return self.term("double") and self._Type
        elif self.lookahead_term == "boolean":
            return self.term("boolean") and self._Type
        elif self.lookahead_term == "string":
            return self.term("string") and self._Type
        elif self.lookahead_cat == "T_Identifier":
            return self.term_cat("T_Identifier") and self._Type
        else:
            # Backtracking
            return False

    def _Type(self):
        if self.lookahead_term == "[]":
            return self.term("[]") and self._Type
        else:
            # epsilon?
            return True

    def FuncDeclare(self):
        if self.lookahead_term == "void":
            return (
                self.term("void")
                and self.term_cat("T_Identifier")
                and self.term("(")
                and self.Formals
                and self.term(")")
                and self._Stmt
            )
        elif self.lookahead_cat == "T_Identifier":
            return (
                self.Type
                and self.term_cat("T_Identifier")
                and self.term("(")
                and self.Formals
                and self.term(")")
                and self._Stmt
            )
        else:
            # Backtracking
            return False

    def _Stmt(self):
        if self.Stmt and self._Stmt:
            return True
        else:
            return True

    def Formals(self):
        if self._Variable and self.term(","):
            return True
        else:
            return True

    def _Variable(self):
        if self.Variable:
            return True
        elif self.Variable and self._Variable:
            return True

    def Stmt(self):
        if self.IfStmt:
            return True
        elif self.ForStmt:
            return True
        elif self.Expr and self.term(";"):
            return True
        else:
            # Backtracking
            return False

    def IfStmt(self):
        if self.lookahead_term == "if":
            return (
                self.term("if")
                and self.term("(")
                and self.Expr
                and self.term(")")
                and self.Stmt
                and self.ElseStmt
            )
        else:
            # Error?
            return False

    def ElseStmt(self):
        if self.lookahead_term == "else":
            return self.term("else") and self.Stmt
        else:
            # epsilon
            return True

    def ForStmt(self):
        if self.lookahead_term == "for":
            return (
                self.term("for")
                and self.term("(")
                and self.OptExpr
                and self.term(";")
                and self.Expr
                and self.term(";")
                and self.OptExpr
                and self.term(")")
                and self.Stmt
            )

    def OptExpr(self):
        if self.Expr:
            return True
        else:
            return True

    def MultExpr(self):
        if self.Expr:
            return True
        elif self.Expr and self.MultExpr:
            return True

    def Expr(self):
        if self.LValue and self.term("=") and self._Expr:
            return True
        elif self._Expr:
            return True
        else:
            # Backtracking
            return False

    def _Expr(self):
        if self.T and self._E:
            return True
        else:
            # Backtracking
            return False

    def _E(self):
        if self.lookahead_term == "||":
            return self.term("||") and self.T and self._E
        else:
            # epsilon
            return True

    def T(self):
        if self.F and self._T:
            return True
        else:
            # Backtracking
            return False

    def _T(self):
        if self.term("&&") and self.F and self._T:
            return True
        else:
            # epsilon
            return True

    def F(self):
        if self.G and self._F:
            return True
        else:
            # Backtracking
            return False

    def _F(self):
        if self.lookahead_term == "==":
            return self.term("==") and self.G and self._F
        elif self.lookahead_term == "!=":
            return self.term("!=") and self.G and self._F
        else:
            # epsilon
            return True

    def G(self):
        if self.H and self._G:
            return True
        else:
            # Backtracking
            return False

    def _G(self):
        if self.lookahead_term == "<":
            return self.term("<") and self.H and self._G
        if self.lookahead_term == ">":
            return self.term(">") and self.H and self._G
        if self.lookahead_term == "<=":
            return self.term("<=") and self.H and self._G
        if self.lookahead_term == ">=":
            return self.term(">=") and self.H and self._G
        else:
            # epsilon
            return True

    def H(self):
        if self.J and self._H:
            return True
        else:
            # Backtracking
            return False

    def _H(self):
        if self.lookahead_term == "+":
            return self.term("+") and self.J and self._H
        elif self.lookahead_term == "-":
            return self.term("-") and self.J and self._H
        else:
            # Backtracking
            # epsilon
            return True

    def J(self):
        if self.K and self._J:
            return True
        else:
            # Backtracking
            return False

    def _J(self):
        if self.lookahead_term == "*":
            return self.term("*") and self.K and self._J
        elif self.lookahead_term == "/":
            return self.term("/") and self.K and self._J
        elif self.lookahead_term == "%":
            return self.term("%") and self.K and self._J
        else:
            # epsilon
            return True

    def K(self):
        if self.lookahead_term == "-":
            return self.term("-") and self.Expr
        elif self.lookahead_term == "!":
            return self.term("!") and self.Expr
        elif self.L:
            return True
        else:
            # Backtracking
            return False

    def L(self):
        if self.lookahead_term == "(":
            return self.term("(") and self.Expr and self.term(")")
        elif self.lookahead_term == "this":
            return self.term("this")
        elif self.lookahead_term == "New":
            return (
                self.term("New")
                and self.term("(")
                and self.term_cat("T_Identifier")
                and self.term(")")
            )
        elif self.Constant:
            return True
        elif self.LValue:
            return True
        else:
            # Backtracking and error
            return False

    def LValue(self):
        if self.lookahead_cat == "T_Identifier":
            return self.term_cat("T_Identifier")
        elif self.Expr and self.term(".") and self.term_cat("T_Identifier"):
            return True
        elif self.Expr and self.term("[") and self.Expr and self.term("]"):
            return True
        else:
            # Backtracking and error
            return False

    def Constant(self):
        if self.lookahead_cat == "T_IntConstant_Hexadecimal":
            return self.term_cat("T_IntConstant_Hexadecimal")
        elif self.lookahead_cat == "T_IntConstant_Decimal":
            return self.term_cat("T_IntConstant_Decimal")
        elif self.lookahead_cat == "T_StringConstant":
            return self.term_cat("T_StringConstant")
        elif self.lookahead_cat == "T_BooleanConstant":
            return self.term_cat("T_BooleanConstant")
        elif self.lookahead_cat == "T_DoubleConstant":
            return self.term_cat("T_DoubleConstant")
        else:
            # epsilon
            return True

    def term(self, expected):
        if self.__tokens__[self.cursor].word == expected:
            self.cursor += self.cursor
            return True
        else:
            return False

    def term_cat(self, expected):
        if self.__tokens__[self.cursor].category == expected:
            self.cursor += self.cursor
            return True
        else:
            return False

    def save_cursor(self):
        self.saved = self.cursor

    def backtrack(self):
        self.cursor = self.saved

    def lookahead_term(self):
        return self.__tokens__[self.cursor].word

    def lookahead_cat(self):
        return self.__tokens__[self.cursor].category
