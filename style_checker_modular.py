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

TODO: Write Tests

Features to add:
* long line checking for line with comments at the end
* checking in_class or not

author: Omar, Sumant
email: oibra@uw.edu, guhas2@uw.edu
"""
import re
import sys
import traceback
import inspect
import tokenize
from configparser import RawConfigParser
from io import TextIOWrapper

# Regex Setup
BLANK_PRINTLNS = re.compile(r'System\.out\.println[\s]*\(""\)')
BOOLEAN_TRUE = re.compile(r'(.*)==( *)true(.*)')
BOOLEAN_FALSE = re.compile(r'(.*)==( *)false(.*)')

_checks = {'visible': {}, 'private': {}}


def exception_handler(exception_type, exception, tb):
    traceback.print_tb(tb)
    print(f"\n{exception_type.__name__}: {exception}")


sys.excepthook = exception_handler


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
        if args and args[0] in ('visible', 'private'):
            if code is None:
                code = ''
            _add_check(check, args[0], code, args)
    return check


@add_check
def check_blank_printlns(visible):
    """check for println("") instead of println()"""
    match = BLANK_PRINTLNS.search(visible)
    key = 'Blank println statements'
    if match:
        try:
            return (key, BANK[key])
        except KeyError as e:
            raise SearchError(
                '(TA Note) This test probably broke, post on the message board')


@add_check
def check_long_lines(visible, max_line_length):
    """checks if line is longer than max_line_length"""
    key = 'Long lines'
    if len(visible) >= max_line_length - 1:
        try:
            return (key, BANK[key])
        except KeyError as e:
            raise SearchError(
                '(TA Note) This test probably broke, post on the message board')


@add_check
def check_bad_boolean_zen(visible):
    """checks if boolean zen is good"""
    match_true = BOOLEAN_TRUE.search(visible)
    if match_true:
        return ('Bad boolean zen (== true)',
                'You should never test booleans for equality, ' +
                'you should just use x itself as a condition')

    match_false = BOOLEAN_FALSE.search(visible)
    if match_false:
        return ('Bad boolean zen (== false)',
                'You should never test booleans for equality, ' +
                'you should just use !x itself as a condition')


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
        self.private = checks['private']
        self.single_comment = False
        self.multi_comment = False

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
        """Reports check results for visible tests"""
        self.line = line
        for name, check, categories in self.visible:
            result = self.run_checks(check, categories)
            if result is not None:
                (info, message) = result
                self.report_error(self.line_number, info, message, check)

    def report_private_results(self, line):
        """Reports check results for private tests"""
        self.line = line
        for name, check, categories in self.private:
            result = self.run_checks(check, categories)
            if result is not None:
                (info, message) = result
                self.report_error(self.line_number, info, message, check)

    def run_checks(self, check, categories):
        """Runs all checks"""
        arguments = [getattr(self, name) for name in categories][1:]
        return check(self.line, *arguments)

    def handle_comments(self, line):
        if line.strip().startswith('//'):
            self.single_comment = True
            line = self.readline()
            return ''
        elif '//' in line:
            idx = line.index('//')
            line = line[:idx].strip()

        if not self.single_comment \
                and not self.multi_comment and '/*' in line:
            self.multi_comment = True
            if line.find('*/') > line.find('/*'):
                line = line[: line.find('/*')] + \
                    line[line.find('*/') + 1:]
                self.multi_comment = False
            else:
                line = line[: line.find('/*')]

        if self.multi_comment and '*/' in line:
            self.multi_comment = False
            line = line[line.find('*/') + 2:]

        return line

    def display_results(self, line, mode):
        self.report_visible_results(line)
        if mode == 'private':
            self.report_private_results(line)

    def check_all(self, expected=None, mode='visible'):
        """ Run tests on file and return the the list of errors"""
        self.report.init_file(self.filename, expected)
        self.line_number = 0
        line = self.readline()
        while line:
            line = self.handle_comments(line)

            if not self.single_comment and not self.multi_comment:
                self.display_results(line, mode)

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

        if self.mode != 'visible' and self.mode != 'private':
            raise InputError(
                'Create Checker with mode either visible or private')

        result = checker.check_all(expected=expected, mode=self.mode)

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
            self.lines[info] = [line_num]

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
        """Report number of unique errors"""
        return len(self.categories)

    def present_file_results(self):
        """Prints out errors in a ordered fashion"""
        errors = ''
        index = 1
        for category, count in sorted(self.categories.items()):
            phrase = 'line' if len(self.lines[category]) == 1 else 'lines'
            s = f"\t{index}) {category} on " + \
                f"{phrase} {str(self.lines[category]).replace('[', '{').replace(']', '}')}"
            errors = ''.join([errors, s])

            if self.verbose:
                errors = ''.join([errors, f' [Total Count = {count}]\n'])
                message = f"\tTA Note: {self.messages[category]}\n"
                errors = ''.join([errors, message])
            errors += '\n'
            index += 1

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


# Annotation Bank
BANK = {
    'Long lines': 'Lines of code should ideally max out at 80 characters, \n' +
    '\tand should never exceed 100 characters in length. Lines that \n' +
    '\tare too long should be broken up and wrapped to the next line.',

    'Blank println statements': 'A blank println should actually be blank. \n' +
    '\tYou should always print a blank line using System.out.println(). Printing \n' +
    '\tan empty String with System.out.println("") is considered bad style; it makes\n' +
    '\tthe intention less clear.'
}


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


class SearchError(Error):
    """Exception raised for errors in the annotations search

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        print(self.message)


def main():
    checker = CodeQualityChecker(mode='private', verbose=True)
    if len(sys.argv) != 2:
        raise InputError('Usage: python style_checker.py [CLASS_NAME]')
    print(checker.run_tests(sys.argv[1]))


if __name__ == '__main__':
    main()
