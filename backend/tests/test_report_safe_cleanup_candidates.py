from pathlib import Path

import tools.report_safe_cleanup_candidates as cleanup


def test_is_excluded_blocks_common_web_paths():
    assert cleanup.is_excluded(Path("/var/www/html"))
    assert cleanup.is_excluded(Path("/etc/nginx/sites-enabled"))
    assert not cleanup.is_excluded(Path("/tmp/cicero-cache"))


def test_build_report_is_report_only_and_sorts_candidates(monkeypatch):
    sizes = {
        "/tmp/small-cache": 5,
        "/tmp/large-cache": 80,
    }

    monkeypatch.setattr(cleanup.Path, "exists", lambda self: True)
    monkeypatch.setattr(cleanup, "directory_size_mb", lambda path: sizes[str(path)])
    monkeypatch.setattr(
        cleanup,
        "disk_status",
        lambda path=Path("/"): {"path": "/", "used_percent": 70.0, "total_gb": 0.0, "free_gb": 14.2},
    )

    report = cleanup.build_report([Path("/tmp/small-cache"), Path("/tmp/large-cache")])

    assert report["schema_version"] == "safe-cleanup-candidates-v1"
    assert report["mode"] == "report-only"
    assert report["total_candidate_size_mb"] == 85
    assert report["reserve_10_percent_free_gb"] == 0.0
    assert report["recommended_manual_actions"] == [
        "Disk at or above 70%: review top cache/log/temp candidates before any manual cleanup."
    ]
    assert [row["path"] for row in report["candidates"]] == ["/tmp/large-cache", "/tmp/small-cache"]
    assert "No deletion is performed by this script." in report["guardrails"]


def test_build_report_warns_when_free_disk_below_10_percent_reserve(monkeypatch):
    monkeypatch.setattr(cleanup.Path, "exists", lambda self: True)
    monkeypatch.setattr(cleanup, "directory_size_mb", lambda path: 1)
    monkeypatch.setattr(
        cleanup,
        "disk_status",
        lambda path=Path("/"): {"path": "/", "used_percent": 92.0, "total_gb": 100.0, "free_gb": 8.0},
    )

    report = cleanup.build_report([Path("/tmp/cache")])

    assert report["reserve_10_percent_free_gb"] == 10.0
    assert report["recommended_manual_actions"] == [
        "Disk at or above 70%: review top cache/log/temp candidates before any manual cleanup.",
        "Free disk is below the 10% reserve: avoid new downloads/build artifacts until space is recovered.",
    ]


def test_build_report_marks_web_path_without_sizing(monkeypatch):
    calls = []

    def fake_size(path):
        calls.append(path)
        return 42

    monkeypatch.setattr(cleanup.Path, "exists", lambda self: True)
    monkeypatch.setattr(cleanup, "directory_size_mb", fake_size)
    monkeypatch.setattr(
        cleanup,
        "disk_status",
        lambda path=Path("/"): {"path": "/", "used_percent": 70.0, "total_gb": 0.0, "free_gb": 14.2},
    )

    report = cleanup.build_report([Path("/var/www/html"), Path("/tmp/cache")])

    assert calls == [Path("/tmp/cache")]
    assert report["candidates"][1]["path"] == "/var/www/html"
    assert report["candidates"][1]["note"] == "excluded: web/server path"
