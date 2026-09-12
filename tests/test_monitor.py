from fleet_ops.monitor import assess


def test_fresh_robot_is_healthy() -> None:
    result = assess({"robot_id": "a", "timestamp_s": 100.0, "battery_pct": 80, "x_m": 0, "y_m": 0, "faults": []}, 105.0)
    assert result.state == "healthy"


def test_stale_low_battery_is_degraded() -> None:
    result = assess({"robot_id": "a", "timestamp_s": 0.0, "battery_pct": 10, "x_m": 0, "y_m": 0, "faults": []}, 20.0)
    assert result.state == "degraded"
    assert "telemetry_stale" in result.reasons
