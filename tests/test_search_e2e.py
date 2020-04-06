from os.path import isfile

import pytest
from os import listdir, path

from tests.utils import search_in_files, search_in_directory

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


def benchmark_it(func, file, search_str, ofile):
    def wrapper(benchmark):
        benchmark(func, file, search_str, ofile)

    return wrapper


class TestSearch:
    @pytest.mark.benchmark(min_rounds=10)
    def test_search_in_directory(self,
                                 benchmark):

        ofile = 'out_test_search_in_files.text'

        @benchmark
        def result():
            return search_in_directory(path='resources/', search_str='god', ofile=ofile)

        assert isfile(ofile)

    @pytest.mark.parametrize("search_str",
                             ['god', '[0-9]', '\wgod+', 'god |war'])
    def test_search_in_files(self,
                             search_str,
                             benchmark):
        """
        Test E2E search for file. the test runs over the resource dir with txt
         run the test multiple times, measuring performance over time.
        :param search_str: the regex to search for, use strings as it was regex
        """

        ofile = 'out_test_search_in_dir.text'
        kwargs = {"files_list": files_list, "search_str": search_str, "ofile": ofile}
        benchmark(search_in_files, **kwargs)
        assert isfile(ofile)


if __name__ == "__main__":
    pass
