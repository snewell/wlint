#!/usr/bin/python3

import unittest

import env

import wlint.punctuation


class TestPunctuation(unittest.TestCase):
    def test_ctor(self):
        punc = wlint.punctuation.PunctuationRules()


if __name__ == '__main__':
    unittest.main()

