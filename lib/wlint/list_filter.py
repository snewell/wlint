#!/usr/bin/python3

import operator
import pkg_resources

import wlint.tool
import wlint.filter

listDir = pkg_resources.resource_filename(__name__, "share/filter-lists/")
defaultLists = wlint.filter.DirectoryLists(listDir)

_SORTS = [
    ("alpha", "Sort output based on the actual words."),
    ("sequential", "Sort output based on the order words appear.")
]

_SORT_FNS = {
    "alpha": lambda hits: hits.sort(),
    "sequential": lambda hits: hits.sort(key=operator.itemgetter(1, 2))
}


class ListFilter(wlint.tool.Tool):

    def __init__(self):
        super().__init__(description="Detect troublesome words",
                         prog="wlint list-filter")
        defaultListsStr = ",".join(defaultLists.files)
        self.add_argument(
            "--lists",
            help="Change the set of word lists.  This should be a "
                 "comma-separated list of built-in lists.",
            default=defaultListsStr)
        self.add_argument(
            "--list",
            help="Use a custom word list.  The list should be a plain text "
                 "file with one word per line.",
            action="append")

        self.add_sort(_SORTS)

    def execute(self, parsed_args):
        def _make_lists():
            if parsed_args.lists:
                lists = parsed_args.lists.split(",")
                # Read the built in lists
                return defaultLists.buildWordList(lists)
            else:
                return wlint.filter.WordList()

        words = _make_lists()
        # Read any extra lists
        if parsed_args.list:
            for wordList in parsed_args.list:
                words.addWords(wordList)

        # WordList is complete, so setup variables
        filter_list = wlint.filter.Filter(words)
        sorter = _SORT_FNS[parsed_args.sort]
        purifier = wlint.tool.get_purifier(parsed_args)

        def _print_hits(hits, fn):
            sorter(hits)
            for (word, line, col) in hits:
                fn(word, line, col)

        def _process(file_handle):
            hits = []
            filter_list.filter_sequence(
                file_handle, lambda word, line, col: hits.append(
                    (word, line, col)), purifier)
            _print_hits(
                hits, lambda word, line, col: print(
                    "{} {} ({}:{})".format(
                        file_handle.name, word, line, col)))

        return wlint.tool.iterate_files(parsed_args, _process)


def main(args=None):
    listFilter = ListFilter()
    wlint.tool.execute_tool(listFilter, args)


_LIST_FILTER_COMMAND = (
    main,
    "List filter words")

if __name__ == '__main__':
    main()
