from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Health:
    robot_id: str
    state: str
    reasons: tuple[str, ...]
    age_s: float
    battery_pct: float


def assess(message: dict[str, Any], now_s: float, stale_after_s: float = 15.0) -> Health:
    required = {"robot_id", "timestamp_s", "battery_pct", "x_m", "y_m", "faults"}
    missing = required - message.keys()
    if missing:
        raise ValueError(f"missing telemetry fields: {sorted(missing)}")
    age = max(0.0, now_s - float(message["timestamp_s"]))
    battery = float(message["battery_pct"])
    faults = tuple(str(fault) for fault in message["faults"])
    reasons: list[str] = list(faults)
    if age > stale_after_s:
        reasons.append("telemetry_stale")
    if battery < 20:
        reasons.append("battery_low")
    state = "fault" if faults else "degraded" if len(reasons) else "healthy"
    return Health(str(message["robot_id"]), state, tuple(reasons), age, battery)
