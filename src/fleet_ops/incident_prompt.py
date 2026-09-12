from __future__ import annotations

import json

from .monitor import Health


def grounded_prompt(health: list[Health]) -> str:
    facts = [
        {
            "robot_id": item.robot_id,
            "state": item.state,
            "reasons": list(item.reasons),
            "age_s": item.age_s,
            "battery_pct": item.battery_pct,
        }
        for item in health
        if item.state != "healthy"
    ]
    return (
        "Summarize only the supplied fleet facts. Return JSON with keys incidents and next_checks. "
        "Do not infer causes not present in reasons. FACTS=" + json.dumps(facts, sort_keys=True)
    )
