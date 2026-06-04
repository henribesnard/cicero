import csv
import json
import subprocess
import sys
from pathlib import Path

from tools.summarize_hard_cases_csv import summarize_csv


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


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def test_summarize_csv_writes_actionable_buckets(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    output_json = tmp_path / "summary.json"
    _write_csv(
        input_csv,
        [
            {
                "review_priority": "92",
                "scan_id": "scan-miss",
                "status": "not_found",
                "score": "0.12",
                "created_at": "2026-06-03T14:05:00Z",
                "model_version": "vision-lite-1.0.0",
                "city_id": "paris",
                "candidate_monument_id": "",
                "user_feedback": "unknown",
                "notes": "",
            },
            {
                "review_priority": "57",
                "scan_id": "scan-low",
                "status": "low_confidence",
                "score": "0.54",
                "created_at": "2026-06-03T14:00:00Z",
                "model_version": "vision-lite-1.0.0",
                "city_id": "paris",
                "candidate_monument_id": "notre-dame",
                "user_feedback": "poor_angle",
                "notes": "angle latéral",
            },
            {
                "review_priority": "70",
                "scan_id": "scan-empty-feedback",
                "status": "not_found",
                "score": "0.42",
                "created_at": "2026-06-03T13:00:00Z",
                "model_version": "vision-lite-1.0.0",
                "city_id": "lyon",
                "candidate_monument_id": "",
                "user_feedback": "",
                "notes": "à revoir",
            },
        ],
    )

    summary = summarize_csv(input_csv, output_json, top=2)

    assert summary["record_count"] == 3
    assert summary["counts_by_status"] == {"low_confidence": 1, "not_found": 2}
    assert summary["counts_by_feedback"] == {"poor_angle": 1, "unknown": 1, "unlabeled": 1}
    assert summary["top_cities"] == [("paris", 2), ("lyon", 1)]
    assert summary["top_city_status_pairs"] == [("paris|not_found", 1), ("paris|low_confidence", 1)]
    assert [row["scan_id"] for row in summary["top_unresolved"]] == ["scan-miss", "scan-empty-feedback"]

    saved = json.loads(output_json.read_text(encoding="utf-8"))
    assert saved["schema_version"] == "hard-case-summary-v1"
    assert saved["top_unresolved"][0]["review_priority"] == 92


def test_cli_prints_summary_count(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    output_json = tmp_path / "nested" / "summary.json"
    _write_csv(
        input_csv,
        [
            {
                "review_priority": "80",
                "scan_id": "scan-one",
                "status": "not_found",
                "score": "0.2",
                "created_at": "2026-06-03T14:00:00Z",
                "model_version": "vision-lite-1.0.0",
                "city_id": "",
                "candidate_monument_id": "",
                "user_feedback": "",
                "notes": "",
            }
        ],
    )

    result = subprocess.run(
        [sys.executable, "tools/summarize_hard_cases_csv.py", str(input_csv), str(output_json)],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        text=True,
        capture_output=True,
    )

    assert result.stdout == f"summarized 1 hard-case record(s) to {output_json}\n"
    assert output_json.exists()
