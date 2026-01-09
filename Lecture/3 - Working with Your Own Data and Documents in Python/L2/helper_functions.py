#import gradio as gr
import os

from openai import OpenAI
from dotenv import load_dotenv
import ipywidgets as widgets
from IPython.display import display
import io
import csv

# Get the OpenAI API key from the .env file
load_dotenv('.env', override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

# Set up the OpenAI client
client = OpenAI(api_key=openai_api_key)


def read_csv_dict(csv_file_path):
    """This function takes a csv file and loads it as a dict."""

    # Initialize an empty list to store the data
    data_list = []

    # Open the CSV file
    with open(csv_file_path, mode='r') as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)
    
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Append the row to the data list
            data_list.append(row)

    # Convert the list to a dictionary
    data_dict = {i: data_list[i] for i in range(len(data_list))}
    return data_dict


def print_llm_response(prompt):
    """This function takes as input a prompt, which must be a string enclosed in quotation marks,
    and passes it to OpenAI's GPT3.5 model. The function then prints the response of the model.
    """
    try:
        if not isinstance(prompt, str):
            raise ValueError("Input must be a string enclosed in quotes.")
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful but terse AI assistant who gets straight to the point.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )
        response = completion.choices[0].message.content
        print(response)
    except TypeError as e:
        print("Error:", str(e))


def get_llm_response(prompt):
    """This function takes as input a prompt, which must be a string enclosed in quotation marks,
    and passes it to OpenAI's GPT3.5 model. The function then saves the response of the model as
    a string.
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful but terse AI assistant who gets straight to the point.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    response = completion.choices[0].message.content
    return response


def upload_txt_file():
    """
    Uploads a text file and saves it to the specified directory.
    
    Args:
        directory (str): The directory where the uploaded file will be saved. 
        Defaults to the current working directory.
    """
    # Create the file upload widget
    upload_widget = widgets.FileUpload(
        accept='.txt',  # Accept text files only
        multiple=False  # Do not allow multiple uploads
    )
    # Impose file size limit
    output = widgets.Output()
    
    # Function to handle file upload
    def handle_upload(change):
        with output:
            output.clear_output()
            # Read the file content
            content = upload_widget.value[0]['content']
            name = upload_widget.value[0]['name']
            size_in_kb = len(content) / 1024
            
            if size_in_kb > 3:
                print(f"Your file is too large, please upload a file that doesn't exceed 3KB.")
                return
		    
            # Save the file to the specified directory
            with open(name, 'wb') as f:
                f.write(content)
            # Confirm the file has been saved
            print(f"The {name} file has been uploaded.")

    # Attach the file upload event to the handler function
    upload_widget.observe(handle_upload, names='value')

    display(upload_widget, output)

def list_files_in_directory(directory='.'):
    """
    Lists all non-hidden files in the specified directory.
    
    Args:
        directory (str): The directory to list files from. Defaults to the current working directory.
    """
    try:
        files = [f for f in os.listdir(directory) if (not f.startswith('.') and not f.startswith('_'))]
        for file in files:
            print(file)
    except Exception as e:
        print(f"An error occurred: {e}")
