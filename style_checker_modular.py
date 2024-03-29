#!/usr/bin/env python3
"""Java Style Checker (CSE 142)

Code quality linter for Java, specifically designed for CSE 142 @ UW, Seattle
Usage: (Supports python 3.x)


authors: Omar, Sumant, Aidan
emails: oibra@uw.edu, guhas2@uw.edu, thalea@uw.edu
"""
import re
import sys
import subprocess
import traceback
import inspect
import tokenize
from configparser import RawConfigParser
from io import TextIOWrapper
import rich


from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
console = Console()

# Global Setup
NUM_CONSOLE_SCANNER = 0
NUM_RANDOM = 0
DEBUG = False

# Regex Setup
BLANK_PRINTLNS = re.compile(r'System\.out\.println[\s]*\(""\)')
BOOLEAN_TRUE = re.compile(r'(.*)==( *)true(.*)')
BOOLEAN_FALSE = re.compile(r'(.*)==( *)false(.*)')
BREAK = re.compile(r'break[\s]*;')
CONTINUE = re.compile(r'continue[\s]*;')
CATCH = re.compile(r'catch[\s]*\(.*\){')
VAR = re.compile(r'var.*=')
TO_ARRAY = re.compile(r'\.toArray.*')
STRING_BUILDER = re.compile(r'StringBuilder.*')
STRING_BUFFER = re.compile(r'StringBuffer')
STRING_JOINER = re.compile(r'StringJoiner')
STRING_TOKENIZER = re.compile(r'StringTokenizer')
TO_CHAR_ARRAY = re.compile(r'\.toCharArray.*')
CONSOLE_SCANNER = re.compile(r'.*new.*Scanner.*\(.*System.*\.in.*\).*')
RANDOM = re.compile(r'.*new.*Random.*\(.*\).*')
FILE_READER = re.compile(r'FileReader')
FILE_WRITER = re.compile(r'FileWriter')
BUFFERED_READER = re.compile(r'BufferedReader')
STRING_JOIN = re.compile(r'\.join')
STRING_MATCHES = re.compile(r'\.matches')
ARRAYS_AS_LIST = re.compile(r'Arrays\.asList')
ARRAYS_FILL = re.compile(r'Arrays\.fill')
ARRAYS_COPY_OF = re.compile(r'Arrays\.copyOf')
ARRAYS_COPY_OF_RANGE = re.compile(r'Arrays\.copyOfRange')
ARRAYS_SORT = re.compile(r'Arrays\.sort')
COLLECTIONS_COPY = re.compile(r'Collections\.copy')
COLLECTIONS_SORT = re.compile(r'Collections\.sort')
BACKSLASH_N = re.compile(r'\\n')
BACKSLASH_N_CORRECT = re.compile(r'printf\(\'|\".*\\n\'|\"\)')
CAMEL_CASING = re.compile(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])')

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
        return [key, BANK[key]]


@add_check
def check_long_lines(visible, max_line_length):
    """checks if line is longer than max_line_length"""
    key = 'Long lines'
    if len(visible) >= max_line_length - 1:
        return [key, BANK[key]]


@add_check
def check_consolescanner(visible):
    """checks for new Scanner(System.in)"""
    global NUM_CONSOLE_SCANNER
    match = CONSOLE_SCANNER.search(visible)
    key = 'Multiple console scanners'
    if match:
        NUM_CONSOLE_SCANNER += 1
        if NUM_CONSOLE_SCANNER == 2:
            return [key, BANK[key]]


@add_check
def check_random(visible):
    """checks for new Random()"""
    global NUM_RANDOM
    match = RANDOM.search(visible)
    key = 'Multiple random objects'
    if match:
        NUM_RANDOM += 1
        if NUM_RANDOM == 2:
            return [key, BANK[key]]


@add_check
def check_bad_boolean_zen(visible):
    """checks if boolean zen is good"""
    match_true = BOOLEAN_TRUE.search(visible)
    key = 'Bad boolean zen ( == true)'
    if match_true:
        return (key, BANK[key])

    match_false = BOOLEAN_FALSE.search(visible)
    key = 'Bad boolean zen ( == false)'
    if match_false:
        return [key, BANK[key]]


