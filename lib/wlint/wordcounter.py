#!/usr/bin/python3

import re

import wlint.purify

_RIGHT_SINGLE_QUOTE = "’"
_PATTERN = re.compile(r"\b([\w\-\'{}]+)\b".format(_RIGHT_SINGLE_QUOTE))


def count_line(text):
    counts = {}

    local_count = 0
    match = _PATTERN.search(text)
    while match:
        word = match.group(1)
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
        local_count += 1
        match = _PATTERN.search(text, match.end())

    return (counts, local_count)


def _update_full_counts(full_counts, line_counts):
    for word, count in line_counts[0].items():
        new_count = full_counts.get(word, 0) + count
        full_counts[word] = new_count


def count_handle(handle, purifier):
    full_counts = {}
    total_word_count = 0

    for text in handle:
        counts = count_line(purifier(text))
        _update_full_counts(full_counts, counts)
        total_word_count += counts[1]

    return (full_counts, total_word_count)
