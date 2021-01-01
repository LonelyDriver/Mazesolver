class Error(Exception):
    def __init__(self, message):
        super().__init__(message)


class MazeparsingError(Error):
    def __init__(self, exception, function):
        self.exception = exception
        self.function = function
        super().__init__(self.__str__())

    def __str__(self):
        return
        "MazeparsingError: [Exception] {} [Message] {} [Function] {}".format(
            type(self.exception),
            self.exception,
            self.function)


class SolveError(Error):
    def __init__(self, exception, function):
        self.exception = exception
        self.function = function

    def __repr__(self):
        return
        "SolveError: [Exception] {} [Message] {} [Function] {}".format(
            type(self.exception),
            self.exception,
            self.function)
