#!/usr/bin/python3

import argparse
import sys


class Tool:

    def __init__(self, description):
        self.parser = argparse.ArgumentParser(description=description)

        # add common arguments
        self.parser.add_argument(
            "--file",
            help="Process a file.  This is only necessary if an input file "
            "matches an argument (e.g., --help).",
            action="append",
            default=[])
        self.parser.add_argument(
            "--stdin",
            help="Parse stdin.  If both files and this option are "
                 "used, files are processed before stdin.",
            action="store_true")
        self.parser.add_argument("files",
                                 help="Files to process.", nargs="*",
                                 metavar="file")

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def execute(self, *args, **kwargs):
        args = self.parser.parse_args(*args, **kwargs)

        self.setup(args)

        missingFiles = []

        def parseFiles(files):
            """Parse a list of files, searching for filtered words.

            Arguments:
            files -- a list of files to parse (each file should be a
                        full path)"""

            for f in files:
                try:
                    with open(f, 'r') as readFile:
                        self.process(readFile)
                except FileNotFoundError:
                    missingFiles.append(f)

        # parse normal files, plus anything that was passed in via the
        # "--file" option
        parseFiles(args.files)
        parseFiles(args.file)

        # check for stdin
        if args.stdin:
            self.process(sys.stdin)

        missingFiles.sort()
        self.missingFiles = missingFiles

    def validate_arguments(self, arguments):
        if not arguments.files and not arguments.file and not arguments.stdin:
            print(
                "Error: no files specified ({} -h)".format(sys.argv[0]),
                file=sys.stderr)
            exit(1)
