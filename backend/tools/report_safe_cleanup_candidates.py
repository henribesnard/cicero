#!/usr/bin/env python3
"""Report non-destructive disk cleanup candidates for a modest VPS.

The script only inspects conservative cache/log/temp locations. It never deletes
files and intentionally excludes common web/server document roots.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

DEFAULT_CANDIDATES = [
    Path.home() / ".cache",
    Path.home() / ".npm",
    Path.home() / ".cache" / "pip",
    Path.home() / ".cache" / "uv",
    Path.home() / ".local" / "share" / "pipx",
    Path("/tmp"),
    Path("/var/tmp"),
    Path("/var/log"),
]

EXCLUDED_PREFIXES = [
    Path("/var/www"),
    Path("/srv/www"),
    Path("/srv/http"),
    Path("/etc/nginx"),
    Path("/etc/apache2"),
]


@dataclass(frozen=True)
class CleanupCandidate:
    path: str
    exists: bool
    size_mb: int
    note: str


def is_excluded(path: Path, excluded_prefixes: Iterable[Path] = EXCLUDED_PREFIXES) -> bool:
    resolved = path.resolve(strict=False)
    for prefix in excluded_prefixes:
        try:
            resolved.relative_to(prefix.resolve(strict=False))
            return True
        except ValueError:
            continue
    return False


def directory_size_mb(path: Path) -> int:
    """Return an approximate directory/file size using du, rounded up to MiB.

    Some broad temp/log directories can contain unreadable children. GNU du still
    prints a useful top-level size before returning non-zero, so parse stdout
    when available and let callers mark only truly unmeasurable paths unreadable.
    """
    if not path.exists():
        return 0
    result = subprocess.run(
        ["du", "-sm", "--", str(path)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.stdout.split():
        first_field = result.stdout.split()[0]
        return int(first_field)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, result.args, result.stdout, result.stderr)
    return 0


def disk_status(path: Path = Path("/")) -> dict[str, Any]:
    usage = shutil.disk_usage(path)
    used_percent = round((usage.used / usage.total) * 100, 1) if usage.total else 0.0
    return {
        "path": str(path),
        "total_gb": round(usage.total / (1024**3), 2),
        "used_gb": round(usage.used / (1024**3), 2),
        "free_gb": round(usage.free / (1024**3), 2),
        "used_percent": used_percent,
    }


def build_report(candidates: Iterable[Path] = DEFAULT_CANDIDATES) -> dict[str, Any]:
    rows: list[CleanupCandidate] = []
    for candidate in candidates:
        if is_excluded(candidate):
            rows.append(CleanupCandidate(str(candidate), candidate.exists(), 0, "excluded: web/server path"))
            continue
        try:
            size_mb = directory_size_mb(candidate)
            note = "candidate: inspect before manual cleanup" if size_mb else "missing or empty"
        except (OSError, subprocess.CalledProcessError) as exc:
            size_mb = 0
            note = f"unreadable: {exc.__class__.__name__}"
        rows.append(CleanupCandidate(str(candidate), candidate.exists(), size_mb, note))

    rows.sort(key=lambda row: row.size_mb, reverse=True)
    disk = disk_status(Path("/"))
    reserve_10_percent_free_gb = round(disk["total_gb"] * 0.10, 2)
    recommended_manual_actions = []
    if disk["used_percent"] >= 70.0:
        recommended_manual_actions.append(
            "Disk at or above 70%: review top cache/log/temp candidates before any manual cleanup."
        )
    if disk["free_gb"] < reserve_10_percent_free_gb:
        recommended_manual_actions.append(
            "Free disk is below the 10% reserve: avoid new downloads/build artifacts until space is recovered."
        )
    return {
        "schema_version": "safe-cleanup-candidates-v1",
        "mode": "report-only",
        "disk": disk,
        "candidates": [row.__dict__ for row in rows],
        "total_candidate_size_mb": sum(row.size_mb for row in rows),
        "reserve_10_percent_free_gb": reserve_10_percent_free_gb,
        "recommended_manual_actions": recommended_manual_actions,
        "guardrails": [
            "No deletion is performed by this script.",
            "Web/server paths are excluded from candidates.",
            "Manual review is required before cleanup.",
        ],
    }


def actionable_candidates(report: dict[str, Any], min_size_mb: int = 1, limit: int | None = None) -> list[dict[str, Any]]:
    """Return cleanup candidates worth reviewing, without changing report data.

    Excluded, missing, empty, and tiny paths are useful audit data but create
    noise in a cron report. This helper keeps the full JSON schema intact while
    making the command-line summary directly actionable for a low-quota VPS.
    """
    rows = [
        row
        for row in report["candidates"]
        if row["exists"] and row["size_mb"] >= min_size_mb and not row["note"].startswith("excluded:")
    ]
    if limit is not None:
        return rows[:limit]
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report safe disk cleanup candidates without deleting anything.")
    parser.add_argument("--json", action="store_true", help="Print full JSON report.")
    parser.add_argument("--top", type=int, default=5, help="Number of actionable candidates to print in text mode.")
    parser.add_argument(
        "--min-size-mb",
        type=int,
        default=1,
        help="Minimum candidate size shown in text mode; JSON still includes every candidate.",
    )
    parser.add_argument(
        "--path",
        action="append",
        type=Path,
        dest="paths",
        help="Override candidate path; repeatable. Defaults to conservative cache/log/temp paths.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(args.paths or DEFAULT_CANDIDATES)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    disk = report["disk"]
    print(
        f"safe cleanup report: disk {disk['used_percent']}% used, "
        f"{report['total_candidate_size_mb']} MiB candidate(s), report-only"
    )
    for row in actionable_candidates(report, min_size_mb=args.min_size_mb, limit=args.top):
        print(f"- {row['size_mb']} MiB\t{row['path']}\t{row['note']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
