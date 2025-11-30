# Munder Difflin Multi-Agent System Project

Welcome to the starter code repository for the **Munder Difflin Paper Company Multi-Agent System Project**! This repository contains the starter code and tools you will need to design, build, and test a multi-agent system that supports core business operations at a fictional paper manufacturing company.

## Project Context

You’ve been hired as an AI consultant by Munder Difflin Paper Company, a fictional enterprise looking to modernize their workflows. They need a smart, modular **multi-agent system** to automate:

- **Inventory checks** and restocking decisions
- **Quote generation** for incoming sales inquiries
- **Order fulfillment** including supplier logistics and transactions

Your solution must use a maximum of **5 agents** and process inputs and outputs entirely via **text-based communication**.

This project challenges your ability to orchestrate agents using modern Python frameworks like `smolagents`, `pydantic-ai`, or `npcsh`, and combine that with real data tools like `sqlite3`, `pandas`, and LLM prompt engineering.

---

## What’s Included

From the `project.zip` starter archive, you will find:

- `project_starter.py`: The main Python script you will modify to implement your agent system
- `quotes.csv`: Historical quote data used for reference by quoting agents
- `quote_requests.csv`: Incoming customer requests used to build quoting logic
- `quote_requests_sample.csv`: A set of simulated test cases to evaluate your system

---

## Workspace Instructions

All the files have been provided in the VS Code workspace on the Udacity platform. Please install the agent orchestration framework of your choice.

## Local setup instructions

1. Install dependencies

Make sure you have Python 3.8+ installed.

You can install all required packages using the provided requirements.txt file:

`pip install -r requirements.txt`

If you're using smolagents, install it separately:

`pip install smolagents`

For other options like pydantic-ai or npcsh[lite], refer to their documentation.

2. Create .env File

Add your OpenAI-compatible API key:

`UDACITY_OPENAI_API_KEY=your_openai_key_here`

This project uses a custom OpenAI-compatible proxy hosted at https://openai.vocareum.com/v1.

## How to Run the Project

Start by defining your agents in the `"YOUR MULTI AGENT STARTS HERE"` section inside `template.py`. Once your agent team is ready:

1. Run the `run_test_scenarios()` function at the bottom of the script.
2. This will simulate a series of customer requests.
3. Your system should respond by coordinating inventory checks, generating quotes, and processing orders.

Output will include:

- Agent responses
- Cash and inventory updates
- Final financial report
- A `test_results.csv` file with all interaction logs

---

## Tips for Success

- Start by sketching a **flow diagram** to visualize agent responsibilities and interactions.
- Test individual agent tools before full orchestration.
- Always include **dates** in customer requests when passing data between agents.
- Ensure every quote includes **bulk discounts** and uses past data when available.
- Use the **exact item names** from the database to avoid transaction failures.

---

## Submission Checklist

Make sure to submit the following files:

1. Your completed `template.py` or `project_starter.py` with all agent logic
2. A **workflow diagram** describing your agent architecture and data flow
3. A `README.txt` or `design_notes.txt` explaining how your system works
4. Outputs from your test run (like `test_results.csv`)

---

## Updated Run Instructions (Enhanced System)

### Environment
Dieses Projekt nutzt das vorhandene venv `py-3-13-9`. Falls du lokal arbeitest und kein identisches venv hast, kannst du ein neues erstellen:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements_local.txt
```

### Vollständiger Systemlauf
Verarbeitet alle Requests aus `quote_requests_sample.csv` und erzeugt `test_results.csv`:
```bash
cd Course-04/project
../../py-3-13-9/bin/python multi_agent_system.py
```

### Smoke-Test (nur erste Anfrage zur schnellen Prüfung)
```bash
cd Course-04/project
USE_SMOKE=1 ../../py-3-13-9/bin/python multi_agent_system.py
```

### Unit-Tests ausführen
```bash
cd Course-04/project
../../py-3-13-9/bin/python -m unittest discover -s tests -p 'test_*.py' -v
```

### Diagram rendering (optional)
If Node.js is available, you can render the Mermaid diagram to PNG/SVG:
```bash
cd Course-04/project
chmod +x render_diagram.sh
./render_diagram.sh workflow.mmd
```

### Wichtige Dateien
- `multi_agent_system.py`: Konsolidierte Implementierung aller Agents und Tools
- `workflow.mmd`: Mermaid Diagramm der Agenten-Architektur
- `requirements_local.txt`: Gepinnte Abhängigkeiten (falls `requirements.txt` leer ist)
- `tests/test_core.py`: Unit-Tests für Kernlogik
- `test_results.csv`: Output nach vollständigem Lauf

### Funktionale Verbesserungen
- Synonym-Normalisierung für Item-Namen (reduziert Fehlkäufe)
- Caching von Lieferzeit-Berechnungen (vermeidet redundante Tool-Aufrufe)
- Smoke-Test Umschalter via `USE_SMOKE` Environment-Variable
- Robuste Fehlerausgaben mit konsistentem Prefix

### Bewertungskriterien Abdeckung (Rubric)
| Kriterium | Status |
|-----------|--------|
| Architekturdiagramm | Vorhanden (`workflow.mmd`) |
| Max. 5 Agents | 4 implementiert (Orchestrator, Inventory, Quote, Sales) |
| Tools nutzen DB-Funktionen | Erfüllt (siehe Mapping im Diagramm) |
| Fehlerbehandlung & kein Endlosloop | Erfüllt (deterministische Iteration, try/except) |
| Finanz-/Inventar-Updates | Erfüllt (Berichte nach jeder Anfrage) |
| Output-Transparenz | Erfüllt (Kunden-orientierte Antwort + System-Report) |
| Tests | Basis-Unit-Tests vorhanden |

---

## Notes

See `design_notes.md` for architectural decisions, error handling, testing scope, and file map.
