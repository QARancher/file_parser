#!/usr/bin/python

import sys
from argparse import ArgumentParser
from search_in_file import SearchClass


def main():
    usage = "{prog} -f <list_of_files> -r <regex> -u <True/False> -c " \
            "<True/False> -m <True/False>" \
            "The script that searches for a pattern using a regular " \
            "expression in lines of text, and prints the lines which contain" \
            " matching text. The script's output format should be:" \
            " 'file_name line_number line'".format(prog=sys.argv[0])
    if len(sys.argv) == 2:
        print("Wrong usage! \n {usage}".format(usage=usage))
        sys.exit(1)
    print('ARGV      :{args}'.format(args=sys.argv[1:]))
    parser = ArgumentParser(usage=usage)
    parser.add_argument("-r", "--regex",
                        action="store", dest="regex", default="god",
                        required=False, help="Mandatory - the regular "
                                             "expression to search for.")
    parser.add_argument("-b", "--buffer", dest="buffer", type=int,
                        required=False,
                        help="Optional - Buffer size in Bytes for the file to "
                             "be loaded "
                             "in memory rather on disk. Use this flag for "
                             "large files.")
    parser.add_argument("-f", "--file", dest="inputfile",
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
    srch = SearchClass(search_str=args.regex)
    if not args.inputfile:
        srch.search_in_string(searched_line=sys.stdin)
    for file in args.inputfile:
        srch.search_in_file(in_file=file, buffer=args.buffer)


if __name__ == "__main__":
    main()
