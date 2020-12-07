# Style linter for Java programs
import re
import sys
import json

# Constant setup
max_line_length = 100
boolean_true = '(.*)==( *)true(.*)'
boolean_false = '(.*)==( *)false(.*)'
scanners = '(.*)new Scanner\(System\.in\)(.)*'
random = '(.*)new Random(.)*'
empty_printlns = 'System\.out\.println[\s]*\(""\)'
state = {
    'line_errors': [],
    'errors_by_type': {}
}
tab_size = 4
in_class = False
in_main = False
perhaps_redundancy_count = 0
return_count = 0
for_count = 0
next_count = 0
double_count = 0
right_count = 0
lower_higher_count = 0
guess_count = 0
while_count = 0
move_count = 0
f_count = 0
m_count = 0

style = json.load(open('style.json'))

# Checking correct usage of program
if len(sys.argv) != 2:
    sys.exit('Usage: python style_checker_grading.py [CLASS_NAME]')


def main():
    lint_code(sys.argv[1])
    print_errors()


def lint_code(file: str):
    """
    Check code for style errors. Checks regular expressions to
    catch errors with line length, indentation, comments, and
    object creation.

    Args:
        filename to be linted: string
    """

    empty_struct = False
    num_scanners = 0
    num_random = 0

    # Strip newline characters
    with open(file, 'r') as f:
        file_list = [line.rstrip('\n') for line in f if line != '']

    indent_level = 0
    multi_comment = False

    # Parse file list and check for errors
    for num, line in enumerate(file_list):
        # Tracks line number
        line_num = num + 1

        # Tracks error log on each line
        lineLog = {
            'line': line_num,
            'code': line,
            'errors': []
        }

        # Append to state
        state['line_errors'].append(lineLog)

        # REGEX TESTS

        # Matching whitespace
        whitespace = re.search('^[ \t]*$', line)
        if whitespace:
            continue

        # Removing curly
        if '}' in line:
            indent_level -= 1

        # Line length
        if check_length(line):
            add_error(line_num, 'long_lines')

        # Indentation
        if indent_level == 1 and num < len(file_list) - 1:
            # if '}' in line:
            #     print(line + "\n" + file_list[num + 1] + "\n")
            if '}' in line and blank(file_list[num + 1]):
                add_error(line_num, "blank_lines")

        indent4 = check_indentation(line, indent_level, 4, line_num, file_list)
        indent3 = check_indentation(
            line, indent_level, 3,  line_num, file_list)
        indent2 = check_indentation(
            line, indent_level, 2,  line_num, file_list)
        if (indent4 and indent3 and indent2) and not multi_comment:
            add_error(line_num, "indentation", "either")

        # Adding indentation
        if '{' in line:
            indent_level += 1
            global in_class
            in_class = False

        # COMMENTS
        # Single line comments
        single_comment = False
        if line.strip()[:2] == '//':
            single_comment = True

        # Multi line comments
        if not single_comment and not multi_comment and '/*' in line:
            multi_comment = True
            if line.find('*/') > line.find('/*'):
                line = line[: line.find('/*')] + line[line.find('*/') + 1:]
                multi_comment = False
            else:
                line = line[: line.find('/*')]

        # TODO: Check with Omar
        if multi_comment and '*/' in line:
            multi_comment = False
            line = line[line.find('*/') + 2:]

        # Code Ignoring comments
        if not single_comment and not multi_comment:
            if 'class ' in line:
                in_class = True

            # TODO: Fix this
            # old_indent_level = None
            # if 'main' in line:
            #     global in_main
            #     old_indent_level = indent_level
            #     in_main = True

            # if old_indent_level is not None and indent_level == old_indent_level:
            #     in_main = False

            # Private fields (No encapsulation!)
            if in_class:
                if not check_private_fields(line):
                    add_error(line_num, 'private_fields')

            # Boolean zen
            if check_boolean_zen_true(line):
                add_error(line_num, 'boolean_zen', 'equals_true')

            if check_boolean_zen_false(line):
                add_error(line_num, 'boolean_zen', 'equals_false')

            # Empty structures
            if '}' in line and empty_struct:
                add_error(line_num, 'empty_struct')

            # Multiple console scanners
            if re.search(scanners, line):
                num_scanners += 1
                if num_scanners > 1:
                    add_error(line_num, 'scanners')

            # Multiple Ranom objects
            if re.search(random, line):
                num_random += 1
                if num_random > 1:
                    add_error(line_num, 'random')

            # VARIABLE NAMING CONVENTIONS
            # Check constant conventions
            # if check_screaming_case(line):
            #   add_error(line_num, 'naming_conventions', 'screaming')

            # Class naming conventions
            # if check_pascal_case(line):
            #    add_error(line_num, 'naming_conventions', 'pascal')

            # Variable naming conventions
            if check_camel_case(line):
                add_error(line_num, 'naming_conventions', 'camel')

            # Checking bad variable names
            if not check_bad_variable_names(line):
                add_error(line_num, 'naming_conventions', 'bad_variable_names')

            # CHECK ADVANCED MATERIAL
            # TODO: added regex for forbidden

            # Check Break
            if check_break(line):
                add_error(line_num, 'forbidden_features', 'break')

            # Check continue
            if check_continue(line):
                add_error(line_num, 'forbidden_features', 'continue')

            # Check try/catch
            if check_try_catch(line):
                add_error(line_num, 'forbidden_features', 'try/catch')

            # Check var
            if check_var(line):
                add_error(line_num, 'forbidden_features', 'var')

            # Check toArray
            if check_to_array(line):
                add_error(line_num, 'forbidden_features', 'toArray')

            # Check String Builder
            if check_string_builder(line):
                add_error(line_num, 'forbidden_features', 'string', 'builder')

            # Check String Buffer
            if check_string_buffer(line):
                add_error(line_num, 'forbidden_features', 'string', 'buffer')

            # Check String Joiner
            if check_string_joiner(line):
                add_error(line_num, 'forbidden_features', 'string', 'joiner')

            # Check String Tokenizer
            if check_string_tokenizer(line):
                add_error(line_num, 'forbidden_features',
                          'string', 'tokenizer')

            # Check String toCharArray
            # TODO: Check String.toCharArray?
            if check_string_char_array(line):
                add_error(line_num, 'forbidden_features',
                          'string', 'toCharArray')

            # Check String Join
            if check_string_join(line):
                add_error(line_num, 'forbidden_features', 'string', 'join')

            # Check String Matches
            if check_string_matches(line):
                add_error(line_num, 'forbidden_features', 'string', 'matches')

            # Check Arrays asList
            if check_arrays_as_list(line):
                add_error(line_num, 'forbidden_features', 'arrays', 'asList')

            # Check Arrays copyOf
            if check_arrays_copy_of(line):
                add_error(line_num, 'forbidden_features', 'arrays', 'copyOf')

            # Check Arrays copyOfRange
            if check_arrays_copy_of_range(line):
                add_error(line_num, 'forbidden_features',
                          'arrays', 'copyOfRange')

            # Check Arrays sort
            if check_arrays_sort(line):
                add_error(line_num, 'forbidden_features', 'arrays', 'sort')

            # Check Collections copy
            if check_collections_copy(line):
                add_error(line_num, 'forbidden_features',
                          'collections', 'copy')

            # Check Collections Sort
            if check_collections_copy(line):
                add_error(line_num, 'forbidden_features',
                          'collections', 'sort')

            # Check Multiple Statements
            if check_multiple_statements(line):
                add_error(line_num, 'multiple_statements_per_line')

            # Check Printing Problems
            if check_blank_printlns(line):
                add_error(line_num, 'printing_problems', 'blank')

            if check_backslash_n(line):
                add_error(line_num, 'printing_problems', 'backslash_n')

            # HOMEWORK SPECIFIC TESTS
            if file == 'Song.java':
                song_tests(line, line_num)
            elif file == 'SpaceNeedle.java':
                space_needle_tests(line, line_num)
            elif file == 'CafeWall.java':
                global for_count
                for_count += cafe_wall_tests(line, line_num, 0)
                if num == len(file_list) - 1 and for_count < 2:
                    add_error(line_num, 'redundancy', 'missing_for')
            elif file == 'Budgeter.java':
                global return_count
                return_count += budgeter_tests(line, line_num, 0)
                # if num == len(file_list) - 1 and return_count < 4:
                #    add_error(line_num, 'returns')
            elif file == 'GuessingGame.java':
                global while_count
                while_count += guess_tests(line, line_num, 0)
                # if num == len(file_list) - 1 and while_count < 2:
                #    add_error(line_num, 'redundancy', 'missing_while')
            elif file == 'MadLibs.java':
                while_count += madlibs_tests(line, line_num, 0)
                if num == len(file_list) - 1 and while_count < 2:
                    add_error(line_num, 'redundancy', 'missing_while')
            elif file == 'Personality.java':
                for_count += personality_tests(line, line_num, 0)
                if num == len(file_list) - 1 and for_count < 3:
                    add_error(line_num, 'redundancy', 'missing_for')
            elif file == 'Ant.java':
                ant_tests(line, line_num)
            elif file == 'Bird.java':
                bird_tests(line, line_num)
            elif file == 'Hippo.java':
                hippo_tests(line, line_num)
            elif file == 'Vulture.java':
                vulture_tests(line, line_num)

            # Helper files
            if file == 'AsciiArt.java':
                global f_count
                global m_count
                x, y = ascii_tests(line, line_num, 0, 0)
                f_count += x
                m_count += y
                if num == len(file_list) - 1 and f_count < 1 and m_count < 1:
                    add_error(line_num, 'ascii_art')


