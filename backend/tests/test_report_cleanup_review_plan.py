from pathlib import Path

import tools.report_cleanup_review_plan as plan


def test_classify_path_assigns_known_categories():
    assert plan.classify_path("/home/hermes/.cache/pip")[0] == "python-cache"
    assert plan.classify_path("/home/hermes/.cache/uv")[0] == "python-cache"
    assert plan.classify_path("/home/hermes/.npm")[0] == "node-cache"
    assert plan.classify_path("/tmp")[0] == "system-temp"
    assert plan.classify_path("/var/log")[0] == "system-logs"
    assert plan.classify_path("/home/hermes/.cache")[0] == "generic-cache"


def test_urgency_accounts_for_size_and_disk_pressure():
    assert plan.urgency_for(50, 50.0) == "low"
    assert plan.urgency_for(600, 50.0) == "medium"
    assert plan.urgency_for(100, 72.0) == "medium"
    assert plan.urgency_for(2048, 50.0) == "high"
    assert plan.urgency_for(100, 85.0) == "high"


def test_build_plan_is_report_only_and_keeps_manual_guardrails(monkeypatch):
    cleanup_report = {
        "schema_version": "safe-cleanup-candidates-v1",
        "disk": {"path": "/", "used_percent": 70.0, "total_gb": 24.0, "free_gb": 7.2},
        "candidates": [
            {"path": "/home/hermes/.npm", "exists": True, "size_mb": 738, "note": "candidate: inspect before manual cleanup"},
            {"path": "/var/log", "exists": True, "size_mb": 1619, "note": "candidate: inspect before manual cleanup"},
            {"path": "/small", "exists": True, "size_mb": 10, "note": "candidate: inspect before manual cleanup"},
            {"path": "/var/www/html", "exists": True, "size_mb": 9999, "note": "excluded: web/server path"},
        ],
        "total_candidate_size_mb": 12366,
    }
    monkeypatch.setattr(plan.cleanup, "build_report", lambda paths: cleanup_report)

    review = plan.build_plan(min_size_mb=100, limit=5, candidate_paths=[Path("/ignored")])

    assert review["schema_version"] == "cleanup-review-plan-v1"
    assert review["mode"] == "report-only"
    assert review["review_item_count"] == 2
    assert [item["path"] for item in review["review_items"]] == ["/home/hermes/.npm", "/var/log"]
    assert review["review_items"][0]["category"] == "node-cache"
    assert review["review_items"][0]["allowed_automation"] == "none"
    assert review["review_items"][0]["requires_human_validation"] is True
    assert review["review_items"][1]["category"] == "system-logs"
    assert "Aucune suppression automatique." in review["guardrails"]


def test_build_plan_honors_limit_after_actionable_filter(monkeypatch):
    cleanup_report = {
        "schema_version": "safe-cleanup-candidates-v1",
        "disk": {"path": "/", "used_percent": 60.0},
        "candidates": [
            {"path": "/big-a", "exists": True, "size_mb": 300, "note": "candidate: inspect before manual cleanup"},
            {"path": "/big-b", "exists": True, "size_mb": 200, "note": "candidate: inspect before manual cleanup"},
        ],
        "total_candidate_size_mb": 500,
    }
    monkeypatch.setattr(plan.cleanup, "build_report", lambda paths: cleanup_report)

    review = plan.build_plan(min_size_mb=100, limit=1)

    assert review["review_item_count"] == 1
    assert review["review_items"][0]["path"] == "/big-a"
