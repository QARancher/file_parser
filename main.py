#!/usr/bin/python

import sys
from argparse import ArgumentParser

from search.search_in_file import SearchClass


def _single_true(iterable):
    """
    consume from "i" until first true or it's exhausted.
    carry on consuming until another true value / exhausted
    :param iterable: iterable object
    :return: True if exactly one true found
    """
    iterator = iter(iterable)
    has_true = any(iterator)
    has_another_true = any(iterator)
    return has_true and not has_another_true


def main():
    usage = "python {prog} --file=<list_of_files> --search=<str or " \
            "regex> --machine=<True/False>\n" \
            "--file= path to a file to search in, can take a list of files.\n" \
            "--regex= regex or string to search for in the file.\n" \
            "--output= optional flag for output file's name\n" \
            "--machine= optional - if true - print the output" \
            " in the format:\n " \
            "'file_name:line_number:start_position:matched_text'.\n" \
            "The matched lines with the number of lines are saved in" \
            "output.txt file. in the format:\n" \
            "file_name line_number line\n".format(prog=sys.argv[0])
    if len(sys.argv) == 1:
        print("Wrong usage! \n ARGS: {args} \n{usage}".format(usage=usage,
                                                              args=sys.argv[
                                                                   1:]))
        sys.exit(1)
    print('Search flags: {args}'.format(args=sys.argv[1:]))
    parser = ArgumentParser(usage=usage)
    parser.add_argument("-s", "--search",
                        action="store", dest="regex", default="god",
                        required=True, help="Mandatory - the regular "
                                            "expression to search for.")
    parser.add_argument("-b", "--buffer", dest="buffer", type=int,
                        help="Optional - Buffer size in Bytes for the file to "
                             "be loaded "
                             "in memory rather on disk. Use this flag for "
                             "large files.")
    parser.add_argument("-o", "--output", dest="output_file", default="output.txt",
                        help="Optional - output file's name to write to the matched lines")
    files = parser.add_argument_group('files')
    files.add_argument("-f", "--file", action="append",
                       dest="inputfiles", default=[],
                       help="List of files to search in.\n"
                            "Optional - a list of "
                            "files to search in. If this "
                            "parameter is omitted, the script expects text "
                            "input from STDIN as the last argument")
    pretty = parser.add_argument_group('pretty')
    pretty.add_argument("-u", "--underline ",
                        action="store_false", dest="underline",
                        help="optional - '^' is printed underneath the matched "
                             "text.")
    pretty.add_argument("-c", "--color",
                        action="store_false", dest="color", default=False,
                        help="optional - the matched text is highlighted in "
                             "color")
    pretty.add_argument("-m", "--machine", dest="machine", default=False,
                        help="optional - print the output in the format: "
                             "'file_name:line_number:start_position"
                             ":matched_text'")

    args = parser.parse_args()

    for file in args.inputfiles:
        srch = SearchClass(search_str=args.regex,
                           search_path=file,
                           buffer_size=args.buffer,
                           output_file=args.output_file)
        if args.machine:
            srch.set_machine(machine=True)
        srch.search()


if __name__ == "__main__":
    main()
