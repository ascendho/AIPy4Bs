import os
import re
import time
from dlai_grader.grading import test_case
from dlai_grader.io import read_notebook
from dlai_grader.notebook import get_named_cells
from IPython.display import display, Javascript


def print_feedback(test_cases):
    failed_cases = [t for t in test_cases if t.failed]
    feedback_msg = "\033[92m All tests passed!"

    if failed_cases:
        feedback_msg = ""
        for failed_case in failed_cases:
            feedback_msg += f"\033[91mFailed test case: {failed_case.msg}.\nGrader expected: {failed_case.want}\nYou got: {failed_case.got}\n\n"

    print(feedback_msg)


# +
def autosave():
    display(Javascript("IPython.notebook.save_checkpoint();"))
    
def remove_comments(code):
    # This regex pattern matches comments in the code
    pattern = r'#.*'
    
    # Use re.sub() to replace comments with an empty string
    code_without_comments = re.sub(pattern, '', code)
    
    # Split the code into lines, strip each line, and filter out empty lines
    lines = code_without_comments.splitlines()
    non_empty_lines = [line.rstrip() for line in lines if line.strip()]
    
    # Join the non-empty lines back into a single string
    return '\n'.join(non_empty_lines)

def check_import_statements(code_string):
    # Split the input string into individual lines
    lines = code_string.split('\n')
    
    # Initialize a list to store import statements
    import_lines = []
    
    # Iterate through each line to check for import statements
    for line in lines:
        # Strip leading and trailing whitespace from the line
        stripped_line = line.strip()
        
        # Check if the line starts with "import"
        if stripped_line.startswith('import'):
            # Split the line by commas to handle multiple imports
            imports = stripped_line.split(',')
            for imp in imports:
                # Strip leading and trailing whitespace from each import
                imp = imp.strip()
                # Check if the import statement is valid
                if imp.startswith('import'):
                    import_lines.append(imp)
                else:
                    # Handle the case where the line starts with 'import' but subsequent parts do not
                    import_lines.append(f'import {imp}')
    
    # Check if any import statements were found
    if import_lines:
        return True, import_lines
    else:
        return False, None


# -

