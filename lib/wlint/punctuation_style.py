#!/usr/bin/python3

import re

import wlint.plugin
import wlint.tool


def _get_enabled_rules(enabled_rules):
    ret = {}
    rules = enabled_rules.split(",")
    for rule in rules:
        pattern = re.compile(rule.replace(".", "\.").replace("*", ".*"))
        for (message, fn) in _AVAILABLE_RULES:
            if pattern.match(message):
                ret[message] = fn
    return ret


def _remove_disabled_rules(disabled_rules, checks):
    for rule in disabled_rules:
        if rule:  # don't deal with empty strings
            pattern = re.compile(rule.replace(
                ".", "\.").replace("*", ".*"))
            rms = []
            for message in checks:
                if pattern.match(message):
                    rms.append(message)
            for message in rms:
                del checks[message]

    return checks


def _build_available_rules():
    found_rules = wlint.plugin.query_plugins("wlint.punctuation_rules")
    rule_lists = []
    for name, rules in found_rules.items():
        del name
        rule_lists += rules
    return rule_lists


_AVAILABLE_RULES = _build_available_rules()


def _check_rules(rules, text, hit_fn):
    for (message, fn) in rules:
        fn(text, lambda pos: hit_fn(message, pos))


def _check_handle(rules, handle, hit_fn, purifier):
    line_number = 0
    for text in handle:
        line_number += 1
        _check_rules(
            rules,
            purifier(text),
            lambda message,
            pos: hit_fn(
                line_number,
                message,
                pos))


class PunctuationStyle(wlint.tool.Tool):

    def __init__(self):
        super().__init__(description="Check for common punctuation issues",
                         prog="wlint punctuation-style")
        self.add_argument(
            "--enable",
            help="Rules to use when processing text.  An asterisk (*) can be "
                 "used for wildcard matching.",
            default="*")
        self.add_argument(
            "--disable",
            help="Rules to disable when processing text.  If a rule is both "
                 "enabled and disabled, disable takes precedence.")

    def execute(self, parsed_args):
        rules = _get_enabled_rules(parsed_args.enable)
        if parsed_args.disable:
            disable = parsed_args.disable.split(",")
            rules = _remove_disabled_rules(disable, rules)

        checks = []
        for (message, fn) in rules.items():
            checks.append((message, fn))

        purifier = wlint.tool.get_purifier(parsed_args)

        def _process(file_handle):
            hits = []
            _check_handle(checks, file_handle,
                          lambda line_number, message, pos: hits.append((line_number, pos, message)), purifier)
            hits.sort()
            for (line, col, message) in hits:
                print("{}-{}:{} {}".format(file_handle.name, line, col, message))

        return wlint.tool.iterate_files(parsed_args, _process)


def main(args=None):
    punctuationStyle = PunctuationStyle()
    wlint.tool.execute_tool(punctuationStyle, args)


_PUNCTUATION_STYLE_COMMAND = (
    main,
    "Check for punctuation errors")

if __name__ == '__main__':
    main()