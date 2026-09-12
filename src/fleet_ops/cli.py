from __future__ import annotations

import argparse
import json
from pathlib import Path

from .incident_prompt import grounded_prompt
from .monitor import assess


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("telemetry_jsonl", type=Path)
    parser.add_argument("--now", required=True, type=float, help="evaluation time in the same clock domain as telemetry")
    args = parser.parse_args()
    health = []
    for line in args.telemetry_jsonl.read_text(encoding="utf-8").splitlines():
        if line.strip():
            health.append(assess(json.loads(line), args.now))
    for item in health:
        print(json.dumps({"robot_id": item.robot_id, "state": item.state, "reasons": item.reasons, "age_s": item.age_s, "battery_pct": item.battery_pct}, sort_keys=True))
    print(json.dumps({"vllm_grounded_prompt": grounded_prompt(health)}, sort_keys=True))


if __name__ == "__main__":
    main()
