class Parser:
    def __init__(self):
        self.__tokens__ = None
        self.__errors__ = []
        self.cursor = 0
        self.saved = 0
        self.__expected__ = []

    # Try to parse the tokens list, true if no errors
    def try_parse(self, tokens):
        # self.__tokens__ = iter(tokens)
        self.__tokens__ = tokens
        # breakpoint()
        while not len(self.__tokens__) == self.cursor:
            self.__expected__ = []
            self.Program()
            if not len(self.__tokens__) == self.cursor:
                self.__add_error__(
                    self.__tokens__[self.cursor], self.__expected__
                )
                self.cursor += 1
            else:
                break

        return len(self.__errors__) == 0

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
    # Program → Decl _Program
    def Program(self):
        if self.Decl():
            return self._Program()
        else:
            # self.__expected__ = []
            # self.__expected__.append("unrecognized")
            return False
        # return self.Decl() and self._Program()

    # _Program → Program | ε
    def _Program(self):
        if self.Program():
            return True
        else:
            return True

    # Decl → VarDecl | FuncDecl
    def Decl(self):
        return self.VarDecl() or self.FuncDeclare()
        # if not self.VarDecl():
        #     if not self.FuncDeclare():
        #         self.__expected__ = []
        #         self.__expected__.append("unrecognized")
        #         return False
        #     else:
        #         return True
        # else:
        #     return True

    # VarDecl → Variable ;
    def VarDecl(self):
        if self.Variable():
            if self.term(";"):
                return True
            else:
                self.__expected__.append("a ;")
                return False
        else:
            return False

    # Variable → Type ident
    def Variable(self):
        if self.Type():
            if self.term_cat("Identifier"):
                return True
            else:
                self.__expected__.append(" an identifier")
                return False
        else:
            self.__expected__.append("a type value")
            return False

    # Type → int _Type | double _Type | bool _Type| string _Type | ident _Type
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
            # self.__expected__.append("a declaration")
            return False

    # _Type → [] _Type | ε
    def _Type(self):
        if self.lookahead_term() == "[]":
            return self.term("[]") and self._Type()
        else:
            # epsilon?
            return True

    # FuncDecl → Type ident ( Formals ) _Stmt | void ident ( Formals ) _Stmt
    def FuncDeclare(self):
        if self.term("void"):
            if self.term_cat("Identifier"):
                lookparth = self.lookahead_term()
                if lookparth == "()":
                    self.term("()")
                    return self._Stmt()
                elif lookparth == "(":
                    self.term("(")
                    return self.Formals() and self.term(")") and self._Stmt()
                else:
                    self.__expected__.append("a (")
                    return False
            else:
                self.__expected__.append("an identifier")
                return False
        elif self.Type():
            if self.term_cat("Identifier"):
                lookparth = self.lookahead_term()
                if lookparth == "()":
                    return self._Stmt()
                elif lookparth == "(":
                    return self.Formals() and self.term(")") and self._Stmt()
                else:
                    self.__expected__.append("a (")
                    return False
            else:
                self.__expected__.append("an identifier")
                return False
        else:
            self.__expected__.append("unrecognized token")
            return False

    # _Stmt → Stmt _Stmt | ε
    def _Stmt(self):
        # return (self.Stmt() and self._Stmt()) or True
        if self.Stmt() and self._Stmt():
            return True
        else:
            # epsilon
            return True

    # Formals → _Variable , | ε
    def Formals(self):
        # return (self._Variable() and self.term(",")) or True
        if self._Variable() and self.term(","):
            return True
        else:
            return True

    # _Variable → Variable | Variable _Variable
    def _Variable(self):
        # return self.Variable() or (self.Variable() and self._Variable())
        if self.Variable():
            return True
        elif self.Variable() and self._Variable():
            return True

    # Stmt → IfStmt | ForStmt | Expr ;
    def Stmt(self):
        if self.IfStmt():
            return True
        elif self.ForStmt():
            return True
        elif self.Expr():
            if self.term(";"):
                return True
            else:
                self.__expected__.append(" a ;")
                return False
        else:
            return False

    # IfStmt → if ( Expr ) Stmt ElseStmt
    def IfStmt(self):
        if self.term("if"):
            if self.term("("):
                if self.Expr():
                    if self.term(")"):
                        return self.Stmt() and self.ElseStmt()
                    else:
                        self.__expected__.append(" a )")
                        return False
                else:
                    self.__expected__.append("an expresion")
                    return False
            else:
                self.__expected__.append("a (")
                return False
        else:
            return False

    # ElseStmt → else Stmt | ε
    def ElseStmt(self):
        if self.lookahead_term() == "else":
            return self.term("else") and self.Stmt
        else:
            # epsilon
            return True

    # ForStmt → for ( OptExpr ; Expr ; OptExpr ) Stmt
    def ForStmt(self):
        if self.term("for"):
            if self.term("("):
                if self.OptExpr():
                    if self.term(";"):
                        if self.Expr():
                            if self.term(";"):
                                if self.OptExpr():
                                    if self.term(")"):
                                        if self.Stmt():
                                            return True
                                        else:
                                            return False
                                    else:
                                        self.__expected__.append(" a )")
                                        return False
                                else:
                                    return False
                            else:
                                self.__expected__.append("a ;")
                                return False
                        else:
                            return False
                    else:
                        self.__expected__.append("a ;")
                        return False
                else:
                    return False
            else:
                self.__expected__.append("a (")
                return False
        else:
            return False

    # OptExpr → Expr | ε
    def OptExpr(self):
        # return self.Expr() or True
        if self.Expr():
            return True
        else:
            return True

    # MultExpr → Expr | Expr MultExpr
    def MultExpr(self):
        # return self.Expr() or (self.Expr() and self.MultExpr())
        if self.Expr():
            return True
        elif self.Expr() and self.MultExpr():
            return True

    # Expr → _Expr | LValue = _Expr
    def Expr(self):
        # save cursor in case of backtracking
        self.save_cursor
        if self.LValue():
            if self.lookahead_term == "=":
                return self.term("=") and self._Expr()
            else:
                # backtrack if '=' is not found and call _Expr
                self.backtrack
                return self._Expr()
        else:
            return False

    # _Expr → T _E
    def _Expr(self):
        # return self.T() and self._E()
        if self.T() and self._E():
            return True
        else:
            # Backtracking
            return False

    # _E → || T _E | ε
    def _E(self):
        if self.lookahead_term() == "||":
            return self.term("||") and self.T() and self._E()
        else:
            # epsilon
            return True

    # T → F _T
    def T(self):
        # return self.F() and self._T()
        if self.F() and self._T():
            return True
        else:
            # Backtracking
            return False

    # _T → && F _T | ε
    def _T(self):
        if self.lookahead_term() == "&&":
            return self.term("&&") and self.F() and self._T()
        else:
            # epsilon
            return True

    # F → G _F
    def F(self):
        # return self.G() and self._F()
        if self.G() and self._F():
            return True
        else:
            # Backtracking
            return False

    # _F → == G _F | != G _F | ε
    def _F(self):
        lookahead = self.lookahead_term()
        if lookahead == "==":
            return self.term("==") and self.G() and self._F()
        elif lookahead == "!=":
            return self.term("!=") and self.G() and self._F()
        else:
            # epsilon
            return True

    # G → H _G
    def G(self):
        # return self.H() and self._G()
        if self.H() and self._G():
            return True
        else:
            # Backtracking
            return False

    # _G → < H _G | > H _G | <= H _G | >= H _G | ε
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

    # H → J _H
    def H(self):
        # return self.J() and self._H()
        if self.J() and self._H():
            return True
        else:
            # Backtracking
            return False

    # _H → + J _H | - J _H | ε
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

    # J → K _J
    def J(self):
        # return self.K() and self._J()
        if self.K() and self._J():
            return True
        else:
            # Backtracking
            return False

    # _J → * K _J | / K _J | % K _J | ε
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

    # K → New ( ident ) | L
    def K(self):
        if self.term("New"):
            if self.term("("):
                if self.term_cat("Identifier"):
                    if self.term(")"):
                        return True
                    else:
                        self.__expected__.append(" a ')'")
                        return False
                else:
                    self.__expected__.append("an identifier")
                    return False
            else:
                self.__expected__.append("a '('")
                return False

        elif self.L():
            return True
        else:
            return False

    # L → - Expr | ! Expr | M
    def L(self):
        lookahead = self.lookahead_term()
        if lookahead == "-":
            return self.term("-") and self.Expr()
        elif lookahead == "!":
            return self.term("!") and self.Expr()
        elif self.M():
            return True
        else:
            return False

    # M → LValue | ( Expr ) | this | Constant
    def M(self):
        lookahead = self.lookahead_term()
        if self.LValue():
            return True
        elif lookahead == "(":
            return self.term("(") and self.Expr() and self.term(")")
        elif lookahead == "this":
            return self.term("this")
        elif self.Constant():
            return True
        else:
            return False

    # LValue → ident | Expr _LValue
    def LValue(self):
        if self.term_cat("Identifier"):
            if self.term("."):
                return self.Expr()
            elif self.term("["):
                return self.Expr() and self.term("]")
            else:
                return True
        else:
            self.__expected__.append("an identifier")
            return False

    # Constant → intConstant|doubleConstant|boolConstant|stringConstant|null
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
        elif self.lookahead_term() == "null":
            return self.term("null")
        else:
            self.__expected__.append("a constant")
            return False

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
