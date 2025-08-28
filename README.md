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

## 📤 What to Submit
- Push this repo to GitHub
- Attach your latest resume
- Record a 3–5 min video walking through:
  - Stage modeling & non-determinism (DECIDE)
  - State persistence (payload growth across stages)
  - MCP orchestration (COMMON vs ATLAS)
  - Demo run + logs
- Email:
  - **To:** santosh.thota@analytos.ai
  - **Cc:** shashwat.shlok@analytos.ai, sasidhar.sunkesula@analytos.ai
  - **Subject:** `Lang Graph Agent Task – <your name>`

## ✅ Evaluation Rubric (Suggested)
1. Correct Stage Modeling (11/11 stages reflected)
2. Proper State Persistence (state carried & enriched)
3. MCP Integration (correct routing to COMMON/ATLAS)
4. Non-deterministic Orchestration (DECIDE with threshold)
5. Logs & Observability (stage/ability trace)
6. Final Structured Output Payload
7. Code Quality & README clarity

---

### Notes
- This reference implementation is dependency-light and **simulates** ATLAS/COMMON servers for demo repeatability. Replace stubs in `src/mcp/clients.py` with real MCP calls as needed.
