import re
import time
from dlai_grader.grading import test_case
from dlai_grader.io import read_notebook
from dlai_grader.notebook import get_named_cells
from IPython.core.display import HTML, clear_output
from IPython.display import display, Javascript


from ex1_helper_functions import read_candy_data


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

################################### Check for correct import in ex 1
def check_ex1_import_statement():
    autosave()  # Save the notebook
    time.sleep(3)  # Wait for 3 seconds

    assignment_name = "C1M4_Assignment.ipynb"
    nb = read_notebook(assignment_name)  # Read the notebook
    cells = get_named_cells(nb)  # Get cells with names
    source = cells["import_cell_1"]["source"]  # Get source code of the cell

    student_code_without_comments = remove_comments(source).strip()  # Remove comments and leading/trailing whitespace

    correct_import_statement = "from ex1_helper_functions import *"

    # First: Check for any import statement
    has_imports, import_lines = check_import_statements(student_code_without_comments)
    if not has_imports:
        return HTML('<p style="color: red;">No import statement found</p>')

    # Second: Check for the correct import statement
    if correct_import_statement not in student_code_without_comments:
        return HTML('<p style="color: red;">Expected import statement not found. Use the expected format: <code>from file_name import *</code>. </p>')

    # Third: Check for any other import statements
    other_imports = [line for line in import_lines if line != correct_import_statement]
    if other_imports:
        return HTML(f'<p style="color: red;">Unexpected import statement found. Please remove <code>{other_imports[0]}</code> from your code.</p>')

    # Fourth: Check if the cleaned source is exactly the correct import statement
    if student_code_without_comments != correct_import_statement:
        return HTML('<p style="color: red;">Ensure the only valid line of code present in the cell is the expected import statement. Remove anything else present in your code.</p>')

    # Fifth: Check for comments after the import statement on the same line
    lines = source.splitlines()  # Split the source into lines
    for line in lines:
        if correct_import_statement in line:
            comment_match = re.search(rf"{re.escape(correct_import_statement)}\s*(#.*)$", line)
            if comment_match:
                comment = comment_match.group(1)
                return HTML(f'<p style="color: red;">Remove the comment, <code>{comment}</code> after the import statement</p>')

    # All checks passed
    return HTML('<p style="color: green;">All tests passed! Correct import statement used!</p>')


# +
################################### Check implementation for correct function use in ex 1
def exercise_1(candy_data: list):
    def g():
        cases = []

        assignment_name = "C1M4_Assignment.ipynb"
        autosave()  # Save the notebook
        time.sleep(3)  # Wait for 3 seconds

        nb = read_notebook(assignment_name)  # Read the notebook
        cells = get_named_cells(nb)  # Get cells with names
        source = cells["exercise_1"]["source"]  # Get source code of the cell

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

        ############## Test to check if candy_data returns expected data ##############
        expected_output = read_candy_data("candy_data.csv")  # Expected output
        t = test_case()
        if candy_data != expected_output:
            t.failed = True
            t.msg = '"candy_data" does not return expected data.'
            t.want = expected_output
            t.got = candy_data
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


################################### Check for correct import in ex 2
def check_ex2_import_statement():
    autosave()  # Save the notebook
    time.sleep(3)  # Wait for 3 seconds
    
    # Clear previous output
    clear_output(wait=True)

    assignment_name = "C1M4_Assignment.ipynb"
    nb = read_notebook(assignment_name)  # Read the notebook
    cells = get_named_cells(nb)  # Get cells with names
    source = cells["import_cell_2"]["source"]  # Get source code of the cell

    student_code_without_comments = remove_comments(source).strip()  # Remove comments and leading/trailing whitespace

    correct_import_statement = "from ex2_helper_functions import get_popularity_scores, print_scores"

    # First: Check for any import statement
    has_imports, import_lines = check_import_statements(student_code_without_comments)
    if not has_imports:
        return HTML('<p style="color: red;">No import statement found</p>')

    # Second: Check for the correct import statement
    if correct_import_statement not in student_code_without_comments:
        return HTML('<p style="color: red;">Expected import statement not found. Use the expected format: <code>from file_name import function_name_1, function_name_2</code>. </p>')

    # Third: Check for any other import statements
    other_imports = [line for line in import_lines if line != correct_import_statement]
    if other_imports:
        return HTML(f'<p style="color: red;">Unexpected import statement found. Please remove <code>{other_imports[0]}</code> from your code.</p>')

    # Fourth: Check if the cleaned source is exactly the correct import statement
    if student_code_without_comments != correct_import_statement:
        return HTML('<p style="color: red;">Ensure the only valid line of code present in the cell is the expected import statement. Remove anything else present in your code.</p>')

    # Fifth: Check for comments after the import statement on the same line
    lines = source.splitlines()  # Split the source into lines
    for line in lines:
        if correct_import_statement in line:
            comment_match = re.search(rf"{re.escape(correct_import_statement)}\s*(#.*)$", line)
            if comment_match:
                comment = comment_match.group(1)
                return HTML(f'<p style="color: red;">Remove the comment, <code>{comment}</code> after the import statement</p>')

    # All checks passed
    return HTML('<p style="color: green;">All tests passed! Correct import statement used!</p>')        


