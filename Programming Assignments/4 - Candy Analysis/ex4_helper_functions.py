import pandas as pd
from IPython.display import display, HTML
from prettytable import PrettyTable

def get_top_candies(candy_data, avg):
    """
    Returns a list of candies with a popularity score greater than or equal to the given average.
    
    Parameters:
    - candy_data (List[Dict]): A list of dictionaries containing candy data.
    - avg (float): The average popularity score to compare against.
    
    Returns:
    - List[Dict]: A list of dictionaries representing the top candies.
    """
    top_candies = []
    
    for candy in candy_data:
        # Check if the popularity score is greater than or equal to the average
        if float(candy['Popularity Score']) >= avg:
            # Append the candy to the top_candies list
            top_candies.append(candy)
    
    return top_candies

def display_pretty_table(data):
    if not data:
        print("No data available to display.")
        return

    # Create a PrettyTable object
    table = PrettyTable()

    # Set the column names
    table.field_names = data[0].keys()

    # Add rows to the table
    for item in data:
        table.add_row(item.values())

    # Print the table
    print(table)