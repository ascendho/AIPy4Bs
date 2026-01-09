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
        
        # Check if the line starts with "import" or "from"
        if stripped_line.startswith('import'):
            # Split the line by commas to handle multiple imports
            imports = stripped_line.split(',')
            for imp in imports:
                # Strip leading and trailing whitespace from each import
                imp = imp.strip()
                if imp.startswith('import'):
                    import_lines.append(imp)
                else:
                    # Handle the case where the line starts with 'import' but subsequent parts do not
                    import_lines.append(f'import {imp}')
        
        elif stripped_line.startswith('from'):
            # Directly add the whole 'from ... import ...' line
            import_lines.append(stripped_line)
    
    # Check if any import statements were found
    if import_lines:
        return True, import_lines
    else:
        return False, None


# -

################### Exercise 1 Test
def exercise_1(book: dict):
    def g():
        cases = []

        assignment_name = "C1M2_Assignment.ipynb"
        autosave()  # Save the notebook
        time.sleep(3)  # Wait for 3 seconds

        nb = read_notebook(assignment_name)  # Read the notebook
        cells = get_named_cells(nb)  # Get cells with names
        source = cells["exercise_1"]["source"]  # Get source code of the cell

        expected_output = {  # Expected output dictionary
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "on_shelf": False,
            "borrower": "Arthur Dent",
            "overdue": True,
            "on_hold": False,
        }
        
        # Remove comments from code
        student_code_without_comments = remove_comments(source)
        
        ############## Test to check for test_your_code calls ##############
        test_your_code_pattern = r"test_your_code\..*"
        test_your_code_matches = re.findall(test_your_code_pattern, student_code_without_comments)

        if test_your_code_matches:
            t = test_case()
            t.failed = True
            t.msg = f"Found usage of \"test_your_code.\" in your implemented code. Please remove it from your code ({', '.join(set(test_your_code_matches))}) . Use the test function as provided in the next cell"
            t.want = "No usage of \"test_your_code.\" in your implemented code"
            t.got = f"Usage of \"test_your_code.\" found: {', '.join(set(test_your_code_matches))}"
            return [t]
        #######################################

        ############## Test to check for import statements ##############
        
        # Check for import statements
        has_imports, import_lines = check_import_statements(student_code_without_comments)
        
        t = test_case()
        if has_imports:
            t.failed = True
            t.msg = "Import statements are not allowed within your solution code. Please remove them from your code"
            t.want = "No import statements"
            t.got = f"Import statement(s) found: {', '.join(import_lines)}"
            return [t]  # Return early if import statements are found
        
        #######################################

        ############## Test to check for 'book' initialization ##############
        
        # Check for variable initializations
        assignment_pattern = r"(\b\w+\b)\s*="
        assignments = re.findall(assignment_pattern, student_code_without_comments)  # Find all variable assignments

        # Count occurrences of 'book' initialization
        book_initializations = assignments.count("book")

        # Check if 'book' is initialized more than once
        t = test_case()
        if book_initializations != 1:
            t.failed = True
            t.msg = "The variable 'book' should be initialized exactly once. Please ensure it is initialized only once, and as a Python Dictionary as instructed in the exercise"
            t.want = "One initialization of 'book'"
            t.got = f"{book_initializations} initializations of 'book'"
            return [t]  # Return early if book is initialized incorrectly
        
        #######################################

        ############## Test to check for other variable initializations ##############
        
        # Check for any other variable initializations
        other_initializations = [var for var in assignments if var != "book"]
        t = test_case()
        if other_initializations:
            t.failed = True
            t.msg = "New variables should not be initialized. Please only use 'book' as instructed in the exercise, and remove any additional variable initializations"
            t.want = "No new variables initialized"
            t.got = f"New variables initialized: {', '.join(other_initializations)}"
            return [t]  # Return early if other variables are initialized
        
        #######################################
        
        ############## Test to check for correct dictionary ##############

        t = test_case()
        if book == expected_output:
            return [t] # Return early if the dictionary is correct
        
        # Get expected keys
        expected_keys = list(expected_output.keys())
        # Get student's book keys
        book_keys = list(book.keys())
        
        ### Check for extra keys
        extra_keys = [k for k in book_keys if k not in expected_keys]
        t = test_case()
        if extra_keys:
            t.failed = True
            t.msg = "book dictionary has unexpected keys"
            t.want = "no additional keys from the ones mentioned in the exercise (check your spelling)"
            t.got = extra_keys
            return [t]
        
        ### Check for missing keys
        for k in expected_keys:
            t = test_case()
            if k not in book_keys:
                t.failed = True
                t.msg = f"missing key '{k}'"
                t.want = f"a key named '{k}' inside the book dictionary"
                t.got = None
            cases.append(t)
        
        ### Check for incorrect values
        for k, v in book.items():
            t = test_case()
            if v != expected_output[k]:
                t.failed = True
                t.msg = f"incorrect value for key '{k}' (check your spelling or the data types you used)"
                t.want = expected_output[k]
                t.got = v
            cases.append(t)
        #######################################
        
        return cases

    cases = g()
    print_feedback(cases)


