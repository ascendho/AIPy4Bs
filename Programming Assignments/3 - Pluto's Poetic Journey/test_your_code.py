import os
import re
import time
import tempfile
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
def exercise_1(read_article):
    def g():
        cases = []
        
        autosave()
        time.sleep(3)

        filename = "news_article.txt"

        try:
            learner_output = read_article(filename)
        except Exception as e:
            print(f"There was an error when running your function. Details: {str(e)}")

        with open(filename, "r") as f:
            expected_output = f.read()
            
        assignment_name = "C1M3_Assignment.ipynb"

        nb = read_notebook(assignment_name)
        cells = get_named_cells(nb)
        source = cells["exercise_1"]["source"]
        
        student_code_without_comments = remove_comments(source)
        has_imports, import_lines = check_import_statements(student_code_without_comments)
        
        # Check for the use of "open" and the absence of "with"
        if "open" in student_code_without_comments and "with " not in student_code_without_comments:
            pass  # Student used open() as requested
        else:
            t = test_case()
            t.failed = True
            t.msg = 'Your solution should not use the `with` statement'
            t.want = (f"""Use only the `open()` function to open the file and read it as: 
                      
                      # "Open" "text_file" in "read" mode
                      f = open(text_file, "r")
                      
                      # Use "f.read()" to read the file into "contents"
                      contents = f.read()
                      
                      # Close the file "f.close()"
                      f.close()
                      """)
            t.got = '`with` statment found in the implementation'
            return [t]
        
        t = test_case()
        if has_imports:
            t.failed = True
            t.msg = "Import statements are not allowed within your solution code. Please remove them from your code"
            t.want = "No import statements"
            t.got = f"Import statement(s) found: {', '.join(import_lines)}"
        cases.append(t) 

        t = test_case()
        if learner_output != expected_output:
            t.failed = True
            t.msg = '"read_article" did not behave as expected. Make sure you have followed all of the instructions in implementing the function "read_article"'
            t.want = '"read_article" to be able to correctly read a file'
            t.got = '"read_article" did not correctly read a file'
        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)


################### Exercise 2 Test
def exercise_2(key_topics: list):
    def g():
        cases = []
        
        assignment_name = "C1M3_Assignment.ipynb"
        autosave()
        time.sleep(3)

        nb = read_notebook(assignment_name)
        cells = get_named_cells(nb)
        source = cells["exercise_2"]["source"]

        # Default placeholder topics
        default_topics = [
            "Copy/Paste your first topic as a string in here",
            "Copy/Paste your second topic as a string in here",
            "Copy/Paste your third topic as a string in here",
        ]
        
        student_code_without_comments = remove_comments(source)
        has_imports, import_lines = check_import_statements(student_code_without_comments)
        t = test_case()
        if has_imports:
            t.failed = True
            t.msg = "Import statements are not allowed within your solution code. Please remove them from your code"
            t.want = "No import statements"
            t.got = f"Import statement(s) found: {', '.join(import_lines)}"
        cases.append(t)

        t = test_case()
        if not isinstance(key_topics, list):
            t.failed = True
            t.msg = '"key_topics" is not a list.'
            t.want = '"key_topics" should be implemented as a Python list'
            t.got = f'"key_topics" has been implemented as a Python {type(key_topics)}'
        cases.append(t)

        t = test_case()
        if len(key_topics) != 3:
            t.failed = True
            t.msg = '"key_topics" is either an empty list or does not contain 3 topics'
            t.want = '"key_topics" should contain exactly 3 topics'
            t.got = key_topics
        cases.append(t)

        t = test_case()
        if not all(isinstance(item, str) for item in key_topics):
            t.failed = True
            t.msg = "Not all elements in the list are strings"
            t.want = "3 topics which are of string type"
            t.got = key_topics
        cases.append(t)

        t = test_case()
        if len(set(key_topics)) != len(key_topics):
            t.failed = True
            t.msg = "The list contains duplicate topics"
            t.want = "3 topics which are unique"
            t.got = key_topics
        cases.append(t)

        # Check for default placeholder topics
        t = test_case()
        if key_topics == default_topics:
            t.failed = True
            t.msg = "Default placeholder topics detected"
            t.want = 'Please copy/paste the topics received from the "response" above'
            t.got = key_topics
        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)


