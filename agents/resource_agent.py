
import json
from pathlib import Path

from agents.risk_agent import assess_disaster_risk

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "resources.json"
)


def manage_resources():

    print("\n===== RESQ AI RESOURCE MANAGEMENT AGENT =====")

    # Automatically obtain risk assessment
    risk = assess_disaster_risk()

    if risk is None or risk["risk_level"] == "UNKNOWN":
        print("Cannot recommend resources: risk assessment unavailable.")
        return None

    risk_level = risk["risk_level"]

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError) as error:
        print("Database error:", error)
        return None

    resources = data["resources"]

    recommendations = []

    for resource in resources:

        if resource["status"] != "operational":
            continue

        if resource["type"] == "hospital":
            recommendations.append(resource)

        elif resource["available"] > 0:
            recommendations.append(resource)

    # Determine response priority
    if risk_level == "HIGH":
        priority = "URGENT"
    elif risk_level == "MODERATE":
        priority = "PREPAREDNESS"
    else:
        priority = "NORMAL"

    result = {
        "location": data["location"],
        "risk_level": risk_level,
        "priority": priority,
        "resources_found": len(recommendations),
        "recommendations": recommendations
    }

    print("\nLocation:", result["location"])
    print("Automatically detected risk:", risk_level)
    print("Response priority:", priority)

    print("\nRecommended resources:")

    for resource in recommendations:
        print(
            "-", resource["name"],
            "| Type:", resource["type"],
            "| Available:", resource["available"]
        )

    print("\nTotal resources found:", len(recommendations))

    return result


if __name__ == "__main__":
    manage_resources()
