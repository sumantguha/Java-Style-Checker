#!/usr/bin/env python3
"""Java Style Checker (CSE 142)

Code quality linter for Java, specifically designed for CSE 142 @ UW, Seattle
Usage: (Supports python 3.x)

Run script with ```python3 style_checker.py <PATH_TO_JAVA_FILE>``` to view
console output with list of code quality errors. 
Refer to https://courses.cs.washington.edu/courses/cse142/20au/quality.html
for a comprehensive list of features

author: Omar, Sumant
email: oibra@uw.edu, guhas2@uw.edu
"""
import re
import sys
