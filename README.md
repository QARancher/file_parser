
Python stand-alone script that searches for a string or regex in list of files.
The script that searches for a pattern using a regular expression in lines of text, and prints the lines which contain
matching text, non case sensitive.   
The script's output format should be: 'file_name line_number line'  
run the following command from linux CLI:   
  

    python main.py --file=<list_of_files> --search=<str or regex> --machine=<True/False> 

 
  
search in single file:

    python3 main.py --search='god' --file=~/file_parser/tests/resources/The_Kingdom_of_God_Is_Within_You_by_graf_Leo_Tolstoy.txt
    
search in multiple files:

    python3 main.py --search='god' --file=~/file_parser/tests/resources/The_Kingdom_of_God_Is_Within_You_by_graf_Leo_Tolstoy.txt
     --file=The_Queen_Matrimonial_Ladder_by_William_Hone.txt

search in directory:

    python3 main.py --search='god' --file=~/file_parser/tests/resources/
    
search in string:

    python3 main.py --search='god' --file="bla bla bla god bla"
* searching in multiple string is the same as in multiple files.

flags:

    --file= path to a file to search in, accepts directory, files, if string is given the search will be on that string 
    --search= regex or string to search for in the file.  
    --machine= optional - if true - print the output in the format: "file_name:line_number:start_position:matched_text".  

  
The matched lines, with the number of line, are saved in output.txt file. in the format: `file_name line_number line`