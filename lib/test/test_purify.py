#!/usr/bin/python3

import unittest

import env

import wlint.purify


class TestPurifyText(unittest.TestCase):
    def setUp(self):
        self.fn = wlint.purify.text

    def test_text(self):
        input = "This is a test."
        output = self.fn(input)
        self.assertEqual(input, output)


class TestPurifyTex(unittest.TestCase):
    def setUp(self):
        self.fn = wlint.purify.tex

    def test_text(self):
        input = "This is a test."
        output = self.fn(input)
        self.assertEqual(input, output)

    def test_strip_comment(self):
        input = "% this is a comment"
        output = self.fn(input)
        self.assertEqual(output, "")

    def test_strip_command(self):
        input    = R"\textbf{This is bold text.}"
        expected =  "       {This is bold text.}"
        output = self.fn(input)
        self.assertEqual(output, expected)

    def test_strip_nested_command(self):
        input    = R"\textbf{This is bold \textit{and slanted text.}}"
        expected =  "       {This is bold        {and slanted text.}}"
        output = self.fn(input)
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
