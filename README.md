# Java-Style-Checker

## Usage (Python)

This project uses Python 3.x. It uses a single python script along with a stylesheet to track errors and display them.

Assuming you have python 3.x installed in your system and `style.json` in the same directory as `style_checker.py`, you can run the checker by running the following command:

```shell
python style_checker_grading.py [PATH_TO_JAVA_FILE]
```

For example, suppose you wanted to run the checker against a student's `GuessingGame.java` implementation which is located in the parent directory, you would run

```shell
python style_checker_grading.py GuessingGame.java
```

There are a set of specific tests for the 8 current take home 142 assessments (they run automatically based on file name)
