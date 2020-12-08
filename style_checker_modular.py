#!/usr/bin/env python3
"""Java Style Checker (CSE 142)

Code quality linter for Java, specifically designed for CSE 142 @ UW, Seattle
Usage: (Supports python 3.x)

Run script with ```python3 style_checker.py <PATH_TO_JAVA_FILE>``` to view
console output with list of code quality errors.
Refer to https://courses.cs.washington.edu/courses/cse142/20au/quality.html
for a comprehensive list of features. Should be run in the same module as
style.py and constant.py

To instansiate CSE142Checker object run:
checker = CSE142Checker(<path to file>)

TODO: Make other modes work
TODO: Add a style dictionary
TODO: Write Tests
TODO: Factor constants.py

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


# Regex Setup
BLANK_PRINTLNS = re.compile('System\.out\.println[\s]*\(""\)')


_checks = {'visible': {}, 'private': {}}


def _get_parameters(function):
    return [parameter.name
            for parameter
            in inspect.signature(function).parameters.values()
            if parameter.kind == parameter.POSITIONAL_OR_KEYWORD]


def add_check(check, code=None):
    """Add a new check"""
    def _add_check(check, kind, code, args):
        if check in _checks[kind]:
            _checks[kind][check][0].extend(code or [])
        else:
            _checks[kind][check] = (code or [''], args)

    if inspect.isfunction(check):
        args = _get_parameters(check)
        if args and args[0] in ('visible', 'hidden'):
            if code is None:
                code = ''
            _add_check(check, args[0], code, args)
    return check


@add_check
def check_blank_printlns(visible):
    """
    Check Blank Println statements
    """

    return 'Blank println statements', 'Your should say println() instead of println("")'


@add_check
def check_long_lines(visible):
    """
    Checks long lines
    """
    return 'Long Lines', 'Your lines should ideally cap out at 100 characters'


# Code Quality Checking
class CSE142Checker:
    """Load a Java source file, tokenize it, check coding style."""

    def __init__(self, filename, checks, options=None, **kwargs):
        if options is None:
            options = CodeQualityChecker(kwargs).options
        else:
            assert not kwargs
        self.check_file(filename)
        self.max_line_length = options["MAX_LINE_LENGTH"]
        self.tab_size = options["TAB_SIZE"]
        self.verbose = options["VERBOSE"]
        self.lines = readlines(filename)
        self.total_lines = len(self.lines)
        self.report = GenerateReport(
            verbose=self.verbose, total=self.total_lines)
        self.report_error = self.report.error
        self.visible = checks['visible']
        self.private_checks = checks['private']
        self.noqa = False

    # TODO: Check if file exists
    def check_file(self, filename):
        """Checks valdity of input file"""
        if not isinstance(filename, str):
            raise InputError('Usage: python style_checker.py [CLASS_NAME]')

        if filename[-5:] != '.java':
            raise InputError('File extension should be .java')

        self.filename = filename

    def readline(self):
        """Get the next line from the input buffer."""
        if self.line_number >= self.total_lines:
            return ''
        line = self.lines[self.line_number]
        self.line_number += 1
        return line

    def report_visible_results(self, line):
        """Reports check results"""
        for name, check, category in self.visible:
            result = self.run_checks(check, category)
            if result is not None:
                (info, message) = result
                self.report_error(self.line_number, info, message, check)

    def run_checks(self, check, category):
        """Runs all checks for a category"""
        categories = [getattr(self, name) for name in category]
        return check(*categories)

    def check_all(self, expected=None):
        """ Run tests on file and return the the list of errors"""
        self.report.init_file(self.filename, expected)
        self.line_number = 0
        line = self.readline()
        while line:
            self.report_visible_results(line)
            line = self.readline()

        return self.report.present_file_results()


# CSE142 Style Guide
class CodeQualityChecker:
    """Guide defined for CSE 142"""

    def __init__(self, *args, **kwargs):
        self.checker_class = CSE142Checker
        self.verbose = kwargs.pop('verbose', False)
        self.report = GenerateReport(verbose=self.verbose)
        self.mode = kwargs.pop('mode', 'visible')
        self.checks = {
            'visible': self.get_checks('visible'),
            'private': self.get_checks('private')
        }
        self.options = {
            "MAX_LINE_LENGTH": 100,
            "TAB_SIZE": 4,
            "VERBOSE": self.verbose
        }

    def run_tests(self, filename, expected=None):
        """Run all checks on a java source file"""
        print(f'Checking {filename}: ')

        checker = self.checker_class(
            filename, self.checks, options=self.options)
        result = None
        if self.mode == 'visible':
            result = checker.check_visible(expected=expected)
        elif self.mode == 'private':
            result = checker.check_private(expected=expected)
        elif self.mode == 'free':
            result = checker.check_all(expected=expected)
        else:
            raise InputError(
                'Create Checker with mode either visible, private, or free')

        if not result:
            return '\tPassed!'
        return result

    def get_checks(self, category):
        """Get all the checks for a category"""
        checks = []
        for check, attrs in _checks[category].items():
            (codes, args) = attrs
            checks.append((check.__name__, check, args))
        return sorted(checks)


# Reporting Code Quality Errors
class GenerateReport:
    """Collect the results of the checks"""

    def __init__(self, verbose, total=None):
        """Specific fields: total errors, errors by category
        and errors messages """
        self.messages = {}
        self.categories = {}
        self.lines = {}
        self.verbose = verbose
        self.total = total

    def init_file(self, filename, expected):
        """Constructs a new file"""
        self.filename = filename
        self.expected = expected or 'Passed!'
        self.file_errors = 0

    def error(self, line_num, info, message, check):
        """Report an error with options"""
        if info in self.categories:
            self.categories[info] += 1
            self.lines[info].append(line_num)
        else:
            self.categories[info] = 1
            self.messages[info] = message
            self.lines[info] = []

        self.file_errors += 1

    def get_count(self):
        """Returns the total count of all errors"""
        return sum(self.categories[key] for key in self.messages)

    def get_statistics(self):
        """Report statics of all errors"""
        return [
            f'Error {key} occured {self.categories[key]} times'
            for key in sorted(self.messages)
        ]

    def get_unique(self):
        """Report statics of unique errors"""
        return len(self.categories)

    def present_file_results(self):
        """Prints out errors in a ordered fashion"""
        errors = ''
        for category, count in sorted(self.categories.items()):
            s = f"\t{category} on " + \
                f"lines {str(self.lines[category]).replace('[', '{').replace(']', '}')}"
            errors = ''.join([errors, s])

            if self.verbose:
                errors = ''.join([errors, f' [Total Count = {count}]\n'])
                message = f"\tTA Note: {self.messages[category]}\n"
                errors = ''.join([errors, message])
            errors += '\n'

        if self.verbose and errors:
            errors += 'Statistics: \n'
            if self.total:
                errors = ''.join(
                    [errors, f'\tTotal Lines Checked: {self.total}\n'])
            errors = ''.join([errors, f'\tTotal Errors: {self.get_count()}\n'])
            errors = ''.join(
                [errors, f'\tUnique Errors: {self.get_unique()}\n'])

        return errors


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


checker = CodeQualityChecker(mode='free', verbose=True)
print(checker.run_tests('Test.java'))
