import os

from openai import OpenAI
from dotenv import load_dotenv
import requests
import json
import folium


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

def display_map():
    # Define the bounding box for the continental US
    us_bounds = [[24.396308, -125.0], [49.384358, -66.93457]]
    # Create the map centered on the US with limited zoom levels
    m = folium.Map(
	    location=[37.0902, -95.7129],  # Center the map on the geographic center of the US
	    zoom_start=5,  # Starting zoom level
	    min_zoom=4,  # Minimum zoom level
	    max_zoom=10,
	    max_bounds=True,
	    control_scale=True  # Maximum zoom level
	)

    # Set the bounds to limit the map to the continental US
    m.fit_bounds(us_bounds)
    # Add a click event to capture the coordinates
    m.add_child(folium.LatLngPopup())
    title_html = '''
	<div style="
	display: flex;
	justify-content: center;
	align-items: center;
	width: 100%; 
	height: 50px; 
	border:0px solid grey; 
	z-index:9999; 
	font-size:30px;
	padding: 5px;
	background-color:white;
	text-align: center;
	">
	&nbsp;<b>Click to view coordinates</b>
	</div>
	'''
	
    m.get_root().html.add_child(folium.Element(title_html))

    # Display the map
    return m
    
def get_forecast(lat, lon):
    url = f"https://api.weather.gov/points/{lat},{lon}"

    # Make the request to get the grid points
    response = requests.get(url)
    data = response.json()
    # Extract the forecast URL from the response
    forecast_url = data['properties']['forecast']

    # Make a request to the forecast URL for the selected location
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()
    
    daily_forecast = forecast_data['properties']['periods']
    return daily_forecast
