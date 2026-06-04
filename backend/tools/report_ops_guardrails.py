#!/usr/bin/env python3
"""Combine Cicero cron guardrails into one lightweight report.

The report stays strictly non-destructive: it reads VPS health and safe cleanup
candidates, then emits a compact status suitable for scheduled run summaries.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:  # Script execution from backend/tools
    import report_safe_cleanup_candidates as cleanup
    import report_vps_health as health
except ModuleNotFoundError:  # Package import from tests
    from tools import report_safe_cleanup_candidates as cleanup
    from tools import report_vps_health as health


def build_report(
    *,
    top_cleanup: int = 3,
    min_cleanup_size_mb: int = 100,
    cleanup_paths: list[Path] | None = None,
    disk_path: Path = Path("/"),
) -> dict[str, Any]:
    """Return a combined, report-only ops guardrail report."""
    health_report = health.build_report(disk_path=disk_path)
    cleanup_report = cleanup.build_report(cleanup_paths or cleanup.DEFAULT_CANDIDATES)
    actionable = cleanup.actionable_candidates(
        cleanup_report,
        min_size_mb=min_cleanup_size_mb,
        limit=top_cleanup,
    )

    recommendations = list(health_report["recommendations"])
    if actionable:
        recommendations.append(
            f"Revoir {len(actionable)} candidat(s) de nettoyage non destructif avant tout ménage manuel."
        )
    elif cleanup_report["total_candidate_size_mb"] == 0:
        recommendations.append("Aucun candidat de nettoyage détecté dans les chemins conservateurs.")

    return {
        "schema_version": "ops-guardrails-v1",
        "mode": "report-only",
        "health": health_report,
        "cleanup": {
            "schema_version": cleanup_report["schema_version"],
            "mode": cleanup_report["mode"],
            "disk": cleanup_report["disk"],
            "total_candidate_size_mb": cleanup_report["total_candidate_size_mb"],
            "actionable_candidates": actionable,
            "recommended_manual_actions": cleanup_report["recommended_manual_actions"],
            "guardrails": cleanup_report["guardrails"],
        },
        "summary": {
            "status": health_report["status"],
            "cleanup_review_needed": health_report["cleanup_review_needed"] or bool(actionable),
            "actionable_cleanup_count": len(actionable),
            "recommendations": recommendations,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report combined Cicero VPS ops guardrails without changing anything.")
    parser.add_argument("--json", action="store_true", help="Print full JSON report.")
    parser.add_argument("--top-cleanup", type=int, default=3, help="Number of cleanup candidates shown in text/summary.")
    parser.add_argument(
        "--min-cleanup-size-mb",
        type=int,
        default=100,
        help="Minimum cleanup candidate size included in the compact actionable summary.",
    )
    parser.add_argument("--disk-path", type=Path, default=Path("/"), help="Disk path to inspect; default: root.")
    parser.add_argument(
        "--cleanup-path",
        action="append",
        type=Path,
        dest="cleanup_paths",
        help="Override cleanup candidate path; repeatable.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(
        top_cleanup=args.top_cleanup,
        min_cleanup_size_mb=args.min_cleanup_size_mb,
        cleanup_paths=args.cleanup_paths,
        disk_path=args.disk_path,
    )
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    health_report = report["health"]
    memory = health_report["memory"]
    disk = health_report["disk"]
    summary = report["summary"]
    cleanup_summary = report["cleanup"]

    print(
        f"ops guardrails: status={summary['status']}, "
        f"ram_free={memory['free_mb']} MiB, ram_available={memory['available_mb']} MiB, "
        f"disk={disk['used_percent']}% used, "
        f"cleanup_candidates={cleanup_summary['total_candidate_size_mb']} MiB, report-only"
    )
    for recommendation in summary["recommendations"]:
        print(f"- {recommendation}")
    for row in cleanup_summary["actionable_candidates"]:
        print(f"- cleanup {row['size_mb']} MiB\t{row['path']}\t{row['note']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