def print_errors():
    if len(state['errors_by_type'].keys()) == 0:
        print('Passed!')
        return

    print('Code Quality Issues:')
    forbidden = []
    for key, value in state['errors_by_type'].items():
        if key != 'forbidden_features':
            print(key + ': ')
            for v in value:
                print('\tLine ' + str(v['line']) +
                      ': ' + v['annotation']['title'])
        else:
            forbidden = value
    print('\nForbidden Features:')
    for v in forbidden:
        print('\tLine ' + str(v['line']) +
              ': ' + v['annotation']['title'])


def add_error(line_num, category, sub_category=None, sub_sub_category=None):
    if category not in state['errors_by_type'].keys():
        state['errors_by_type'][category] = []

    error = {
        'line': line_num,
        'code': state['line_errors'][line_num - 1]['code']
    }

    if sub_category is not None:
        if sub_sub_category is not None:
            error['annotation'] = style[category][sub_category][sub_sub_category]
            state['line_errors'][line_num -
                                 1]['errors'].append(style[category][sub_category][sub_sub_category])
        else:
            error['annotation'] = style[category][sub_category]
            state['line_errors'][line_num -
                                 1]['errors'].append(style[category][sub_category])
    else:
        error['annotation'] = style[category]
        state['line_errors'][line_num -
                             1]['errors'].append(style[category])

    state['errors_by_type'][category].append(error)


