import json
import subprocess
import sys
from pathlib import Path

from tests.test_validate_hard_cases_csv import _valid_row, _write_csv
from tools.report_hard_case_review_capacity import _parse_budgets, report_review_capacity


def test_report_review_capacity_counts_cases_for_time_budgets(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    output_json = tmp_path / "capacity.json"
    _write_csv(
        input_csv,
        [
            _valid_row(scan_id="scan-a", review_priority="95", status="not_found", user_feedback=""),
            _valid_row(scan_id="scan-b", review_priority="90", status="low_confidence", user_feedback="unknown", candidate_monument_id="notre-dame"),
            _valid_row(scan_id="scan-done", review_priority="99", user_feedback="correct"),
            _valid_row(scan_id="scan-c", review_priority="70", status="low_confidence", user_feedback=""),
        ],
    )

    report = report_review_capacity(input_csv, output_json, budgets=[5, 10, 20])

    assert report["valid"] is True
    assert report["input_record_count"] == 4
    assert report["unresolved_count"] == 3
    assert [budget["budget_minutes"] for budget in report["budgets"]] == [5, 10, 20]
    assert report["budgets"][0]["scan_ids"] == ["scan-c"]
    assert report["budgets"][1]["scan_ids"] == ["scan-a"]
    assert report["budgets"][2]["scan_ids"] == ["scan-a", "scan-b", "scan-c"]
    written = json.loads(output_json.read_text(encoding="utf-8"))
    assert written["schema_version"] == "hard-case-review-capacity-v1"


def test_report_review_capacity_invalid_csv_writes_no_artifact(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    output_json = tmp_path / "capacity.json"
    _write_csv(input_csv, [_valid_row(score="2")])

    report = report_review_capacity(input_csv, output_json)

    assert report["valid"] is False
    assert "input CSV is invalid; aborting capacity report" in report["errors"]
    assert not output_json.exists()


def test_parse_budgets_sorts_deduplicates_and_rejects_invalid_values() -> None:
    assert _parse_budgets("60,30,60") == [30, 60]

    for raw in ["", "0", "ten"]:
        try:
            _parse_budgets(raw)
        except ValueError:
            pass
        else:  # pragma: no cover - explicit failure path for readability
            raise AssertionError(f"expected ValueError for {raw!r}")


def test_capacity_cli_prints_compact_report(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    output_json = tmp_path / "capacity.json"
    _write_csv(
        input_csv,
        [
            _valid_row(scan_id="scan-a", review_priority="95", status="not_found", user_feedback=""),
            _valid_row(scan_id="scan-b", review_priority="90", status="low_confidence", user_feedback=""),
        ],
    )

    result = subprocess.run(
        [
            sys.executable,
            "tools/report_hard_case_review_capacity.py",
            str(input_csv),
            str(output_json),
            "--budgets",
            "5,12",
        ],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        text=True,
        capture_output=True,
    )

    assert result.stdout == f"review capacity: 5min=1 case(s), 12min=2 case(s) to {output_json}\n"
    assert output_json.exists()
