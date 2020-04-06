from search.search_in_file import SearchClass


def search_func(file, search_str, ofile):
    srch = SearchClass(search_str=search_str, search_path=file, output_file=ofile)
    srch.search()


def search_in_files(files_list, search_str, ofile):
    for file in files_list:
        search_func(file=file, search_str=search_str, ofile=ofile)


def search_in_directory(path, search_str, ofile):
    srch = SearchClass(search_str=search_str, search_path=path, output_file=ofile)
    srch.search()