@add_check
def check_multiplestatements(visible):
    """checks for multiple statements on a line"""
    match = len(visible.split(';')) > 2 and 'for' not in visible
    key = 'Multiple statements per line'
    if match:
        return [key, BANK[key]]


@add_check
def check_backslashn(visible):
    """checks for backslash n on a line"""
    match = BACKSLASH_N.search(
        visible) and not BACKSLASH_N_CORRECT.search(visible)
    key = '\\n on line'
    if match:
        return [key, BANK[key]]


@add_check
def check_break(visible):
    """checks for break"""
    match = BREAK.search(visible)
    key = '[FORBIDDEN] Break'
    if match:
        return [key, BANK[key]]


@add_check
def check_continue(visible):
    """checks for continue"""
    match = CONTINUE.search(visible)
    key = '[FORBIDDEN] Continue'
    if match:
        return [key, BANK[key]]


@add_check
def check_try_catch(visible):
    """checks for try/catch statements"""
    match = CATCH.search(visible)
    key = '[FORBIDDEN] Try/Catch'
    if match:
        return [key, BANK[key]]


@add_check
def check_var(visible):
    """checks for var statements"""
    match = VAR.search(visible)
    key = '[FORBIDDEN] Var'
    if match:
        return [key, BANK[key]]


@add_check
def check_toarray(visible):
    """checks for .toArray statements"""
    match = TO_ARRAY.search(visible)
    key = '[FORBIDDEN] .toArray'
    if match:
        return [key, BANK[key]]


@add_check
def check_stringbuilder(visible):
    """checks for StringBuilder declerations"""
    match = STRING_BUILDER.search(visible)
    key = '[FORBIDDEN] StringBuilder'
    if match:
        return [key, BANK[key]]


@add_check
def check_stringbuffer(visible):
    """checks for StringBuffer declerations"""
    match = STRING_BUFFER.search(visible)
    key = '[FORBIDDEN] StringBuffer'
    if match:
        return [key, BANK[key]]


@add_check
def check_stringjoiner(visible):
    """checks for StringJoiner declerations"""
    match = STRING_JOINER.search(visible)
    key = '[FORBIDDEN] StringJoiner'
    if match:
        return [key, BANK[key]]


@add_check
def check_stringtokenizer(visible):
    """checks for StringTokenizer declerations"""
    match = STRING_TOKENIZER.search(visible)
    key = '[FORBIDDEN] StringTokenizer'
    if match:
        return [key, BANK[key]]


@add_check
def check_tochararray(visible):
    """checks for .toCharArray() calls"""
    match = TO_CHAR_ARRAY.search(visible)
    key = '[FORBIDDEN] .toCharArray'
    if match:
        return [key, BANK[key]]


@add_check
def check_filereader(visible):
    """checks for FileReader()"""
    match = FILE_READER.search(visible)
    key = '[FORBIDDEN] FileReader'
    if match:
        return [key, BANK[key]]


@add_check
def check_filewriter(visible):
    """checks for FileWriter()"""
    match = FILE_WRITER.search(visible)
    key = '[FORBIDDEN] FileWriter'
    if match:
        return [key, BANK[key]]


@add_check
def check_bufferedreader(visible):
    """checks for BufferedReader()"""
    match = BUFFERED_READER.search(visible)
    key = '[FORBIDDEN] BufferedReader'
    if match:
        return [key, BANK[key]]


@add_check
def check_stringjoin(visible):
    """checks for String.join()"""
    match = STRING_JOIN.search(visible)
    key = '[FORBIDDEN] String.join()'
    if match:
        return [key, BANK[key]]


@add_check
def check_stringmatches(visible):
    """checks for String.matches()"""
    match = STRING_MATCHES.search(visible)
    key = '[FORBIDDEN] String.matches()'
    if match:
        return [key, BANK[key]]


