#!/usr/bin/python3

import argparse
import sys


class ArgumentParser:

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

    def parse_args(self, *args, **kwargs):
        args = self.parser.parse_args(*args, **kwargs)
        if not args.files and not args.file and not args.stdin:
            print(
                "Error: no files specified ({} -h)".format(sys.argv[0]),
                file=sys.stderr)
            exit(1)
        return args
