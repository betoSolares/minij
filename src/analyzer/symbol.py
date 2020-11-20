class Symbol:
    def __init__(self, lexeme, type, category, value, scope):
        self.__lexeme__ = lexeme
        self.__type__ = type
        self.__category__ = category
        self.__value__ = value
        self.__scope__ = scope

    @property
    def lexeme(self):
        return self.__lexeme__

    @lexeme.setter
    def lexeme(self, lexeme):
        self.__lexeme__ = lexeme

    @property
    def type(self):
        return self.__type__

    @type.setter
    def type(self, type):
        self.__type__ = type

    @property
    def category(self):
        return self.__category__

    @category.setter
    def category(self, category):
        self.__category__ = category

    @property
    def value(self):
        return self.__value__

    @value.setter
    def value(self, value):
        self.__value__ = value

    @property
    def scope(self):
        return self.__scope__

    @scope.setter
    def scope(self, scope):
        self.__scope__ = scope
