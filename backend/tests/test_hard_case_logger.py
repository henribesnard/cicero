import pytest

from app.hard_case_logger import HardCaseLogger


def test_record_low_confidence_case_keeps_privacy_safe_metadata() -> None:
    logger = HardCaseLogger(max_records=10)

    record = logger.record(
        scan_id="scan-001",
        status="low_confidence",
        score=0.612345,
        model_version="vision-lite-1.0.0",
        city_id="paris",
        candidate_monument_id="notre-dame",
        user_feedback="wrong_monument",
        notes="façade latérale ressemblante",
        created_at="2026-06-03T14:00:00Z",
    )

    assert record == {
        "scan_id": "scan-001",
        "status": "low_confidence",
        "score": 0.6123,
        "created_at": "2026-06-03T14:00:00Z",
        "model_version": "vision-lite-1.0.0",
        "city_id": "paris",
        "candidate_monument_id": "notre-dame",
        "user_feedback": "wrong_monument",
        "notes": "façade latérale ressemblante",
    }
    assert logger.list_records() == [record]


def test_record_rejects_non_hard_cases_and_invalid_feedback() -> None:
    logger = HardCaseLogger()

    with pytest.raises(ValueError, match="status must be low_confidence or not_found"):
        logger.record(scan_id="scan-ok", status="matched", score=0.95, model_version="vision-lite-1.0.0")
    with pytest.raises(ValueError, match="score must be between 0 and 1"):
        logger.record(scan_id="scan-bad", status="not_found", score=-0.1, model_version="vision-lite-1.0.0")
    with pytest.raises(ValueError, match="user_feedback is not an allowed label"):
        logger.record(
            scan_id="scan-feedback",
            status="not_found",
            score=0.1,
            model_version="vision-lite-1.0.0",
            user_feedback="free-text-label",
        )


def test_export_retraining_batch_summarizes_hard_cases_without_raw_signals() -> None:
    logger = HardCaseLogger()
    logger.record(
        scan_id="scan-low",
        status="low_confidence",
        score=0.54,
        model_version="vision-lite-1.0.0",
        user_feedback="poor_angle",
        created_at="2026-06-03T14:00:00Z",
    )
    logger.record(
        scan_id="scan-miss",
        status="not_found",
        score=0.12,
        model_version="vision-lite-1.0.0",
        user_feedback="unknown",
        created_at="2026-06-03T14:05:00Z",
    )

    batch = logger.export_retraining_batch()

    assert batch["schema_version"] == "hard-cases-v1"
    assert batch["record_count"] == 2
    assert batch["counts_by_status"] == {"low_confidence": 1, "not_found": 1}
    assert batch["counts_by_feedback"]["poor_angle"] == 1
    assert batch["counts_by_feedback"]["unknown"] == 1
    assert [record["scan_id"] for record in batch["review_queue"]] == ["scan-miss", "scan-low"]
    assert batch["review_queue"][0]["review_priority"] == 87
    assert batch["privacy"] == {
        "stores_raw_image": False,
        "stores_raw_embedding": False,
        "stores_precise_location": False,
    }
    assert [record["scan_id"] for record in batch["records"]] == ["scan-low", "scan-miss"]


def test_queue_is_bounded_and_clearable() -> None:
    logger = HardCaseLogger(max_records=2)
    logger.record(scan_id="scan-1", status="not_found", score=0.1, model_version="vision-lite-1.0.0")
    logger.record(scan_id="scan-2", status="not_found", score=0.2, model_version="vision-lite-1.0.0")
    logger.record(scan_id="scan-3", status="not_found", score=0.3, model_version="vision-lite-1.0.0")

    assert [record["scan_id"] for record in logger.list_records()] == ["scan-2", "scan-3"]
    assert logger.clear() == 2
    assert logger.list_records() == []


def test_jsonl_storage_persists_records_annotations_and_clear(tmp_path) -> None:
    storage_path = tmp_path / "hard-cases.jsonl"
    logger = HardCaseLogger(max_records=10, storage_path=storage_path)
    logger.record(
        scan_id="scan-persisted",
        status="low_confidence",
        score=0.56789,
        model_version="vision-lite-1.0.0",
        city_id="paris",
        candidate_monument_id="notre-dame",
        created_at="2026-06-03T15:00:00Z",
    )
    logger.annotate("scan-persisted", user_feedback="wrong_monument", notes="révision humaine")

    reloaded = HardCaseLogger(max_records=10, storage_path=storage_path)

    assert reloaded.list_records() == [
        {
            "scan_id": "scan-persisted",
            "status": "low_confidence",
            "score": 0.5679,
            "created_at": "2026-06-03T15:00:00Z",
            "model_version": "vision-lite-1.0.0",
            "city_id": "paris",
            "candidate_monument_id": "notre-dame",
            "user_feedback": "wrong_monument",
            "notes": "révision humaine",
        }
    ]
    assert reloaded.clear() == 1
    assert storage_path.read_text(encoding="utf-8") == ""


def test_jsonl_storage_respects_max_records_on_reload(tmp_path) -> None:
    storage_path = tmp_path / "hard-cases.jsonl"
    writer = HardCaseLogger(max_records=10, storage_path=storage_path)
    writer.record(scan_id="scan-1", status="not_found", score=0.1, model_version="vision-lite-1.0.0")
    writer.record(scan_id="scan-2", status="not_found", score=0.2, model_version="vision-lite-1.0.0")
    writer.record(scan_id="scan-3", status="not_found", score=0.3, model_version="vision-lite-1.0.0")

    reloaded = HardCaseLogger(max_records=2, storage_path=storage_path)

    assert [record["scan_id"] for record in reloaded.list_records()] == ["scan-2", "scan-3"]


def test_list_records_can_filter_by_hard_case_status() -> None:
    logger = HardCaseLogger()
    logger.record(scan_id="scan-low", status="low_confidence", score=0.55, model_version="vision-lite-1.0.0")
    logger.record(scan_id="scan-miss", status="not_found", score=0.2, model_version="vision-lite-1.0.0")

    assert [record["scan_id"] for record in logger.list_records(status="not_found")] == ["scan-miss"]
    with pytest.raises(ValueError, match="status filter"):
        logger.list_records(status="matched")


def test_annotate_updates_existing_hard_case_feedback_without_raw_signals() -> None:
    logger = HardCaseLogger()
    logger.record(
        scan_id="scan-review",
        status="low_confidence",
        score=0.57,
        model_version="vision-lite-1.0.0",
        city_id="paris",
        candidate_monument_id="notre-dame",
    )

    annotated = logger.annotate("scan-review", user_feedback="wrong_monument", notes="façade confondue")
    exported = logger.export_retraining_batch()

    assert annotated["user_feedback"] == "wrong_monument"
    assert annotated["notes"] == "façade confondue"
    assert exported["counts_by_feedback"]["wrong_monument"] == 1
    assert exported["records"] == [annotated]


def test_annotate_rejects_unknown_scan_and_invalid_feedback() -> None:
    logger = HardCaseLogger()
    logger.record(scan_id="scan-known", status="not_found", score=0.0, model_version="vision-lite-1.0.0")

    with pytest.raises(KeyError, match="Hard case not found"):
        logger.annotate("scan-missing", user_feedback="unknown")
    with pytest.raises(ValueError, match="user_feedback is not an allowed label"):
        logger.annotate("scan-known", user_feedback="invalid-label")