def song_tests(line: str, line_num: int):
    """
    Specific tests for Song.java (redundancy, advanced material)
    """
    if check_perhaps_redundancy(line):
        global perhaps_redundancy_count
        perhaps_redundancy_count += 1
        if (perhaps_redundancy_count > 1):
            add_error(line_num, 'redundancy', 'perhaps_redundancy')

    if check_for_while_if(line):
        add_error(line_num, 'forbidden_features', 'song', 'for_while_if')


def ascii_tests(line: str, line_num: int, for_count: int, method_count: int):
    if check_for_loop(line):
        for_count += 1

    if check_method(line):
        method_count += 1

    return for_count, method_count


def space_needle_tests(line: str, line_num: int):
    """
    Specific tests for SpaceNeedle.java (redundancy, advanced material)
    """
    if check_while_if(line):
        add_error(line_num, 'forbidden_features', 'space_needle', 'while_if')


def cafe_wall_tests(line: str, line_num: int, for_count: int):
    """
    Specific tests for CafeWall.java
    """
    # TODO: Fix this
    # if in_main and check_variables_main(line):
    #     add_error(line_num, 'printlns_main')

    if check_for_loop(line):
        for_count += 1

    return for_count


def budgeter_tests(line: str, line_num: int, return_count: int):
    """
    Specific tests for Budgeter.java
    """
    # TODO: Fix this
    # if in_main and check_variables_main(line):
    #     add_error(line_num, 'printlns_main')
    global next_count

    if check_returns(line):
        return_count += 1

    # if check_next_redundancy(line):
        #next_count += 1
        # if next_count > 1:
        # add_error(line_num, 'redundancy', 'next_redundancy')

    return return_count


