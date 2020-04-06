import timeit
import pytest
from os import listdir, path

from search.search_in_file import SearchClass

file_dir = 'resources/'
files_list = [path.join(file_dir, file) for file in listdir(file_dir)]


def generate_permutation_matrix(num_options):
    """
    this function generates a square binary matrix of permutations
    :param num_options: the number of options, this number will be used as
    2**num
    for example, matrix of 2**2 :
    | 0 | 0 |
    | 0 | 1 |
    | 1 | 0 |
    | 1 | 1 |

     the yield will return each time a list (row) in the matrix

    :return: list of lists with boolean of all possible permutations
    """
    for num in (bin(opt)[2:].zfill(num_options) for opt in
                range(2 ** num_options)):
        option = []
        for char in num:
            option.append(char == '1')
        yield option


def format_types():
    for machine, color, underline in \
            generate_permutation_matrix(num_options=3):
        yield {
            'machine': machine,
            'color': color,
            'underline': underline
        }


class TestSearch:
    @pytest.mark.parametrize("search_str",
                             ['god', '[0-9]', '\wgod+', 'god |war'])
    def test_search_in_files(self,
                            search_str):
        """
        Test E2E search for file. the test runs over the resource dir with txt
         run the test multiple times, measuring performance over time.
        :param search_str: the regex to search for, use strings as it was regex
        """
        for file in files_list:
            srch = SearchClass(search_str=search_str, search_path=file)
            srch.search()

    # TODO - fix underline and color funtion will failed.
    @pytest.mark.parametrize("format_types_attributes", format_types())
    def test_search_in_files_with_format_types(self,
                                               format_types_attributes):
        start = timeit.timeit()
        for file in files_list:
            srch = SearchClass(search_str="god|war", search_path=file)
            srch.search(**format_types_attributes)
        stop = timeit.timeit()
        print("total time: {total}".format(total=start - stop))


if __name__ == "__main__":
    pass
