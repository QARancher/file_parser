import re
from re import finditer, error, IGNORECASE

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
        pattern = re.compile(pattern, IGNORECASE)
        for match in finditer(pattern=pattern, string=searched_line):
            return match
    except error:
        raise SearchException(message="Failed compiling pattern"
                                      " {pattern}".format(pattern=pattern))
