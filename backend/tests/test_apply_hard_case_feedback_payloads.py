import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

from tools.apply_hard_case_feedback_payloads import apply_payloads, load_payloads


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n", encoding="utf-8")


def _valid_payload(scan_id: str = "scan-one", feedback: str = "wrong_monument") -> dict:
    return {
        "scan_id": scan_id,
        "method": "POST",
        "path": f"/v1/hard-cases/{scan_id}/feedback",
        "payload": {"user_feedback": feedback, "notes": "revue humaine"},
    }


def test_load_payloads_accepts_prepared_privacy_safe_jsonl(tmp_path) -> None:
    input_jsonl = tmp_path / "payloads.jsonl"
    _write_jsonl(input_jsonl, [_valid_payload("scan-one"), _valid_payload("scan-two", "poor_angle")])

    report = load_payloads(input_jsonl)

    assert report["valid"] is True
    assert report["payload_count"] == 2
    assert report["counts_by_feedback"] == {"poor_angle": 1, "wrong_monument": 1}
    assert report["privacy"] == {
        "sends_raw_image": False,
        "sends_raw_embedding": False,
        "sends_precise_location": False,
    }
    assert [record["scan_id"] for record in report["records"]] == ["scan-one", "scan-two"]


def test_apply_payloads_default_is_dry_run_without_network(tmp_path) -> None:
    input_jsonl = tmp_path / "payloads.jsonl"
    _write_jsonl(input_jsonl, [_valid_payload("scan-dry")])

    with patch("tools.apply_hard_case_feedback_payloads._post_feedback") as post_feedback:
        report = apply_payloads(input_jsonl)

    post_feedback.assert_not_called()
    assert report["valid"] is True
    assert report["mode"] == "dry_run"
    assert report["payload_count"] == 1
    assert report["applied_count"] == 0
    assert "records" not in report


def test_load_payloads_rejects_forbidden_privacy_fields(tmp_path) -> None:
    input_jsonl = tmp_path / "payloads.jsonl"
    payload = _valid_payload("scan-private")
    payload["payload"]["raw_embedding"] = [0.1, 0.2]
    _write_jsonl(input_jsonl, [payload])

    report = load_payloads(input_jsonl)

    assert report["valid"] is False
    assert report["payload_count"] == 0
    assert "line 1: payload has unsupported field(s): raw_embedding" in report["errors"]
    assert "line 1: forbidden privacy field(s): payload.raw_embedding" in report["errors"]


def test_apply_requires_base_url_and_token_when_explicitly_enabled(tmp_path) -> None:
    input_jsonl = tmp_path / "payloads.jsonl"
    _write_jsonl(input_jsonl, [_valid_payload("scan-apply")])

    report = apply_payloads(input_jsonl, apply=True)

    assert report["valid"] is False
    assert report["mode"] == "apply"
    assert report["applied_count"] == 0
    assert "--base-url is required with --apply" in report["errors"]


def test_apply_posts_when_explicitly_enabled_with_token(tmp_path) -> None:
    input_jsonl = tmp_path / "payloads.jsonl"
    _write_jsonl(input_jsonl, [_valid_payload("scan-apply")])

    with patch("tools.apply_hard_case_feedback_payloads._post_feedback") as post_feedback:
        post_feedback.return_value = {"scan_id": "scan-apply", "ok": True, "status_code": 200, "body": {}}
        report = apply_payloads(
            input_jsonl,
            apply=True,
            base_url="http://127.0.0.1:8000/",
            bearer_token="token",
        )

    post_feedback.assert_called_once()
    assert post_feedback.call_args.args[0] == "http://127.0.0.1:8000/"
    assert post_feedback.call_args.args[1] == "token"
    assert report["valid"] is True
    assert report["applied_count"] == 1
    assert report["failed_count"] == 0


def test_cli_dry_run_prints_compact_report(tmp_path) -> None:
    input_jsonl = tmp_path / "payloads.jsonl"
    _write_jsonl(input_jsonl, [_valid_payload("scan-cli")])

    result = subprocess.run(
        [sys.executable, "tools/apply_hard_case_feedback_payloads.py", str(input_jsonl)],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        text=True,
        capture_output=True,
    )

    assert result.stdout == "dry-run ok: 1 feedback payload(s) validated, 0 sent\n"
