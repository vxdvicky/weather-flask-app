from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("17031fe5103246b286c114933252708")
BASE_URL = "https://api.weatherapi.com/v1/current.json"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            try:
                url = f"{BASE_URL}?key={API_KEY}&q={city}&aqi=no"
                response = requests.get(url, timeout=5)
                data = response.json()

                if "error" in data:
                    error = data["error"]["message"]
                else:
                    weather_data = {
                        "city": data["location"]["name"],
                        "country": data["location"]["country"],
                        "temperature_c": data["current"]["temp_c"],
                        "temperature_f": data["current"]["temp_f"],
                        "feels_like": data["current"]["feelslike_c"],
                        "humidity": data["current"]["humidity"],
                        "wind_speed": data["current"]["wind_kph"],
                        "condition": data["current"]["condition"]["text"],
                        "icon": "https:" + data["current"]["condition"]["icon"]
                    }
            except Exception as e:
                error = "Something went wrong. Try again."

    return render_template("inex.html", weather=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
