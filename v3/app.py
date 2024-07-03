from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import requests
from sys import argv

app = Flask(__name__)

API_KEY = argv[1]
DEFAULT_CITY = 'Nairobi'
FORM_DATA_FILE = 'form_data.json'

@app.route('/')
def dashboard():
    city = request.args.get('city', DEFAULT_CITY)
    weather_data = get_weather_data(city)
    return render_template('index.html', weather_data=weather_data, city=city)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    form_data = {
        'name': request.form['name'],
        'number': request.form['number'],
        'email': request.form['email'],
        'message': request.form['message']
    }
    
    if os.path.exists(FORM_DATA_FILE):
        with open(FORM_DATA_FILE, 'r+') as file:
            data = json.load(file)
            data.append(form_data)
            file.seek(0)
            json.dump(data, file, indent=4)
    else:
        with open(FORM_DATA_FILE, 'w') as file:
            json.dump([form_data], file, indent=4)

    return redirect(url_for('dashboard'))

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        weather = {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind': data['wind']['speed'],
            'visibility': data['visibility'] / 1000,
            'condition': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'city': data['name'],
            'country': data['sys']['country'],
            'aqi': get_air_quality_data(lat, lon),
            'forecast': get_forecast_data(lat, lon)
        }
    else:
        weather = None
    return weather

def get_air_quality_data(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        aqi = data['list'][0]['main']['aqi']
        return aqi
    else:
        return None

def get_forecast_data(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    forecast = []
    if response.status_code == 200:
        for i in range(0, len(data['list']), 8):
            day_data = data['list'][i]
            forecast.append({
                'date': day_data['dt_txt'].split(' ')[0],
                'temperature': day_data['main']['temp'],
                'condition': day_data['weather'][0]['description'],
                'icon': day_data['weather'][0]['icon']
            })
    return forecast
 

if __name__ == '__main__':
    app.run(debug=True)
