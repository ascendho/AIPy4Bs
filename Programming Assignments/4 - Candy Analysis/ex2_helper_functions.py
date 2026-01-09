def get_popularity_scores(candies):
    """
    Extracts and returns a list of popularity scores from a list of candy data.

    Parameters:
    candies (list of dict): A list of dictionaries where each dictionary contains 
                            details about a candy, 'Candy Name', 'Popularity Score'
                            and 'Price in USD'

    Returns:
    list of int: A list of integers representing the popularity scores of the candies.
    """
    
    # Create a list to store the popularity scores
    popularity_scores = []
    
    # Iterate over each dictionary in the candy_data list
    for candy in candies:
        # Extract the 'Popularity Score' and append it to the list
        popularity_scores.append(candy['Popularity Score'])
    
    # Return the list of popularity scores
    return popularity_scores

def print_scores(scores):
    """
    Prints the list of integers.

    Parameters:
    scores (list of int): A list of integers to be printed.
    """
    print(scores)