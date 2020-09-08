class Parser:
    def __init__(self):
        self.__tokens__ = None
        self.__errors__ = []
        cursor = 0
        saved_cursor = cursor

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
        if self.term("int") and self._Type:
            return True
        elif self.term("double") and self._Type:
            return True
        elif self.term("boolean") and self._Type:
            return True
        elif self.term("string") and self._Type:
            return True
        elif self.term_cat("T_Identifier") and self._Type:
            return True
        else:
            # Backtracking
            return False

    def _Type(self):
        if self.term("[]") and self._Type:
            return True
        else:
            return True

    def FuncDeclare(self):
        if (
            self.Type
            and self.term_cat("T_Identifier")
            and self.term("(")
            and self.Formals
            and self.term(")")
            and self._Stmt
        ):
            return True
        elif (
            self.term("void")
            and self.term_cat("T_Identifier")
            and self.term("(")
            and self.Formals
            and self.term(")")
            and self._Stmt
        ):
            return True
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
        return (
            self.term("if")
            and self.term("(")
            and self.Expr
            and self.term(")")
            and self.Stmt
            and self.ElseStmt
        )

    def ElseStmt(self):
        if self.term("else") and self.Stmt:
            return True
        else:
            # epsilon
            return True

    def ForStmt(self):
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
        if self.term("||") and self.T and self._E:
            return True
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
        if self.term("==") and self.G and self._F:
            return True
        elif self.term("!=") and self.G and self._F:
            return True
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
        if self.term("<") and self.H and self._G:
            return True
        elif self.term(">") and self.H and self._G:
            return True
        elif self.term("<=") and self.H and self._G:
            return True
        elif self.term(">=") and self.H and self._G:
            return True
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
        if self.term("+") and self.J and self._H:
            return True
        elif self.term("-") and self.J and self._H:
            return True
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
        if self.term("*") and self.K and self._J:
            return True
        elif self.term("/") and self.K and self._J:
            return True
        elif self.term("%") and self.K and self._J:
            return True
        else:
            # epsilon
            return True

    def K(self):
        if self.term("-") and self.Expr:
            return True
        elif self.term("!") and self.Expr:
            return True
        elif self.L:
            return True
        else:
            # Backtracking
            return False

    def L(self):
        if self.term("(") and self.Expr and self.term(")"):
            return True
        elif self.term("this"):
            return True
        elif (
            self.term("New")
            and self.term("(")
            and self.term_cat("T_Identifier", "category")
            and self.term(")")
        ):
            return True
        elif self.Constant:
            return True
        elif self.LValue:
            return True
        else:
            # Backtracking and error
            return False

    def LValue(self):
        if self.term_cat("T_Identifier"):
            return True
        elif self.Expr and self.term(".") and self.term_cat("T_Identifier"):
            return True
        elif self.Expr and self.term("[") and self.Expr and self.term("]"):
            return True
        else:
            # Backtracking and error
            return False

    def Constant(self):
        if (
            self.term_cat("T_IntConstant_Hexadecimal")
            or self.term_cat("T_IntConstant_Decimal")
            or self.term_cat("T_StringConstant")
            or self.term_cat("T_BooleanConstant")
            or self.term_cat("T_DoubleConstant")
        ):
            return True
        else:
            # epsilon
            return True

    def term(self, expected):
        if self.__tokens__[cursor].word == expected:
            cursor += cursor
            return True
        else:
            return False

    def term_cat(self, expected):
        if self.__tokens__[cursor].category == expected:
            cursor += cursor
            return True
        else:
            return False

    def save_cursor(self):
        saved_cursor = cursor

    def backtrack(self):
        cursor = saved_cursor

    def lookahead_term(self):
        return self.__tokens__[cursor].word

    def lookahead_cat(self):
        return self.__tokens__[cursor].category