@add_check
def check_arraysaslist(visible):
    """checks for Arrays.asList()"""
    match = ARRAYS_AS_LIST.search(visible)
    key = '[FORBIDDEN] Arrays.asList()'
    if match:
        return [key, BANK[key]]


@add_check
def check_arrayscopyof(visible):
    """checks for Arrays.copyOf()"""
    match = ARRAYS_COPY_OF.search(visible)
    match_range = ARRAYS_COPY_OF_RANGE.search(visible)
    key = '[FORBIDDEN] Arrays.copyOf()'
    if match and not match_range:
        return [key, BANK[key]]


@add_check
def check_arrayscopyofrange(visible):
    """checks for Arrays.copyOfRange()"""
    match = ARRAYS_COPY_OF_RANGE.search(visible)
    key = '[FORBIDDEN] Arrays.copyOfRange()'
    if match:
        return [key, BANK[key]]


@add_check
def check_arrayssort(visible):
    """checks for Arrays.sort()"""
    match = ARRAYS_SORT.search(visible)
    key = '[FORBIDDEN] Arrays.sort()'
    if match:
        return [key, BANK[key]]


@add_check
def check_arraysfill(visible):
    """checks for Arrays.fill()"""
    match = ARRAYS_FILL.search(visible)
    key = '[FORBIDDEN] Arrays.fill()'
    if match:
        return [key, BANK[key]]


@add_check
def check_collectionscopy(visible):
    """checks for Collections.copy()"""
    match = COLLECTIONS_COPY.search(visible)
    key = key = '[FORBIDDEN] Collections.copy()'
    if match:
        return [key, BANK[key]]


@add_check
def check_collectionssort(visible):
    """checks for Collections.sort()"""
    match = COLLECTIONS_SORT.search(visible)
    key = key = '[FORBIDDEN] Collections.sort()'
    if match:
        return [key, BANK[key]]


@add_check
def check_camelcasing(visible):
    """checks for non camelCased variables"""
    rv = _getProperties(visible)
    if rv is None:
        return
    type, isVariable, name, params = rv
    key = 'Incorrect camel casing'
    if params is not None:
        vars = []
        params = params[2:-1]
        # print(params)
        if params:
            vars.append(params[0].split('(')[-1])
            for p in params[1:-1]:
                p = p.replace(',', '')
                vars.append(p)
            vars.append(params[-1].split(')')[0])
            if 'throws' in vars:
                idx = vars.index('throws')
                vars = vars[:idx]
            for _type, _name in _pairwise(vars):
                if _name.isalpha() and not _camelHelper(_name):
                    return [key, BANK[key]]

    if name is not None:
        name = name.replace(';', '')
        if '_' in name or not _camelHelper(name):
            return [key, BANK[key]]


@add_check
def check_nondescriptivevariables(visible):
    """checks for non descriptive variable names"""
    rv = _getProperties(visible)
    if rv is None:
        return
    type, isVariable, name, params = rv
    key = 'Non-Descriptive variable name'
    if params is not None:
        vars = []
        params = params[3:-1]
        if params:
            vars.append(params[0].split('(')[-1])
            for p in params[1:-1]:
                p = p.replace(',', '')
                vars.append(p)
            vars.append(params[-1].split(')')[0])
            if 'throws' in vars:
                idx = vars.index('throws')
                vars = vars[:idx]
            for _type, _name in _pairwise(vars):
                if _name.isalpha() and not _nameHelper(_type, True, _name):
                    return [key, BANK[key]]

    if name is not None:
        name = name.replace(';', '')
        if '(' in type:
            type = type.split('(')[1]
        if name.isalpha() and not _nameHelper(type, isVariable, name):
            return [key, BANK[key]]


def _pairwise(iterable):
    """Returns a pairwise iterable version of iterable"""
    a = iter(iterable)
    return zip(a, a)