def exercise_2():
    def g():
        cases = []

        assignment_name = "C1M2_Assignment.ipynb"
        autosave()  # Save the notebook
        time.sleep(3)  # Wait for 3 seconds

        nb = read_notebook(assignment_name)  # Read the notebook
        cells = get_named_cells(nb)  # Get cells with names
        source = cells["exercise_2"]["source"]  # Get source code of the cell
        out = cells["exercise_2"]["outputs"]  # Get outputs of the cell
        
        # Remove comments from code
        student_code_without_comments = remove_comments(source)  

        ############## Test to check if 'book' is initialized ##############
        
        pattern_book_init = r'\bbook\s*='
        t = test_case()
        if re.search(pattern_book_init, student_code_without_comments):
            t.failed = True
            t.msg = "The dictionary variable 'book' must not be overridden in your code. Ensure you remove any code that modifies the 'book' variable. Re-run the cells of Exercise 1 to restore 'book' to its expected state as defined in that exercise. IMPORTANT: Failing to re-run Exercise 1 will result in errors, even if your code for this and following exercises is correct."
            t.want = "No overriding of 'book' variable"
            t.got = "'book' variable is being overridden"
            return [t]  # Return early if 'book' is overridden
        
        #######################################

        ############## Test to check for import statements ##############
        
        has_imports, import_lines = check_import_statements(student_code_without_comments)  
        t = test_case()
        if has_imports:
            t.failed = True
            t.msg = "Import statements are not allowed within your solution code. Please remove them from your code"
            t.want = "No import statements"
            t.got = f"Import statement(s) found: {', '.join(import_lines)}"
        cases.append(t)
        #######################################

        ############## Test to check for variable initializations ##############
        
        # Find variable initializations
        pattern_var_init = r'\b(\w+)\s*=\s*[^=]'
        var_init_matches = re.findall(pattern_var_init, student_code_without_comments)  

        t = test_case()
        if var_init_matches:
            t.failed = True
            t.msg = "Variable initialization is not allowed within your solution code. Please remove any variable initializations."
            t.want = "No variable initializations"
            t.got = f"Variable initialization(s) found: {', '.join(var_init_matches)}"
        cases.append(t)
        #######################################

        ############## Test to check for 'is' or 'not' in 'if' statements ##############
        
        pattern_is_not_in_if = r'\bif\s+.*\b(is|not)\b'
        t = test_case()
        if re.search(pattern_is_not_in_if, student_code_without_comments):
            t.failed = True
            t.msg = "Avoid using the 'is' or 'not' keywords in 'if' statements. Use the equality operator '==' instead."
            t.want = "No use of 'is' or 'not' keywords in 'if' statements, expected to use '==' operator instead"
            t.got = "'is' or 'not' keyword found in 'if' statements"
        cases.append(t)
        #######################################

        ############## Test to check for cell output ##############
        t = test_case()
        if not out:
            t.failed = True
            t.msg = "There was no output for Exercise 2 cell, check that you run it"
            t.want = "An output generated from print statement"
            t.got = None
            return [t]
        #######################################

        ############## Test to check for the correct number of print statements ##############
        
        pattern = r'print\(\s*["\']'
        matches = re.findall(pattern, source)  # Find print statements

        t = test_case()
        if len(matches) != 2:
            t.failed = True
            t.msg = "Detected incorrect number of valid print statements (without f-strings)"
            t.want = 2
            t.got = len(matches)
        cases.append(t)
        #######################################

        ############## Test to check for the correct 'if' statement ##############
        pattern = r"if\s+(.+?)\s+and\s+(.+?):"
        t = test_case()
        if not re.search(pattern, source):
            t.failed = True
            t.msg = "Unable to detect valid if statement that checks if the book is on_shelf and is not on_hold"
            t.want = "a valid if statement that checks if the book is on_shelf and is not on_hold"
            t.got = None
        cases.append(t)
        #######################################

        ############## Test to check for the correct 'else' statement ##############
        pattern = r"else\s*:"
        t = test_case()
        if not re.search(pattern, source):
            t.failed = True
            t.msg = "Unable to detect else statement"
            t.want = "an else statement being used when book is not overdue"
            t.got = None
        cases.append(t)
        #######################################

        ############## Test to check for the correct printed message (unavailable) ##############
        
        # Get the standard output
        std_out = out[0]["text"]  
        pattern = "Book is not available to be borrowed"
        t = test_case()
        if pattern not in std_out:
            t.failed = True
            t.msg = "Missing printed information"
            t.want = "Book is not available to be borrowed"
            t.got = "Missing or incorrect message for book. Please make sure you are using uppercase and lowercase letters where needed. Also, check for typos"
        cases.append(t)
        #######################################

        ############## Test to check for incorrect printed message (available) ##############
        pattern = "Book is available to be borrowed"
        t = test_case()
        if pattern in std_out:
            t.failed = True
            t.msg = "Incorrect information printed for book"
            t.want = "Printed message should reflect that the book is not available to be borrowed "
            t.got = "Book is available to be borrowed"
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