def guess_tests(line: str, line_num: int, while_count: int):
    """
    Specific tests for Guess.java
    """
    global double_count
    global right_count
    global lower_higher_count
    global guess_count

    if check_while_loop(line):
        while_count += 1

    if check_double_count(line):
        double_count += 1
        # if double_count > 2:
        #   add_error(line_num, 'casting', 'overuse_double')

    if check_right_redundancy(line):
        right_count += 1
        if right_count > 2:
            pass
            # add_error(line_num, 'redundancy', 'right_redundancy')

    if check_lower_higher_redundancy(line):
        lower_higher_count += 1
        if lower_higher_count > 2:
            pass
            # add_error(line_num, "redundancy", "lower_higher")

    if check_your_guess(line):
        guess_count += 1
        if guess_count > 2:
            pass
            # add_error(line_num, "redundancy", "guess_count")

    return while_count


def madlibs_tests(line: str, line_num: int, while_count: int):
    """
    Specific tests for MadLibs.java
    """
    global right_count
    global double_count

    if check_while_loop(line):
        while_count += 1

    if check_double_count(line):
        double_count += 1
        if double_count > 2:
            add_error(line_num, 'casting', 'overuse_double')

    if check_right_redundancy(line):
        right_count += 1
        if right_count > 2:
            add_error(line_num, 'redundancy', 'right_redundancy')

    return while_count


def personality_tests(line: str, line_num: int, for_count: int):
    """
    Specific tests for Personality.java
    """
    if arrays_34(line):
        add_error(line_num, 'redundancy', 'size_4_arrays')

    if for_34(line):
        add_error(line_num, 'redundancy', 'size_4_for')

    if check_for_loop(line):
        for_count += 1

    if arrays_8(line):
        add_error(line_num, 'redundancy', 'size_8_arrays')

    if check_two_dimensional_arrays(line):
        add_error(line_num, 'redundancy', 'two_dimensional_arrays')

    return for_count


def ant_tests(line: str, line_num: int):
    """
    Specific tests for Ant.java
    """
    global move_count
    if check_static(line):
        add_error(line_num, 'static_members')

    if check_direction(line):
        move_count += 1
        if move_count > 3:
            add_error(line_num,  'redundancy', 'move_count')


def bird_tests(line: str, line_num: int):
    """
    Specific tests for Bird.java
    """
    global move_count
    if check_static(line):
        add_error(line_num, 'static_members')

    if check_direction(line):
        move_count += 1
        if move_count > 4:
            add_error(line_num,  'redundancy', 'move_count')


def hippo_tests(line: str, line_num: int):
    """
    Specific tests for Hippo.java
    """
    if check_static(line):
        add_error(line_num, 'static_members')


def vulture_tests(line: str, line_num: int):
    """
    Specific tests for Hippo.java
    """
    global move_count
    if check_static(line):
        add_error(line_num, 'static_members')

    if check_attack(line):
        move_count += 1
        if move_count > 2:
            add_error(line_num,  'redundancy', 'move_count')


def blank(line):
    """
    Checks if a line is blank
    """
    if not line.strip() or '}' in line:
        return False
    return True


def check_attack(line):
    """
    Checking for return Direction
    """
    pattern = 'return[\s]+Attack'
    return re.search(pattern, line)


def check_direction(line):
    """
    Checking for return Direction
    """
    pattern = 'return[\s]+Direction'
    return re.search(pattern, line)


def check_static(line: str):
    """
    Checking for static members
    """
    pattern = 'static'
    return re.search(pattern, line)


def check_two_dimensional_arrays(line: str):
    """
    Checking for two dimensional arrays
    """
    pattern = 'new[\s]+(int|String|double|char)[\s]+.*\[.*\][\s]*\[.*\]'
    return re.search(pattern, line)


def arrays_8(line: str):
    """
    Checking for arrays with size 8
    """
    pattern = 'new[\s]+(int|String|double|char)[\s]+.*\[8\]'
    return re.search(pattern, line)


def arrays_34(line: str):
    """
    Checking for arrays with size 4
    """
    pattern = 'new[\s]+(int|String|double|char)[\s]+.*\[4\]'
    return re.search(pattern, line)


def for_34(line: str):
    """
    Checking for arrays with size 4
    """
    pattern = 'for[\s]*.*<[\s]*(3|4).*'
    return re.search(pattern, line)


def arrays_34(line: str):
    """
    Checking for arrays with size 4
    """
    pattern = 'new[\s]+(int|String|double|char)[\s]+.*\[4\]'
    return re.search(pattern, line)


