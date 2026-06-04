import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.select_hard_case_review_batch import estimate_review_effort_minutes, select_review_batch


FIELDNAMES = [
    "review_priority",
    "scan_id",
    "status",
    "score",
    "created_at",
    "model_version",
    "city_id",
    "candidate_monument_id",
    "user_feedback",
    "notes",
]


def _row(
    scan_id: str,
    *,
    priority: int,
    city: str = "paris",
    status: str = "not_found",
    feedback: str = "",
    score: str = "0.20",
    created_at: str = "2026-06-04T00:00:00Z",
) -> dict[str, str]:
    return {
        "review_priority": str(priority),
        "scan_id": scan_id,
        "status": status,
        "score": score,
        "created_at": created_at,
        "model_version": "vision-lite-1.0.0",
        "city_id": city,
        "candidate_monument_id": "",
        "user_feedback": feedback,
        "notes": "",
    }


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def test_select_review_batch_prioritizes_unresolved_and_caps_city(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    output_json = tmp_path / "batch.json"
    _write_csv(
        input_csv,
        [
            _row("scan-paris-1", priority=99, city="paris", feedback="unknown"),
            _row("scan-paris-2", priority=98, city="paris"),
            _row("scan-paris-annotated", priority=97, city="paris", feedback="correct"),
            _row("scan-lyon", priority=80, city="lyon", status="low_confidence", score="0.55"),
            _row("scan-paris-capped", priority=70, city="paris"),
        ],
    )

    batch = select_review_batch(input_csv, output_json, limit=4, max_per_city=2, max_per_status=4)

    assert batch["schema_version"] == "hard-case-review-batch-v1"
    assert batch["input_record_count"] == 5
    assert batch["unresolved_count"] == 4
    assert [item["scan_id"] for item in batch["items"]] == [
        "scan-paris-1",
        "scan-paris-2",
        "scan-lyon",
    ]
    assert batch["counts_by_city"] == {"lyon": 1, "paris": 2}
    assert batch["skipped_due_to_caps"] == 1
    assert [item["review_effort_minutes"] for item in batch["items"]] == [6, 5, 4]
    assert batch["estimated_review_effort_minutes"] == 15

    saved = json.loads(output_json.read_text(encoding="utf-8"))
    assert saved["selected_count"] == 3
    assert saved["items"][2]["score"] == 0.55


def test_estimate_review_effort_minutes_caps_complex_rows() -> None:
    row = _row(
        "scan-complex",
        priority=95,
        status="not_found",
        feedback="unknown",
    )
    row["candidate_monument_id"] = "arc-triomphe"
    row["notes"] = "confusion possible avec façade similaire"

    assert estimate_review_effort_minutes(row) == 8


def test_select_review_batch_caps_status_bucket(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    output_json = tmp_path / "batch.json"
    _write_csv(
        input_csv,
        [
            _row("scan-a", priority=90, city="paris", status="not_found"),
            _row("scan-b", priority=89, city="lyon", status="not_found"),
            _row("scan-c", priority=88, city="marseille", status="low_confidence"),
        ],
    )

    batch = select_review_batch(input_csv, output_json, limit=5, max_per_city=5, max_per_status=1)

    assert [item["scan_id"] for item in batch["items"]] == ["scan-a", "scan-c"]
    assert batch["counts_by_status"] == {"low_confidence": 1, "not_found": 1}
    assert batch["skipped_due_to_caps"] == 1


def test_select_review_batch_rejects_non_positive_limit(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    _write_csv(input_csv, [_row("scan-a", priority=90)])

    with pytest.raises(ValueError, match="limit must be a positive integer"):
        select_review_batch(input_csv, tmp_path / "batch.json", limit=0)


def test_cli_prints_selection_count(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    output_json = tmp_path / "nested" / "batch.json"
    _write_csv(input_csv, [_row("scan-a", priority=90), _row("scan-b", priority=89, feedback="correct")])

    result = subprocess.run(
        [
            sys.executable,
            "tools/select_hard_case_review_batch.py",
            str(input_csv),
            str(output_json),
            "--limit",
            "2",
        ],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        text=True,
        capture_output=True,
    )

    assert result.stdout == f"selected 1 of 1 unresolved hard-case row(s) to {output_json}\n"
    assert output_json.exists()
