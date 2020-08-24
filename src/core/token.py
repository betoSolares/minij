class Token:
    def __init__(self, lexeme, line, col_start, col_finish, category):
        self.lexeme = lexeme
        self.line = line
        self.col_start = col_start
        self.col_finish = col_finish
        self.category = category

    @property
    def lexeme(self):
        return self.__lexeme__

    @lexeme.setter
    def lexeme(self, lexeme):
        self.__lexeme__ = lexeme

    @property
    def line(self):
        return self.__line__

    @line.setter
    def line(self, line):
        self.__line__ = line

    @property
    def col_start(self):
        return self.__col_start__

    @col_start.setter
    def col_start(self, col_start):
        self.__col_start__ = col_start

    @property
    def col_finish(self):
        return self.__col_finish__

    @col_finish.setter
    def col_finish(self, col_finish):
        self.__col_finish__ = col_finish

    @property
    def category(self):
        return self.__category__

    @category.setter
    def category(self, category):
        self.__category__ = category
