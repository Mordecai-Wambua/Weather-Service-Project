from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = '0644a5f97d708b240fd0ee2ee3bbae27'
DEFAULT_CITY = 'Nairobi'

@app.route('/')
def dashboard():
    city = request.args.get('city', DEFAULT_CITY)
    weather_data = get_weather_data(city)
    return render_template('index.html', weather_data=weather_data, city=city)

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
            'aqi': get_air_quality_data(lat, lon)
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

if __name__ == '__main__':
    app.run(debug=True)
