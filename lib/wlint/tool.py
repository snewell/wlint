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
                ", ".join([i[0] for i in sort_methods])),
            default=sort_methods[0][0])
        self.add_argument(
            "--list-sorts",
            action='store_true',
            help="List supported sort methods.",
            default=argparse.SUPPRESS)
        self.sort_methods = sort_methods

    def execute(self, parsed_args):
        pass


def get_purifier(args):
    purifier = _INPUT_PURIFIERS.get(args.input_type)[0]
    if not purifier:
        raise ValueError(
            "'{}' is not a supported input type".format(args.input_type))
    return purifier


def iterate_files(parsed_args, process_fn):
    if parsed_args.files:
        missing_files = []
        for f in parsed_args.files:
            try:
                with open(f, 'r') as read_file:
                    process_fn(read_file)
            except FileNotFoundError:
                missing_files.append(f)
        return sorted(missing_files)
    else:
        # no files provided, so default to stdin
        process_fn(sys.stdin)
        return []


def _check_special_options(tool, parsed_args):
    def _list_sorts():
        for (name, description) in tool.sort_methods:
            print("{} - {}".format(name, description))

    def _list_input_types():
        for name, info in _INPUT_PURIFIERS.items():
            print("{} - {}".format(name, info[1]))

    if "list_sorts" in parsed_args and parsed_args.list_sorts:
        return _list_sorts
    elif "list_input_types" in parsed_args and parsed_args.list_input_types:
        return _list_input_types
    return None


def _parse_args(tool, *args, **kwargs):
    parsed_args = tool.parser.parse_args(*args, **kwargs)
    return parsed_args


def execute_tool(tool, args):
    if args is None:
        args = sys.argv[1:]
    try:
        parsed_args = _parse_args(tool, args)
        special_fn = _check_special_options(tool, parsed_args)
        if special_fn:
            special_fn()
        else:
            missing_files = tool.execute(parsed_args)

            if missing_files:
                print(
                    "Error opening files: {}".format(
                        missing_files),
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
