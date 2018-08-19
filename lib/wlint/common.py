#!/usr/bin/python3

import argparse
import errno
import sys

import wlint.plugin
import wlint.purify

_INPUT_PURIFIERS = wlint.plugin.query_plugins('wlint.puririfiers')


def _print_input_types():
    for input_type in sorted(_INPUT_PURIFIERS):
        print("{} - {}".format(input_type, _INPUT_PURIFIERS[input_type][1]))


class Tool:

    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            *args, **kwargs)

        # add common arguments
        self.parser.add_argument("files",
                                 help="Files to process.", nargs="*",
                                 metavar="file")
        self.add_argument(
            "--input-type",
            help="Type of input file.",
            default="text")
        self.add_argument(
            "--list-input-types",
            action='store_true',
            help="List supported input types.",
            default=argparse.SUPPRESS)

        self.sort_methods = None

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def add_sort(self, sort_methods):
        self.add_argument(
            "--sort",
            help="Method to sort output.  Options are: {}".format(
                sort_methods),
            default=sort_methods[0])
        self.sort_methods = sort_methods

    def execute(self, *args, **kwargs):
        parsed_args = self.parser.parse_args(*args, **kwargs)

        if "list_input_types" in parsed_args:
            self.missingFiles = None
            return _print_input_types()

        self.purifier = _INPUT_PURIFIERS.get(parsed_args.input_type)[0]
        if not self.purifier:
            raise ValueError(
                "'{}' is not a supported input type".format(parsed_args.input_type))

        if self.sort_methods:
            if parsed_args.sort in self.sort_methods:
                self.sort = parsed_args.sort
            else:
                raise ValueError(
                    "'{}' is not a valid sort method".format(self.sort))

        self.setup(parsed_args)

        missingFiles = []

        def parseFiles(files):
            """Parse a list of files, searching for filtered words.

            Arguments:
            files -- a list of files to parse (each file should be a
                        full path)"""

            if files:
                for f in files:
                    try:
                        with open(f, 'r') as readFile:
                            self.process(readFile)
                    except FileNotFoundError:
                        missingFiles.append(f)

        if parsed_args.files:
            # parse normal files, plus anything that was passed in via the
            # "--file" option
            parseFiles(parsed_args.files)
        else:
            # no files provided, so default to stdin
            self.process(sys.stdin)

        missingFiles.sort()
        self.missingFiles = missingFiles

    def validate_arguments(self, arguments):
        pass

    def display_results(self):
        pass

    def purify(self, text):
        return self.purifier(text)


def execute_tool(tool, args):
    if args is None:
        args = sys.argv[1:]
    try:
        tool.execute(args)
        tool.display_results()

        if tool.missingFiles:
            print(
                "Error opening files: {}".format(
                    tool.missingFiles),
                file=sys.stderr)
            exit(1)

    except IOError as e:
        if e.errno == errno.EPIPE:
            # This probably means we were piped into something that terminated
            # (e.g., head).  Might be a better way to handle this, but for now
            # silently swallowing the error isn't terrible.
            pass

    except Exception as e:
        print("Error: {}".format(str(e)), file=sys.stderr)
        exit(1)
