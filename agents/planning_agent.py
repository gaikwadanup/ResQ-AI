
import json
import ollama

MODEL_NAME = "llama3.2:3b"

ALLOWED_TOOLS = [
    "routine_monitoring",
    "resource_lookup",
    "distance_ranking",
    "generate_report"
]


def create_execution_plan(weather, risk, ai_decision):
    """
    AI Planning Agent.
    Selects which approved workflow tools should execute.
    """

    risk_level = risk.get("risk_level", "UNKNOWN").upper()

    prompt = f"""
You are the AI Planning Agent of ResQ AI.

Your task is to select the appropriate workflow tools.

Weather:
{json.dumps(weather, indent=2)}

Risk assessment:
{json.dumps(risk, indent=2)}

AI decision:
{json.dumps(ai_decision, indent=2)}

Available tools:
- routine_monitoring
- resource_lookup
- distance_ranking
- generate_report

Rules:
- LOW risk: select routine_monitoring and generate_report.
- MODERATE risk: select resource_lookup, distance_ranking and generate_report.
- HIGH risk: select resource_lookup, distance_ranking and generate_report.
- Never select tools outside the available list.
- Do not claim that resources have actually been deployed.
- Return only valid JSON.

Required format:
{{
    "tools": ["tool_name"],
    "reasoning": "Explain why these tools were selected"
}}
"""

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            format="json",
            options={"temperature": 0.1}
        )

        result = json.loads(response["message"]["content"])

        selected_tools = result.get("tools", [])

        if not isinstance(selected_tools, list):
            selected_tools = []

        # Remove tools that are not approved.
        selected_tools = [
            tool for tool in selected_tools
            if tool in ALLOWED_TOOLS
        ]

        # SAFETY VALIDATION
        # The risk assessment determines the minimum required tools.
        if risk_level in ["MODERATE", "HIGH"]:
            required_tools = [
                "resource_lookup",
                "distance_ranking",
                "generate_report"
            ]

            selected_tools = required_tools

        elif risk_level == "LOW":
            selected_tools = [
                "routine_monitoring",
                "generate_report"
            ]

        else:
            selected_tools = ["routine_monitoring"]

        return {
            "tools": selected_tools,
            "reasoning": result.get(
                "reasoning",
                "Execution plan validated by safety rules."
            ),
            "planner_status": "SUCCESS"
        }

    except Exception as error:
        print("Planning Agent Error:", error)

        # Safe fallback plan.
        if risk_level in ["MODERATE", "HIGH"]:
            tools = [
                "resource_lookup",
                "distance_ranking",
                "generate_report"
            ]
        else:
            tools = [
                "routine_monitoring",
                "generate_report"
            ]

        return {
            "tools": tools,
            "reasoning": (
                "AI planning unavailable. "
                "A predefined safety plan was selected."
            ),
            "planner_status": "FALLBACK"
        }
