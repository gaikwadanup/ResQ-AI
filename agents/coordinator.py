import json
import math
from pathlib import Path
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents.monitoring_agent import monitor_weather
from agents.decision_agent import make_ai_decision
from agents.planning_agent import create_execution_plan


# ============================================================
# SHARED STATE BETWEEN AGENTS
# ============================================================

class ResQState(TypedDict, total=False):
    scenario: str
    weather: dict
    risk_score: int
    risk_level: str
    risk_reasons: list
    ai_decision: dict
    agent_plan: dict
    resources: list
    logistics: list
    final_report: dict
    error: str


# ============================================================
# NODE 1: WEATHER MONITORING AGENT
# ============================================================

def weather_node(state: ResQState):
    scenario = state.get("scenario", "LIVE").upper()

    if scenario == "LIVE":
        print("\n[COORDINATOR] Starting Live Weather Agent")
        weather = monitor_weather()

        if weather is None:
            return {"error": "Weather data unavailable"}

        return {"weather": weather}

    print(f"\n[SIMULATION] Loading {scenario} scenario")

    scenarios = {
        "LOW": {
            "location": "Sangli, Maharashtra",
            "temperature": 29,
            "humidity": 45,
            "rainfall": 0,
            "wind_speed": 10,
            "forecast_rainfall": 2,
            "max_rain_probability": 10,
            "max_wind": 15
        },
        "MODERATE": {
            "location": "Sangli, Maharashtra",
            "temperature": 27,
            "humidity": 75,
            "rainfall": 5,
            "wind_speed": 25,
            "forecast_rainfall": 25,
            "max_rain_probability": 60,
            "max_wind": 35
        },
        "HIGH": {
            "location": "Sangli, Maharashtra",
            "temperature": 24,
            "humidity": 90,
            "rainfall": 25,
            "wind_speed": 55,
            "forecast_rainfall": 70,
            "max_rain_probability": 90,
            "max_wind": 70
        }
    }

    if scenario not in scenarios:
        return {
            "error": "Invalid scenario. Choose LIVE, LOW, MODERATE or HIGH."
        }

    return {"weather": scenarios[scenario]}


# ============================================================
# NODE 2: RISK ASSESSMENT AGENT
# ============================================================

def risk_node(state: ResQState):
    print("\n[COORDINATOR] Starting Risk Agent")

    weather = state["weather"]

    score = 0
    reasons = []

    rain = weather["forecast_rainfall"]
    probability = weather["max_rain_probability"]
    wind = weather["max_wind"]
    current_rain = weather["rainfall"]

    if rain >= 50:
        score += 3
        reasons.append("High forecast rainfall")
    elif rain >= 20:
        score += 2
        reasons.append("Moderate forecast rainfall")
    elif rain >= 10:
        score += 1
        reasons.append("Some forecast rainfall")

    if probability >= 70:
        score += 2
        reasons.append("High rain probability")
    elif probability >= 40:
        score += 1
        reasons.append("Moderate rain probability")

    if wind >= 60:
        score += 3
        reasons.append("High forecast wind")
    elif wind >= 40:
        score += 2
        reasons.append("Moderate forecast wind")

    if current_rain >= 20:
        score += 2
        reasons.append("High current precipitation")

    if score >= 5:
        level = "HIGH"
    elif score >= 3:
        level = "MODERATE"
    else:
        level = "LOW"

    if not reasons:
        reasons.append("No significant weather risk indicators")

    print("Risk Score:", score)
    print("Risk Level:", level)

    return {
        "risk_score": score,
        "risk_level": level,
        "risk_reasons": reasons
    }


# ============================================================
# NODE 3: AI DECISION AGENT
# ============================================================

def ai_decision_node(state: ResQState):
    print("\n[COORDINATOR] Starting AI Decision Agent")

    risk = {
        "risk_score": state["risk_score"],
        "risk_level": state["risk_level"],
        "reasons": state["risk_reasons"]
    }

    decision = make_ai_decision(
        weather=state["weather"],
        risk=risk
    )

    print("\n[COORDINATOR] AI recommendation received")

    return {"ai_decision": decision}


# ============================================================
# NODE 4: AI PLANNING AGENT
# ============================================================