def exercise_1a(
    book_title: str, author: str, year_published: int, available_copies: int
):
    def g():
        cases = []

        assignment_name = "C1M1_Assignment.ipynb"
        autosave()  # Save the notebook
        time.sleep(3)  # Wait for 3 seconds

        nb = read_notebook(assignment_name)  # Read the notebook
        cells = get_named_cells(nb)  # Get cells with names
        source = cells["exercise_1a"]["source"]  # Get source code of the cell
        
        # Remove comments from code
        student_code_without_comments = remove_comments(source)
        
        ############## Test to check import statements ##############
        
        # Check for import statements
        has_imports, import_lines = check_import_statements(student_code_without_comments)
        
        t = test_case()
        if has_imports:
            t.failed = True
            t.msg = "Import statements are not allowed within your solution code. Please remove them from your code"
            t.want = "No import statements"
            t.got = f"Import statement(s) found: {', '.join(import_lines)}"
        cases.append(t)
        #######################################
        
        
        ############## Test to check variable assignments ###########
        
        # Check for variable assignments
        # Extract variable assignments using regex
        variable_pattern = r"\b(\w+)\s*="
        assigned_variables = re.findall(variable_pattern, student_code_without_comments)

        # Define the allowed variables
        allowed_variables = {"book_title", "author", "year_published", "available_copies"}

        # Track checked variables to avoid duplicate error messages
        checked_variables = set()

        ###
        for var in assigned_variables:
            if var not in checked_variables:
                t = test_case()
                if var not in allowed_variables:
                    t.failed = True
                    t.msg = f"Unexpected variable '{var}' found. Please remove it."
                    t.want = (
                        f"Only variables {', '.join(allowed_variables)} should be initialized."
                    )
                    t.got = f"Variable '{var}' initialized."
                    cases.append(t)
                elif assigned_variables.count(var) > 1:
                    t.failed = True
                    t.msg = (
                        f"Variable '{var}' is being overridden. Please ensure it is initialized only once."
                    )
                    t.want = f"Variable '{var}' should be initialized once."
                    t.got = f"Variable '{var}' initialized multiple times."
                    cases.append(t)
                checked_variables.add(var)
        #######################################

        ############## Test to check book_title value ##############
        t = test_case()
        if book_title != "Brave New World":
            t.failed = True
            t.msg = "Please make sure the name of the book is Brave New World and it is being stored as a string, and that you are using uppercase and lowercase letters where needed. Also, check for typos"
            t.want = "Brave New World"
            t.got = book_title
        cases.append(t)
        #######################################

        ############## Test to check author value ##############
        t = test_case()
        if author != "Aldous Huxley":
            t.failed = True
            t.msg = "Please make sure the name of the author is Aldous Huxley and it is being stored as a string, and that you are using uppercase and lowercase letters where needed Also, check for typos"
            t.want = "Aldous Huxley"
            t.got = author
        cases.append(t)
        #######################################

        ############## Test to check year_published value ##############
        t = test_case()
        if year_published != 1932:
            t.failed = True
            t.msg = "Please make sure year_published is 1932 and it is being stored as an integer."
            t.want = 1932
            t.got = year_published
        cases.append(t)
        #######################################

        ############## Test to check available_copies value ##############
        t = test_case()
        if available_copies != 4:
            t.failed = True
            t.msg = "Please make sure available_copies is 4 it is being stored as an integer."
            t.want = 4
            t.got = available_copies
        cases.append(t)
        #######################################
        
        ############## Test to check for test_your_code calls ##############
        test_your_code_pattern = r"test_your_code\..*"
        test_your_code_matches = re.findall(test_your_code_pattern, student_code_without_comments)

        if test_your_code_matches:
            t = test_case()
            t.failed = True
            t.msg = f"Found usage of \"test_your_code.\" in your implemented code. Please remove it from your code ({', '.join(set(test_your_code_matches))}) . Use the test function as provided in the next cell"
            t.want = "No usage of \"test_your_code.\" in your implemented code"
            t.got = f"Usage of \"test_your_code.\" found: {', '.join(set(test_your_code_matches))}"
            cases.append(t)
        #######################################

        return cases

    cases = g()
    print_feedback(cases)