# +
def exercise_3():
    def g():
        cases = []

        assignment_name = "C1M2_Assignment.ipynb"
        autosave()  # Save the notebook
        time.sleep(3)  # Wait for 3 seconds

        nb = read_notebook(assignment_name)  # Read the notebook
        cells = get_named_cells(nb)  # Get cells with names
        source = cells["exercise_3"]["source"]  # Get source code of the cell
        out = cells["exercise_3"]["outputs"]  # Get outputs of the cell
        
        # Remove comments from code
        student_code_without_comments = remove_comments(source)  

        ############## Test to check if 'book' is initialized ##############
        
        pattern_book_init = r'\bbook\s*='
        t = test_case()
        if re.search(pattern_book_init, student_code_without_comments):
            t.failed = True
            t.msg = "The dictionary variable 'book' must not be overridden in your code. Ensure you remove any code that modifies the 'book' variable. Re-run the cells of Exercise 1 and Exercise 2 to restore 'book' to its expected state. IMPORTANT: Failing to re-run Exercise 1 and Exercise 2 will result in errors, even if your code for this and following exercises is correct."
            t.want = "No overriding of 'book' variable"
            t.got = "'book' variable is being overridden"
            return [t]  # Return early if 'book' is overridden
        
        #######################################

        ############## Test to check for import statements ##############
        
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

        ############## Test to check for variable initializations ##############
        
        # Find variable initializations
        pattern_var_init = r'\b(\w+)\s*=\s*[^=]'
        var_init_matches = re.findall(pattern_var_init, student_code_without_comments)

        t = test_case()
        if var_init_matches:
            t.failed = True
            t.msg = "Variable initialization is not allowed within your solution code. Please remove any variable initializations."
            t.want = "No variable initializations"
            t.got = f"Variable initialization(s) found: {', '.join(var_init_matches)}"
        cases.append(t)
        #######################################

        ############## Test to check for 'is' or 'not' in 'if' statements ##############
        
        pattern_is_not_in_if = r'\bif\s+.*\b(is|not)\b'
        t = test_case()
        if re.search(pattern_is_not_in_if, student_code_without_comments):
            t.failed = True
            t.msg = "Avoid using the 'is' or 'not' keywords in 'if' statement. Use the equality operator '==' instead."
            t.want = "No use of 'is' or 'not' keywords in 'if' statement, expected to use '==' operator instead"
            t.got = "'is' or 'not' keyword found in 'if' statement"
        cases.append(t)
        #######################################

        ############## Test to check for cell output ##############
        t = test_case()
        if not out:
            t.failed = True
            t.msg = "There was no output for Exercise 3 cell, check that you run it"
            t.want = "An output generated from print statement"
            t.got = None
            return [t]
        #######################################

        ############## Test to check for the correct number of print statements (f-strings) ##############
        
        # Find f-string print statements
        pattern = r'print\(\s*f["\']'
        matches = re.findall(pattern, source)  

        t = test_case()
        if len(matches) != 1:
            t.failed = True
            t.msg = (
                "Detected incorrect number of valid print statements (with f-strings)"
            )
            t.want = 1
            t.got = len(matches)
        cases.append(t)
        #######################################

        ############## Test to check for the correct number of print statements (without f-strings) ##############
        
        # Find non-f-string print statements
        pattern = r'print\(\s*["\']'
        matches = re.findall(pattern, source)  

        t = test_case()
        if len(matches) != 1:
            t.failed = True
            t.msg = "Detected incorrect number of valid print statements (without f-strings)"
            t.want = 1
            t.got = len(matches)
        cases.append(t)
        #######################################

        ############## Test to check for the correct 'else' statement ##############
        pattern = r"else\s*:"
        t = test_case()
        if not re.search(pattern, source):
            t.failed = True
            t.msg = "Unable to detect else statement"
            t.want = "an else statement being used when book is not overdue"
            t.got = None
        cases.append(t)
        #######################################

        ############## Test to check for the correct 'if' statement ##############
        pattern = r"""if\s+book\s*\[\s*['"]overdue['"]\s*\](?:\s*(?:is\s+True|==\s*True))?\s*:?"""
        t = test_case()
        if not re.search(pattern, source):
            t.failed = True
            t.msg = (
                "Unable to detect valid if statement that checks if the book is overdue"
            )
            t.want = "a valid if statement that checks if the book is overdue"
            t.got = None
        cases.append(t)
        #######################################

        ############## Test to check for the correct printed message ##############
        std_out = out[0]["text"]  
        pattern = "Book is overdue - Contact Arthur Dent to return it"
        t = test_case()
        if pattern not in std_out:
            t.failed = True
            t.msg = "Missing printed information"
            t.want = "Book is overdue - Contact Arthur Dent to return it"
            t.got = "Missing or incorrect message for book. Please make sure you are using uppercase and lowercase letters where needed. Also, check for typos"
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
    
    
# -

