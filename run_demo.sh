#!/usr/bin/env bash
set -euo pipefail
python -m src.agent --config agent_config.yaml --input sample_input.json --out outputs/final_payload.json --log outputs/demo_logs.txt
echo
echo '--- Final payload written to outputs/final_payload.json'
echo '--- Logs written to outputs/demo_logs.txt'
