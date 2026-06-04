#!/usr/bin/env python3
"""Export Cicero hard-case JSONL records to a privacy-safe CSV review sheet.

Input JSONL is the optional `CICERO_HARD_CASES_JSONL_PATH` store written by
HardCaseLogger. The CSV contains metadata and computed review priority only:
no image, no embedding, no precise location.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

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

ALLOWED_STATUSES = {"low_confidence", "not_found"}
ALLOWED_FEEDBACK = {"correct", "wrong_monument", "unknown", "poor_angle", "too_dark", "other"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export privacy-safe hard-case JSONL records to CSV for human review."
    )
    parser.add_argument("input_jsonl", type=Path, help="Path to hard-cases-v1 JSONL file")
    parser.add_argument("output_csv", type=Path, help="Destination CSV path")
    return parser.parse_args()


def _required_text(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return value.strip()


def _optional_text(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if value is None:
        return ""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string when provided")
    return value.strip()


def _review_priority(record: dict[str, Any]) -> int:
    priority = 45 if record["status"] == "not_found" else 25
    priority += round((1 - record["score"]) * 25)

    feedback = record["user_feedback"]
    if feedback in {"wrong_monument", "unknown"}:
        priority += 20
    elif feedback in {"poor_angle", "too_dark"}:
        priority += 10

    if record["city_id"]:
        priority += 5
    if record["candidate_monument_id"]:
        priority += 5
    return min(priority, 100)


def _load_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"line {line_number}: expected JSON object")

        status = payload.get("status")
        if status not in ALLOWED_STATUSES:
            raise ValueError(f"line {line_number}: status must be low_confidence or not_found")

        score = payload.get("score")
        if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 1:
            raise ValueError(f"line {line_number}: score must be between 0 and 1")

        feedback = payload.get("user_feedback")
        if feedback is not None and feedback not in ALLOWED_FEEDBACK:
            raise ValueError(f"line {line_number}: user_feedback is not an allowed label")

        records.append(
            {
                "scan_id": _required_text(payload, "scan_id"),
                "status": status,
                "score": round(float(score), 4),
                "created_at": _required_text(payload, "created_at"),
                "model_version": _required_text(payload, "model_version"),
                "city_id": _optional_text(payload, "city_id"),
                "candidate_monument_id": _optional_text(payload, "candidate_monument_id"),
                "user_feedback": feedback or "",
                "notes": _optional_text(payload, "notes"),
            }
        )
    return records


def export_csv(input_jsonl: Path, output_csv: Path) -> int:
    records = _load_records(input_jsonl)
    rows = [{"review_priority": _review_priority(record), **record} for record in records]
    rows.sort(key=lambda row: (-row["review_priority"], row["created_at"], row["scan_id"]))

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main() -> int:
    args = parse_args()
    count = export_csv(args.input_jsonl, args.output_csv)
    print(f"exported {count} hard-case record(s) to {args.output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
