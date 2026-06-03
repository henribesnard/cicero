from datetime import UTC, datetime

import pytest

from app.travel_log import TravelLog


def test_record_scan_keeps_monument_date_score_and_status() -> None:
    log = TravelLog()

    entry = log.record_scan(
        monument_id="notre-dame",
        score=0.923456,
        status="matched",
        scanned_at=datetime(2026, 6, 3, 8, 30, tzinfo=UTC),
    )

    assert entry == {
        "monument_id": "notre-dame",
        "scanned_at": "2026-06-03T08:30:00Z",
        "score": 0.9235,
        "status": "matched",
    }


def test_list_scans_is_sortable_by_date() -> None:
    log = TravelLog()
    log.record_scan("notre-dame", 0.9, scanned_at="2026-06-03T08:30:00Z")
    log.record_scan("arc-de-triomphe", 0.7, status="low_confidence", scanned_at="2026-06-03T09:00:00Z")

    assert [entry["monument_id"] for entry in log.list_scans()] == ["arc-de-triomphe", "notre-dame"]
    assert [entry["monument_id"] for entry in log.list_scans(sort="asc")] == ["notre-dame", "arc-de-triomphe"]


def test_record_scan_rejects_invalid_values() -> None:
    log = TravelLog()

    with pytest.raises(ValueError, match="monument_id is required"):
        log.record_scan("", 0.5)
    with pytest.raises(ValueError, match="score must be between 0 and 1"):
        log.record_scan("notre-dame", 1.2)
    with pytest.raises(ValueError, match="status must be matched"):
        log.record_scan("notre-dame", 0.8, status="pending")
    with pytest.raises(ValueError, match="sort must be asc or desc"):
        log.list_scans(sort="newest")