def exercise_1b():
    def g():
        cases = []

        assignment_name = "C1M1_Assignment.ipynb"
        autosave()  # Save the notebook
        time.sleep(3)  # Wait for 3 seconds

        nb = read_notebook(assignment_name)  # Read the notebook
        cells = get_named_cells(nb)  # Get cells with names
        source = cells["exercise_1b"]["source"]  # Get source code of the cell
        out = cells["exercise_1b"]["outputs"]  # Get outputs of the cell
        
        # Remove comments from code
        student_code_without_comments = remove_comments(source)
        
        ############## Test to check import statements ##############
        
        # Check for import statements
        has_imports, import_lines = check_import_statements(student_code_without_comments)
        
        t = test_case()
        if has_imports:
            t.failed = True
            t.msg = "Import statements are not allowed within your solution code. Please remove them from your code"
            t.want = "No import statements"
            t.got = f"Import statement(s) found: {', '.join(import_lines)}"
        cases.append(t)
        #######################################

        ############## Test to check for cell output ##############
        t = test_case()
        if not out:
            t.failed = True
            t.msg = "There was no output for exercise 1b cell, check that you run it"
            t.want = "An output generated from print statements"
            t.got = None
            return [t]  # Return early if no output
        cases.append(t)
        #######################################

        ############## Test to check for variable initializations ##############
        
        # Check for variable initializations
        variable_init_pattern = r"\b\w+\s*="
        # Find variable initializations
        variable_inits = re.findall(variable_init_pattern, student_code_without_comments)  

        t = test_case()
        if variable_inits:
            t.failed = True
            t.msg = "Variable initialization detected in the code. Please remove any variable assignments and use only print statements."
            t.want = "No variable initializations"
            t.got = f"Variable initialization(s) found: {', '.join(variable_inits)}"
        cases.append(t)
        #######################################
        
        
        ############## Test to check for the correct number of f-string print statements ##############
        
        # Check for the correct number of f-string print statements
        pattern = r'print\(\s*f["\']'
        matches = re.findall(pattern, source)  # Find f-string print statements

        t = test_case()
        if len(matches) != 4:
            t.failed = True
            t.msg = "Detected incorrect number of valid print statements with f-strings"
            t.want = 4
            t.got = len(matches)
        cases.append(t)
        #######################################

        
        ############## Test to check for title output ###########
        
        std_out = out[0]["text"]  # Get the standard output

        pattern = "Title: Brave New World"
        t = test_case()
        if pattern not in std_out:
            t.failed = True
            t.msg = "Missing printed information about title"
            t.want = "Title: Brave New World"
            t.got = "Missing or incorrect message for title. Please make sure you are using uppercase and lowercase letters where needed. Also, check for typos"
        cases.append(t)
        #######################################

        ############## Test to check for author output ##############
        pattern = "Author: Aldous Huxley"
        t = test_case()
        if pattern not in std_out:
            t.failed = True
            t.msg = "Missing printed information about author"
            t.want = "Author: Aldous Huxley"
            t.got = "Missing or incorrect message for author. Please make sure you are using uppercase and lowercase letters where needed. Also, check for typos"
        cases.append(t)
        #######################################

        ############## Test to check for published year output ##############
        pattern = "Published: 1932"
        t = test_case()
        if pattern not in std_out:
            t.failed = True
            t.msg = "Missing printed information about year_published"
            t.want = "Published: 1932"
            t.got = "Missing or incorrect message for year_published. Please make sure you are using uppercase and lowercase letters where needed. Also, check for typos"
        cases.append(t)
        #######################################

        ############## Test to check for available copies output ##############
        pattern = "Available Copies: 4"
        t = test_case()
        if pattern not in std_out:
            t.failed = True
            t.msg = "Missing printed information about available_copies"
            t.want = "Available Copies: 4"
            t.got = "Missing or incorrect message for available_copies. Please make sure you are using uppercase and lowercase letters where needed. Also, check for typos"
        cases.append(t)
        #######################################
        
        ############## Test to check for test_your_code calls ##############
        test_your_code_pattern = r"test_your_code\..*"
        test_your_code_matches = re.findall(test_your_code_pattern, student_code_without_comments)

        if test_your_code_matches:
            t = test_case()
            t.failed = True
            t.msg = f"Found usage of \"test_your_code.\" in your implemented code. Please remove it from your code ({', '.join(set(test_your_code_matches))}) . Use the test function as provided in the next cell"
            t.want = "No usage of \"test_your_code.\" in your implemented code"
            t.got = f"Usage of \"test_your_code.\" found: {', '.join(set(test_your_code_matches))}"
            cases.append(t)
        #######################################

        return cases

    cases = g()
    print_feedback(cases)


