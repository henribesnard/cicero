import csv
import json
import subprocess
import sys
from pathlib import Path

from tools.validate_hard_cases_csv import validate_csv


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


def _write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str] = FIELDNAMES) -> None:
    with path.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _valid_row(**overrides: str) -> dict[str, str]:
    row = {
        "review_priority": "92",
        "scan_id": "scan-one",
        "status": "not_found",
        "score": "0.12",
        "created_at": "2026-06-03T14:05:00Z",
        "model_version": "vision-lite-1.0.0",
        "city_id": "paris",
        "candidate_monument_id": "",
        "user_feedback": "wrong_monument",
        "notes": "confusion façade latérale",
    }
    row.update(overrides)
    return row


def test_validate_csv_accepts_review_sheet_and_counts_annotations(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    _write_csv(
        input_csv,
        [
            _valid_row(scan_id="scan-one", user_feedback="wrong_monument"),
            _valid_row(scan_id="scan-two", status="low_confidence", user_feedback="", notes=""),
        ],
    )

    report = validate_csv(input_csv)

    assert report["valid"] is True
    assert report["row_count"] == 2
    assert report["annotated_count"] == 1
    assert report["counts_by_status"] == {"low_confidence": 1, "not_found": 1}
    assert report["counts_by_feedback"] == {"unlabeled": 1, "wrong_monument": 1}
    assert report["errors"] == []


def test_validate_csv_rejects_invalid_labels_and_duplicate_scan_ids(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    _write_csv(
        input_csv,
        [
            _valid_row(scan_id="scan-dup", user_feedback="invented_label"),
            _valid_row(scan_id="scan-dup", status="maybe", score="1.5"),
        ],
    )

    report = validate_csv(input_csv)

    assert report["valid"] is False
    assert "row 2: user_feedback is not an allowed label" in report["errors"]
    assert "row 3: duplicate scan_id=scan-dup" in report["errors"]
    assert "row 3: status must be low_confidence or not_found" in report["errors"]
    assert "row 3: score must be between 0 and 1" in report["errors"]


def test_cli_returns_json_report_and_nonzero_on_invalid_csv(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    _write_csv(input_csv, [_valid_row(review_priority="101")])

    result = subprocess.run(
        [sys.executable, "tools/validate_hard_cases_csv.py", str(input_csv), "--json"],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["schema_version"] == "hard-case-csv-validation-v1"
    assert report["valid"] is False
    assert "row 2: review_priority must be between 0 and 100" in report["errors"]


def test_cli_prints_compact_valid_line(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    _write_csv(input_csv, [_valid_row()])

    result = subprocess.run(
        [sys.executable, "tools/validate_hard_cases_csv.py", str(input_csv)],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        text=True,
        capture_output=True,
    )

    assert result.stdout == "valid: 1 row(s), 1 annotated, 0 error(s), 0 warning(s)\n"


def test_require_all_annotated_rejects_blank_feedback(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    _write_csv(input_csv, [_valid_row(user_feedback="")])

    report = validate_csv(input_csv, require_all_annotated=True)

    assert report["valid"] is False
    assert "row 2: user_feedback must be annotated" in report["errors"]


def test_cli_require_all_annotated_returns_nonzero_for_incomplete_review(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    _write_csv(input_csv, [_valid_row(user_feedback="")])

    result = subprocess.run(
        [
            sys.executable,
            "tools/validate_hard_cases_csv.py",
            str(input_csv),
            "--require-all-annotated",
            "--json",
        ],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["valid"] is False
    assert "row 2: user_feedback must be annotated" in report["errors"]
