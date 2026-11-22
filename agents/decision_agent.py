
import json
import ollama

MODEL_NAME = "llama3.2:3b"


def make_ai_decision(weather, risk, resources=None):
    """
    Local AI Decision Agent.
    Analyses weather and risk information and recommends
    the next action for ResQ AI.
    """

    if resources is None:
        resources = []

    input_data = {
        "weather": weather,
        "risk": risk,
        "available_resources": resources
    }

    prompt = f"""
You are the AI Decision Agent of ResQ AI,
a disaster management coordination system for Sangli, Maharashtra.

Analyse the following information:

{json.dumps(input_data, indent=2)}

Your responsibilities:
1. Understand current weather conditions.
2. Evaluate the supplied risk assessment.
3. Decide the appropriate response level.
4. Recommend resource preparation.
5. Explain your reasoning.

Return ONLY valid JSON:

{{
    "decision": "MONITOR or PREPARE or MOBILIZE",
    "priority": "LOW or MODERATE or HIGH",
    "reasoning": "Explain your decision",
    "recommended_actions": [
        "Action 1",
        "Action 2"
    ],
    "resource_recommendation": "Explain resource requirements"
}}

Rules:
- LOW risk: MONITOR.
- MODERATE risk: PREPARE.
- HIGH risk: MOBILIZE.
- Never claim that alerts were sent or resources deployed.
- Never invent weather measurements or resource availability.
- Recommendations require human authority review.
"""

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            format="json",
            options={"temperature": 0.2}
        )

        result = json.loads(response["message"]["content"])

        # SAFETY GUARDRAIL
        # Rule-based risk assessment has final authority.
        risk_level = risk.get("risk_level", "UNKNOWN").upper()

        if risk_level == "HIGH":
            result["decision"] = "MOBILIZE"
            result["priority"] = "HIGH"
            result["reasoning"] = (
                "HIGH risk detected by the Risk Agent. "
                "Safety guardrail overrides any lower AI recommendation. "
                "Emergency resources should be prepared for human review."
            )
            result["recommended_actions"] = [
                "Notify responsible emergency authorities through approved channels",
                "Prepare ambulance, rescue team and shelter resources",
                "Identify vulnerable populations and high-risk areas",
                "Continue monitoring weather conditions"
            ]
            result["resource_recommendation"] = (
                "Prepare available emergency resources. "
                "Actual deployment requires human authority approval."
            )

        elif risk_level == "MODERATE":
            result["decision"] = "PREPARE"
            result["priority"] = "MODERATE"

        elif risk_level == "LOW":
            result["decision"] = "MONITOR"
            result["priority"] = "LOW"

        else:
            result["decision"] = "MONITOR"
            result["priority"] = "UNKNOWN"
            result["reasoning"] = (
                "Risk level is unknown. Manual assessment is required."
            )

        print("\n===== RESQ AI DECISION AGENT =====")
        print("Decision:", result["decision"])
        print("Priority:", result["priority"])
        print("Reasoning:", result["reasoning"])
        print("Recommended Actions:")

        for action in result["recommended_actions"]:
            print("-", action)

        print(
            "Resource Recommendation:",
            result["resource_recommendation"]
        )

        return result

    except Exception as error:
        print("AI Decision Agent Error:", error)

        # Safety fallback even if the local AI fails.
        risk_level = risk.get("risk_level", "UNKNOWN").upper()

        if risk_level == "HIGH":
            decision = "MOBILIZE"
            priority = "HIGH"
        elif risk_level == "MODERATE":
            decision = "PREPARE"
            priority = "MODERATE"
        else:
            decision = "MONITOR"
            priority = "UNKNOWN" if risk_level == "UNKNOWN" else "LOW"

        return {
            "decision": decision,
            "priority": priority,
            "reasoning": (
                "Local AI unavailable. Decision follows the "
                "rule-based safety assessment. Human review required."
            ),
            "recommended_actions": [
                "Verify weather and risk information",
                "Have responsible authorities review the situation"
            ],
            "resource_recommendation": (
                "No automated resource deployment. Human approval required."
            )
        }


if __name__ == "__main__":

    sample_weather = {
        "location": "Sangli, Maharashtra",
        "temperature": 28,
        "rainfall": 0,
        "wind_speed": 10
    }

    sample_risk = {
        "risk_score": 0,
        "risk_level": "LOW",
        "reasons": ["No significant weather indicators detected"]
    }

    make_ai_decision(sample_weather, sample_risk)
