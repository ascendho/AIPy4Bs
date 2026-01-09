# import gradio as gr
import os

from openai import OpenAI
from dotenv import load_dotenv

import random

#Get the OpenAI API key from the .env file
load_dotenv('.env', override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

# Set up the OpenAI client
client = OpenAI(api_key=openai_api_key)


def print_llm_response(prompt):
    """This function takes as input a prompt, which must be a string enclosed in quotation marks,
    and passes it to OpenAI's GPT3.5 model. The function then prints the response of the model.
    """
    llm_response = get_llm_response(prompt)
    print(llm_response)


def get_llm_response(prompt):
    """This function takes as input a prompt, which must be a string enclosed in quotation marks,
    and passes it to OpenAI's GPT3.5 model. The function then saves the response of the model as
    a string.
    """
    try:
        if not isinstance(prompt, str):
            raise ValueError("Input must be a string enclosed in quotes.")
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
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
    except TypeError as e:
        print("Error:", str(e))


def get_chat_completion(prompt, history):
    history_string = "\n\n".join(["\n".join(turn) for turn in history])
    prompt_with_history = f"{history_string}\n\n{prompt}"
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful but terse AI assistant who gets straight to the point.",
            },
            {"role": "user", "content": prompt_with_history},
        ],
        temperature=0.0,
    )
    response = completion.choices[0].message.content
    return response


# def open_chatbot():
#     """This function opens a Gradio chatbot window that is connected to OpenAI's GPT3.5 model."""
#     gr.close_all()
#     gr.ChatInterface(fn=get_chat_completion).launch(quiet=True)

def get_dog_age(human_age):
    """This function takes one parameter: a person's age as an integer and returns their age if
    they were a dog, which is their age divided by 7. """
    return human_age / 7

def get_goldfish_age(human_age):
    """This function takes one parameter: a person's age as an integer and returns their age if
    they were a dog, which is their age divided by 5. """
    return human_age / 5

def get_cat_age(human_age):
    if human_age <= 14:
        # For the first 14 human years, we consider the age as if it's within the first two cat years.
        cat_age = human_age / 7
    else:
        # For human ages beyond 14 years:
        cat_age = 2 + (human_age - 14) / 4
    return cat_age

def get_random_ingredient():
    """
    Returns a random ingredient from a list of 20 smoothie ingredients.
    
    The ingredients are a bit wacky but not gross, making for an interesting smoothie combination.
    
    Returns:
        str: A randomly selected smoothie ingredient.
    """
    ingredients = [
        "rainbow kale", "glitter berries", "unicorn tears", "coconut", "starlight honey",
        "lunar lemon", "blueberries", "mermaid mint", "dragon fruit", "pixie dust",
        "butterfly pea flower", "phoenix feather", "chocolate protein powder", "grapes", "hot peppers",
        "fairy floss", "avocado", "wizard's beard", "pineapple", "rosemary"
    ]
    
    return random.choice(ingredients)

def get_random_number(x, y):
    """
        Returns a random integer between x and y, inclusive.
        
        Args:
            x (int): The lower bound (inclusive) of the random number range.
            y (int): The upper bound (inclusive) of the random number range.
        
        Returns:
            int: A randomly generated integer between x and y, inclusive.

        """
    return random.randint(x, y)

def calculate_llm_cost(characters, price_per_1000_tokens=0.015):
    tokens = characters / 4
    cost = (tokens / 1000) * price_per_1000_tokens
    return f"${cost:.4f}"