def _nameHelper(type, isVariable, name):
    """helper for checking if a word is non-descriptive"""
    if isVariable:
        if type == 'Graphics' and name == 'g':
            return True
        if ((type == 'int' or type == 'double') and (
                name == 'x' or name == 'y')):
            return True
        if type == 'int' and (name == 'i' or name == 'j' or name == 'k'):
            return True
        if type == 'Random' and name == 'r':
            return True
        if type == 'File' and name == 'f':
            return True
        if type == 'int[]' and (name == 'a' or name == 'b'):
            return True
        if type == 'DrawingPanel' and name == 'p':
            return True

    if len(name) < 2:
        return False
    return True


def _camelHelper(word):
    """helper for checking if a word is camelCased"""
    split = re.split(CAMEL_CASING, word)
    if not split[0].islower():
        return False

    for word in split[1:]:
        if not word[0].isupper():
            return False
        sub = word[1:]
        if sub != sub.lower() and sub != sub.upper():
            return False

    return True


def _getProperties(visible):
    """gets variable name, type and isVariable, params from a line"""
    visible = visible.strip()
    split = re.split(' ', visible)
    if 'final' in visible or 'class' in visible or 'import' in visible:
        return

    name = None
    type = None
    isVariable = False
    params = None
    if (len(split) == 2 and 'return' not in visible and '++' not in split[0] and
            '++' not in split[1] and '--' not in split[0] and '--' not in split[1] and
            ';' in split[1]):
        isVariable = True
        name = split[1]
        type = split[0]
    elif '=' in split and split.index('=') > 1:
        isVariable = True
        idx = split.index('=')
        name = split[idx - 1]
        type = split[idx - 2]
    elif 'public' in visible or 'private' in visible or 'protected' in visible:
        if not '@' in visible:
            if 'static' in visible:
                name = split[3].split('(')[0]
                type = split[2]
            else:
                if len(split) != 2:
                    name = split[2].split('(')[0]
                    type = split[1]

        params = split

    return type, isVariable, name, params


