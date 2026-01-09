import pandas as pd
from IPython.display import display, HTML
import csv

def read_candy_data(file_path):
    """
    Reads candy data from a CSV file and returns a list of dictionaries.
    
    Parameters:
    - file_path (str): The path to the CSV file.
    
    Returns:
    - List[Dict]: A list of dictionaries with "Candy Name" as a string, 
      "Popularity Score" as an integer, and "Price in USD" as a float.
    """
    candy_list = []
    
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            candy = {
                'Candy Name': row['Candy Name'],
                'Popularity Score': int(row['Popularity Score']),
                'Price in USD': float(row['Price in USD'])
            }
            candy_list.append(candy)
    
    return candy_list


def display_table(data):
    df = pd.DataFrame(data)

    # Display the DataFrame as an HTML table
    display(HTML(df.to_html(index=False)))