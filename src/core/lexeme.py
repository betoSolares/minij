class Lexeme:
    def __init__(self, word, line, col_start, col_finish):
        self.word = word
        self.line = line
        self.col_start = col_start
        self.col_finish = col_finish

    @property
    def word(self):
        return self.__word__

    @word.setter
    def word(self, word):
        self.__word__ = word

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
