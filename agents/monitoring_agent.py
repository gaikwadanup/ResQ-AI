
from backend.weather_api import get_weather


def monitor_weather():

    print("\n===== RESQ AI MONITORING AGENT =====")

    weather = get_weather()

    if weather is None:
        return None

    rainfall = weather["rainfall"]
    wind_speed = weather["wind_speed"]

    forecast_rainfall = sum(weather["hourly_rainfall"])
    max_rain_probability = max(weather["rain_probability"])
    max_wind = max(weather["hourly_wind"])

    alerts = []

    if forecast_rainfall >= 50:
        alerts.append("Heavy forecast rainfall")

    if max_rain_probability >= 70:
        alerts.append("High probability of rainfall")

    if max_wind >= 60:
        alerts.append("High forecast wind speed")

    if not alerts:
        alerts.append("No significant weather indicators detected")

    result = {
        "location": weather["location"],
        "temperature": weather["temperature"],
        "humidity": weather["humidity"],
        "rainfall": rainfall,
        "wind_speed": wind_speed,
        "forecast_rainfall": forecast_rainfall,
        "max_rain_probability": max_rain_probability,
        "max_wind": max_wind,
        "risk_alerts": alerts
    }

    print("Location:", result["location"])
    print("Forecast Rainfall:", forecast_rainfall, "mm")
    print("Maximum Rain Probability:", max_rain_probability, "%")
    print("Maximum Forecast Wind:", max_wind, "km/h")
    print("Alerts:", alerts)

    return result


if __name__ == "__main__":
    monitor_weather()
