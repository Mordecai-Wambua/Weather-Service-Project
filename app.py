from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import requests
from sys import argv

# Initialize the Flask application
app = Flask(__name__)

# Read API key from command-line arguments
API_KEY = argv[1]

# Set the default city to 'Nairobi'
DEFAULT_CITY = 'Nairobi'

# Define the file name for storing form data
FORM_DATA_FILE = 'form_data.json'

# Define the route for the dashboard (home page)
@app.route('/')
def dashboard():
    # Get the city from query parameters, defaulting to DEFAULT_CITY if not provided
    city = request.args.get('city', DEFAULT_CITY)
    # Retrieve weather data for the city
    weather_data = get_weather_data(city)
    # Render the 'index.html' template with the weather data and city name
    return render_template('index.html', weather_data=weather_data, city=city)

# Define the route for form submission
@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Collect form data from the POST request
    form_data = {
        'name': request.form['name'],
        'number': request.form['number'],
        'email': request.form['email'],
        'message': request.form['message']
    }
    
    # Check if the form data file exists
    if os.path.exists(FORM_DATA_FILE):
        # If it exists, read the existing data, append the new data, and save it
        with open(FORM_DATA_FILE, 'r+') as file:
            data = json.load(file)
            data.append(form_data)
            file.seek(0)
            json.dump(data, file, indent=4)
    else:
        # If it doesn't exist, create the file and save the form data
        with open(FORM_DATA_FILE, 'w') as file:
            json.dump([form_data], file, indent=4)

    # Redirect to the dashboard after form submission
    return redirect(url_for('dashboard'))

def get_weather_data(city):
    # Construct the URL for the weather API with the specified city and API key
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    # Make a GET request to the weather API
    response = requests.get(url)
    data = response.json()
    
    # Check if the request was successful
    if response.status_code == 200:
        # Extract relevant weather data from the response
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        weather = {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind': data['wind']['speed'],
            'visibility': data['visibility'] / 1000,  # Convert visibility from meters to kilometers
            'condition': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'city': data['name'],
            'country': data['sys']['country'],
            'aqi': get_air_quality_data(lat, lon),
            'forecast': get_forecast_data(lat, lon)
        }
    else:
        weather = None  # If request failed, set weather to None
    return weather

def get_air_quality_data(lat, lon):
    # Construct the URL for the air quality API with the specified latitude and longitude
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}'
    # Make a GET request to the air quality API
    response = requests.get(url)
    data = response.json()
    
    # Check if the request was successful
    if response.status_code == 200:
        # Extract the air quality index from the response
        aqi = data['list'][0]['main']['aqi']
        return aqi
    else:
        return None  # If request failed, return None

def get_forecast_data(lat, lon):
    # Construct the URL for the forecast API with the specified latitude and longitude
    url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    # Make a GET request to the forecast API
    response = requests.get(url)
    data = response.json()
    forecast = []
    
    # Check if the request was successful
    if response.status_code == 200:
        # Extract daily forecast data from the response
        for i in range(0, len(data['list']), 8):
            day_data = data['list'][i]
            forecast.append({
                'date': day_data['dt_txt'].split(' ')[0],
                'temperature': day_data['main']['temp'],
                'condition': day_data['weather'][0]['description'],
                'icon': day_data['weather'][0]['icon']
            })
    return forecast  # Return the forecast data

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)