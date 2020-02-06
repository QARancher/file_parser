Python stand-alone script that searches for a string or regex in list of files: The script that searches for a pattern
using a regular expression in lines of text, and prints the lines which contain matching text. 
The script's output format should be: 'file_name line_number line'
run the following command from linux CLI: 

python main.py --file=<list_of_files> --regex=<str or regex> --machine=<True/False>

i.e

python3 main.py --regex='god' --file='~/file_parser/tests/resources/The_Kingdom_of_God_Is_Within_You_by_graf_Leo_Tolstoy.txt'


--file= path to a file to search in, can take a list of files.
--regex= regex or string to search for in the file.
--machine= optional - if true - print the output in the format: "file_name:line_number:start_position:matched_text".

the matched lines with the number of lines are saved in output.txt file. in the format: file_name line_number line

