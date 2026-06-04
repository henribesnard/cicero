import json
import subprocess
import sys
from pathlib import Path

from tests.test_validate_hard_cases_csv import _valid_row, _write_csv
from tools.run_hard_case_review_pipeline import run_pipeline


def test_run_pipeline_writes_all_dry_run_artifacts(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    output_dir = tmp_path / "ops-out"
    _write_csv(
        input_csv,
        [
            _valid_row(scan_id="scan-annotated", city_id="paris", user_feedback="wrong_monument", notes="confusion"),
            _valid_row(scan_id="scan-open", city_id="lyon", user_feedback="", review_priority="88"),
        ],
    )

    report = run_pipeline(input_csv, output_dir, top=2, batch_limit=5)

    assert report["valid"] is True
    assert report["record_count"] == 2
    assert report["annotated_count"] == 1
    assert report["selected_review_count"] == 1
    assert report["payload_count"] == 1
    assert report["review_markdown_item_count"] == 1
    assert Path(report["artifacts"]["summary_json"]).exists()
    assert Path(report["artifacts"]["review_batch_json"]).exists()
    assert Path(report["artifacts"]["review_markdown"]).exists()
    assert Path(report["artifacts"]["feedback_payloads_jsonl"]).exists()

    batch = json.loads(Path(report["artifacts"]["review_batch_json"]).read_text(encoding="utf-8"))
    assert [item["scan_id"] for item in batch["items"]] == ["scan-open"]
    review_sheet = Path(report["artifacts"]["review_markdown"]).read_text(encoding="utf-8")
    assert "scan-open" in review_sheet
    assert "aucune image brute" in review_sheet


def test_run_pipeline_invalid_csv_creates_no_artifacts(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    output_dir = tmp_path / "ops-out"
    _write_csv(input_csv, [_valid_row(score="2")])

    report = run_pipeline(input_csv, output_dir)

    assert report["valid"] is False
    assert report["artifacts"] == {}
    assert not (output_dir / "hard-case-summary.json").exists()
    assert "row 2: score must be between 0 and 1" in report["validation"]["errors"]


def test_pipeline_cli_prints_compact_report(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    output_dir = tmp_path / "ops-out"
    _write_csv(input_csv, [_valid_row(scan_id="scan-cli", user_feedback="poor_angle")])

    result = subprocess.run(
        [
            sys.executable,
            "tools/run_hard_case_review_pipeline.py",
            str(input_csv),
            str(output_dir),
            "--batch-limit",
            "3",
        ],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        text=True,
        capture_output=True,
    )

    assert result.stdout == f"pipeline ok: 1 row(s), 1 annotated, 0 selected, 1 payload(s) to {output_dir}\n"
