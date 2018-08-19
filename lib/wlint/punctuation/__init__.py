#!/usr/bin/python3

import re

import wlint.purify


def make_regex_rule(pattern_text):
    pattern = re.compile(pattern_text)

    def execute(text, fn):
        hit = False
        match = pattern.search(text)
        while match:
            hit = True
            fn(match.start())
            match = pattern.search(text, match.end())
        return hit

    return execute


def make_pair_regex_rule(first, second):
    return make_regex_rule("{}{}".format(first, second))
