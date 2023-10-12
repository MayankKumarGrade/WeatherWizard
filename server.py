from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5/9
    return celsius

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    if not bool(city.strip()):
        city = "Kansas City"

    weather_data = get_current_weather(city)

    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')

    temp_celsius = fahrenheit_to_celsius(float(weather_data['main']['temp']))
    feels_like_celsius = fahrenheit_to_celsius(float(weather_data['main']['feels_like']))

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{temp_celsius:.1f}",
        feels_like=f"{feels_like_celsius:.1f}"
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
