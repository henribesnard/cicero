#!/usr/bin/env python3
"""Build a lightweight daily Cicero ops report from guardrails + trend data.

This script is intentionally read-only. It combines the current VPS guardrail
summary with the recent JSONL trend so a cron run can paste one compact Markdown
block instead of calling and formatting multiple tools by hand.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:  # Script execution from backend/tools
    import report_ops_guardrails as guardrails
    import report_ops_guardrails_trend as trend
except ModuleNotFoundError:  # Package import from tests
    from tools import report_ops_guardrails as guardrails
    from tools import report_ops_guardrails_trend as trend


def build_daily_report(
    *,
    trend_input: Path = trend.DEFAULT_INPUT,
    trend_limit: int = 7,
    top_cleanup: int = 3,
    min_cleanup_size_mb: int = 100,
    cleanup_paths: list[Path] | None = None,
    disk_path: Path = Path("/"),
) -> dict[str, Any]:
    """Return a combined report-only daily ops report."""
    guardrail_report = guardrails.build_report(
        top_cleanup=top_cleanup,
        min_cleanup_size_mb=min_cleanup_size_mb,
        cleanup_paths=cleanup_paths,
        disk_path=disk_path,
    )
    compact = guardrails.build_compact_summary(guardrail_report)
    trend_report = trend.build_trend(trend.load_snapshots(trend_input, limit=trend_limit))

    recommendations = list(compact["recommendations"])
    recommendations.extend(
        recommendation
        for recommendation in trend_report["recommendations"]
        if recommendation not in recommendations
    )

    return {
        "schema_version": "ops-guardrails-daily-v1",
        "mode": "report-only",
        "status": "light" if compact["status"] == "light" or trend_report["status"] == "light" else compact["status"],
        "current": compact,
        "trend": trend_report,
        "recommendations": recommendations,
    }


def build_markdown(report: dict[str, Any]) -> str:
    """Return a compact Markdown daily report."""
    current = report["current"]
    vps = current["vps"]
    cleanup = current["cleanup"]
    trend_report = report["trend"]

    lines = [
        "# Rapport quotidien ops guardrails",
        "",
        f"- Statut combiné: `{report['status']}`",
        f"- RAM actuelle: {vps['ram_free_mb']} MiB libres / {vps['ram_available_mb']} MiB disponibles",
        f"- Disque actuel: {vps['disk_used_percent']}% utilisé",
        f"- Revue nettoyage: {'oui' if vps['cleanup_review_needed'] else 'non'} "
        f"({cleanup['total_candidate_size_mb']} MiB candidats, {cleanup['manual_review_item_count']} revue(s) manuelle(s))",
        f"- Tendance: `{trend_report['status']}` sur {trend_report['snapshot_count']} snapshot(s)",
    ]

    if trend_report.get("snapshot_count", 0) > 0:
        lines.extend(
            [
                f"- RAM tendance: min {trend_report['memory']['min_free_mb']} MiB, "
                f"moyenne {trend_report['memory']['avg_free_mb']} MiB, "
                f"delta {trend_report['memory']['delta_free_mb']} MiB",
                f"- Disque tendance: max {trend_report['disk']['max_used_percent']}%, "
                f"delta {trend_report['disk']['delta_used_percent']} point(s)",
            ]
        )

    if cleanup["top_review_paths"]:
        lines.extend(["", "## Chemins à revoir"])
        lines.extend(f"- `{path}`" for path in cleanup["top_review_paths"])

    lines.extend(["", "## Recommandations"])
    lines.extend(f"- {recommendation}" for recommendation in report["recommendations"])
    lines.extend(["", "_Mode report-only: aucune suppression ni mutation système._"])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a combined Cicero daily ops report without changing anything.")
    parser.add_argument("--json", action="store_true", help="Print full JSON report.")
    parser.add_argument("--markdown", action="store_true", help="Print compact Markdown daily report.")
    parser.add_argument("--trend-input", type=Path, default=trend.DEFAULT_INPUT, help="JSONL archive path for trend input.")
    parser.add_argument("--trend-limit", type=int, default=7, help="Number of recent snapshots to summarize.")
    parser.add_argument("--top-cleanup", type=int, default=3, help="Number of cleanup paths shown.")
    parser.add_argument("--min-cleanup-size-mb", type=int, default=100, help="Minimum cleanup size included.")
    parser.add_argument("--disk-path", type=Path, default=Path("/"), help="Disk path to inspect; default: root.")
    parser.add_argument("--cleanup-path", action="append", type=Path, dest="cleanup_paths", help="Override cleanup candidate path; repeatable.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_daily_report(
        trend_input=args.trend_input,
        trend_limit=args.trend_limit,
        top_cleanup=args.top_cleanup,
        min_cleanup_size_mb=args.min_cleanup_size_mb,
        cleanup_paths=args.cleanup_paths,
        disk_path=args.disk_path,
    )
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if args.markdown:
        print(build_markdown(report))
        return 0

    current = report["current"]
    trend_report = report["trend"]
    print(
        f"ops daily: status={report['status']}, ram_free={current['vps']['ram_free_mb']} MiB, "
        f"disk={current['vps']['disk_used_percent']}% used, trend_snapshots={trend_report['snapshot_count']}, "
        f"cleanup_candidates={current['cleanup']['total_candidate_size_mb']} MiB, report-only"
    )
    for recommendation in report["recommendations"]:
        print(f"- {recommendation}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