def check_double_count(line: str):
    """
    Checking for number of variables of type double
    """
    pattern = 'double.*='
    return re.search(pattern, line)


def check_right_redundancy(line: str):
    """
    Checking for number of times 'got it right in' is printed
    """
    pattern = 'got it right in'
    return re.search(pattern, line)


def check_your_guess(line: str):
    """
    Checking for number of times '[y]our guess' is printed
    """
    pattern = 'our guess'
    return re.search(pattern, line)


def check_lower_higher_redundancy(line: str):
    """
    Checking for number of times 'lower|higher' is printed
    """
    pattern = "It's (lower|higher)"
    return re.search(pattern, line)


def check_variables_main(line: str):
    """
    Checking for println statements in main
    """
    pattern = 'System.out.println|System.out.print'
    return re.search(pattern, line)


def check_returns(line: str):
    """
    Counting returns
    """
    pattern = 'return[\s]*.*;'
    return re.search(pattern, line)


def check_bad_variable_names(line: str):
    """
    Checking for bad variable names
    """
    c = find_variables(line)
    if c is not None and len(c) < 2 and (c != 'g' and c != 'x' and c != 'y' and c != 'p' and c != 'i' and c != 'j' and c != 'k' and c != 'r' and c != 'f'):
        return False
    return True


def find_variables(line: str):
    """
    Finds variables
    """
    def getChar(c):
        split = re.split('[\s\t[\]]+', line)
        for i, w in enumerate(split):
            if w == c:
                return split[i + 1]

    line = line.strip()
    if 'int' in line:
        return getChar('int')
    elif 'double' in line:
        return getChar('double')
    elif 'boolean' in line:
        return getChar('boolean')
    elif 'Scanner' in line:
        return getChar('Scanner')
    elif 'Random' in line:
        return getChar('Random')
    elif 'String' in line:
        return getChar('String')


def check_for_loop(line: str):
    """
    Counting for loops
    """
    pattern = 'for\s*\([^;]*?;[^;]*?;[^)]*?\)'
    return re.search(pattern, line)


def check_while_loop(line: str):
    """
    Counting while loops
    """
    pattern = 'while *\(.*\)'
    return re.search(pattern, line)


def check_next_redundancy(line: str):
    """
    Counting next redundancy
    """
    pattern = 'Next.*amount'
    return re.search(pattern, line)


def check_perhaps_redundancy(line: str):
    """
    Checks if 'perhaps she'll die' is printed twice
    """
    pattern = "Perhaps she'll die.*\).*;"
    return re.search(pattern, line)


def check_for_while_if(line: str):
    """
    Checks if for, while or if statements used
    """
    pattern = 'for\s*\([^;]*?;[^;]*?;[^)]*?\)|while *\(.*\)|if *\(.*\)'
    return re.search(pattern, line)


def check_while_if(line: str):
    """
    Checks if while or if statements used
    """
    pattern = 'while *\(.*\)|if *\(.*\)'
    return re.search(pattern, line)


def check_length(line: str):
    """
    Checks if a line is longer than max_line_length (100 character)
    """
    return len(line) > max_line_length


def check_indentation(line: str, indent_level: int, size: int, line_num: int, file_list):
    """
    Checks indentation of each line
    """

    # Removes extra whitespaces and adds correct whitespace
    if line_num > 0 and (';' not in file_list[line_num - 2]) and ('{' not in file_list[line_num - 2]):
        return 0

    correct_spaces = ' ' * (indent_level * size) + line.strip()
    correct_tab = '\t' * indent_level + line.strip()
    while (line[len(line) - 1] == ' '):
        line = line[: len(line) - 1]

    if (len(correct_spaces) > len(line) and len(correct_tab) > len(line)):
        return 2
    elif (len(correct_spaces) < len(line) and len(correct_tab) < len(line)):
        return 1
    else:
        return 0


def check_private_fields(line: str):
    """
    Checks for the existence of private fields (global variables)
    """
    if 'final' not in line:
        if ';' in line:
            if not line.strip().startswith('private'):
                return False
    return True


def check_boolean_zen_true(line: str):
    """
    Checks boolean zen for true case
    """
    return re.search(boolean_true, line)


def check_boolean_zen_false(line: str):
    """
    Checks boolean zen for false case
    """
    return re.search(boolean_false, line)


