class Parser:
    def __init__(self):
        self.__tokens__ = None
        self.__errors__ = []
        cursor = 0

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

    def Program():
        return Decl() and _Program()

    def _Program():
        if Program():
            return True
        else:
            return True

    def Decl():
        if VarDecl():
            return True
        elif FuncDeclare():
            return True
        else:
            #Backtracking
            return False

    def VarDecl():
        return Variable() and term(';')

    def Variable():
        return Type() and term_constant('T_Identifier')

    def Type():
        if term('int') and _Type():
            return True
        elif term('double') and _Type():
            return True
        elif term('boolean') and _Type():
            return True
        elif term('string') and _Type():
            return True
        elif term_constant('T_Identifier') and _Type():
            return True
        else:
            #Backtracking
            return False

    def _Type():
        if term('[]') and _Type():
            return True
        else:
            return True

    def FuncDeclare():
        if Type() and term_constant('T_Identifier') and term('(') and Formals() and term(')') and _Stmt():
            return True
        elif term('void') and and term_constant('T_Identifier') and term('(') and Formals() and term(')') and _Stmt():
            return True
        else:
            #Backtracking
            return False

    def _Stmt():
        if Stmt() and _Stmt():
            return True
        else:
            return True

    def Formals():
        if _Variable and term(','):
            return True
        else:
            return True

    def _Variable():
        if Variable():
            return True
        elif Variable() and _Variable():
            return True

    def Stmt():
        if IfStmt():
            return True
        elif ForStmt():
            return True
        elif Expr() and term(';'):
            return True
        else:
            #Backtracking
            return False

    def IfStmt():
        return term('if') and term('(') and Expr() and term(')') and Stmt() and ElseStmt()

    def ElseStmt():
        if term('else') and Stmt():
            return True
        else:
            #epsilon
            return True

    def ForStmt():
        return term('for') and term('(') and OptExpr() and term(';') and Expr() and term(';') and OptExpr() and term(')') and Stmt()

    def OptExpr():
        if Expr():
            return True
        else:
            return True

    def MultExpr():
        if Expr():
            return True
        elif Expr() and MultExpr():
            return True

    def Expr():
        if LValue() and term('=') and _Expr():
            return True
        elif _Expr():
            return True
        else:
            #Backtracking
            return False

    def _Expr():
        if T() and _E():
            return True
        else:
            #Backtracking
            return False

    def _E():
        if term('||') and T() and _E():
            return True
        else:
            #epsilon
            return True

    def T():
        if F() and _T():
            return True
        else:
            #Backtracking
            return False

    def _T():
        if term('&&') and F() and _T():
            return True
        else:
            #epsilon
            return True

    def F():
        if G() and _F():
            return True
        else:
            #Backtracking
            return False

    def _F():
        if term('==') and G() and _F():
            return True
        elif term('!=') and G() and _F():
            return True
        else:
            #epsilon
            return True

    def G():
        if H() and _G():
            return True
        else:
            #Backtracking
            return False

    def _G():
        if term('<') and H() and _G():
            return True
        elif term('>') and H() and _G():
            return True
        elif term('<=') and H() and _G():
            return True
        elif term('>=') and H() and _G():
            return True
        else:
            #epsilon
            return True

    def H():
        if J() and _H():
            return True
        else:
            #Backtracking
            return False

    def _H():
        if term('+') and J() and _H():
            return True
        elif term('-') and J() and _H():
            return True
        else:
            #Backtracking
            #epsilon
            return True

    def J():
        if K() and _J():
            return True
        else:
            #Backtracking
            return False

    def _J():
        if term('*') and K() and _J():
            return True
        elif term('/') and K() and _J():
            return True
        elif term('%') and K() and _J():
            return True
        else:
            #epsilon
            return True

    def K():
        if term('-') and Expr():
            return True
        elif term('!') and Expr():
            return True
        elif L():
            return True
        else:
            #Backtracking
            return False

    def L():
        if term('(') and Expr() and term(')'):
            return True
        elif term('this'):
            return True
        elif term('New') and term('(') and term_constant('T_Identifier', 'category') and term(')'):
            return True
        elif Constant():
            return True
        elif LValue():
            return True
        else:
            #Backtracking and error
            return False

    def LValue():
        if term('T_Identifier', 'category'):
            return True
        elif Expr() and term('.') and term_constant('T_Identifier', 'category'):
            return True
        elif Expr() and term('[') and Expr() and term(']'):
            return True
        else:
            #Backtracking and error
            return False

    def Constant():
        if term_constant('T_IntConstant_Hexadecimal') or term_constant('T_IntConstant_Decimal') or term_constant('T_StringConstant') or term_constant('T_BooleanConstant') or term_constant('T_DoubleConstant'):
            return True
        else:
            #epsilon
            return True

    def term(expected):
        return self.__tokens__[cursor].word == expected

    def term_constant(expected):
        return self.__tokens__[cursor].category == expected
