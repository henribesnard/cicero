import csv
import json
import subprocess
import sys
from pathlib import Path

from tests.test_validate_hard_cases_csv import FIELDNAMES, _valid_row, _write_csv
from tools.import_hard_case_review_markdown import import_markdown_decisions, parse_markdown_decisions


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as input_file:
        return list(csv.DictReader(input_file))


def _markdown(*, checked_label: str = "wrong_monument", notes: str = "confusion façade latérale") -> str:
    return f"""# Cicero — Fiche de revue cas difficiles

## À annoter

### 1. `scan-open` — priorité 88

- Statut: `low_confidence`

Décision revue:
- [ ] correct
- [x] {checked_label}
- [ ] unknown
- [ ] poor_angle
- [ ] too_dark
- [ ] other

Notes revue: {notes}

### 2. `scan-skip` — priorité 71

Décision revue:
- [ ] correct
- [ ] wrong_monument
- [ ] unknown
- [ ] poor_angle
- [ ] too_dark
- [ ] other

Notes revue: ________________________________________________
"""


def test_parse_markdown_decisions_extracts_checked_label_and_notes(tmp_path) -> None:
    input_md = tmp_path / "review.md"
    input_md.write_text(_markdown(), encoding="utf-8")

    report = parse_markdown_decisions(input_md)

    assert report["section_count"] == 2
    assert report["decision_count"] == 1
    assert report["errors"] == []
    assert report["decisions"] == {
        "scan-open": {"user_feedback": "wrong_monument", "notes": "confusion façade latérale"}
    }


def test_import_markdown_decisions_updates_matching_rows_and_preserves_unchecked(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    input_md = tmp_path / "review.md"
    output_csv = tmp_path / "annotated.csv"
    _write_csv(
        input_csv,
        [
            _valid_row(scan_id="scan-open", status="low_confidence", user_feedback="", notes=""),
            _valid_row(scan_id="scan-skip", user_feedback="", notes="original note"),
        ],
    )
    input_md.write_text(_markdown(), encoding="utf-8")

    report = import_markdown_decisions(input_csv, input_md, output_csv)

    assert report["valid"] is True
    assert report["applied_count"] == 1
    rows = _read_rows(output_csv)
    assert rows[0]["user_feedback"] == "wrong_monument"
    assert rows[0]["notes"] == "confusion façade latérale"
    assert rows[1]["user_feedback"] == ""
    assert rows[1]["notes"] == "original note"


def test_import_rejects_multiple_checked_labels_without_writing_output(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    input_md = tmp_path / "review.md"
    output_csv = tmp_path / "annotated.csv"
    _write_csv(input_csv, [_valid_row(scan_id="scan-open", user_feedback="")])
    input_md.write_text(
        _markdown().replace("- [ ] correct", "- [x] correct"),
        encoding="utf-8",
    )

    report = import_markdown_decisions(input_csv, input_md, output_csv)

    assert report["valid"] is False
    assert "section scan-open: exactly one checked label expected, got 2" in report["errors"]
    assert not output_csv.exists()


def test_import_rejects_unknown_scan_id(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    input_md = tmp_path / "review.md"
    output_csv = tmp_path / "annotated.csv"
    _write_csv(input_csv, [_valid_row(scan_id="scan-other", user_feedback="")])
    input_md.write_text(_markdown(), encoding="utf-8")

    report = import_markdown_decisions(input_csv, input_md, output_csv)

    assert report["valid"] is False
    assert "Markdown decision references unknown scan_id=scan-open" in report["errors"]
    assert not output_csv.exists()


def test_cli_imports_markdown_decisions_and_prints_compact_report(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    input_md = tmp_path / "review.md"
    output_csv = tmp_path / "annotated.csv"
    _write_csv(input_csv, [_valid_row(scan_id="scan-open", user_feedback="")])
    input_md.write_text(_markdown(checked_label="poor_angle", notes="angle oblique"), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "tools/import_hard_case_review_markdown.py",
            str(input_csv),
            str(input_md),
            str(output_csv),
        ],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        text=True,
        capture_output=True,
    )

    assert result.stdout == f"imported 1 markdown decision(s) to {output_csv}\n"
    assert _read_rows(output_csv)[0]["user_feedback"] == "poor_angle"


def test_cli_json_returns_nonzero_when_required_section_missing_decision(tmp_path) -> None:
    input_csv = tmp_path / "review.csv"
    input_md = tmp_path / "review.md"
    output_csv = tmp_path / "annotated.csv"
    _write_csv(
        input_csv,
        [
            _valid_row(scan_id="scan-open", user_feedback=""),
            _valid_row(scan_id="scan-skip", user_feedback=""),
        ],
        fieldnames=FIELDNAMES,
    )
    input_md.write_text(_markdown(), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "tools/import_hard_case_review_markdown.py",
            str(input_csv),
            str(input_md),
            str(output_csv),
            "--require-decision-for-each-section",
            "--json",
        ],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["valid"] is False
    assert "section scan-skip: no checked decision label" in report["errors"]
    assert not output_csv.exists()
