import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.export_hard_case_review_markdown import export_review_markdown, render_markdown


def _batch() -> dict:
    return {
        "schema_version": "hard-case-review-batch-v1",
        "source_csv": "/tmp/review.csv",
        "input_record_count": 2,
        "unresolved_count": 2,
        "selected_count": 1,
        "estimated_review_effort_minutes": 5,
        "selection_policy": {"limit": 20, "max_per_city": 8, "max_per_status": 12},
        "items": [
            {
                "review_priority": 91,
                "review_effort_minutes": 5,
                "scan_id": "scan-a",
                "status": "low_confidence",
                "score": 0.57,
                "created_at": "2026-06-04T00:00:00Z",
                "model_version": "vision-lite-1.0.0",
                "city_id": "paris",
                "candidate_monument_id": "notre-dame",
                "user_feedback": "unknown",
                "notes": "à revoir",
            }
        ],
    }


def test_render_markdown_includes_privacy_context_and_checklist() -> None:
    markdown = render_markdown(_batch())

    assert "# Cicero — Fiche de revue cas difficiles" in markdown
    assert "aucune image brute, aucun embedding brut, aucune position précise" in markdown
    assert "Effort revue estimé: 5 min" in markdown
    assert "### 1. `scan-a` — priorité 91" in markdown
    assert "Effort estimé: 5 min" in markdown
    assert "- [ ] wrong_monument" in markdown
    assert "Notes revue:" in markdown


def test_export_review_markdown_writes_file(tmp_path) -> None:
    input_json = tmp_path / "batch.json"
    output_md = tmp_path / "nested" / "review.md"
    input_json.write_text(json.dumps(_batch(), ensure_ascii=False), encoding="utf-8")

    report = export_review_markdown(input_json, output_md)

    assert report["item_count"] == 1
    assert output_md.exists()
    assert "scan-a" in output_md.read_text(encoding="utf-8")


def test_export_review_markdown_rejects_wrong_schema(tmp_path) -> None:
    input_json = tmp_path / "batch.json"
    input_json.write_text(json.dumps({"schema_version": "wrong", "items": []}), encoding="utf-8")

    with pytest.raises(ValueError, match="schema_version=hard-case-review-batch-v1"):
        export_review_markdown(input_json, tmp_path / "review.md")


def test_cli_prints_markdown_count(tmp_path) -> None:
    input_json = tmp_path / "batch.json"
    output_md = tmp_path / "review.md"
    input_json.write_text(json.dumps(_batch(), ensure_ascii=False), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "tools/export_hard_case_review_markdown.py", str(input_json), str(output_md)],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        text=True,
        capture_output=True,
    )

    assert result.stdout == f"review markdown: 1 item(s) to {output_md}\n"
    assert output_md.exists()
