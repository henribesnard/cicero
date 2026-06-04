import json

import pytest

import tools.report_ops_guardrails_trend as trend


def snapshot(observed_at: str, *, free_mb: int, available_mb: int, disk_used: float, cleanup_mb: int, status: str = "normal"):
    return {
        "schema_version": "ops-guardrails-snapshot-v1",
        "observed_at": observed_at,
        "status": status,
        "memory": {"free_mb": free_mb, "available_mb": available_mb, "total_mb": 3915},
        "disk": {"used_percent": disk_used, "path": "/"},
        "cleanup": {"total_candidate_size_mb": cleanup_mb, "review_needed": cleanup_mb > 0},
    }


def test_load_snapshots_keeps_last_valid_rows(tmp_path):
    archive = tmp_path / "ops.jsonl"
    rows = [
        snapshot("2026-06-04T10:00:00Z", free_mb=900, available_mb=1200, disk_used=68.5, cleanup_mb=0),
        {"schema_version": "other"},
        snapshot("2026-06-04T11:00:00Z", free_mb=700, available_mb=900, disk_used=69.5, cleanup_mb=256, status="light"),
        snapshot("2026-06-04T12:00:00Z", free_mb=650, available_mb=850, disk_used=70.2, cleanup_mb=512, status="light"),
    ]
    archive.write_text("\n".join([json.dumps(rows[0]), "not-json", json.dumps(rows[1]), json.dumps(rows[2]), "", json.dumps(rows[3])]), encoding="utf-8")

    loaded = trend.load_snapshots(archive, limit=2)

    assert [row["observed_at"] for row in loaded] == ["2026-06-04T11:00:00Z", "2026-06-04T12:00:00Z"]


def test_load_snapshots_requires_positive_limit(tmp_path):
    with pytest.raises(ValueError, match="limit must be positive"):
        trend.load_snapshots(tmp_path / "missing.jsonl", limit=0)


def test_build_trend_reports_light_mode_and_deltas():
    snapshots = [
        snapshot("2026-06-04T10:00:00Z", free_mb=900, available_mb=1200, disk_used=68.5, cleanup_mb=0),
        snapshot("2026-06-04T12:00:00Z", free_mb=650, available_mb=850, disk_used=70.2, cleanup_mb=512, status="light"),
    ]

    report = trend.build_trend(snapshots)

    assert report["schema_version"] == "ops-guardrails-trend-v1"
    assert report["mode"] == "report-only"
    assert report["snapshot_count"] == 2
    assert report["status"] == "light"
    assert report["memory"]["delta_free_mb"] == -250
    assert report["memory"]["min_free_mb"] == 650
    assert report["disk"]["delta_used_percent"] == 1.7
    assert report["cleanup"]["last_review_needed"] is True
    assert "Mode léger recommandé" in report["recommendations"][0]


def test_build_trend_handles_empty_archive():
    report = trend.build_trend([])

    assert report == {
        "schema_version": "ops-guardrails-trend-v1",
        "mode": "report-only",
        "snapshot_count": 0,
        "status": "no_data",
        "recommendations": ["Aucune archive ops disponible: lancer archive_ops_guardrails.py avant la tendance."],
    }