def planning_node(state: ResQState):
    print("\n[COORDINATOR] Starting AI Planning Agent")

    risk = {
        "risk_score": state["risk_score"],
        "risk_level": state["risk_level"],
        "reasons": state["risk_reasons"]
    }

    plan = create_execution_plan(
        weather=state["weather"],
        risk=risk,
        ai_decision=state["ai_decision"]
    )

    print("\nSelected Tools:")
    for tool in plan.get("tools", []):
        print("-", tool)

    print("Planning Reasoning:", plan.get("reasoning"))
    print("Planner Status:", plan.get("planner_status"))

    return {"agent_plan": plan}


# ============================================================
# NODE 5: RESOURCE MANAGEMENT AGENT
# ============================================================

def resource_node(state: ResQState):
    print("\n[COORDINATOR] Starting Resource Agent")

    file_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "resources.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    resources = [
        item for item in data["resources"]
        if item["status"] == "operational"
        and (
            item["type"] == "hospital"
            or item["available"] > 0
        )
    ]

    print("Available resources:", len(resources))

    return {"resources": resources}


# ============================================================
# CALCULATE GEOGRAPHICAL DISTANCE
# ============================================================

def calculate_distance(lat1, lon1, lat2, lon2):
    radius = 6371

    lat1, lon1, lat2, lon2 = map(
        math.radians,
        [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    return radius * 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )


# ============================================================
# NODE 6: LOGISTICS AGENT
# ============================================================

def logistics_node(state: ResQState):
    print("\n[COORDINATOR] Starting Logistics Agent")

    # Prototype incident location: Sangli coordinates.
    incident_lat = 16.8524
    incident_lon = 74.5815

    ranked = []

    for resource in state["resources"]:
        distance = calculate_distance(
            incident_lat,
            incident_lon,
            resource["latitude"],
            resource["longitude"]
        )

        ranked.append({
            "name": resource["name"],
            "type": resource["type"],
            "available": resource["available"],
            "distance_km": round(distance, 2)
        })

    ranked.sort(key=lambda item: item["distance_km"])

    return {"logistics": ranked}


# ============================================================
# NODE 7: LOW-RISK COMPLETION
# ============================================================

def complete_node(state: ResQState):
    print("\n[COORDINATOR] Routine monitoring recommended")

    return {
        "final_report": {
            "risk_level": state["risk_level"],
            "ai_decision": state.get("ai_decision", {}),
            "agent_plan": state.get("agent_plan", {}),
            "message": "Continue routine weather monitoring.",
            "resources_dispatched": False,
            "resource_plan": []
        }
    }


# ============================================================
# NODE 8: FINAL RESOURCE REPORT
# ============================================================

def final_report_node(state: ResQState):
    print("\n[COORDINATOR] Generating Emergency Resource Plan")

    return {
        "final_report": {
            "risk_level": state["risk_level"],
            "ai_decision": state.get("ai_decision", {}),
            "agent_plan": state.get("agent_plan", {}),
            "message": (
                "Resource assessment and logistics plan generated. "
                "Human authority approval required before deployment."
            ),
            "resources_dispatched": False,
            "resource_plan": state.get("logistics", [])
        }
    }


# ============================================================
# CONDITIONAL WORKFLOW DECISION
# ============================================================

def decide_next_step(state: ResQState):
    if state.get("error"):
        return "stop"

    risk = state["risk_level"]
    plan = state.get("agent_plan", {})
    tools = plan.get("tools", [])

    print("\n[COORDINATOR] Validating AI execution plan")

    if risk == "LOW":
        if "routine_monitoring" not in tools:
            print("Safety fallback: routine monitoring required")

        print("Routine monitoring workflow selected")
        return "complete"

    if risk == "MODERATE":
        if "resource_lookup" not in tools:
            print("Safety fallback: resource lookup required")

        return "prepare"

    if risk == "HIGH":
        if "resource_lookup" not in tools:
            print("Safety fallback: emergency resource lookup required")

        return "mobilize"

    print("Unknown risk level. Stopping workflow.")
    return "stop"


# ============================================================
# ERROR HANDLING
# ============================================================

def error_node(state: ResQState):
    print("\n[COORDINATOR] Workflow stopped due to an error")

    return {
        "final_report": {
            "risk_level": "UNKNOWN",
            "message": state.get("error", "Unknown workflow error"),
            "resources_dispatched": False
        }
    }


# ============================================================
# BUILD LANGGRAPH WORKFLOW
# ============================================================

workflow = StateGraph(ResQState)

workflow.add_node("weather", weather_node)
workflow.add_node("risk", risk_node)
workflow.add_node("ai_decision", ai_decision_node)
workflow.add_node("planner", planning_node)
workflow.add_node("resources", resource_node)
workflow.add_node("logistics", logistics_node)
workflow.add_node("complete", complete_node)
workflow.add_node("final_report", final_report_node)
workflow.add_node("error", error_node)

workflow.add_edge(START, "weather")

workflow.add_conditional_edges(
    "weather",
    lambda state: "stop" if state.get("error") else "continue",
    {
        "stop": "error",
        "continue": "risk"
    }
)

workflow.add_edge("risk", "ai_decision")

# IMPORTANT: the planner must run after the AI Decision Agent.
workflow.add_edge("ai_decision", "planner")

# IMPORTANT: route from planner, NOT directly from ai_decision.
workflow.add_conditional_edges(
    "planner",
    decide_next_step,
    {
        "complete": "complete",
        "prepare": "resources",
        "mobilize": "resources",
        "stop": "error"
    }
)

workflow.add_edge("resources", "logistics")
workflow.add_edge("logistics", "final_report")

workflow.add_edge("complete", END)
workflow.add_edge("final_report", END)
workflow.add_edge("error", END)

app = workflow.compile()


# ============================================================
# MAIN COORDINATOR
# ============================================================

def run_resq_ai(scenario="LIVE"):
    print("\n================================")
    print("     RESQ AI COORDINATOR")
    print("================================")

    print("Selected Scenario:", scenario)

    result = app.invoke({
        "scenario": scenario.upper()
    })

    print("\n===== FINAL RESQ AI REPORT =====")

    if result.get("error"):
        print("Error:", result["error"])
        return result

    print("Risk Level:", result.get("risk_level"))
    print("Risk Score:", result.get("risk_score"))

    print("\nRisk Reasons:")
    for reason in result.get("risk_reasons", []):
        print("-", reason)

    decision = result.get("ai_decision", {})

    if decision:
        print("\nAI Decision:", decision.get("decision"))
        print("AI Priority:", decision.get("priority"))
        print("AI Reasoning:", decision.get("reasoning"))

        print("\nAI Recommended Actions:")
        for action in decision.get("recommended_actions", []):
            print("-", action)

    # Print the plan independently of the decision display block.
    plan = result.get("agent_plan", {})

    if plan:
        print("\n===== AI EXECUTION PLAN =====")
        for tool in plan.get("tools", []):
            print("-", tool)

        print("Planner Status:", plan.get("planner_status"))
        print("Planner Reasoning:", plan.get("reasoning"))
    else:
        print("\nAI execution plan was not returned.")

    logistics = result.get("logistics", [])

    if logistics:
        print("\n===== RECOMMENDED RESOURCES =====")
        for item in logistics:
            print(
                item["name"],
                "| Type:", item["type"],
                "| Available:", item["available"],
                "| Distance:", item["distance_km"], "km"
            )

    report = result.get("final_report", {})

    if report:
        print("\nFinal Message:", report["message"])
        print(
            "Resources Dispatched:",
            report.get("resources_dispatched", False)
        )

    print("\n===== WORKFLOW COMPLETED =====")

    return result


# ============================================================
# SIMULATION MENU
# ============================================================

if __name__ == "__main__":
    print("\n===== RESQ AI SIMULATION MENU =====")
    print("1. Live Weather")
    print("2. Low Risk")
    print("3. Moderate Risk")
    print("4. High Risk")

    choice = input("\nSelect scenario (1-4): ").strip()

    scenarios = {
        "1": "LIVE",
        "2": "LOW",
        "3": "MODERATE",
        "4": "HIGH"
    }

    selected = scenarios.get(choice)

    if selected is None:
        print("Invalid selection. Please choose 1, 2, 3 or 4.")
    else:
        run_resq_ai(selected)