# -


################################### Check implementation for correct function use in ex 2
def exercise_2(popularity_scores: list):
    def g():
        cases = []

        expected_output = [  # Expected output list
            92,
            83,
            85,
            84,
            83,
            94,
            84,
            95,
            84,
            83,
            91,
            83,
            88,
            84,
            84,
            84,
            84,
            84,
            84,
        ]

        assignment_name = "C1M4_Assignment.ipynb"
        autosave()  # Save the notebook
        time.sleep(3)  # Wait for 3 seconds

        nb = read_notebook(assignment_name)  # Read the notebook
        cells = get_named_cells(nb)  # Get cells with names
        source = cells["exercise_2"]["source"]  # Get source code of the cell

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

        ############## Test to check if popularity_scores returns expected results ##############
        t = test_case()
        if popularity_scores != expected_output:
            t.failed = True
            t.msg = '"popularity_scores" does not return expected results.'
            t.want = expected_output
            t.got = popularity_scores
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


################################### Check for correct import in ex 3
def check_ex3_import_statement():
    autosave()  # Save the notebook
    time.sleep(3)  # Wait for 3 seconds
    
    # Clear previous output
    clear_output(wait=True)

    assignment_name = "C1M4_Assignment.ipynb"
    nb = read_notebook(assignment_name)  # Read the notebook
    cells = get_named_cells(nb)  # Get cells with names
    source = cells["import_cell_3"]["source"]  # Get source code of the cell

    student_code_without_comments = remove_comments(source).strip()  # Remove comments and leading/trailing whitespace

    correct_import_statement = "import statistics as stats"

    # First: Check for any import statement
    has_imports, import_lines = check_import_statements(student_code_without_comments)
    if not has_imports:
        return HTML('<p style="color: red;">No import statement found</p>')

    # Second: Check for the correct import statement
    if correct_import_statement not in student_code_without_comments:
        return HTML('<p style="color: red;">Expected import statement not found. Use the expected format: <code>import module_name as alias_name</code>. Make sure you are using the same alias name as expected. </p>')

    # Third: Check for any other import statements
    other_imports = [line for line in import_lines if line != correct_import_statement]
    if other_imports:
        return HTML(f'<p style="color: red;">Unexpected import statement found. Please remove <code>{other_imports[0]}</code> from your code.</p>')

    # Fourth: Check if the cleaned source is exactly the correct import statement
    if student_code_without_comments != correct_import_statement:
        return HTML('<p style="color: red;">Ensure the only valid line of code present in the cell is the expected import statement. Remove anything else present in your code.</p>')

    # Fifth: Check for comments after the import statement on the same line
    lines = source.splitlines()  # Split the source into lines
    for line in lines:
        if correct_import_statement in line:
            comment_match = re.search(rf"{re.escape(correct_import_statement)}\s*(#.*)$", line)
            if comment_match:
                comment = comment_match.group(1)
                return HTML(f'<p style="color: red;">Remove the comment, <code>{comment}</code> after the import statement</p>')

    # All checks passed
    return HTML('<p style="color: green;">All tests passed! Correct import statement used!</p>')        


################################### Check implementation for correct function use in ex 3
def exercise_3(avg_popularity: float):
    def g():
        cases = []

        expected_output = 85.94736842105263  # Expected output value

        assignment_name = "C1M4_Assignment.ipynb"
        autosave()  # Save the notebook
        time.sleep(3)  # Wait for 3 seconds

        nb = read_notebook(assignment_name)  # Read the notebook
        cells = get_named_cells(nb)  # Get cells with names
        source = cells["exercise_3"]["source"]  # Get source code of the cell

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

        ############## Test to check if avg_popularity returns expected results ##############
        t = test_case()
        if avg_popularity != expected_output:
            t.failed = True
            t.msg = '"avg_popularity" does not return expected results'
            t.want = expected_output
            t.got = avg_popularity
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


