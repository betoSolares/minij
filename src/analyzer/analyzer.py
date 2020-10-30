from .lexer import Lexer
from .parser import Parser


class Analyzer:
    def __init__(self, text):
        self.__errors__ = []
        self.__lexer__ = Lexer()
        self.__parser__ = Parser()
        self.__text__ = text
        self.__warnings__ = []

    # Get a list with all the errors
    @property
    def errors(self):
        return self.__errors__

    @property
    def warnings(self):
        return self.__warnings__

    # Try to analyze the text
    def try_analyze(self):
        if self.__lexer__.tokenize(self.__text__):
            if self.__parser__.analyze(self.__lexer__.tokens):
                self.__lexer__warnings__()
                return True
            else:
                self.__lexer__warnings__()
                self.__parser__errors__()
                return False
        else:
            self.__lexer__warnings__()
            self.__lexer__errors__()
            return False

    # Convert the lexer errors
    def __lexer__errors__(self):
        for error in self.__lexer__.errors:
            line = str(error.line)
            reason = error.reason
            word = error.word

            if error.finish is None:
                col = " column " + str(error.start)
            else:
                col = " columns " + str(error.start) + " to " + str(error.finish)

            e = "*** ERROR on line " + line + col + " *** " + reason + " " + word
            self.__errors__.append(e)

    # Convert the lexer warnings
    def __lexer__warnings__(self):
        for warning in self.__lexer__.warnings:
            line = str(warning.line)
            reason = warning.reason
            word = warning.word

            if warning.finish is None:
                col = " column " + str(warning.start)
            else:
                col = (
                    " columns "
                    + str(warning.start)
                    + " to "
                    + str(warning.finish)
                )

            w = "WARNING on line " + line + col + " " + reason + " " + word
            self.__warnings__.append(w)

    # Convert the parser errors
    def __parser__errors__(self):
        for error in self.__parser__.errors:
            line = str(error[0].line)
            obtained = error[1]
            expected = " or ".join(error[2])

            if error[0].finish is None:
                col = " column " + str(error[0].start)
            else:
                col = (
                    " columns "
                    + str(error[0].start)
                    + " to "
                    + str(error[0].finish)
                )

            e = (
                "*** ERROR on line "
                + line
                + col
                + " *** got "
                + obtained
                + " expected "
                + expected
            )
            self.__errors__.append(e)
