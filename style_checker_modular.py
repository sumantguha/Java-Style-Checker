#!/usr/bin/env python3
"""Java Style Checker (CSE 142)

Code quality linter for Java, specifically designed for CSE 142 @ UW, Seattle
Usage: (Supports python 3.x)

Run script with ```python3 style_checker.py <PATH_TO_JAVA_FILE>``` to view
console output with list of code quality errors. 
Refer to https://courses.cs.washington.edu/courses/cse142/20au/quality.html
for a comprehensive list of features. Should be run in the same module as
style.py and constant.py

To instansiate CodeQualityChecker object run:
checker = CodeQualityChecker(<path to file>)

// TODO: Translate style.py into a class StyleGuide

author: Omar, Sumant
email: oibra@uw.edu, guhas2@uw.edu
"""
import re
import sys
import inspect
import tokenize

try:
    from functools import lru_cache
except ImportError:
    def lru_cache(maxsize=128):
        return lambda function: function

try:
    from configparser import RawConfigParser
    from io import TextIOWrapper
except ImportError:
    pass

# Local Constant Setup
import constant


# Code Quality Checking
class CodeQualityChecker():
    """Load a Java source file, tokenize it, check coding style."""

    def __init__(self, filename,

                 ):
        self.file = self.check_file(filename)
        self.max_line_length = constant.MAX_LINE_LENGTH
        self.tab_size = constant.TAB_SIZE
        self.verbose = constant.VERBOSE
        self.lines = readlines(filename)

    def check_file(self, filename):
        if not isinstance(filename, str):
            raise InputError('Usage: python style_checker.py [CLASS_NAME]')

    def printLines(self):
        print(self.lines)


# Helper Functions
def readlines(filename):
    """Read the source code."""
    try:
        with open(filename, 'rb') as f:
            (coding, lines) = tokenize.detect_encoding(f.readline)
            f = TextIOWrapper(f, coding, line_buffering=True)
            return [line.decode(coding) for line in lines] + f.readlines()
    except (LookupError, SyntaxError, UnicodeError):
        # Fall back if file encoding is improperly declared
        with open(filename, encoding='latin-1') as f:
            return f.readlines()


# Error Handling
class Error(Exception):
    """Base case for exceptions"""
    pass


class InputError(Error):
    """Exception raised for errors in the input

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


checker = CodeQualityChecker('Test.java')
checker.printLines()