def check_screaming_case(line: str):
    """
    Check constant naming conventions
    """
    split = re.split('[\s\t[\]]+', line)
    if 'final' in line and '=' in line:
        name = split[split.index('final') + 2]
        return name != name.upper()
    return False


def check_pascal_case(line: str):
    """
    Check class naming conventions
    """
    split = re.split('[\s\t[\])]+', line)
    if split[0] == '':
        split = split[1:]
    if 'class ' in line:
        if 'public' in line or 'private' in line or 'protected' in line:
            if 'final' in line:
                name = split[3]
            else:
                name = split[2]
        else:
            if 'final' in line:
                name = split[2]
            else:
                name = split[1]

        return (name == name.upper() and len(name) > 1) or name[0].upper() != name[0] or '_' in name

    return False


def check_camel_case(line: str):
    """
    Check variable naming conventions
    """
    line = line.strip()
    split = re.split('[\s\t[\]()]+', line)
    # TODO: Check len(name) > 1!
    if 'final' not in line and 'class' not in line:
        if len(split) == 2 and 'return' not in line and split[0] != '++' and split[1] != '++' and ';' in split[1]:
            name = split[1]
            return (name == name.upper() and len(name) > 1) or name[0].lower() != name[0] or "_" in name
        elif '=' in split and split.index('=') > 1:
            name = split[split.index('=') - 1]
            return (name == name.upper() and len(name) > 1) or name[0].lower() != name[0] or "_" in name
        elif 'public' in line or 'private' in line or 'protected' in line:
            if 'static' in line:
                name = split[3]
            else:
                name = split[2]
            return (name == name.upper() and len(name) > 1) or name[0].lower() != name[0] or "_" in name
    return False


def check_break(line: str):
    """
    Check break
    """
    return re.search('break[\s]*;', line)


def check_continue(line: str):
    """
    Check continue
    """
    return re.search('continue[\s]*;', line)


def check_try_catch(line: str):
    """
    Check try/catch
    """
    return re.search('catch[\s]*{', line)


def check_var(line: str):
    """
    Check var
    """
    return re.search('^[ \t]*var', line)


def check_to_array(line: str):
    """
    Check toArray
    """
    return '.toArray' in line


def check_string_builder(line: str):
    """
    Check String Builder
    """
    return 'StringBuilder' in line


def check_string_buffer(line: str):
    """
    Check String Buffer
    """
    return 'StringBuffer' in line


def check_string_joiner(line: str):
    """
    Check String Joiner
    """
    return 'StringJoiner' in line


def check_string_tokenizer(line: str):
    """
    Check String Tokenizer
    """
    return 'StringTokenizer' in line


def check_string_char_array(line: str):
    """
    Check String toCharArray
    """
    return '.toCharArray' in line


def check_string_join(line: str):
    """
    Check String join
    """
    return '.join' in line


def check_string_matches(line: str):
    """
    Check String matches
    """
    return '.matches' in line


def check_arrays_as_list(line: str):
    """
    Check Arrays asList
    """
    return 'Arrays.asList' in line


def check_arrays_copy_of(line: str):
    """
    Check Arrays copyOf
    """
    return 'Arrays.copyOf' in line


def check_arrays_copy_of_range(line: str):
    """
    Check Arrays copyOfRange
    """
    return 'Arrays.copyOfRange' in line


def check_arrays_sort(line: str):
    """
    Check Arrays Sort
    """
    return 'Arrays.sort' in line


def check_collections_copy(line: str):
    """
    Check Collections Copy
    """
    return 'Collections.copy' in line


def check_collections_sort(line: str):
    """
    Check Collections Sort
    """
    return 'Collections.sort' in line


def check_multiple_statements(line: str):
    """
    Check Multiple Statements per line
    """
    return len(line.split(';')) > 2 and 'for' not in line


def check_blank_printlns(line: str):
    """
    Check Blank Println statements
    """
    return re.search(empty_printlns, line)


def check_backslash_n(line: str):
    """
    Check \n characters
    """
    return '\\n' in line and 'printf' not in line


def check_method(line: str):
    """
    Checks if a line starts a method
    """
    check = 'void' in line or 'int' in line or 'String' in line or 'boolean' in line
    return 'public' in line and 'static' in line and check


if __name__ == '__main__':
    main()
