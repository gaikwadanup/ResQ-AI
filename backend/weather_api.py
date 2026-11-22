
import requests

WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

# Sangli, Maharashtra
LATITUDE = 16.8524
LONGITUDE = 74.5815


def get_weather():

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,

        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
            "weather_code"
        ],

        "hourly": [
            "precipitation",
            "precipitation_probability",
            "wind_speed_10m"
        ],

        "forecast_days": 1,
        "timezone": "Asia/Kolkata"
    }

    try:

        response = requests.get(
            WEATHER_API_URL,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        current = data["current"]
        hourly = data["hourly"]

        weather = {
            "location": "Sangli, Maharashtra",

            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "rainfall": current["precipitation"],
            "wind_speed": current["wind_speed_10m"],
            "weather_code": current["weather_code"],
            "time": current["time"],

            # Hourly forecast data
            "hourly_time": hourly["time"],
            "hourly_rainfall": hourly["precipitation"],
            "rain_probability": hourly["precipitation_probability"],
            "hourly_wind": hourly["wind_speed_10m"]
        }

        return weather

    except (requests.RequestException, KeyError, ValueError) as error:

        print("Weather API Error:", error)

        return None


if __name__ == "__main__":

    print("\n===== RESQ AI WEATHER MONITOR =====")

    weather = get_weather()

    if weather:

        print("Location:", weather["location"])
        print("Temperature:", weather["temperature"], "°C")
        print("Humidity:", weather["humidity"], "%")
        print("Rainfall:", weather["rainfall"], "mm")
        print("Wind Speed:", weather["wind_speed"], "km/h")
        print("Data Time:", weather["time"])

        print("\n===== 24 HOUR FORECAST =====")

        print(
            "Total Forecast Rainfall:",
            sum(weather["hourly_rainfall"]),
            "mm"
        )

        print(
            "Maximum Rain Probability:",
            max(weather["rain_probability"]),
            "%"
        )

        print(
            "Maximum Wind Speed:",
            max(weather["hourly_wind"]),
            "km/h"
        )

    else:

        print("Weather information unavailable.")
