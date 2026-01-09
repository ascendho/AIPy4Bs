from openai import AzureOpenAI, DefaultHttpxClient
import ipywidgets as widgets
from IPython.display import display, HTML
import base64

# +
e2_extracted_topics = """Pluto's geological activity and features

New Horizons' discoveries of Kuiper Belt Objects

Future observations with Subaru Telescope collaboration"""

ex4_poem = """The API stumbled, OpenAI's call went astray,
Yet in your work, don't let this cause dismay.
Embrace the hiccup, refine your path anew,
And press on with confidence, for success awaits you.
"""


# -

def get_llm_response(prompt):
    """This function takes as input a prompt, which must be a string enclosed in quotation marks,
    and passes it to OpenAI's GPT 4o-mini model. The function then saves the response of the model as
    a string.
    """
    
    ########### Try/except in case the OpenAI service fails
    ########### In case it fails, return a hardcoded response
    try:
        client = AzureOpenAI(
            api_key="abcdefg",
            api_version="2024-02-01",
            azure_endpoint = "https://cour-external-playground.openai.azure.com/",
            http_client=DefaultHttpxClient(verify=False)
        )
        
        completion = client.chat.completions.create(
            model='gpt-4o-mini',
            messages = [
                {
                    "role": "system", 
                    "content": "You are a helpful but terse AI assistant who gets straight to the point."
                },
                
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
        )
        response = completion.choices[0].message.content
        return response
    
    
    except:
        
        ########### If OpenAI service fails in Exercise 2, send hardcoded response:
        if "key" in prompt:
            print("\033[34mOops! Looks like the OpenAI service is down at the moment, but don't worry, we have loaded the response:\n\n")
            print(e2_extracted_topics)
            print("\n\ninto your \"response\" variable. You can use that and carry on with your assignment.\033[0m")
            
            response = e2_extracted_topics
            
            return response
        ########### If OpenAI service fails in Exercise 4, send hardcoded response:
        if "poem" in prompt:
            print("\033[34mOops! Looks like the OpenAI service is down at the moment, but don't worry, we have loaded the response:\n\n")
            print(ex4_poem)
            print("\n\ninto your \"poem\" variable. You can use that and carry on with your assignment.\033[0m")
            
            response = ex4_poem
            
            return response

# +
def print_formatted_list(list_of_strings):
    # Start the list
    print("[")
    
    # Iterate over the list_of_strings and print each one in the required format
    for i, string in enumerate(list_of_strings):
        # Print the string with indentation and quotes
        if i == len(list_of_strings) - 1:
            print(f'    "{string}"')
        else:
            print(f'    "{string}",')
    
    # Close the list
    print("]")


def print_formatted_list_of_dict(topic_list):
    # Start the list
    print("[")
    
    # Iterate over the topic_list and print each dictionary in the required format
    for i, topic_dict in enumerate(topic_list):
        # Print the formatted dictionary
        print("    {")
        for key, value in topic_dict.items():
            # Format the key-value pairs correctly
            if isinstance(value, str):
                print(f'        "{key}": "{value}",')
            else:
                print(f'        "{key}": {value},')
        
        # Remove the trailing comma and close the dictionary
        print("    }" if i == len(topic_list) - 1 else "    },")
    
    # Close the list
    print("]")


# +
def create_download_link(file_path, description):
    with open(file_path, 'rb') as file:
        file_data = file.read()
        encoded_data = base64.b64encode(file_data).decode()
        href = f'<a href="data:text/html;base64,{encoded_data}" download="{file_path}">{description}</a>'
    return HTML(href)


def download_file():
    """
    Creates a widget to download a file from the working directory.
    """
    # Text input to specify the file name
    file_name_input = widgets.Text(
        value='',
        placeholder='Enter file name',
        description='File:',
        disabled=False
    )
    
    # Button to initiate the download
    download_button = widgets.Button(
        description='Download',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Download the specified file',
        icon='download' # (FontAwesome names without the `fa-` prefix)
    )
    
    # Output widget to display the download link
    output = widgets.Output()

    def on_button_click(b):
        with output:
            output.clear_output()
            file_name = file_name_input.value
            if (not file_name.startswith('.') and not file_name.startswith('_')):
                try:
                    download_link = create_download_link(file_name, 'Click here to download your file')
                    display(download_link)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Please enter a valid file name.")
    
    # Attach the button click event to the handler
    download_button.on_click(on_button_click)
    
    # Display the widgets
    display(widgets.HBox([file_name_input, download_button]), output)