def exercise_2(available_copies):
    def g():
        cases = []

        assignment_name = "C1M1_Assignment.ipynb"
        autosave()  # Save the notebook
        time.sleep(3)  # Wait for 3 seconds

        nb = read_notebook(assignment_name)  # Read the notebook
        cells = get_named_cells(nb)  # Get cells with names
        source = cells["exercise_2"]["source"]  # Get source code of the cell
        out = cells["exercise_2"]["outputs"]  # Get outputs of the cell
        
        # Remove comments from code
        student_code_without_comments = remove_comments(source)
        
        
        ############## Test to check for import statements ##############
        
        # Check for import statements
        has_imports, import_lines = check_import_statements(student_code_without_comments)

        t = test_case()
        if has_imports:
            t.failed = True
            t.msg = "Import statements are not allowed within your solution code. Please remove them from your code."
            t.want = "No import statements"
            t.got = f"Import statement(s) found: {', '.join(import_lines)}"
        cases.append(t)
        #######################################
        
        ############## Test to check initialization of available_copies ##############
        
        # Check for initialization of available_copies
        init_count = len(
            re.findall(r"\bavailable_copies\s*=", student_code_without_comments)
        )  # Count initializations

        t = test_case()
        if init_count > 2:
            t.failed = True
            t.msg = "The variable 'available_copies' is initialized more than twice. Please ensure it is initialized only up to two times."
            t.want = "At most two initializations of 'available_copies'"
            t.got = f"{init_count} initializations"
        cases.append(t)
        #######################################

        
        ############## Test to check for new variables introduced ##############
        
        # Check for any new variables introduced
        variable_pattern = r"\b(\w+)\s*="
        variables = re.findall(variable_pattern, student_code_without_comments)  # Find all variables
        unique_variables = set(variables) - {"available_copies"}  # Find new variables

        t = test_case()
        if unique_variables:
            t.failed = True
            t.msg = "You have introduced new variables. Only 'available_copies' should be used."
            t.want = "No new variables"
            t.got = f"New variable(s) found: {', '.join(unique_variables)}"
        cases.append(t)
        #######################################
        
        
        ############## Test to check the number of print statements ##############
        
        # Check for the number of print statements
        print_count = len(re.findall(r"\bprint\(", student_code_without_comments))  # Count print statements

        t = test_case()
        if print_count != 1:
            t.failed = True
            t.msg = "There should be exactly one print statement in your code."
            t.want = "One print statement"
            t.got = f"{print_count} print statements"
        cases.append(t)
        #######################################
        
        ############## Test to check for multi-line f-string print statement ##############

        # Check for a multi-line f-string print statement
        pattern = r'print\(\s*f[\'"]{3}'
        
        t = test_case()
        if not re.search(pattern, source):
            t.failed = True
            t.msg = "Unable to detect a print statement with a multi-line f-string."
            t.want = "A print statement with a multi-line f-string"
            t.got = "No valid print statement with a multi-line f-string"
        cases.append(t)
        #######################################

        ############## Test to check for cell output ##############
        t = test_case()
        if not out:
            t.failed = True
            t.msg = "There was no output for exercise 2 cell, check that you run it."
            t.want = "An output generated from print statements"
            t.got = None
            return [t]  # Return early if no output
        cases.append(t)
        #######################################

        ############## Test to check if available_copies value is correct ##############
        t = test_case()
        if available_copies != 3:
            t.failed = True
            t.msg = "Incorrect value for available_copies"
            t.want = 3
            t.got = available_copies
        cases.append(t)
        #######################################
        
        ############## Test to check if the correct message is printed ##############

        # Check if the correct message is printed
        std_out = out[0]["text"]  # Get the standard output
        pattern = (
            "One copy of Brave New World checked out. There are now 3 copies available."
        )
        
        t = test_case()
        if pattern not in std_out:
            t.failed = True
            t.msg = "Missing correct printed message"
            t.want = pattern
            t.got = "An incorrect message. Please make sure you are using uppercase and lowercase letters, and adding a period/full stop (.) where needed. Also, check for typos."
        cases.append(t)
        #######################################
        
        ############## Test to check for test_your_code calls ##############
        test_your_code_pattern = r"test_your_code\..*"
        test_your_code_matches = re.findall(test_your_code_pattern, student_code_without_comments)

        if test_your_code_matches:
            t = test_case()
            t.failed = True
            t.msg = f"Found usage of \"test_your_code.\" in your implemented code. Please remove it from your code ({', '.join(set(test_your_code_matches))}) . Use the test function as provided in the next cell"
            t.want = "No usage of \"test_your_code.\" in your implemented code"
            t.got = f"Usage of \"test_your_code.\" found: {', '.join(set(test_your_code_matches))}"
            cases.append(t)
        #######################################

        return cases

    cases = g()
    print_feedback(cases)


