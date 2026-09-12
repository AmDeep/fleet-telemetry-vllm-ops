from fleet_ops.nvidia_health import parse_tegrastats


def test_parse_tegrastats_sample() -> None:
    result = parse_tegrastats("RAM 1200/4096MB (lfb 10x4MB) CPU [10%@1420,20%@1420] GR3D_FREQ 35%@918")
    assert result.ram_used_mb == 1200
    assert result.ram_total_mb == 4096
    assert result.gpu_util_pct == 35
    assert result.cpu_util_pct == 15
