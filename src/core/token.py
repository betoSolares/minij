class Token:
    def __init__(self, word, line, start, finish, category, reason=None):
        self.__word__ = word
        self.__line__ = line
        self.__start__ = start
        self.__finish__ = finish
        self.__category__ = category
        self.__reason__ = reason

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
    def start(self):
        return self.__start__

    @start.setter
    def start(self, start):
        self.__start__ = start

    @property
    def finish(self):
        return self.__finish__

    @finish.setter
    def finish(self, finish):
        self.__finish__ = finish

    @property
    def category(self):
        return self.__category__

    @category.setter
    def category(self, category):
        self.__category__ = category

    @property
    def reason(self):
        return self.__reason__

    @reason.setter
    def reason(self, reason):
        self.__reason__ = reason