# Code Quality Checking
class CSE142Checker:
    """Load a Java source file, tokenize it, check coding style."""

    def __init__(self, filename, checks, mode, options=None, **kwargs):
        if options is None:
            options = CodeQualityChecker(kwargs).options
        else:
            assert not kwargs
        self.check_file(filename)
        self.indent_type = options["INDENT_TYPE"]
        self.max_line_length = options["MAX_LINE_LENGTH"]
        self.tab_size = options["TAB_SIZE"]
        self.verbose = options["VERBOSE"]
        self.lines = readlines(filename)
        self.total_lines = len(self.lines)
        self.mode = mode
        self.report = GenerateReport(
            verbose=self.verbose, mode=self.mode, total=self.total_lines)
        self.report_error = self.report.error
        self.visible = checks['visible']
        self.private = checks['private']
        self.single_comment = False
        self.multi_comment = False
        self.indent_level = 0

    def check_file(self, filename):
        """Checks valdity of input file"""
        if not isinstance(filename, str):
            sys.exit('Usage: python style_checker.py [CLASS_NAME]')

        if filename[-5:] != '.java':
            sys.exit('Files should be .java files')

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
                self.report_error(self.line_number, info, message, check, line)

    def report_private_results(self, line):
        """Reports check results for private tests"""
        self.line = line
        for name, check, categories in self.private:
            result = self.run_checks(check, categories)
            if result is not None:
                (info, message) = result
                self.report_error(self.line_number, info, message, check, line)

    def run_checks(self, check, categories):
        """Runs all checks"""
        arguments = [getattr(self, name) for name in categories][1:]
        return check(self.line, *arguments)

    def handle_comments(self, line):
        if line.strip().startswith('//'):
            self.single_comment = True
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

    def check_indentation(self, line):
        if '}' in line:
            return

        correct = None
        if self.indent_type.startswith('t'):
            correct = '\t' * self.indent_level + line.strip()
        else:
            correct = ' ' * (self.indent_level *
                             self.tab_size) + line.strip()

        while line and line[len(line) - 1] == ' ':
            line = line[: len(line) - 1]

        if not line.strip():
            return 0

        if len(correct) > len(line) - 1:
            return 2
        elif len(correct) < len(line) - 1:
            return 1
        else:
            return 0

    def blank(self, line):
        return line.strip() == '' or '}' in line

    def handle_indentation(self, line):
        if '}' in line:
            self.indent_level -= 1

        if self.indent_level == 1 and self.line_number < self.total_lines - 2:
            if '}' in line:
                if not self.blank(self.lines[self.line_number]):
                    self.report_error(self.line_number,
                                    'Blank Lines Between Methods', BANK['Blank Lines Between Methods'], None, line)

        indent = self.check_indentation(line)
        if indent and not self.multi_comment:
            if indent == 2:
                self.report_error(self.line_number,
                                  'Under Indentation', BANK['Under Indentation'], None, line)
            else:  # indent is 1
                self.report_error(self.line_number,
                                  'Over Indentation', BANK['Over Indentation'], None, line)

        if '{' in line:
            self.indent_level += 1

    def check_all(self, expected=None, mode='visible'):
        """ Run tests on file and return the the list of errors"""
        self.report.init_file(self.filename, expected)
        self.line_number = 0
        line = self.readline()
        while line:
            self.single_comment = False
            line = self.handle_comments(line)

            self.handle_indentation(line)

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
        self.tab_size = 4
        self.indent_type = 'spaces'
        tabsize = kwargs.pop('tabsize', None)
        if tabsize:
            split = tabsize.split()
            if len(split) != 2:
                sys.exit(
                    'Specify tabsize in the format: "indentsize spaces" or "indentsize tabs"')
                self.tab_size = int(split[0])
                self.indent_type = split[1]

        self.max_line_length = kwargs.pop('max_line_length', 100)
        self.mode = kwargs.pop('mode', 'visible')
        self.report = GenerateReport(verbose=self.verbose, mode=self.mode)
        self.debug = kwargs.pop('debug', False)
        if (self.debug):
            global DEBUG
            DEBUG = True
        self.checks = {
            'visible': self.get_checks('visible'),
            'private': self.get_checks('private'),
        }
        self.options = {
            "MAX_LINE_LENGTH": self.max_line_length,
            "TAB_SIZE": self.tab_size,
            "VERBOSE": self.verbose,
            "INDENT_TYPE": self.indent_type
        }

    def run_tests(self, filename, expected=None):
        """Run all checks on a java source file"""
        if self.mode != 'web':
            console.print(
                f'[bold]Checking [blue]{filename}[/blue][/bold]: \n')

        checker = self.checker_class(
            filename, self.checks, options=self.options, mode=self.mode)

        if self.mode != 'visible' and self.mode != 'private' and self.mode != 'web':
            sys.exit(
                'Create Checker with mode either visible, private or web')

        result = checker.check_all(expected=expected, mode=self.mode)

        if not result and self.mode != 'web':
            return '\t😀👍 [red]L[/red][orange1]o[/orange1][yellow]o[/yellow]' + \
                '[green]k[/green][blue]s[/blue] [purple]G[/purple][blue]o[/blue]' + \
                '[green]o[/green][yellow]d[/yellow][orange1]![/orange1]\n'

        return result

    def get_checks(self, category):
        """Get all the checks for a category"""
        checks = []
        for check, attrs in _checks[category].items():
            (codes, args) = attrs
            checks.append((check.__name__, check, args))
        return checks


