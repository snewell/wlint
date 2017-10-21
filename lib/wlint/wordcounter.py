#!/usr/bin/python3

import re


_right_single_quote = "’"
_pattern = re.compile(r"\b([\w\-\'{}]+)\b".format(_right_single_quote))


def count_line(text):
    counts = {}

    local_count = 0
    match = _pattern.search(text)
    while match:
        word = match.group(1)
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
        local_count += 1
        match = _pattern.search(text, match.end())

    return (counts, local_count)


def count_handle(handle, purifier=None):
    if not purifier:
        def purifier(t): return t

    full_counts = {}
    total_word_count = 0

    for text in handle:
        counts = count_line(purifier(text))
        for word, count in counts[0].items():
            if word in full_counts:
                full_counts[word] += count
            else:
                full_counts[word] = count
        total_word_count += counts[1]

    return (full_counts, total_word_count)
