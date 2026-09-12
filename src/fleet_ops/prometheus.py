from __future__ import annotations

from .monitor import Health
from .nvidia_health import JetsonHealth


def render_metrics(health: list[Health], jetson: JetsonHealth | None = None) -> str:
    lines: list[str] = []
    for item in health:
        labels = f'robot_id="{item.robot_id}"'
        lines.append(f"robot_health{{{labels}}} {1 if item.state == 'healthy' else 0}")
        lines.append(f"robot_battery_percent{{{labels}}} {item.battery_pct}")
        lines.append(f"robot_telemetry_age_seconds{{{labels}}} {item.age_s}")
    if jetson:
        lines.append(f"jetson_ram_used_megabytes {jetson.ram_used_mb}")
        lines.append(f"jetson_ram_total_megabytes {jetson.ram_total_mb}")
        if jetson.gpu_util_pct is not None:
            lines.append(f"jetson_gpu_utilization_percent {jetson.gpu_util_pct}")
        if jetson.cpu_util_pct is not None:
            lines.append(f"jetson_cpu_utilization_percent {jetson.cpu_util_pct}")
    return "\n".join(lines) + "\n"
