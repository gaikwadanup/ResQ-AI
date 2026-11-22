# ResQ AI – Agentic AI Disaster Coordination System

**Team Name:** AstraResQ  
**Tagline:** Intelligence That Protects. Technology That Saves.

ResQ AI is an AI-assisted disaster coordination prototype designed to monitor weather conditions, assess potential risks, recommend response actions, and support emergency resource coordination.

The project demonstrates how multiple specialized agents can work together through an orchestrated workflow to support disaster-response decision-making.

## Team Members

| Name |
|---|
| Anup Gaikwad |
| Prathmesh Gaikwad |
| Soham Kadam |

## Key Features

- **Weather Monitoring:** Retrieves current weather and forecast information using Open-Meteo.
- **Risk Assessment:** Evaluates weather conditions and assigns a LOW, MODERATE, or HIGH risk level.
- **AI Decision Support:** Uses a locally running Llama 3.2 model to generate response recommendations.
- **AI-Assisted Planning:** Recommends workflow tools according to the assessed risk level.
- **Resource Coordination:** Displays available simulated emergency resources.
- **Logistics Support:** Ranks simulated resources using approximate straight-line distances.
- **Interactive Dashboard:** Displays weather information, risk status, resource information, and agent execution logs.
- **Scenario Simulation:** Supports LIVE, LOW, MODERATE, and HIGH scenarios.

## Agent Architecture

ResQ AI uses a coordinated multi-agent workflow.

1. **Monitoring Agent** – Collects weather information.
2. **Risk Assessment Agent** – Calculates the risk score and risk category.
3. **Decision Agent** – Generates recommended response actions.
4. **Planning Agent** – Suggests the next workflow tools.
5. **Resource Agent** – Retrieves simulated emergency resources.
6. **Logistics Agent** – Ranks resources by approximate distance.
7. **Coordinator Agent** – Orchestrates the workflow using LangGraph.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| LangGraph | Agent workflow orchestration |
| Ollama | Local AI model execution |
| Llama 3.2 (3B) | AI-assisted decision-making |
| Streamlit | Interactive dashboard |
| Plotly | Charts and maps |
| Pandas | Data handling |
| Open-Meteo API | Weather information |

## Project Structure

```text
ResQ-AI/
│
├── agents/
│   ├── coordinator.py
│   ├── monitoring_agent.py
│   ├── risk_agent.py
│   ├── decision_agent.py
│   ├── planning_agent.py
│   ├── resource_agent.py
│   └── logistics_agent.py
│
├── backend/
│   ├── weather_api.py
│   ├── database.py
│   └── main.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── resources.json
│   └── vulnerable_areas.json
│
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/gaikwadanup/ResQ-AI.git
cd ResQ-AI
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install and configure Ollama

Install Ollama, then download the model:

```bash
ollama pull llama3.2:3b
```

Make sure the Ollama service is running before starting the application.

### 5. Run the command-line application

```bash
python -m agents.coordinator
```

### 6. Run the Streamlit dashboard

```bash
python -m streamlit run dashboard/app.py
```

Open the local URL displayed in the terminal to access the dashboard.

## Simulation Scenarios

ResQ AI supports four demonstration scenarios:

| Scenario | Purpose |
|---|---|
| LIVE | Uses current weather and forecast data |
| LOW | Demonstrates a low-risk situation |
| MODERATE | Demonstrates a moderate-risk situation |
| HIGH | Demonstrates a high-risk situation |

Example scenario test results:

| Scenario | Risk Score | Risk Level | Decision |
|---|---:|---|---|
| LOW | 0 | LOW | MONITOR |
| MODERATE | 3 | MODERATE | PREPARE |
| HIGH | 10 | HIGH | MOBILIZE |

LIVE scenario results depend on the weather conditions returned by the API.

## Important Limitations and Safety

- This is an educational prototype, not a certified emergency-response system.
- Risk thresholds are preliminary demonstration heuristics and are not official IMD warning thresholds.
- Weather information is obtained from Open-Meteo; the system does not directly monitor river levels, satellite imagery, or flood inundation.
- Resource records and their capacities are simulated demonstration data, not verified real-world facilities.
- Logistics distances are approximate straight-line distances, not road-network or traffic-based travel distances.
- The prototype does not send real emergency alerts, contact authorities, evacuate people, or dispatch resources.
- Human authority approval is required before any real-world emergency action.

## Future Scope

- Integration with verified government and emergency-service datasets.
- River-level and flood-monitoring integrations.
- GIS-based road-network routing.
- Real-time emergency notification integrations.
- More advanced risk prediction and validation.
- Secure interfaces for authorized disaster-management teams.

## Repository

GitHub: https://github.com/gaikwadanup/ResQ-AI

---

**Developed by Team AstraResQ**  
*Intelligence That Protects. Technology That Saves.*