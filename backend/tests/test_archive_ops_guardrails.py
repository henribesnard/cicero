import json
from pathlib import Path

import tools.archive_ops_guardrails as archive


def test_build_snapshot_keeps_compact_archivable_shape(monkeypatch):
    monkeypatch.setattr(
        archive.ops,
        "build_report",
        lambda **kwargs: {
            "summary": {
                "status": "light",
                "cleanup_review_needed": True,
                "actionable_cleanup_count": 2,
                "recommendations": ["Mode léger", "Revoir nettoyage"],
            },
            "health": {
                "load": {"load_1m": 0.1, "load_5m": 0.2, "load_15m": 0.3},
                "memory": {"total_mb": 3915, "free_mb": 200, "available_mb": 700},
                "disk": {"path": "/", "total_gb": 48.0, "used_gb": 34.0, "free_gb": 14.0, "used_percent": 70.1},
            },
            "cleanup": {"total_candidate_size_mb": 512},
        },
    )

    snapshot = archive.build_snapshot(observed_at="2026-06-04T12:00:00Z", cleanup_paths=[Path("/tmp")])

    assert snapshot == {
        "schema_version": "ops-guardrails-snapshot-v1",
        "mode": "archive-jsonl",
        "observed_at": "2026-06-04T12:00:00Z",
        "status": "light",
        "load": {"load_1m": 0.1, "load_5m": 0.2, "load_15m": 0.3},
        "memory": {"total_mb": 3915, "free_mb": 200, "available_mb": 700},
        "disk": {"path": "/", "total_gb": 48.0, "used_gb": 34.0, "free_gb": 14.0, "used_percent": 70.1},
        "cleanup": {"review_needed": True, "total_candidate_size_mb": 512, "actionable_candidate_count": 2},
        "recommendation_count": 2,
    }


def test_append_snapshot_writes_jsonl_row(tmp_path):
    output = tmp_path / "ops" / "snapshots.jsonl"
    snapshot = {"schema_version": "ops-guardrails-snapshot-v1", "status": "normal"}

    written = archive.append_snapshot(snapshot, output)

    assert written == output
    rows = output.read_text(encoding="utf-8").splitlines()
    assert len(rows) == 1
    assert json.loads(rows[0]) == snapshot