# Reporting Code Quality Errors
class GenerateReport:
    """Collect the results of the checks"""

    def __init__(self, verbose, mode, total=None):
        """Specific fields: total errors, errors by category
        and errors messages """
        self.messages = {}
        self.categories = {}
        self.lines = {}
        self.verbose = verbose
        self.total = total
        self.mode = mode
        self.lineContent = {}

    def init_file(self, filename, expected):
        """Constructs a new file"""
        self.filename = filename
        self.expected = expected or 'Passed!'
        self.file_errors = 0

    def error(self, line_num, info, message, check, line):
        """Report an error with options"""
        if info in self.categories:
            self.categories[info] += 1
            self.lines[info].append(line_num)
        else:
            self.categories[info] = 1
            self.messages[info] = message
            self.lines[info] = [line_num]

        self.lineContent[line_num] = line

        self.file_errors += 1

    def get_count(self):
        """Returns the total count of all errors"""
        return sum(self.categories[key] for key in self.messages)

    def get_statistics(self):
        """Report statics of all errors"""
        return [
            f'Error {key} occured {self.categories[key]} times'
            for key in self.messages
        ]

    def get_unique(self):
        """Report number of unique errors"""
        return len(self.categories)

    def present_file_results(self):
        """Prints out errors in a ordered fashion"""
        errors = ''
        index = 1
        forbidden = []
        other = []
        web_errors = []
        for item in self.categories.items():
            if item[0].startswith('[FORBIDDEN]'):
                forbidden.append(item)
            else:
                other.append(item)
        forbidden.sort(key=lambda x: x[1], reverse=True)
        other.sort(key=lambda x: x[1], reverse=True)
        total = forbidden + other
        for category, count in total:
            formatted_categories = self.messages[category]
            formatted_categories = re.sub(
                '([\[]).*?([\]])', '', formatted_categories)
            formatted_categories = re.sub(
                '\\n', ' ', formatted_categories)
            if self.mode == 'web':
                for index, line in enumerate(self.lines[category]):
                    web_errors.append([
                        category, line, count, formatted_categories, self.lineContent[line]
                    ])

                continue

            multiple_scanners = category.startswith(
                'Multiple console scanners')
            multiple_random = category.startswith('Multiple random objects')

            phrase = 'line' if len(self.lines[category]) == 1 else 'lines'

            linenum = str(self.lines[category]).replace(
                '[', '{').replace(']', '}')

            if multiple_scanners or multiple_random:
                linenum = ''

            if category.startswith('[FORBIDDEN]'):
                s = f"{index}. [bold red]{category}[/bold red] on " + \
                    f"{phrase} {linenum}"
            else:
                s = f"{index}. [bold yellow]{category}[/bold yellow] on " + \
                    f"{phrase} {linenum}"

            errors = ''.join([errors, s])

            if self.verbose:
                if multiple_scanners:
                    count = NUM_CONSOLE_SCANNER
                elif multiple_random:
                    count = NUM_RANDOM
                errors = ''.join(
                    [errors, f' [Total Count = {count}]\n'])
                message = f"TA Note: {self.messages[category]}\n"
                errors = ''.join([errors, message])
            errors += '\n'
            index += 1

        if self.verbose and errors:
            errors += '[bold blue]Statistics:[/bold blue] \n'
            if self.total:
                errors = ''.join(
                    [errors, f'Total Lines Checked: {self.total}\n'])
            errors = ''.join([errors, f'Total Errors: {self.get_count()}\n'])
            errors = ''.join(
                [errors, f'Unique Errors: {self.get_unique()}\n'])

            if len(forbidden) == 0:
                errors = ''.join(
                    [errors, f'Unique Forbidden Features: {len(forbidden)}\n'])
            else:
                errors = ''.join(
                    [errors, f'[red]Unique Forbidden Features:[/red] {len(forbidden)}\n'])
        if self.mode == 'web':
            return sorted(web_errors, key=lambda x: x[1])
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
    'and should [italic]never[/italic] exceed 100 characters in length. Lines that \n' +
    'are too long should be broken up and wrapped to the next line.',

    'Blank println statements': 'A blank println should actually be blank. \n' +
    f'You should always print a blank line using [bold]System.out.println()[/bold]. Printing \n' +
    'an empty String with System.out.println("") is considered bad style; it makes\n' +
    'the intention less clear.',

    'Bad boolean zen ( == true)': 'You should never test booleans for equality, \n' +
    'you should just use x itself as a condition',

    'Bad boolean zen ( == false)': 'You should never test booleans for equality, \n' +
    'you should just use !x itself as a condition',

    'Multiple console scanners': 'There should be one Scanner per source. It\'s best\n' +
    'practice to only have one Scanner',

    'Multiple random objects': 'There should be one Random per file. It\'s best practice\n' +
    'to only have one Random object created, and pass that Random around to anywhere that\n' +
    'needs it.',

    '\\n on line': '\\n should only be used in printf. It\'s best practice\n' +
    'You should just use println if you want to print a full line.',

    'Multiple statements per line': 'There is more than one statement on this line. It\'s best\n' +
    'practice to limit your code to one statement per line',

    'Non-Private fields': 'Fields should be private. This ensures that no client of your object will\n' +
    ' be able to directly change the state of your object in a way that you haven’t allowed them to',

    '[FORBIDDEN] Break': 'Break is a [bold]forbidden[/bold] feature. You are [italic]not[/italic] allowed to use it in \n' +
    'CSE14x. Considering exiting a loop with a different conditional structure',

    '[FORBIDDEN] Continue': 'Continue is a [bold]forbidden[/bold] feature. You are [italic]not[/italic] allowed to use \n' +
    'it in CSE14x. Considering using a different conditional structure',

    '[FORBIDDEN] Try/Catch': 'Try/Catch is a [bold]forbidden[/bold] feature. You are [italic]not[/italic] allowed \n' +
    'to use it in CSE14x. Consider throwing Exceptions instead',

    '[FORBIDDEN] Var': 'Var is a [bold]forbidden[/bold] feature. You are [italic]not[/italic] allowed \n' +
    'to use it in CSE14x. Declare typed variables instead',

    '[FORBIDDEN] .toArray': '.toArray is a [bold]forbidden[/bold] feature. You are [italic]not[/italic] allowed \n' +
    'to use it in CSE14x. Convert to arrays manually',

    '[FORBIDDEN] StringBuilder': 'StringBuilder is a [bold]forbidden[/bold] feature. You are \n' +
    '[italic]not[/italic] allowed to use it in CSE14x. Consider using String concatenation',

    '[FORBIDDEN] StringBuffer': 'StringBuffer is a [bold]forbidden[/bold] feature. You are \n' +
    '[italic]not[/italic] allowed to use it in CSE14x. Consider using simple immutable String',

    '[FORBIDDEN] StringJoiner': 'StringJoiner is a [bold]forbidden[/bold] feature. You are \n' +
    '[italic]not[/italic] allowed to use it in CSE14x. Consider using String concatenation',

    '[FORBIDDEN] StringTokenizer': 'StringJoiner is a [bold]forbidden[/bold] feature. You are \n' +
    '[italic]not[/italic] allowed to use it in CSE14x. [italic]Not[/italic] sure why you are using this in 142 :)',

    '[FORBIDDEN] .toCharArray': '.toCharArray is a [bold]forbidden[/bold] feature. You are \n' +
    '[italic]not[/italic] allowed to use it in CSE14x. You should build up arrays manually _if_ necessary',

    '[FORBIDDEN] FileReader': 'FileReader is a [bold]forbidden[/bold] feature. You are \n' +
    '[italic]not[/italic] allowed to use it in CSE14x. You should use Scanners to read file input',

    '[FORBIDDEN] BufferedReader': 'BufferedReader is a [bold]forbidden[/bold] feature. You are \n' +
    '[italic]not[/italic] allowed to use it in CSE14x. You should use Scanners to read file input',

    '[FORBIDDEN] FileWriter': 'FileWriter is a [bold]forbidden[/bold] feature. You are \n' +
    '[italic]not[/italic] allowed to use it in CSE14x. You should use PrintStreams to write file output',

    '[FORBIDDEN] String.join()': 'String.join() is a [bold]forbidden[/bold] feature. You are [italic]not[/italic] allowed\n' +
    'to use it in CSE14x. Considering using String concatenation instead',

    '[FORBIDDEN] String.matches()': 'String.join() is a [bold]forbidden[/bold] feature. You are [italic]not[/italic]\n' +
    'allowed to use it in CSE14x. You should not use regex!',

    '[FORBIDDEN] Arrays.asList()': 'Arrays.asList() is a [bold]forbidden[/bold] feature. You are [italic]not[/italic]\n' +
    'allowed to use it in CSE142. You should not use ArrayList<E>',

    '[FORBIDDEN] Arrays.copyOf()': 'Arrays.copyOf() is a [bold]forbidden[/bold] feature. You are [italic]not[/italic]\n' +
    'allowed to use it in CSE142. You should not use ArrayList<E>',

    '[FORBIDDEN] Arrays.copyOfRange()': 'Arrays.copyOfRange() is a [bold]forbidden[/bold] feature. You are [italic]not[/italic]\n' +
    'allowed to use it in CSE142. You should not use ArrayList<E>',

    '[FORBIDDEN] Arrays.sort()': 'Arrays.sort() is a [bold]forbidden[/bold] feature. You are [italic]not[/italic]\n' +
    'allowed to use it in CSE142. Sort arrays manually [italic]if[/italic] necessary',

    '[FORBIDDEN] Arrays.fill()': 'Arrays.fill() is a [bold]forbidden[/bold] feature. You are [italic]not[/italic]\n' +
    'allowed to use it in CSE142. Fill arrays manually [italic]if[/italic] necessary',

    '[FORBIDDEN] Collections.copy()': 'Collections.copy() is a [bold]forbidden[/bold] feature. You are [italic]not[/italic]\n' +
    'allowed to use it in CSE142. Copy collections manually [italic]if[/italic] necessary',

    '[FORBIDDEN] Collections.sort()': 'Collections.sort() is a [bold]forbidden[/bold] feature. You are [italic]not[/italic]\n' +
    'allowed to use it in CSE142. Sort collections manually [italic]if[/italic] necessary',

    'Incorrect camel casing': 'This name has the wrong naming conventions (should be camelCased). It\'s best practice\n' +
    'to have all identifier names camelCased by having all words after the first start with an uppercase letter',

    'Non-Descriptive variable name': 'This name is not descriptive. It\'s best practice\n' +
    'to have all identifier names specify what they do',

    'Under Indentation': 'This line is underindented.\n' +
    'You should indent your program one tab further every time you open a\n' +
    'curly brace and indent one tab less every time you close a curly brace.\n' +
    'This line should be indented more. Use the Indenter tool to indent your code automatically',

    'Over Indentation': 'This line is overindented.\n' +
    'You should indent your program one tab further every time you open a\n' +
    'curly brace and indent one tab less every time you close a curly brace.\n' +
    'This line should be indented less. Use the Indenter tool to indent your code automatically',

    'Blank Lines Between Methods': 'You should have blank lines between methods. They help improve readability and structure'
}


