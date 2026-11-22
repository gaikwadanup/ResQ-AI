
import math

from agents.resource_agent import manage_resources

# Incident location: Sangli
INCIDENT_LAT = 16.8524
INCIDENT_LON = 74.5815


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate straight-line distance using Haversine formula."""

    earth_radius = 6371

    lat1, lon1, lat2, lon2 = map(
        math.radians, [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return earth_radius * c


def plan_logistics():

    print("\n===== RESQ AI LOGISTICS AGENT =====")

    resource_data = manage_resources()

    if resource_data is None:
        print("Unable to prepare logistics plan.")
        return None

    resources = resource_data["recommendations"]

    ranked_resources = []

    for resource in resources:

        distance = calculate_distance(
            INCIDENT_LAT,
            INCIDENT_LON,
            resource["latitude"],
            resource["longitude"]
        )

        ranked_resources.append({
            "id": resource["id"],
            "name": resource["name"],
            "type": resource["type"],
            "available": resource["available"],
            "distance_km": round(distance, 2)
        })

    # Sort resources from nearest to farthest
    ranked_resources.sort(
        key=lambda item: item["distance_km"]
    )

    result = {
        "location": resource_data["location"],
        "risk_level": resource_data["risk_level"],
        "priority": resource_data["priority"],
        "nearest_resources": ranked_resources
    }

    print("\n===== LOGISTICS PLAN =====")
    print("Location:", result["location"])
    print("Risk:", result["risk_level"])
    print("Priority:", result["priority"])

    print("\nNearest Available Resources:")

    for item in ranked_resources:
        print(
            item["name"],
            "| Type:", item["type"],
            "| Distance:", item["distance_km"], "km",
            "| Available:", item["available"]
        )

    return result


if __name__ == "__main__":
    plan_logistics()
