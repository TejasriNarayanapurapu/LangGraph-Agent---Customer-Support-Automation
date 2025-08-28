import argparse, json, yaml, time, random, os
from typing import Dict, Any, List, Tuple
from .mcp.clients import CommonClient, AtlasClient

CLIENTS = {"COMMON": CommonClient(), "ATLAS": AtlasClient()}

class LangGraphAgent:
    """
    Langie — a structured and logical Lang Graph Agent.
    - Thinks in stages (nodes).
    - Persists state across stages.
    - Executes deterministic or non-deterministic logic.
    - Orchestrates MCP clients to route abilities to COMMON/ATLAS.
    - Logs every decision and outputs a final structured payload.
    """
    def __init__(self, config: Dict[str, Any], input_payload: Dict[str, Any]):
        self.config = config
        self.state: Dict[str, Any] = dict(input_payload)
        self.logs: List[str] = []
        self.start_time = time.time()

    def log(self, message: str) -> None:
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.logs.append(f"[{ts}] {message}")

    def _exec_ability(self, ability: Dict[str, Any]) -> None:
        name = ability["name"]
        server = ability["server"]
        client = CLIENTS[server]
        self.log(f"Ability: {name} | Server: {server}")
        result = client.execute(name, self.state)
        # Merge result into state
        if isinstance(result, dict):
            self.state.update(result)
        else:
            self.state[name] = result

    def _run_deterministic(self, stage: Dict[str, Any]) -> None:
        for ability in stage.get("abilities", []):
            self._exec_ability(ability)

    def _run_decide(self, stage: Dict[str, Any]) -> None:
        # Non-deterministic: choose abilities based on solution score
        # 1) Always evaluate solution
        eval_ability = next(a for a in stage["abilities"] if a["name"] == "solution_evaluation")
        self._exec_ability(eval_ability)
        score = self.state.get("solution_score", 0)
        self.log(f"Decision: solution_score={score} (threshold=90)")
        # 2) If score < 90 -> escalate via ATLAS
        if score < 90:
            esc_ability = next(a for a in stage["abilities"] if a["name"] == "escalation_decision")
            self._exec_ability(esc_ability)
        # 3) Always update payload state
        upd_ability = next(a for a in stage["abilities"] if a["name"] == "update_payload")
        self._exec_ability(upd_ability)

    def run(self) -> Tuple[Dict[str, Any], List[str]]:
        for stage in self.config["stages"]:
            name = stage["name"]
            mode = stage["mode"]
            self.log(f"=== Stage: {name} | Mode: {mode} ===")
            if mode == "deterministic":
                self._run_deterministic(stage)
            elif mode == "non-deterministic":
                self._run_decide(stage)
            else:
                self.log(f"Unknown mode '{mode}' — skipping.")
        # Complete payload
        self.state["workflow_completed"] = True
        self.state["completed_at"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.log("Workflow complete.")
        return self.state, self.logs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", default="outputs/final_payload.json")
    parser.add_argument("--log", default="outputs/demo_logs.txt")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)
    with open(args.input) as f:
        payload = json.load(f)

    agent = LangGraphAgent(config, payload)
    final_state, logs = agent.run()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(final_state, f, indent=2)
    with open(args.log, "w") as f:
        f.write("\n".join(logs))

    print("=== Final Payload ===")
    print(json.dumps(final_state, indent=2))
    print("\n=== Execution Logs (tail) ===")
    for line in logs[-10:]:
        print(line)

if __name__ == "__main__":
    main()
