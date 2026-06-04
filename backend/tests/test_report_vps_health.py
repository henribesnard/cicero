from pathlib import Path

import tools.report_vps_health as health


def test_memory_status_parses_proc_meminfo(tmp_path):
    meminfo = tmp_path / "meminfo"
    meminfo.write_text(
        "MemTotal:        4005888 kB\n"
        "MemFree:          512000 kB\n"
        "MemAvailable:    900096 kB\n"
        "Buffers:           12345 kB\n",
        encoding="utf-8",
    )

    assert health.memory_status(meminfo) == {"total_mb": 3912, "free_mb": 500, "available_mb": 879}


def test_build_report_switches_to_light_mode_on_low_free_ram(monkeypatch):
    monkeypatch.setattr(health, "memory_status", lambda: {"total_mb": 3900, "free_mb": 167, "available_mb": 754})
    monkeypatch.setattr(health, "load_status", lambda: {"load_1m": 0.01, "load_5m": 0.02, "load_15m": 0.03})
    monkeypatch.setattr(
        health,
        "disk_status",
        lambda path=Path("/"): {"path": "/", "total_gb": 48.0, "used_gb": 33.6, "free_gb": 14.4, "used_percent": 70.0},
    )

    report = health.build_report()

    assert report["schema_version"] == "vps-health-v1"
    assert report["mode"] == "report-only"
    assert report["status"] == "light"
    assert report["cleanup_review_needed"] is False
    assert report["reserve_disk_free_gb"] == 4.8
    assert report["recommendations"] == [
        "Mode léger: privilégier veille, tri, rédaction, tests ciblés; éviter builds/téléchargements lourds."
    ]


def test_build_report_flags_high_load_and_disk_above_threshold(monkeypatch):
    monkeypatch.setattr(health, "memory_status", lambda: {"total_mb": 3900, "free_mb": 1200, "available_mb": 1600})
    monkeypatch.setattr(health, "load_status", lambda: {"load_1m": 3.0, "load_5m": 1.0, "load_15m": 0.5})
    monkeypatch.setattr(
        health,
        "disk_status",
        lambda path=Path("/"): {"path": "/", "total_gb": 50.0, "used_gb": 36.0, "free_gb": 14.0, "used_percent": 72.0},
    )

    report = health.build_report()

    assert report["status"] == "light"
    assert report["cleanup_review_needed"] is True
    assert report["recommendations"] == [
        "Mode léger: privilégier veille, tri, rédaction, tests ciblés; éviter builds/téléchargements lourds.",
        "Disque >70%: proposer un ménage non destructif des caches/logs/temp, sans toucher au serveur web.",
    ]


def test_build_report_warns_when_disk_reserve_is_touched(monkeypatch):
    monkeypatch.setattr(health, "memory_status", lambda: {"total_mb": 3900, "free_mb": 1200, "available_mb": 1600})
    monkeypatch.setattr(health, "load_status", lambda: {"load_1m": 0.1, "load_5m": 0.1, "load_15m": 0.1})
    monkeypatch.setattr(
        health,
        "disk_status",
        lambda path=Path("/"): {"path": "/", "total_gb": 100.0, "used_gb": 92.0, "free_gb": 8.0, "used_percent": 92.0},
    )

    report = health.build_report()

    assert report["status"] == "normal"
    assert report["cleanup_review_needed"] is True
    assert report["recommendations"] == [
        "Disque >70%: proposer un ménage non destructif des caches/logs/temp, sans toucher au serveur web.",
        "Réserve disque 10% entamée: éviter nouveaux artefacts avant arbitrage.",
    ]
