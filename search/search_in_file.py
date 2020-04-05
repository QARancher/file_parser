import logging
from os.path import isfile
from re import compile, finditer, error

from search.exceptions import SearchException, InvalidInputFile


logger = logging.getLogger(__name__)


def _search(pattern,
            searched_line):
    """
    method to search for string or regex in another string.
    :param pattern: the pattern to search for
    :param searched_line: string line as it pass from the file parser
    :return: matched object of type re
    :raise: SearchException if the strings invalid
    """
    try:
        pattern = compile(pattern)
        for match in finditer(pattern=pattern, string=searched_line):
            return match
    except error:
        raise SearchException(message="Failed compiling pattern"
                                      " {pattern}".format(pattern=pattern))


class FileParser(dict):
    def __init__(self, in_file=None, search_str="", buffer_size=None):
        """
        Engine class to search of regex in a file, regardless to the size of
        the file, using buffering to store the file in memory rather on disk.
        returns a dict object in the format {line_number: re.Match object}
        :param in_file: IO object to location of the file to search in
        :param search_str: string or regex to search for in the file
        :param buffer_size: buffering is an optional integer used to set the
        buffering policy.
        Pass 0 to switch buffering off, 1 to select line buffering,
        and an integer > 1 to indicate the size of a fixed-size chunk buffer.
        """
        super(FileParser, self).__init__()
        self.buffer_size = buffer_size or 1
        self.search_path = in_file
        self.update(self._parser(search_str=search_str))

    def _load_line(self,
                   search_str):
        # read input file using buffering of 1 line.
        with open(file=self.search_path, buffering=self.buffer_size) as \
                line_to_parse:
            return [
                _search(pattern=search_str, searched_line=parsed_line)
                for parsed_line in line_to_parse.readlines()
            ]

    def _parser(self,
                search_str):
        """
        function to index the line number in a file, based on matched string
        :param search_str: string or regex to search for in the file
        :return: return a dict obj in format {line_index: parsed_line_keys}
        """
        return {line_index: parsed_line_keys for (line_index, parsed_line_keys)
                in enumerate(self._load_line(search_str=search_str))
                if parsed_line_keys
                }

    def _construct_output_string(self,
                                 num_line,
                                 obj,
                                 machine=False,
                                 color=False,
                                 underline=False):
        wline = obj.string
        # TODO - fix underline and color funtions should be implemented better..
        if color:
            cline = "{str_start}\033[{str_middle}m{str_end}".format(
                str_start=obj.string[:obj.start()],
                str_middle=obj.string[obj.start():obj.stop()],
                str_end=obj.string[obj.end():]
            )
            wline = wline.join(cline)
        if underline:
            uline = "^{str_start}".format(
                str_start=obj.string[obj.start()])
            wline.join(uline)
        if machine:
            wline = "{file_name}:{num_line}:{start_position}:" \
                    "{line_text}".format(file_name=self.search_path,
                                         start_position=obj.start(),
                                         num_line=num_line,
                                         line_text=obj.string)
        else:
            wline = "{file_name} {num_line} {line_text}".format(
                num_line=num_line, line_text=obj.string,
                file_name=self.search_path)
        return wline

    def write_to_file(self,
                      **kwargs):
        """
        Write to output.txt file the matched lines, with the format that is
        passed via kwargs
        """
        with open(file='output.txt', mode='a') as ofile:
            for num_line, obj in self.items():
                ofile.write(str(self._construct_output_string(num_line=num_line,
                                                              obj=obj,
                                                              **kwargs)))


class SearchClass(object):
    def __init__(self,
                 search_str,
                 search_path=None,
                 buffer_size=None):
        """
        class that handles the output of the search result, writing to a
        file in the requested format. implementing factory design pattern
        by inheriting from FileParser class, using its capabilities to
        load a text file, search by line and write the matches to output.txt
        file (saved under this folder)
        :param search_str: str or regex to search for
        """
        self.search_str = search_str
        self.search_path = search_path
        self.buffer_size = buffer_size
        if self.search_path and isfile(path=self.search_path):
            self.src = SearchInFile(search_str=self.search_str,
                                    search_path=self.search_path,
                                    buffer_size=self.buffer_size)
        elif self.search_path and isinstance(self.search_path, str):
            self.src = SearchInString(search_str=self.search_str,
                                      searched_line=self.search_path)
        else:
            raise InvalidInputFile("Failed to get files or string to search in")

    def search(self):
        self.src.search()


class SearchInFile(object):
    def __init__(self,
                 search_str,
                 search_path=None,
                 buffer_size=None):
        self.search_str = search_str
        self.search_path = search_path
        self.buffer_size = buffer_size
        self.fileparser = FileParser(search_str=self.search_str,
                                     in_file=self.search_path,
                                     buffer_size=self.buffer_size)

    def search(self, **kwargs):
        logger.info("Parsing file: {file} searching for {pattern}".format(
            file=self.search_path, pattern=self.search_str))
        self.fileparser.write_to_file(**kwargs)


class SearchInString(object):
    def __init__(self, search_str, searched_line):
        self.search_str = search_str
        self.searched_line = searched_line

    def search(self):
        logger.debug("Searching for {pattern} in string: {str}".format(
            pattern=self.search_str, str=self.searched_line))
        print(_search(pattern=self.search_str,
                      searched_line=self.searched_line).string)
