class Token:
    def __init__(self, lexeme, category):
        self.lexeme = lexeme
        self.category = category

    @property
    def lexeme(self):
        return self.__lexeme__

    @lexeme.setter
    def lexeme(self, lexeme):
        self.__lexeme__ = lexeme

    @property
    def category(self):
        return self.__category__

    @category.setter
    def category(self, category):
        self.__category__ = category