def exercise_3(requested_book):
    def g():
        cases = []

        assignment_name = "C1M1_Assignment.ipynb"
        autosave()  # Save the notebook
        time.sleep(3)  # Wait for 3 seconds

        nb = read_notebook(assignment_name)  # Read the notebook
        cells = get_named_cells(nb)  # Get cells with names
        source = cells["exercise_3"]["source"]  # Get source code of the cell
        out = cells["exercise_3"]["outputs"]  # Get outputs of the cell
        
        # Remove comments from code
        student_code_without_comments = remove_comments(source)  

        ############## Test to check for import statements ##############
        
        has_imports, import_lines = check_import_statements(student_code_without_comments)  # Check for import statements
        
        t = test_case()
        if has_imports:
            t.failed = True
            t.msg = "Import statements are not allowed within your solution code. Please remove them from your code"
            t.want = "No import statements"
            t.got = f"Import statement(s) found: {', '.join(import_lines)}"
        cases.append(t)
        #######################################

        ############## Test to check for multi-line f-string print statement ##############
        pattern = r'print\(\s*f[\'"]{3}'  # Pattern to find multi-line f-string print
        
        t = test_case()
        if not re.search(pattern, source):
            t.failed = True
            t.msg = "Unable to detect a print statement with a multi-line f-string"
            t.want = "a print statement with a multi-line f-string"
            t.got = "no valid print statement with a multi-line f-string"
        cases.append(t)
        #######################################

        ############## Test to check for cell output ##############
        t = test_case()
        if not out:
            t.failed = True
            t.msg = "There was no output for exercise 3 cell, check that you run it"
            t.want = "An output generated from print statements"
            t.got = None
            return [t]  # Return early if no output
        cases.append(t)
        #######################################

        ############## Test to check requested_book value ##############
        t = test_case()
        if requested_book != "To Kill a Mockingbird":
            t.failed = True
            t.msg = "Incorrect value for requested_book"
            t.want = "To Kill a Mockingbird"
            t.got = (
                f"{requested_book}. Please make sure you are using uppercase and lowercase letters where needed. Also, check for typos"
            )
        cases.append(t)
        #######################################

        ############## Test to check for correct printed message ##############
        
        std_out = out[0]["text"]  # Get the standard output
        
        pattern = "To Kill a Mockingbird is currently unavailable. You can request it from the library."
        
        t = test_case()
        if pattern not in std_out:
            t.failed = True
            t.msg = "Missing correct printed message"
            t.want = pattern
            t.got = "An incorrect message. Please make sure you are using uppercase and lowercase letters, and adding a period/full stop (.) where needed. Also, check for typos"
        cases.append(t)
        #######################################

        
        ############## Test to check requested_book initialization count ##############
        
        # Checks for variable initialization and print statements
        variable_pattern = r'^\s*(\w+)\s*='
        variables = re.findall(variable_pattern, student_code_without_comments, re.MULTILINE)  # Find variable initializations
        
        requested_book_initializations = [var for var in variables if var == "requested_book"]  # Count requested_book initializations
        
        t = test_case()
        if len(requested_book_initializations) != 1:
            t.failed = True
            t.msg = "The variable 'requested_book' should be initialized exactly once."
            t.want = "One initialization of 'requested_book'"
            t.got = f"{len(requested_book_initializations)} initializations found"
        cases.append(t)
        #######################################

        ############## Test to check print statement count ##############
        print_statements = re.findall(r'\bprint\(', student_code_without_comments)  # Find print statements
        
        t = test_case()
        if len(print_statements) != 1:
            t.failed = True
            t.msg = "There should be exactly one print statement."
            t.want = "One print statement"
            t.got = f"{len(print_statements)} print statements found"
        cases.append(t)
        #######################################

        ############## Test to check for other variable initializations ##############
        
        # Filter out 'requested_book' if it's initialized exactly once
        filtered_variables = [
            var
            for var in variables
            if var != "requested_book"
            or requested_book_initializations.count(var) != 1
        ]
        t = test_case()
        if filtered_variables:
            t.failed = True
            t.msg = "No new variables other than 'requested_book' should be initialized."
            t.want = "No new variable initializations"
            t.got = f"Variables found: {', '.join(filtered_variables)}"
        cases.append(t)
        #######################################
        
        ############## Test to check for test_your_code calls ##############
        test_your_code_pattern = r"test_your_code\..*"
        test_your_code_matches = re.findall(test_your_code_pattern, student_code_without_comments)

        if test_your_code_matches:
            t = test_case()
            t.failed = True
            t.msg = f"Found usage of \"test_your_code.\" in your implemented code. Please remove it from your code ({', '.join(set(test_your_code_matches))}) . Use the test function as provided in the next cell"
            t.want = "No usage of \"test_your_code.\" in your implemented code"
            t.got = f"Usage of \"test_your_code.\" found: {', '.join(set(test_your_code_matches))}"
            cases.append(t)
        #######################################

        return cases

    cases = g()
    print_feedback(cases)