def exercise_4(borrower_email: str):
    def g():
        cases = []

        assignment_name = "C1M2_Assignment.ipynb"
        autosave()  # Save the notebook
        time.sleep(3)  # Wait for 3 seconds

        nb = read_notebook(assignment_name)  # Read the notebook
        cells = get_named_cells(nb)  # Get cells with names
        source = cells["exercise_4"]["source"]  # Get source code of the cell

        expected_output = "arthur.dent@dlailibrary.com"  # Expected output

        student_code_without_comments = remove_comments(source)  # Remove comments from code

        ############## Test to check if 'book' is initialized ##############
        # Check if 'book' is initialized
        pattern_book_init = r'\bbook\s*='
        t = test_case()
        if re.search(pattern_book_init, student_code_without_comments):
            t.failed = True
            t.msg = "The dictionary variable 'book' must not be overridden in your code. Ensure you remove any code that modifies the 'book' variable. Re-run the cells of Exercise 1, Exercise 2 and Exercise 3 to restore 'book' to its expected state. IMPORTANT: Failing to re-run Exercise 1, Exercise 2 and Exercise 3 will result in errors, even if your code for this and following exercises is correct."
            t.want = "No overriding of 'book' variable"
            t.got = "'book' variable is being overridden"
            return [t]  
        #######################################

        ############## Test to check for import statements ##############
        
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

        ############## Test to check for 'borrower_email' initialization ##############
        
        # Find variable assignments
        assignment_pattern = r'(\b\w+\b)\s*='
        assignments = re.findall(assignment_pattern, student_code_without_comments)  

        # Count occurrences of 'borrower_email' initialization
        book_initializations = assignments.count('borrower_email')

        # Check if 'borrower_email' is initialized more than once
        t = test_case()
        if book_initializations != 1:
            t.failed = True
            t.msg = "The variable 'borrower_email' should be initialized exactly once. Please ensure it is initialized only once, as instructed in the exercise"
            t.want = "One initialization of 'borrower_email'"
            t.got = f"{book_initializations} initializations of 'borrower_email'"
            return [t]  
        #######################################

        ############## Test to check for other variable initializations ##############
        
        # Check for any other variable initializations
        other_initializations = [var for var in assignments if var != 'borrower_email']
        t = test_case()
        if other_initializations:
            t.failed = True
            t.msg = "New variables should not be initialized. Please only use 'borrower_email' as instructed in the exercise, and remove any additional variable initializations"
            t.want = "No new variables initialized"
            t.got = f"New variables initialized: {', '.join(other_initializations)}"
            return [t]  
        #######################################

        ############## Test to check for 'is' or 'not' in 'if' statements ##############
        
        pattern_is_not_in_if = r'\bif\s+.*\b(is|not)\b'
        t = test_case()
        if re.search(pattern_is_not_in_if, student_code_without_comments):
            t.failed = True
            t.msg = "Avoid using the 'is' or 'not' keywords in 'if' statement. Use the equality operator '==' instead."
            t.want = "No use of 'is' or 'not' keywords in 'if' statement, expected to use '==' operator instead"
            t.got = "'is' or 'not' keyword found in 'if' statement"
        cases.append(t)
        #######################################

        ############## Test to check for correct borrower_email value ##############
        t = test_case()
        if borrower_email != expected_output:
            t.failed = True
            t.msg = "Gotten email is incorrect"
            t.want = expected_output
            t.got = borrower_email
        cases.append(t)
        #######################################

        ############## Test to check for 'for' loop ##############
        pattern = r"for\s+(.+?)\s+in\s+(.+?):"
        t = test_case()
        if not re.search(pattern, source):
            t.failed = True
            t.msg = "Unable to detect for loop"
            t.want = "a for loop to iterate over the list of borrowers"
            t.got = None
        cases.append(t)
        #######################################

        ############## Test to check for 'if' statement ##############
        pattern = r"if\s+(.+?)\s*:"
        t = test_case()
        if not re.search(pattern, source):
            t.failed = True
            t.msg = "Unable to detect if statement"
            t.want = "an if statement that checks the name of the borrower"
            t.got = None
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


