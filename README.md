# Lang Graph Agent – Customer Support Workflow (Langie)

This repo implements a **stage-based Customer Support Agent** (“Langie”) that models workflows as a graph with **state persistence**, **deterministic** and **non-deterministic** stages, and **MCP client orchestration** to route abilities to **COMMON** (internal) or **ATLAS** (external) servers.

## ✨ Features
- 11 stages mapped 1:1 to the specification (INTAKE → COMPLETE)
- Deterministic stages run in sequence; **DECIDE** is non-deterministic
- State variables are persisted and enriched across stages
- MCP clients for COMMON (no external data) and ATLAS (external/system actions)
- Clear, human-readable logs per stage & ability
- Demo runner + unit test

## 🧱 Project Structure
```
lang-graph-agent/
├─ README.md
├─ requirements.txt
├─ agent_config.yaml
├─ sample_input.json
├─ src/
│  ├─ agent.py
│  └─ mcp/
│     └─ clients.py
├─ outputs/
│  ├─ final_payload.json
│  └─ demo_logs.txt
├─ tests/
│  └─ test_flow.py
└─ run_demo.sh
```

## ⚙️ Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Run Demo
```bash
python -m src.agent --config agent_config.yaml --input sample_input.json --out outputs/final_payload.json --log outputs/demo_logs.txt
```
Or use the shell script (Unix/macOS):
```bash
bash run_demo.sh
```

## 🧪 Run Tests
```bash
pytest -q
```
Example output

{
  "customer_name": "Alice Kumar",
  "query": "Payment failed for order #ORD-7789 on 24 Aug...",
  "priority": "high",
  "decision": "escalate",
  "ticket_status": "In Progress"
}

Author
Tejasri Narayanapurapu
