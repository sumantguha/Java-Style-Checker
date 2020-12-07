style = {
    "indentation": {
        "either": {
            "title": "This line is indented incorrectly",
            "message": "This line is indented incorrectly. You should indent your program one tab further every time you open a curly brace and indent one tab less every time you close a curly brace. This line should be indented more."
        }
    },
    "Long Lines": {
        "type": "Long Lines",
        "title": "This line is too long (over 100 characters)",
        "message": "Lines of code should ideally max out at 80 characters, and should never exceed 100 characters in length. Lines that are too long should be broken up and wrapped to the next line."
    },
    "naming_conventions": {
        "screaming": {
            "type": "naming_conventions",
            "title": "This name has the wrong naming conventions (should be SCREAMING_CASED)",
            "message": "Constant names should be SCREAMING_CASED, in all uppercase letters with words separated by underscores."
        },
        "pascal": {
            "type": "naming_conventions",
            "title": "This name has the wrong naming conventions (should be PascalCased)",
            "message": "Class names should be PascalCased, a subset of camel casing where the first letter of every word is uppercased."
        },
        "camel": {
            "type": "naming_conventions",
            "title": "This name has the wrong naming conventions (should be camelCased)",
            "message": "Method & variable names should be camelCased, a convention where the first letter of every word after the first is uppercased (you can ignore this message if this is a constructor)."
        },
        "bad_variable_names": {
            "type": "naming_conventions",
            "title": "This name follows bad naming practices",
            "message": "Method and variable names should generally be longer than 3 characters and describe what the variable/method does"
        }
    },
    "empty_struct": {
        "title": "There's no need for this structure",
        "message": "This structure seems to be empty, and therefore you don't need it in your code. You should remove it."
    },
    "boolean_zen": {
        "equals_true": {
            "type": "boolean_zen",
            "title": "You should never test booleans for equality",
            "message": "rather than testing if a boolean x is equal to true, you should just use x itself as a condition"
        },
        "equals_false": {
            "type": "boolean_zen",
            "title": "You should never test booleans for equality",
            "message": "rather than testing if a boolean x is equal to false, you should just use !x itself as a condition"
        }
    },
    "scanners": {
        "title": "There should be one Scanner per source",
        "message": "It's best practice to only have one Scanner hooked up to console input, and pass that Scanner around to anywhere that needs it."
    },
    "random": {
        "title": "There should be one Random per file",
        "message": "It's best practice to only have one Random object created, and pass that Random around to anywhere that needs it."
    },
    "returns": {
        "title": "You should use returns to send values back",
        "message": "It's best practice to use returns in order to avoid chaining"
    },
    "private_fields": {
        "title": "Fields should be private",
        "message": "The fields of your objects should always be declared private. This ensures that no client of your object will be able to directly change the state of your object in a way that you haven’t allowed them to."
    },

    "casting": {
        "overuse_double": {
            "type": "casting",
            "title": "(Probably) more double variables than necessary",
            "message": "Since we are counting quantities, these variables should be of a type integer. Cast your output before performining arithmetic operations"
        }
    },
    "ascii_art": {
        "title": "You are missing both a for loop and a static method",
        "message": "According to our requirements, you should have at least one static method or one for loop"
    },
    "blank_lines": {
        "title": "You should have blank lines between methods",
        "message": "Blank lines help improve readability and structure"
    },
    "forbidden_features": {
        "break": {
            "type": "forbidden_features",
            "title": "break is a forbidden feature.",
            "message": "break is a forbidden feature. You are not allowed to use it in CSE 14X."
        },
        "continue": {
            "type": "forbidden_features",
            "title": "continue is a forbidden feature.",
            "message": "continue is a forbidden feature. You are not allowed to use it in CSE 14X."
        },
        "try/catch": {
            "type": "forbidden_features",
            "title": "try/catch is a forbidden feature.",
            "message": "try/catch is a forbidden feature. You are not allowed to use it in CSE 14X."
        },
        "var": {
            "type": "forbidden_features",
            "title": "var is a forbidden feature.",
            "message": "var is a forbidden feature. You are not allowed to use it in CSE 14X."
        },
        "toArray": {
            "type": "forbidden_features",
            "title": "toArray is a forbidden feature.",
            "message": "toArray is a forbidden feature. You are not allowed to use it in CSE 14X."
        },
        "string": {
            "builder": {
                "type": "forbidden_features",
                "title": "StringBuilder is a forbidden feature.",
                "message": "StringBuilder is a forbidden feature. You are not allowed to use it in CSE 14X."
            },
            "buffer": {
                "type": "forbidden_features",
                "title": "StringBuffer is a forbidden feature.",
                "message": "StringBuffer is a forbidden feature. You are not allowed to use it in CSE 14X."
            },
            "joiner": {
                "type": "forbidden_features",
                "title": "StringJoiner is a forbidden feature.",
                "message": "StringJoiner is a forbidden feature. You are not allowed to use it in CSE 14X."
            },
            "tokenizer": {
                "type": "forbidden_features",
                "title": "StringTokenizer is a forbidden feature.",
                "message": "StringTokenizer is a forbidden feature. You are not allowed to use it in CSE 14X."
            },
            "charArray": {
                "type": "forbidden_features",
                "title": "String.toCharArray() is a forbidden feature.",
                "message": "String.toCharArray() is a forbidden feature. You are not allowed to use it in CSE 14X."
            },
            "join": {
                "type": "forbidden_features",
                "title": "String.join() is a forbidden feature.",
                "message": "String.join() is a forbidden feature. You are not allowed to use it in CSE 14X."
            },
            "matches": {
                "type": "forbidden_features",
                "title": "String.matches() is a forbidden feature.",
                "message": "String.matches() is a forbidden feature. You are not allowed to use it in CSE 14X."
            }
        },
        "arrays": {
            "asList": {
                "type": "forbidden_features",
                "title": "Arrays.asList() is a forbidden feature.",
                "message": "Arrays.asList() is a forbidden feature. You are not allowed to use it in CSE 14X."
            },
            "copyOf": {
                "type": "forbidden_features",
                "title": "Arrays.copyOf() is a forbidden feature.",
                "message": "Arrays.copyOf() is a forbidden feature. You are not allowed to use it in CSE 14X."
            },
            "copyOfRange": {
                "type": "forbidden_features",
                "title": "Arrays.copyOfRange() is a forbidden feature.",
                "message": "Arrays.copyOfRange() is a forbidden feature. You are not allowed to use it in CSE 14X."
            },
            "sort": {
                "type": "forbidden_features",
                "title": "Arrays.sort() is a forbidden feature.",
                "message": "Arrays.sort() is a forbidden feature. You are not allowed to use it in CSE 14X."
            }
        },
        "collections": {
            "copy": {
                "type": "forbidden_features",
                "title": "Collections.copy() is a forbidden feature.",
                "message": "Collections.copy() is a forbidden feature. You are not allowed to use it in CSE 14X."
            },
            "sort": {
                "type": "forbidden_features",
                "title": "Collections.sort() is a forbidden feature.",
                "message": "Collections.sort() is a forbidden feature. You are not allowed to use it in CSE 14X."
            }
        },
        "song": {
            "for_while_if": {
                "type": "forbidden_features",
                "title": "Using for/while loops or if statements",
                "message": "You are using advanced material for this homework"
            }
        },
        "space_needle": {
            "while_if": {
                "type": "forbidden_features",
                "title": "Using while loops or if statements",
                "message": "You are using advanced material for this homework"
            }
        }
    },
    "multiple_statements_per_line": {
        "title": "There is more than one statement on this line",
        "message": "You should limit your code to one statement per line."
    },
    "printing_problems": {
        "backslash_n": {
            "type": "printing_problems",
            "title": "\\n should only be used in printf.",
            "message": "\\n should only be used in printf statements, and only once at the end of the line. Otherwise, you should just use println if you want to print a full line."
        },
        "blank": {
            "type": "printing_problems",
            "title": "A blank println should actually be blank",
            "message": "You should always print a blank line using System.out.println(). Printing an empty String (System.out.println(\"\")) is considered bad style; it makes the intention less clear."
        }
    },
    "redundancy": {
        "perhaps_redundancy": {
            "type": "redundancy",
            "title": "Repeated perhaps she'll die more than once",
            "message": "You should be using the nested doll structure!"
        },
        "missing_for": {
            "type": "redundancy",
            "title": "(Possibly) redundant code blocks",
            "message": "(Possibly redundant) You should be putting all your repetitive code in for loops"
        },
        "next_redundancy": {
            "type": "redundancy",
            "title": "Repeated Next Amount more than once",
            "message": "You should put all repetitive features inside a for loop"
        },
        "missing_while": {
            "type": "redundancy",
            "title": "(Possibly) redundant code blocks",
            "message": "(Possibly redundant) You should be putting all your repetitive code in while loops"
        },
        "right_redundancy": {
            "type": "redundancy",
            "title": "Repeated \" You got it right in \" more than 2 times",
            "message": "You should be printing this line only twice at max!"
        },
        "lower_higher": {
            "type": "redundancy",
            "title": "Repeated \" It's Lower|Higher \" more than 2 times",
            "message": "You should be printing this line only twice at max!"
        },
        "guess_count": {
            "type": "redundancy",
            "title": "Repeated \" Your guess \" more than 2 times",
            "message": "You should be printing this line only twice at max!"
        },
        "size_4_arrays": {
            "type": "redundancy",
            "title": "Arrays declared with size 4",
            "message": "You should be using the class constant while declaring arrays of this size"
        },
        "size_4_for": {
            "type": "redundancy",
            "title": "For loops declared with size 4",
            "message": "You should be using the class constant while declaring for loops of this size"
        },
        "size_8_arrays": {
            "type": "redundancy",
            "title": "Arrays declared with size 8",
            "message": "You should not declare arrays of size 8 and instead use two arrays of size 4"
        },
        "two_dimensional_arrays": {
            "type": "redundancy",
            "title": "Two Dimensional Arrays declared",
            "message": "You should not declare two dimensional arrays"
        },
        "move_count": {
            "type": "redundancy",
            "title": "Redundant getMove() code",
            "message": "(Possibly) have too many if/else branches in getMove()"
        }
    },
    "printlns_main": {
        "title": "Printlns in main",
        "message": "Your main should not have any println statements or logic"
    },
    "static_members": {
        "title": "Static members",
        "message": "(Possibly) bad to have static members in class"
    }
}