def exercise_5(prompt: str):
    def g():
        cases = []

        assignment_name = "C1M2_Assignment.ipynb"
        autosave()  # Save the notebook
        time.sleep(3)  # Wait for 3 seconds

        nb = read_notebook(assignment_name)  # Read the notebook
        cells = get_named_cells(nb)  # Get cells with names
        source = cells["exercise_5"]["source"]  # Get source code of the cell

        expected_name = "Arthur"  # Expected name in prompt
        expected_book = "To Kill a Mockingbird"  # Expected book in prompt
        expected_author = "Harper Lee"  # Expected author in prompt
        expected_date = "16 November 2024"  # Expected date in prompt

        student_code_without_comments = remove_comments(source)  # Remove comments from code

        ############## Test to check for import statements ##############
        
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

        ############## Test to check for 'prompt' initialization ##############
        
        assignment_pattern = r'(\b\w+\b)\s*='
        
        # Find variable assignments
        assignments = re.findall(assignment_pattern, student_code_without_comments)  

        # Count occurrences of 'prompt' initialization
        book_initializations = assignments.count('prompt')

        # Check if 'prompt' is initialized more than once
        t = test_case()
        if book_initializations != 1:
            t.failed = True
            t.msg = "The variable 'prompt' should be initialized exactly once. Please ensure it is initialized only once, as instructed in the exercise"
            t.want = "One initialization of 'prompt'"
            t.got = f"{book_initializations} initializations of 'prompt'"
            return [t]
        ####################################################################################
        
        ############## Test to check for other variable initializations ##############
        
        other_initializations = [var for var in assignments if var != 'prompt']
        if other_initializations:
            t = test_case()
            t.failed = True
            t.msg = "New variables should not be initialized. Please only use 'prompt' as instructed in the exercise, and remove any additional variable initializations"
            t.want = "No new variables initialized"
            t.got = f"New variables initialized: {', '.join(other_initializations)}"
            return [t]
        #######################################

        ############## Test to check if prompt includes expected information ##############
        t = test_case()
        if (
            expected_name not in prompt
            or expected_book not in prompt
            or expected_author not in prompt
            or expected_date not in prompt
        ):
            t.failed = True
            t.msg = (
                "Your prompt does not include 1 or more of the expected information\n"
            )
            t.want = '\nA prompt with mention of:\nperson_name: "Arthur"\nbook_name: "To Kill a Mockingbird"\nbook_author: "Harper Lee"\ndue_date: "16 November 2024"\n'
            t.got = prompt
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
