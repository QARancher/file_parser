class FileParserException(Exception):
    def __init__(self,
                 message=""):
        super(FileParserException, self).__init__(message)


class SearchException(FileParserException):
    def __init__(self,
                 message="Invalid resource's body."):
        super(SearchException, self).__init__(message)


class InvalidInputFile(FileParserException):
    def __init__(self,
                 message):
        message = "Invalid input file. {message}".format(message=message)
        super(InvalidInputFile, self).__init__(message)
