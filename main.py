#!/usr/bin/python

import sys
from argparse import ArgumentParser
from search_in_file import SearchClass


def main():
    usage = "{prog} --file=<list_of_files> --regex=<str or " \
            "regex> --machine=<True/False>\n" \
            "--file= path to a file to search in, can take a list of files.\n" \
            "--regex= regex or string to search for in the file.\n" \
            "--machine= optional - if true - print the output" \
            " in the format:\n " \
            "'file_name:line_number:start_position:matched_text'.\n" \
            "The matched lines with the number of lines are saved in" \
            "output.txt file. in the format:\n" \
            "file_name line_number line\n".format(prog=sys.argv[0])
    if len(sys.argv) == 1:
        print("Wrong usage! \n {usage}".format(usage=usage))
        sys.exit(1)
    print('ARGV      :{args}'.format(args=sys.argv[1:]))
    parser = ArgumentParser(usage=usage)
    parser.add_argument("-r", "--regex",
                        action="store", dest="regex", default="god",
                        required=True, help="Mandatory - the regular "
                                             "expression to search for.")
    parser.add_argument("-b", "--buffer", dest="buffer", type=int,
                        required=False,
                        help="Optional - Buffer size in Bytes for the file to "
                             "be loaded "
                             "in memory rather on disk. Use this flag for "
                             "large files.")
    parser.add_argument("-f", "--file", dest="inputfile", required=True,
                        help="Optional - a list of files to search in. If this "
                             "parameter is omitted, the script expects text "
                             "input from STDIN as the last argument",
                        action="append")
    pretty = parser.add_argument_group('pretty')
    pretty.add_argument("-u", "--underline ",
                        action="store_false", dest="underline",
                        help="optional - '^' is printed underneath the matched "
                             "text.")
    pretty.add_argument("-c", "--color",
                        action="store_false", dest="color", default=False,
                        help="optional - the matched text is highlighted in "
                             "color")
    pretty.add_argument("-m", "--machine",
                        action="store_false", dest="machine", default=False,
                        help="optional - print the output in the format: "
                             "'file_name:line_number:start_position"
                             ":matched_text'")

    args = parser.parse_args()

    if not args.inputfile:
        srch = SearchClass(search_str=args.regex)
        srch.search_in_string(searched_line=sys.stdin)
    for file in args.inputfile:
        srch = SearchClass(search_str=args.regex,
                           in_file=file,
                           buffer_size=args.buffer)
        srch.search_in_file()


if __name__ == "__main__":
    main()
