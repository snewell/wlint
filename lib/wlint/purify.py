#!/usr/bin/python3

import re


def text(s_data):
    return s_data


_TEXT_PURIFIER = (text, "Plain text")


def tex(s_data):
    def strip_comment(text_data):
        index = text_data.find("%")
        if index == -1:
            return text_data
        return text_data[:index]

    pattern = re.compile(r"(\\\w+)")

    def strip_commands(text_data):
        def replace_fn(match):
            return " " * len(match.group(0))

        return re.sub(pattern, replace_fn, text_data)

    return strip_commands(strip_comment(s_data))


_TEX_PURIFIER = (tex, "(La)TeX input")
