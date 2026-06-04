from pathlib import Path

import tools.report_ops_guardrails_daily as daily


def _guardrail_stub(*, status="light"):
    return {
        "schema_version": "ops-guardrails-v1",
        "mode": "report-only",
        "health": {
            "status": status,
            "memory": {"free_mb": 120, "available_mb": 690},
            "disk": {"used_percent": 70.0},
        },
        "cleanup": {"total_candidate_size_mb": 4200},
        "cleanup_review_plan": {
            "review_items": [
                {"path": "/home/hermes/.cache"},
                {"path": "/var/log"},
            ]
        },
        "summary": {
            "status": status,
            "cleanup_review_needed": True,
            "actionable_cleanup_count": 2,
            "manual_review_item_count": 2,
            "recommendations": ["Mode léger."],
        },
    }


def _trend_stub(*, status="light"):
    return {
        "schema_version": "ops-guardrails-trend-v1",
        "mode": "report-only",
        "snapshot_count": 3,
        "status": status,
        "memory": {
            "min_free_mb": 110,
            "avg_free_mb": 150.3,
            "delta_free_mb": -40,
        },
        "disk": {
            "max_used_percent": 70.1,
            "delta_used_percent": 0.2,
        },
        "cleanup": {
            "last_total_candidate_size_mb": 4200,
            "last_review_needed": True,
        },
        "recommendations": ["Candidats de nettoyage présents: revue manuelle uniquement, aucune suppression automatique."],
    }


def test_build_daily_report_combines_current_guardrails_and_trend(monkeypatch, tmp_path):
    monkeypatch.setattr(daily.guardrails, "build_report", lambda **kwargs: _guardrail_stub())
    monkeypatch.setattr(daily.guardrails, "build_compact_summary", daily.guardrails.build_compact_summary)
    monkeypatch.setattr(daily.trend, "load_snapshots", lambda input_path, limit=7: [{"snapshot": 1}])
    monkeypatch.setattr(daily.trend, "build_trend", lambda snapshots: _trend_stub())

    report = daily.build_daily_report(trend_input=tmp_path / "ops.jsonl", trend_limit=5, cleanup_paths=[Path("/tmp")])

    assert report["schema_version"] == "ops-guardrails-daily-v1"
    assert report["mode"] == "report-only"
    assert report["status"] == "light"
    assert report["current"]["vps"]["ram_free_mb"] == 120
    assert report["trend"]["snapshot_count"] == 3
    assert report["recommendations"] == [
        "Mode léger.",
        "Candidats de nettoyage présents: revue manuelle uniquement, aucune suppression automatique.",
    ]


def test_build_markdown_includes_paths_trend_and_report_only():
    report = {
        "schema_version": "ops-guardrails-daily-v1",
        "mode": "report-only",
        "status": "light",
        "current": daily.guardrails.build_compact_summary(_guardrail_stub()),
        "trend": _trend_stub(),
        "recommendations": ["Mode léger."],
    }

    markdown = daily.build_markdown(report)

    assert markdown.startswith("# Rapport quotidien ops guardrails")
    assert "- Statut combiné: `light`" in markdown
    assert "- RAM actuelle: 120 MiB libres / 690 MiB disponibles" in markdown
    assert "- Tendance: `light` sur 3 snapshot(s)" in markdown
    assert "- RAM tendance: min 110 MiB, moyenne 150.3 MiB, delta -40 MiB" in markdown
    assert "- `/home/hermes/.cache`" in markdown
    assert markdown.endswith("_Mode report-only: aucune suppression ni mutation système._")


def test_build_markdown_handles_empty_trend_without_metric_lines():
    report = {
        "schema_version": "ops-guardrails-daily-v1",
        "mode": "report-only",
        "status": "normal",
        "current": daily.guardrails.build_compact_summary(_guardrail_stub(status="normal")),
        "trend": {
            "schema_version": "ops-guardrails-trend-v1",
            "mode": "report-only",
            "snapshot_count": 0,
            "status": "no_data",
            "recommendations": ["Aucune archive ops disponible."],
        },
        "recommendations": ["Aucune archive ops disponible."],
    }

    markdown = daily.build_markdown(report)

    assert "- Tendance: `no_data` sur 0 snapshot(s)" in markdown
    assert "RAM tendance" not in markdown
    assert "Disque tendance" not in markdown
