#!/usr/bin/python3

import unittest

import env

import wlint.purify

def compare(ut, input, expected):
    ut.assertEqual(ut.fn(input), expected)

class TestPurifyText(unittest.TestCase):
    def setUp(self):
        self.fn = wlint.purify.text

    def test_text(self):
        input = "This is a test."
        compare(self, input, input)


class TestPurifyTex(unittest.TestCase):
    def setUp(self):
        self.fn = wlint.purify.tex

    def test_text(self):
        input = "This is a test."
        compare(self, input, input)

    def test_strip_comment(self):
        input = "% this is a comment"
        compare(self, input, "")

    def test_strip_command(self):
        input    = R"\textbf{This is bold text.}"
        expected =  "       {This is bold text.}"
        compare(self, input, expected)

    def test_strip_nested_command(self):
        input    = R"\textbf{This is bold \textit{and slanted text.}}"
        expected =  "       {This is bold        {and slanted text.}}"
        compare(self, input, expected)


if __name__ == '__main__':
    unittest.main()