# Error Handling
def exit_on_error(exctype, value, tb):
    """Exits program on error"""
    import os
    if not DEBUG:
        fname = os.path.split(tb.tb_frame.f_code.co_filename)[1]
        obj = traceback.extract_tb(tb)
        line_num = obj[-1].lineno
        line = obj[-1].line
        console.print(f"""\tGot a [bold blue]{exctype.__name__}[/bold blue] in file {fname} on line [bold blue]{line_num}[/bold blue]
        because of line:""")
        print(f'\t\t{line}')
        console.print(f"""
        (TA Note) This test probably broke :cry: [bold red]Post on the message board![/bold red]
        Terminating program...\n""")
        sys.exit()
    else:
        sys.exit(traceback.print_exception(exctype, value, tb))


sys.excepthook = exit_on_error


def main(filename, mode, verbose, debug, tabsize):
    print()
    if mode != 'web':
        console.rule('CSE 142 Code Quality Checker')
    checker = CodeQualityChecker(
        mode=mode, verbose=verbose, debug=debug, tabsize=tabsize)
    tests = checker.run_tests(filename)
    if mode == 'web':
        return tests
    else:
        console.print(tests)


if __name__ == '__main__':
    main(filename=sys.argv[1], mode=sys.argv[2],
         verbose=bool(sys.argv[3]), debug=bool(sys.argv[4]), tabsize=None)
