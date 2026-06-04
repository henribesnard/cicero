#!/usr/bin/env python3
"""Summarize recent Cicero ops guardrail snapshots from a JSONL archive.

The script is intentionally light and read-only: it parses the append-only archive
created by archive_ops_guardrails.py and emits a compact trend signal for cron
reports or manual VPS checks.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any

DEFAULT_INPUT = Path("docs/ops/ops_guardrails_snapshots.jsonl")


def load_snapshots(input_path: Path, *, limit: int = 7) -> list[dict[str, Any]]:
    """Return the last valid ops snapshots from a JSONL archive.

    Blank lines are ignored. Invalid JSON rows or rows with another schema are
    skipped so one partial/manual line cannot break the operational report.
    """
    if limit <= 0:
        raise ValueError("limit must be positive")
    if not input_path.exists():
        return []

    valid_rows: list[dict[str, Any]] = []
    for line in input_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("schema_version") == "ops-guardrails-snapshot-v1":
            valid_rows.append(row)
    return valid_rows[-limit:]


def _delta(last: float, first: float) -> float:
    return round(last - first, 2)


def build_trend(snapshots: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a compact trend report from already-loaded snapshots."""
    if not snapshots:
        return {
            "schema_version": "ops-guardrails-trend-v1",
            "mode": "report-only",
            "snapshot_count": 0,
            "status": "no_data",
            "recommendations": ["Aucune archive ops disponible: lancer archive_ops_guardrails.py avant la tendance."],
        }

    first = snapshots[0]
    last = snapshots[-1]
    free_values = [row["memory"]["free_mb"] for row in snapshots]
    available_values = [row["memory"]["available_mb"] for row in snapshots]
    disk_values = [row["disk"]["used_percent"] for row in snapshots]
    cleanup_values = [row["cleanup"]["total_candidate_size_mb"] for row in snapshots]
    statuses = [row.get("status", "unknown") for row in snapshots]

    recommendations: list[str] = []
    if last["memory"]["free_mb"] < 800:
        recommendations.append("Mode léger recommandé: dernier snapshot RAM libre < 800 MiB.")
    if last["disk"]["used_percent"] > 70:
        recommendations.append("Préparer une revue de ménage non destructif: disque > 70%.")
    if len(snapshots) >= 2 and _delta(last["disk"]["used_percent"], first["disk"]["used_percent"]) >= 1:
        recommendations.append("Surveiller la dérive disque: hausse >= 1 point sur la fenêtre.")
    if last["cleanup"].get("review_needed"):
        recommendations.append("Candidats de nettoyage présents: revue manuelle uniquement, aucune suppression automatique.")
    if not recommendations:
        recommendations.append("Tendance ops stable: poursuivre les travaux légers/standard selon RAM disponible.")

    return {
        "schema_version": "ops-guardrails-trend-v1",
        "mode": "report-only",
        "snapshot_count": len(snapshots),
        "window": {
            "first_observed_at": first.get("observed_at"),
            "last_observed_at": last.get("observed_at"),
        },
        "status": "light" if "light" in statuses or last["memory"]["free_mb"] < 800 else "normal",
        "memory": {
            "first_free_mb": first["memory"]["free_mb"],
            "last_free_mb": last["memory"]["free_mb"],
            "min_free_mb": min(free_values),
            "avg_free_mb": round(mean(free_values), 1),
            "delta_free_mb": _delta(last["memory"]["free_mb"], first["memory"]["free_mb"]),
            "last_available_mb": last["memory"]["available_mb"],
            "min_available_mb": min(available_values),
        },
        "disk": {
            "first_used_percent": first["disk"]["used_percent"],
            "last_used_percent": last["disk"]["used_percent"],
            "max_used_percent": max(disk_values),
            "delta_used_percent": _delta(last["disk"]["used_percent"], first["disk"]["used_percent"]),
        },
        "cleanup": {
            "last_total_candidate_size_mb": last["cleanup"]["total_candidate_size_mb"],
            "max_total_candidate_size_mb": max(cleanup_values),
            "last_review_needed": bool(last["cleanup"].get("review_needed")),
        },
        "recommendations": recommendations,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report recent Cicero ops guardrail trends without changing anything.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="JSONL archive path to read.")
    parser.add_argument("--limit", type=int, default=7, help="Number of most recent snapshots to summarize.")
    parser.add_argument("--json", action="store_true", help="Print full JSON report.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    snapshots = load_snapshots(args.input, limit=args.limit)
    trend = build_trend(snapshots)
    if args.json:
        print(json.dumps(trend, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if trend["snapshot_count"] == 0:
        print("ops trend: status=no_data, snapshots=0, report-only")
    else:
        print(
            f"ops trend: status={trend['status']}, snapshots={trend['snapshot_count']}, "
            f"ram_free={trend['memory']['last_free_mb']} MiB "
            f"(min={trend['memory']['min_free_mb']}, delta={trend['memory']['delta_free_mb']}), "
            f"disk={trend['disk']['last_used_percent']}% "
            f"(max={trend['disk']['max_used_percent']}, delta={trend['disk']['delta_used_percent']}), "
            f"cleanup_candidates={trend['cleanup']['last_total_candidate_size_mb']} MiB"
        )
    for recommendation in trend["recommendations"]:
        print(f"- {recommendation}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
