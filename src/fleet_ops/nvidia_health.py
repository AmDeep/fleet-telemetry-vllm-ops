from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class JetsonHealth:
    ram_used_mb: int
    ram_total_mb: int
    gpu_util_pct: float | None
    cpu_util_pct: float | None


def parse_tegrastats(line: str) -> JetsonHealth:
    ram = re.search(r"RAM\s+(\d+)/(\d+)MB", line)
    gpu = re.search(r"GR3D_FREQ\s+(\d+)%", line)
    cpu_section = re.search(r"CPU\s*\[([^\]]+)\]", line)
    cpu_values = [int(value) for value in re.findall(r"(\d+)%@\d+", cpu_section.group(1))] if cpu_section else []
    if not ram:
        raise ValueError("tegrastats line has no RAM used/total field")
    return JetsonHealth(int(ram.group(1)), int(ram.group(2)), float(gpu.group(1)) if gpu else None, sum(cpu_values) / len(cpu_values) if cpu_values else None)
