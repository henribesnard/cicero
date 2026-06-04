import json
import subprocess
import sys
from pathlib import Path

from tests.test_validate_hard_cases_csv import _valid_row, _write_csv
from tools.prepare_hard_case_feedback_payloads import build_payloads


def test_build_payloads_writes_only_annotated_rows(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    output_jsonl = tmp_path / "feedback-payloads.jsonl"
    _write_csv(
        input_csv,
        [
            _valid_row(scan_id="scan-one", user_feedback="wrong_monument", notes="confusion façade"),
            _valid_row(scan_id="scan-two", user_feedback="", notes=""),
        ],
    )

    report = build_payloads(input_csv, output_jsonl)

    assert report["valid"] is True
    assert report["payload_count"] == 1
    lines = output_jsonl.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert payload == {
        "method": "POST",
        "path": "/v1/hard-cases/scan-one/feedback",
        "payload": {"notes": "confusion façade", "user_feedback": "wrong_monument"},
        "scan_id": "scan-one",
    }


def test_build_payloads_fails_on_invalid_csv_without_writing_payloads(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    output_jsonl = tmp_path / "feedback-payloads.jsonl"
    _write_csv(input_csv, [_valid_row(score="2")])

    report = build_payloads(input_csv, output_jsonl)

    assert report["valid"] is False
    assert report["payload_count"] == 0
    assert not output_jsonl.exists()
    assert "row 2: score must be between 0 and 1" in report["validation"]["errors"]


def test_cli_prepares_compact_payload_report(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    output_jsonl = tmp_path / "feedback-payloads.jsonl"
    _write_csv(input_csv, [_valid_row(scan_id="scan-cli", user_feedback="poor_angle", notes="angle bas")])

    result = subprocess.run(
        [
            sys.executable,
            "tools/prepare_hard_case_feedback_payloads.py",
            str(input_csv),
            str(output_jsonl),
        ],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        text=True,
        capture_output=True,
    )

    assert result.stdout == f"prepared 1 feedback payload(s) to {output_jsonl}\n"
    assert json.loads(output_jsonl.read_text(encoding="utf-8"))["scan_id"] == "scan-cli"
