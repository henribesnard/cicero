#!/usr/bin/env python3
"""Report VPS health against Cicero cron execution guardrails.

This tool is intentionally lightweight and report-only. It helps scheduled runs
choose between normal work and low-resource mode without touching services.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class HealthThresholds:
    min_free_ram_mb: int = 800
    max_load_1m: float = 2.5
    max_disk_used_percent: float = 70.0
    reserve_disk_percent: float = 10.0


def memory_status(meminfo_path: Path = Path("/proc/meminfo")) -> dict[str, int]:
    values: dict[str, int] = {}
    for line in meminfo_path.read_text(encoding="utf-8").splitlines():
        key, _, raw_value = line.partition(":")
        if key in {"MemTotal", "MemFree", "MemAvailable"}:
            values[key] = int(raw_value.split()[0]) // 1024
    return {
        "total_mb": values.get("MemTotal", 0),
        "free_mb": values.get("MemFree", 0),
        "available_mb": values.get("MemAvailable", 0),
    }


def load_status() -> dict[str, float]:
    load_1m, load_5m, load_15m = os.getloadavg()
    return {"load_1m": round(load_1m, 2), "load_5m": round(load_5m, 2), "load_15m": round(load_15m, 2)}


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


def build_report(thresholds: HealthThresholds = HealthThresholds(), disk_path: Path = Path("/")) -> dict[str, Any]:
    memory = memory_status()
    load = load_status()
    disk = disk_status(disk_path)

    light_mode = memory["free_mb"] < thresholds.min_free_ram_mb or load["load_1m"] > thresholds.max_load_1m
    cleanup_review = disk["used_percent"] > thresholds.max_disk_used_percent
    reserve_free_gb = round(disk["total_gb"] * (thresholds.reserve_disk_percent / 100), 2)

    recommendations: list[str] = []
    if light_mode:
        recommendations.append("Mode léger: privilégier veille, tri, rédaction, tests ciblés; éviter builds/téléchargements lourds.")
    if cleanup_review:
        recommendations.append("Disque >70%: proposer un ménage non destructif des caches/logs/temp, sans toucher au serveur web.")
    if disk["free_gb"] < reserve_free_gb:
        recommendations.append("Réserve disque 10% entamée: éviter nouveaux artefacts avant arbitrage.")

    return {
        "schema_version": "vps-health-v1",
        "mode": "report-only",
        "thresholds": thresholds.__dict__,
        "load": load,
        "memory": memory,
        "disk": disk,
        "reserve_disk_free_gb": reserve_free_gb,
        "status": "light" if light_mode else "normal",
        "cleanup_review_needed": cleanup_review,
        "recommendations": recommendations,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report VPS health against cron guardrails.")
    parser.add_argument("--json", action="store_true", help="Print full JSON report.")
    parser.add_argument("--disk-path", type=Path, default=Path("/"), help="Disk path to inspect; default: root.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(disk_path=args.disk_path)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    load = report["load"]
    memory = report["memory"]
    disk = report["disk"]
    print(
        f"vps health: status={report['status']}, "
        f"load={load['load_1m']}/{load['load_5m']}/{load['load_15m']}, "
        f"ram_free={memory['free_mb']} MiB, ram_available={memory['available_mb']} MiB, "
        f"disk={disk['used_percent']}% used, report-only"
    )
    for recommendation in report["recommendations"]:
        print(f"- {recommendation}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
