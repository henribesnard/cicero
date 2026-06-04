import csv
import json
import subprocess
import sys
from pathlib import Path

from tools.export_hard_cases_csv import export_csv


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text("".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records), encoding="utf-8")


def test_export_csv_writes_review_priority_sorted_rows(tmp_path) -> None:
    input_jsonl = tmp_path / "hard-cases.jsonl"
    output_csv = tmp_path / "review.csv"
    _write_jsonl(
        input_jsonl,
        [
            {
                "scan_id": "scan-low",
                "status": "low_confidence",
                "score": 0.54,
                "created_at": "2026-06-03T14:00:00Z",
                "model_version": "vision-lite-1.0.0",
                "city_id": "paris",
                "candidate_monument_id": "notre-dame",
                "user_feedback": "poor_angle",
                "notes": "angle latéral",
            },
            {
                "scan_id": "scan-miss",
                "status": "not_found",
                "score": 0.12,
                "created_at": "2026-06-03T14:05:00Z",
                "model_version": "vision-lite-1.0.0",
                "city_id": "paris",
                "candidate_monument_id": None,
                "user_feedback": "unknown",
                "notes": None,
            },
        ],
    )

    assert export_csv(input_jsonl, output_csv) == 2

    with output_csv.open(encoding="utf-8", newline="") as output_file:
        rows = list(csv.DictReader(output_file))

    assert [row["scan_id"] for row in rows] == ["scan-miss", "scan-low"]
    assert rows[0]["review_priority"] == "92"
    assert rows[0]["candidate_monument_id"] == ""
    assert rows[0]["notes"] == ""
    assert rows[1]["review_priority"] == "57"
    assert rows[1]["notes"] == "angle latéral"
    assert set(rows[0]) == {
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
    }


def test_cli_prints_export_summary(tmp_path) -> None:
    input_jsonl = tmp_path / "hard-cases.jsonl"
    output_csv = tmp_path / "nested" / "review.csv"
    _write_jsonl(
        input_jsonl,
        [
            {
                "scan_id": "scan-one",
                "status": "not_found",
                "score": 0.0,
                "created_at": "2026-06-03T14:00:00Z",
                "model_version": "vision-lite-1.0.0",
                "city_id": None,
                "candidate_monument_id": None,
                "user_feedback": None,
                "notes": None,
            }
        ],
    )

    result = subprocess.run(
        [sys.executable, "tools/export_hard_cases_csv.py", str(input_jsonl), str(output_csv)],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        text=True,
        capture_output=True,
    )

    assert result.stdout == f"exported 1 hard-case record(s) to {output_csv}\n"
    assert output_csv.exists()