################### Exercise 3 Test
def exercise_3(topics_to_use: list, key_topics: list):
    def g():
        cases = []
        
        assignment_name = "C1M3_Assignment.ipynb"
        autosave()
        time.sleep(3)

        nb = read_notebook(assignment_name)
        cells = get_named_cells(nb)
        source = cells["exercise_3"]["source"]

        student_code_without_comments = remove_comments(source)
        has_imports, import_lines = check_import_statements(student_code_without_comments)
        t = test_case()
        if has_imports:
            t.failed = True
            t.msg = "Import statements are not allowed within your solution code. Please remove them from your code"
            t.want = "No import statements"
            t.got = f"Import statement(s) found: {', '.join(import_lines)}"
        cases.append(t)

        # Check if the input is a list
        t = test_case()
        if not isinstance(topics_to_use, list):
            t.failed = True
            t.msg = '"topics_to_use" is not a list.'
            t.want = '"topics_to_use" should be implemented as a Python list'
            t.got = f'"topics_to_use" has been implemented as a Python {type(topics_to_use)}'
        cases.append(t)

        # Check if the list has exactly 3 dictionaries
        t = test_case()
        if len(topics_to_use) != 3:
            t.failed = True
            t.msg = '"topics_to_use" does not contain exactly 3 dictionaries'
            t.want = '"topics_to_use" should contain exactly 3 dictionaries'
            t.got = topics_to_use
        cases.append(t)

        # Initialize a set to track unique topic values
        topic_values = set()

        for entry in topics_to_use:
            # Check if each entry is a dictionary
            t = test_case()
            if not isinstance(entry, dict):
                t.failed = True
                t.msg = "Not all entries in the list are dictionaries"
                t.want = "Each entry should be a dictionary"
                t.got = entry
                cases.append(t)
                continue

            # Flags to ensure required keys are present
            has_topic = False
            has_to_use = False
            topic_value = None

            # Check for required keys and their types
            for key, value in entry.items():
                if key.startswith("Topic ") and isinstance(value, str):
                    has_topic = True
                    topic_value = value
                elif key == "to_use" and isinstance(value, bool):
                    has_to_use = True

            # Verify both keys are present and valid
            if not (has_topic and has_to_use):
                t.failed = True
                t.msg = "Each dictionary must have a 'Topic #' with a string value and 'to_use' with a boolean value"
                t.want = "Dictionary with 'Topic #' as string and 'to_use' as boolean"
                t.got = entry
            else:
                # Check if the topic value is unique
                if topic_value in topic_values:
                    t.failed = True
                    t.msg = "Duplicate topic values found"
                    t.want = "All topic values should be unique"
                    t.got = f'"{topic_value}" more than once'
                else:
                    topic_values.add(topic_value)

                # Check if the topic value is in key_topics
                if topic_value not in key_topics:
                    t.failed = True
                    t.msg = f'Topic value "{topic_value}" is not in the list \"key_topics\"'
                    t.want = f'Topic value should be one of {key_topics}'
                    t.got = topic_value

            cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)


################### Exercise 4 Test
def exercise_4(prompt: str, topics_to_use: list):
    def g():
        cases = []
        
        assignment_name = "C1M3_Assignment.ipynb"
        autosave()
        time.sleep(3)

        nb = read_notebook(assignment_name)
        cells = get_named_cells(nb)
        source = cells["exercise_4"]["source"]

        student_code_without_comments = remove_comments(source)
        has_imports, import_lines = check_import_statements(student_code_without_comments)
        t = test_case()
        if has_imports:
            t.failed = True
            t.msg = "Import statements are not allowed within your solution code. Please remove them from your code"
            t.want = "No import statements"
            t.got = f"Import statement(s) found: {', '.join(import_lines)}"
        cases.append(t)

        # Convert the list of dictionaries to a string using repr
        result_string = repr(topics_to_use)

        t = test_case()
        if result_string not in prompt:
            t.failed = True
            t.msg = 'You did not include the list "topics_to_use" in your prompt'
            t.want = 'A prompt which includes all of the list "topics_to_use" in it\n'
            t.got = prompt
        cases.append(t)

        t = test_case()
        if "poem" not in prompt:
            t.failed = True
            t.msg = 'You did not specify to write a "poem" in your prompt'
            t.want = 'A prompt which includes the instruction of writing a "poem"'
            t.got = prompt
        cases.append(t)

        t = test_case()
        if not (
            ("4" in prompt or "four" in prompt)
            and ("line" in prompt or "lines" in prompt)
        ):
            t.failed = True
            t.msg = "Missing mention of 4 (four) and/or line (lines) in the prompt"
            t.want = "A prompt which has mention of 4 (four) and line (or lines)"
            t.got = prompt
        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)


################### Exercise 5 Test
def exercise_5(save_to_file):
    def g():
        cases = []
        
        assignment_name = "C1M3_Assignment.ipynb"
        autosave()
        time.sleep(3)

        nb = read_notebook(assignment_name)
        cells = get_named_cells(nb)
        source = cells["exercise_5"]["source"]

        student_code_without_comments = remove_comments(source)
        has_imports, import_lines = check_import_statements(student_code_without_comments)
        t = test_case()
        if has_imports:
            t.failed = True
            t.msg = "Import statements are not allowed within your solution code. Please remove them from your code"
            t.want = "No import statements"
            t.got = f"Import statement(s) found: {', '.join(import_lines)}"
        cases.append(t)

        original_dir = os.getcwd()
        t = test_case()
        dummy_to_save = "Testing Exercise 5"

        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)

            try:
                save_to_file(dummy_to_save)

            except Exception as e:
                t.failed = True
                t.msg = "An exception occurred"
                t.want = "The file should be created without exceptions."
                t.got = f"An exception was raised. Details: {str(e)}"
                return [t]

            finally:
                os.chdir(original_dir)

            file_path = os.path.join(temp_dir, "poem.txt")
            exists = os.path.isfile(file_path)
            if not exists:
                t.failed = True
                t.msg = (
                    'The "save_to_file" function did not create the file as expected.'
                )
                t.want = "The file should exist after saving."
                t.got = "The file 'poem.txt' does not exist."
            cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)
