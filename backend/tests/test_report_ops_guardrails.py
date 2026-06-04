from pathlib import Path

import tools.report_ops_guardrails as ops


def _review_plan_stub(items):
    return {
        "schema_version": "cleanup-review-plan-v1",
        "mode": "report-only",
        "review_item_count": len(items),
        "review_items": items,
        "guardrails": ["Aucune suppression automatique."],
    }


def test_build_report_combines_health_and_actionable_cleanup(monkeypatch):
    monkeypatch.setattr(
        ops.health,
        "build_report",
        lambda disk_path=Path("/"): {
            "schema_version": "vps-health-v1",
            "mode": "report-only",
            "status": "light",
            "cleanup_review_needed": False,
            "recommendations": ["Mode léger: privilégier veille, tri, rédaction, tests ciblés; éviter builds/téléchargements lourds."],
            "memory": {"free_mb": 200, "available_mb": 700},
            "disk": {"used_percent": 69.7},
        },
    )
    monkeypatch.setattr(
        ops.cleanup,
        "build_report",
        lambda candidates: {
            "schema_version": "safe-cleanup-candidates-v1",
            "mode": "report-only",
            "disk": {"used_percent": 69.7},
            "total_candidate_size_mb": 250,
            "candidates": [
                {"path": "/tmp/big", "exists": True, "size_mb": 200, "note": "candidate: inspect before manual cleanup"},
                {"path": "/tmp/tiny", "exists": True, "size_mb": 50, "note": "candidate: inspect before manual cleanup"},
            ],
            "recommended_manual_actions": [],
            "guardrails": ["No deletion is performed by this script."],
        },
    )
    monkeypatch.setattr(
        ops.cleanup_plan,
        "build_plan",
        lambda min_size_mb=100, limit=None, candidate_paths=None: _review_plan_stub(
            [
                {
                    "path": "/tmp/big",
                    "size_mb": 200,
                    "category": "system-temp",
                    "cleanup_risk": "medium",
                    "urgency": "medium",
                    "rationale": "review manually",
                    "manual_checks": ["inspect"],
                    "allowed_automation": "none",
                    "requires_human_validation": True,
                }
            ]
        ),
    )

    report = ops.build_report(top_cleanup=2, min_cleanup_size_mb=100, cleanup_paths=[Path("/tmp")])

    assert report["schema_version"] == "ops-guardrails-v1"
    assert report["mode"] == "report-only"
    assert report["summary"]["status"] == "light"
    assert report["summary"]["cleanup_review_needed"] is True
    assert report["summary"]["actionable_cleanup_count"] == 1
    assert report["summary"]["manual_review_item_count"] == 1
    assert report["cleanup"]["actionable_candidates"] == [
        {"path": "/tmp/big", "exists": True, "size_mb": 200, "note": "candidate: inspect before manual cleanup"}
    ]
    assert report["cleanup_review_plan"]["review_items"][0]["allowed_automation"] == "none"
    assert "Revoir 1 candidat(s) de nettoyage non destructif avant tout ménage manuel." in report["summary"]["recommendations"]


def test_build_report_reports_no_candidates_without_destructive_action(monkeypatch):
    monkeypatch.setattr(
        ops.health,
        "build_report",
        lambda disk_path=Path("/"): {
            "schema_version": "vps-health-v1",
            "mode": "report-only",
            "status": "normal",
            "cleanup_review_needed": False,
            "recommendations": [],
            "memory": {"free_mb": 1000, "available_mb": 1500},
            "disk": {"used_percent": 50.0},
        },
    )
    monkeypatch.setattr(
        ops.cleanup,
        "build_report",
        lambda candidates: {
            "schema_version": "safe-cleanup-candidates-v1",
            "mode": "report-only",
            "disk": {"used_percent": 50.0},
            "total_candidate_size_mb": 0,
            "candidates": [],
            "recommended_manual_actions": [],
            "guardrails": ["No deletion is performed by this script."],
        },
    )
    monkeypatch.setattr(
        ops.cleanup_plan,
        "build_plan",
        lambda min_size_mb=100, limit=None, candidate_paths=None: _review_plan_stub([]),
    )

    report = ops.build_report(cleanup_paths=[Path("/tmp/empty")])

    assert report["summary"] == {
        "status": "normal",
        "cleanup_review_needed": False,
        "actionable_cleanup_count": 0,
        "manual_review_item_count": 0,
        "recommendations": ["Aucun candidat de nettoyage détecté dans les chemins conservateurs."],
    }
    assert report["cleanup"]["guardrails"] == ["No deletion is performed by this script."]


def test_build_compact_summary_keeps_only_cron_decision_fields():
    report = {
        "schema_version": "ops-guardrails-v1",
        "mode": "report-only",
        "health": {
            "status": "light",
            "memory": {"free_mb": 118, "available_mb": 706},
            "disk": {"used_percent": 70.0},
        },
        "cleanup": {"total_candidate_size_mb": 4593},
        "cleanup_review_plan": {
            "review_items": [
                {"path": "/home/hermes/.cache"},
                {"path": "/var/log"},
            ]
        },
        "summary": {
            "status": "light",
            "cleanup_review_needed": True,
            "actionable_cleanup_count": 3,
            "manual_review_item_count": 2,
            "recommendations": ["Mode léger."],
        },
    }

    compact = ops.build_compact_summary(report)

    assert compact == {
        "schema_version": "ops-guardrails-compact-v1",
        "mode": "report-only",
        "status": "light",
        "vps": {
            "ram_free_mb": 118,
            "ram_available_mb": 706,
            "disk_used_percent": 70.0,
            "cleanup_review_needed": True,
        },
        "cleanup": {
            "total_candidate_size_mb": 4593,
            "actionable_count": 3,
            "manual_review_item_count": 2,
            "top_review_paths": ["/home/hermes/.cache", "/var/log"],
        },
        "recommendations": ["Mode léger."],
    }
