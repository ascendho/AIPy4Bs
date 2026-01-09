import os

from openai import OpenAI
from dotenv import load_dotenv
import requests
import json
import folium
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


# Get the OpenAI API key from the .env file
load_dotenv('.env', override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

# Set up the OpenAI client
client = OpenAI(api_key=openai_api_key)


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
    
def beautiful_barh(labels, values):
	# Create the bar chart
	plt.figure(figsize=(9, 5))
	bars = plt.barh(labels, values, color = plt.cm.tab20.colors)

	for bar in bars:
		plt.text(bar.get_width()/2,   # X coordinate 
			 bar.get_y() + bar.get_height()/2,  # Y coordinate 
			 f'${bar.get_width() / 1e9:.1f}B',  # Text label 
			 ha='center', va='center', color='w', fontsize=10, fontweight = "bold")
			 
	# Customizing the x-axis to display values in billions
	def billions(x, pos):
		"""The two args are the value and tick position"""
		return f'${x * 1e-9:.1f}B'

	formatter = FuncFormatter(billions)
	plt.gca().xaxis.set_major_formatter(formatter)


	# Inverting the y-axis to have the highest value on top
	plt.gca().invert_yaxis()

