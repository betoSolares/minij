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
        breakpoint()
        return self.Program() and len(self.__errors__) == 0

    # Get all the errors
    def get_errors(self):
        return self.__errors__

    # Add a new error to the list
    def __add_error__(self, token, expect):
        exp = self.__multiple_expected__(expect) if len(expect) > 0 else expect
        cols = self.__error_columns__(token)
        self.__errors__.append(
            "*** Syntax Error *** on line "
            + str(token.line)
            + cols
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

    # Beginning of parsing algorithm
    def Program(self):
        return self.Decl() and self._Program()

    def _Program(self):
        if self.Program():
            return True
        else:
            return True

    def Decl(self):
        if self.VarDecl():
            return True
        elif self.FuncDeclare():
            return True
        else:
            # Backtracking
            return False

    def VarDecl(self):
        return self.Variable() and self.term(";")

    def Variable(self):
        return self.Type() and self.term_cat("Identifier")

    def Type(self):
        lookahead = self.lookahead_term()
        if lookahead == "int":
            self.save_cursor
            return self.term("int") and self._Type()
        elif lookahead == "double":
            self.backtrack
            self.save_cursor
            return self.term("double") and self._Type()
        elif lookahead == "boolean":
            return self.term("boolean") and self._Type()
        elif lookahead == "string":
            return self.term("string") and self._Type()
        elif self.lookahead_cat() == "Identifier":
            return self.term_cat("Identifier") and self._Type()
        else:
            # Backtracking
            return False

    def _Type(self):
        if self.lookahead_term() == "[]":
            return self.term("[]") and self._Type()
        else:
            # epsilon?
            return True

    def FuncDeclare(self):
        if self.lookahead_term() == "void":
            return (
                self.term("void")
                and self.term_cat("Identifier")
                and self.term("(")
                and self.Formals()
                and self.term(")")
                and self._Stmt()
            )
        elif self.lookahead_cat() == "Identifier":
            return (
                self.Type()
                and self.term_cat("Identifier")
                and self.term("(")
                and self.Formals()
                and self.term(")")
                and self._Stmt()
            )
        else:
            # Backtracking
            return False

    def _Stmt(self):
        if self.Stmt() and self._Stmt():
            return True
        else:
            # epsilon
            return True

    def Formals(self):
        if self._Variable() and self.term(","):
            return True
        else:
            return True

    def _Variable(self):
        if self.Variable():
            return True
        elif self.Variable() and self._Variable():
            return True

    def Stmt(self):
        if self.IfStmt():
            return True
        elif self.ForStmt():
            return True
        elif self.Expr() and self.term(";"):
            return True
        else:
            # Backtracking
            return False

    def IfStmt(self):
        if self.lookahead_term() == "if":
            return (
                self.term("if")
                and self.term("(")
                and self.Expr()
                and self.term(")")
                and self.Stmt()
                and self.ElseStmt()
            )
        else:
            # Error?
            return False

    def ElseStmt(self):
        if self.lookahead_term() == "else":
            return self.term("else") and self.Stmt
        else:
            # epsilon
            return True

    def ForStmt(self):
        if self.lookahead_term() == "for":
            return (
                self.term("for")
                and self.term("(")
                and self.OptExpr()
                and self.term(";")
                and self.Expr()
                and self.term(";")
                and self.OptExpr()
                and self.term(")")
                and self.Stmt()
            )

    def OptExpr(self):
        if self.Expr():
            return True
        else:
            return True

    def MultExpr(self):
        if self.Expr():
            return True
        elif self.Expr() and self.MultExpr():
            return True

    def Expr(self):
        if self.LValue() and self.term("=") and self._Expr():
            return True
        elif self._Expr():
            return True
        else:
            # Backtracking
            return False

    def _Expr(self):
        if self.T() and self._E():
            return True
        else:
            # Backtracking
            return False

    def _E(self):
        if self.lookahead_term() == "||":
            return self.term("||") and self.T() and self._E()
        else:
            # epsilon
            return True

    def T(self):
        if self.F() and self._T():
            return True
        else:
            # Backtracking
            return False

    def _T(self):
        if self.term("&&") and self.F() and self._T():
            return True
        else:
            # epsilon
            return True

    def F(self):
        if self.G() and self._F():
            return True
        else:
            # Backtracking
            return False

    def _F(self):
        lookahead = self.lookahead_term()
        if lookahead == "==":
            return self.term("==") and self.G() and self._F()
        elif lookahead == "!=":
            return self.term("!=") and self.G() and self._F()
        else:
            # epsilon
            return True

    def G(self):
        if self.H() and self._G():
            return True
        else:
            # Backtracking
            return False

    def _G(self):
        lookahead = self.lookahead_term()
        if lookahead == "<":
            return self.term("<") and self.H() and self._G()
        if lookahead == ">":
            return self.term(">") and self.H() and self._G()
        if lookahead == "<=":
            return self.term("<=") and self.H() and self._G()
        if lookahead == ">=":
            return self.term(">=") and self.H() and self._G()
        else:
            # epsilon
            return True

    def H(self):
        if self.J() and self._H():
            return True
        else:
            # Backtracking
            return False

    def _H(self):
        lookahead = self.lookahead_term()
        if lookahead == "+":
            return self.term("+") and self.J() and self._H()
        elif lookahead == "-":
            return self.term("-") and self.J() and self._H()
        else:
            # Backtracking
            # epsilon
            return True

    def J(self):
        if self.K() and self._J():
            return True
        else:
            # Backtracking
            return False

    def _J(self):
        lookahead = self.lookahead_term()
        if lookahead == "*":
            return self.term("*") and self.K() and self._J()
        elif lookahead == "/":
            return self.term("/") and self.K() and self._J()
        elif lookahead == "%":
            return self.term("%") and self.K() and self._J()
        else:
            # epsilon
            return True

    def K(self):
        lookahead = self.lookahead_term()
        if lookahead == "-":
            return self.term("-") and self.Expr()
        elif lookahead == "!":
            return self.term("!") and self.Expr()
        elif self.L():
            return True
        else:
            # Backtracking
            return False

    def L(self):
        lookahead = self.lookahead_term()
        if lookahead == "(":
            return self.term("(") and self.Expr() and self.term(")")
        elif lookahead == "this":
            return self.term("this")
        elif lookahead == "New":
            return (
                self.term("New")
                and self.term("(")
                and self.term_cat("Identifier")
                and self.term(")")
            )
        elif self.Constant():
            return True
        elif self.LValue():
            return True
        else:
            # Backtracking and error
            return False

    def LValue(self):
        if self.lookahead_cat() == "Identifier":
            return self.term_cat("Identifier")
        elif self.Expr() and self.term(".") and self.term_cat("Identifier"):
            return True
        elif self.Expr() and self.term("[") and self.Expr() and self.term("]"):
            return True
        else:
            # Backtracking and error
            return False

    def Constant(self):
        lookahead = self.lookahead_cat()
        if lookahead == "IntConstant_Hexadecimal":
            return self.term_cat("IntConstant_Hexadecimal")
        elif lookahead == "IntConstant_Decimal":
            return self.term_cat("IntConstant_Decimal")
        elif lookahead == "StringConstant":
            return self.term_cat("StringConstant")
        elif lookahead == "BooleanConstant":
            return self.term_cat("BooleanConstant")
        elif lookahead == "DoubleConstant":
            return self.term_cat("DoubleConstant")
        else:
            # epsilon
            return True

    def term(self, expected):
        if self.__tokens__[self.cursor].word == expected:
            self.cursor += 1
            return True
        else:
            return False

    def term_cat(self, expected):
        if self.__tokens__[self.cursor].category == expected:
            self.cursor += 1
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

    def __error_columns__(self, token):
        if token.finish is None:
            cols = " column " + str(token.start)
        else:
            cols = " columns " + str(token.start) + " to " + str(token.finish)

        return cols