################################### Check for correct import in ex 4
def check_ex4_import_statement():
    autosave()  # Save the notebook
    time.sleep(3)  # Wait for 3 seconds
    
    # Clear previous output
    clear_output(wait=True)

    assignment_name = "C1M4_Assignment.ipynb"
    nb = read_notebook(assignment_name)  # Read the notebook
    cells = get_named_cells(nb)  # Get cells with names
    source = cells["import_cell_4"]["source"]  # Get source code of the cell

    student_code_without_comments = remove_comments(source).strip()  # Remove comments and leading/trailing whitespace

    correct_import_statement = "import ex4_helper_functions"

    # First: Check for any import statement
    has_imports, import_lines = check_import_statements(student_code_without_comments)
    if not has_imports:
        return HTML('<p style="color: red;">No import statement found</p>')

    # Second: Check for the correct import statement
    if correct_import_statement not in student_code_without_comments:
        return HTML('<p style="color: red;">Expected import statement not found. Use the expected format: <code>import file_name</code>. </p>')

    # Third: Check for any other import statements
    other_imports = [line for line in import_lines if line != correct_import_statement]
    if other_imports:
        return HTML(f'<p style="color: red;">Unexpected import statement found. Please remove <code>{other_imports[0]}</code> from your code.</p>')

    # Fourth: Check if the cleaned source is exactly the correct import statement
    if student_code_without_comments != correct_import_statement:
        return HTML('<p style="color: red;">Ensure the only valid line of code present in the cell is the expected import statement. Remove anything else present in your code.</p>')

    # Fifth: Check for comments after the import statement on the same line
    lines = source.splitlines()  # Split the source into lines
    for line in lines:
        if correct_import_statement in line:
            comment_match = re.search(rf"{re.escape(correct_import_statement)}\s*(#.*)$", line)
            if comment_match:
                comment = comment_match.group(1)
                return HTML(f'<p style="color: red;">Remove the comment, <code>{comment}</code> after the import statement</p>')

    # All checks passed
    return HTML('<p style="color: green;">All tests passed! Correct import statement used!</p>')         


# +
################################### Check implementation for correct function use in ex 4
def exercise_4(top_candiies: list):
    def g():
        cases = []

        expected_output = [  # Expected output list of dictionaries
            {"Candy Name": "Twix", "Popularity Score": 92, "Price in USD": 1.25},
            {"Candy Name": "M&M's", "Popularity Score": 94, "Price in USD": 1.25},
            {"Candy Name": "Snickers", "Popularity Score": 95, "Price in USD": 1.25},
            {"Candy Name": "Kit Kat", "Popularity Score": 91, "Price in USD": 1.25},
            {"Candy Name": "Starburst", "Popularity Score": 88, "Price in USD": 1.0},
        ]

        assignment_name = "C1M4_Assignment.ipynb"
        autosave()  # Save the notebook
        time.sleep(3)  # Wait for 3 seconds

        nb = read_notebook(assignment_name)  # Read the notebook
        cells = get_named_cells(nb)  # Get cells with names
        source = cells["exercise_4"]["source"]  # Get source code of the cell

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

        ############## Test to check if top_candies returns expected results ##############
        t = test_case()
        if top_candiies != expected_output:
            t.failed = True
            t.msg = '"top_candies" does not return expected results'
            t.want = expected_output
            t.got = top_candiies
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


################################### Check for correct change in ex 5
def check_change_in_ex5():
    def g():
        cases = []

        assignment_name = "C1M4_Assignment.ipynb"
        autosave()  # Save the notebook
        time.sleep(5)  # Wait for 5 seconds

        nb = read_notebook(assignment_name)  # Load the current notebook
        cells = get_named_cells(nb)  # Get cells with names
        source = cells["cell_for_ex5"]["source"]  # Get source code of the cell

        student_code_without_comments = remove_comments(source)  # Remove comments from the source code

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

        ############## Test to check for the presence of the function ##############
        t = test_case()
        if "def get_llm_response(prompt):" not in student_code_without_comments:
            t.failed = True
            t.msg = 'Function <code>get_llm_response</code> not found in the specified cell.'
            t.want = "Function definition for get_llm_response"
            t.got = "Function definition not found"
        else:
            # Check for the specific lines that should not have default values
            temperature_check = re.search(
                r"temperature\s*=\s*0\.0", student_code_without_comments
            )
            content_check = re.search(
                r'["\']content["\']\s*:\s*["\']You are an AI assistant\.?["\']',
                student_code_without_comments,
            )

            ############## Test to check for default values ##############
            if temperature_check or content_check:
                t.failed = True
                t.msg = 'Please ensure that "temperature" is not set to 0.0 and "content" is not set to "You are an AI assistant." in the function \"get_llm_response\"'
                t.want = "No default values for temperature and content"
                t.got = "Default values found"
            cases.append(t)
            #######################################

            ############## Test to check for function calls ##############
            # This regex is more robust to handle different ways the function might be called
            function_call_pattern = r"\bget_llm_response\s*\("
            function_call_matches = re.findall(function_call_pattern, student_code_without_comments)

            # Exclude the function definition itself from the matches
            function_definition_pattern = r"def get_llm_response\s*\(prompt\s*\)\s*:"
            function_definition_match = re.search(function_definition_pattern, student_code_without_comments)

            if function_definition_match:
                # Remove the function definition from the code before checking for calls
                student_code_without_definition = re.sub(re.escape(function_definition_match.group(0)), "", student_code_without_comments)
                function_call_matches = re.findall(function_call_pattern, student_code_without_definition)

            if function_call_matches:
                t = test_case()
                t.failed = True
                t.msg = "Function \"get_llm_response\" should only be defined in this cell, not called. Remove the function call and any other associated code."
                t.want = "No calls to get_llm_response"
                t.got = f"Calls to get_llm_response found" #Simplified the got message
                cases.append(t)
            #######################################

        return cases

    cases = g()
    print_feedback(cases)
