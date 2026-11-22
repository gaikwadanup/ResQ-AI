
from agents.monitoring_agent import monitor_weather


def assess_disaster_risk():

    print("\n===== RESQ AI RISK ASSESSMENT AGENT =====")

    weather = monitor_weather()

    if weather is None:
        return {
            "risk_level": "UNKNOWN",
            "risk_score": None,
            "reasons": ["Weather data unavailable"]
        }

    score = 0
    reasons = []

    # Forecast rainfall assessment
    rain = weather["forecast_rainfall"]

    if rain >= 50:
        score += 3
        reasons.append("High forecast rainfall")

    elif rain >= 20:
        score += 2
        reasons.append("Moderate forecast rainfall")

    elif rain >= 10:
        score += 1
        reasons.append("Some forecast rainfall")

    # Rain probability assessment
    probability = weather["max_rain_probability"]

    if probability >= 70:
        score += 2
        reasons.append("High probability of rainfall")

    elif probability >= 40:
        score += 1
        reasons.append("Moderate probability of rainfall")

    # Wind assessment
    wind = weather["max_wind"]

    if wind >= 60:
        score += 3
        reasons.append("High forecast wind speed")

    elif wind >= 40:
        score += 2
        reasons.append("Moderate forecast wind speed")

    # Current precipitation assessment
    current_rain = weather["rainfall"]

    if current_rain >= 20:
        score += 2
        reasons.append("High current precipitation")

    # Final risk classification
    if score >= 5:
        risk_level = "HIGH"

    elif score >= 3:
        risk_level = "MODERATE"

    else:
        risk_level = "LOW"

    if not reasons:
        reasons.append("No significant weather risk indicators")

    result = {
        "location": weather["location"],
        "risk_score": score,
        "risk_level": risk_level,
        "reasons": reasons
    }

    print("\nLocation:", result["location"])
    print("Risk Score:", score)
    print("Risk Level:", risk_level)

    print("\nAssessment Reasons:")

    for reason in reasons:
        print("-", reason)

    return result


if __name__ == "__main__":
    assess_disaster_risk()
