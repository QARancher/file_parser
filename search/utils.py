import re

from search.exceptions import SearchException


def search(pattern,
           searched_line):
    """
    method to search for string or regex in another string.
    :param pattern: the pattern to search for
    :param searched_line: string line as it pass from the file parser
    :return: matched object of type re
    :raise: SearchException if the strings invalid
    """
    try:
        pattern = re.compile(pattern, re.IGNORECASE)
        for match in re.finditer(pattern=pattern, string=searched_line):
            return match
    except re.error:
        raise SearchException(message="Failed compiling pattern"
                                      " {pattern}".format(pattern=pattern))
