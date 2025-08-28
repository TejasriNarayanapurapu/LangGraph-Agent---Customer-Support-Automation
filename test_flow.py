import json, yaml, os
from src.agent import LangGraphAgent

def test_decide_branching():
    # force configuration
    with open("agent_config.yaml") as f:
        cfg = yaml.safe_load(f)
    payload = {
        "customer_name": "Test",
        "email": "t@example.com",
        "query": "Card charged but order failed.",
        "priority": "high",
        "ticket_id": "T-1"
    }
    agent = LangGraphAgent(cfg, payload)
    final_state, logs = agent.run()
    assert "decision" in final_state
    assert final_state["decision"] in {"resolve","escalate"}
    assert final_state.get("workflow_completed") is True
