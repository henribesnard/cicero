#!/usr/bin/env python3
"""Append a lightweight ops guardrail snapshot to a JSONL archive.

This script is report-only except for writing the requested archive file. It is
meant for cron runs that need a tiny historical signal for RAM/disk drift.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:  # Script execution from backend/tools
    import report_ops_guardrails as ops
except ModuleNotFoundError:  # Package import from tests
    from tools import report_ops_guardrails as ops

DEFAULT_OUTPUT = Path("docs/ops/ops_guardrails_snapshots.jsonl")


def utc_now_iso() -> str:
    """Return an archive-friendly UTC timestamp."""
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_snapshot(
    *,
    observed_at: str | None = None,
    top_cleanup: int = 3,
    min_cleanup_size_mb: int = 100,
    cleanup_paths: list[Path] | None = None,
    disk_path: Path = Path("/"),
) -> dict[str, Any]:
    """Return one compact, archivable ops snapshot."""
    report = ops.build_report(
        top_cleanup=top_cleanup,
        min_cleanup_size_mb=min_cleanup_size_mb,
        cleanup_paths=cleanup_paths,
        disk_path=disk_path,
    )
    health = report["health"]
    cleanup = report["cleanup"]
    return {
        "schema_version": "ops-guardrails-snapshot-v1",
        "mode": "archive-jsonl",
        "observed_at": observed_at or utc_now_iso(),
        "status": report["summary"]["status"],
        "load": health["load"],
        "memory": health["memory"],
        "disk": health["disk"],
        "cleanup": {
            "review_needed": report["summary"]["cleanup_review_needed"],
            "total_candidate_size_mb": cleanup["total_candidate_size_mb"],
            "actionable_candidate_count": report["summary"]["actionable_cleanup_count"],
        },
        "recommendation_count": len(report["summary"]["recommendations"]),
    }


def append_snapshot(snapshot: dict[str, Any], output_path: Path) -> Path:
    """Append one JSON object as a JSONL row and return the written path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(snapshot, ensure_ascii=False, sort_keys=True))
        handle.write("\n")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Archive a compact Cicero ops guardrail snapshot as JSONL.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="JSONL archive path to append.")
    parser.add_argument("--dry-run", action="store_true", help="Print the snapshot without writing the archive.")
    parser.add_argument("--top-cleanup", type=int, default=3, help="Number of cleanup candidates considered actionable.")
    parser.add_argument(
        "--min-cleanup-size-mb",
        type=int,
        default=100,
        help="Minimum cleanup candidate size included in the actionable summary.",
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
    snapshot = build_snapshot(
        top_cleanup=args.top_cleanup,
        min_cleanup_size_mb=args.min_cleanup_size_mb,
        cleanup_paths=args.cleanup_paths,
        disk_path=args.disk_path,
    )
    if args.dry_run:
        print(json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    written = append_snapshot(snapshot, args.output)
    print(
        f"ops snapshot archived: path={written}, status={snapshot['status']}, "
        f"ram_free={snapshot['memory']['free_mb']} MiB, "
        f"disk={snapshot['disk']['used_percent']}% used, "
        f"cleanup_candidates={snapshot['cleanup']['total_candidate_size_mb']} MiB"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
