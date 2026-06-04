#!/usr/bin/env python3
"""Build a non-destructive manual review plan for cleanup candidates.

This tool intentionally does not delete, compress, truncate, or mutate anything.
It turns the conservative cleanup candidate report into a path-by-path checklist so
an operator can decide what to inspect manually without touching web/server roots.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:  # Script execution from backend/tools
    import report_safe_cleanup_candidates as cleanup
except ModuleNotFoundError:  # Package import from tests
    from tools import report_safe_cleanup_candidates as cleanup

CATEGORY_RULES: tuple[tuple[str, str, str, tuple[str, ...]], ...] = (
    (
        "python-cache",
        "low",
        "Cache d'outils Python: inspecter les sous-dossiers, puis purger uniquement via l'outil propriétaire si validé.",
        ("pip cache dir", "uv cache dir", "pip cache purge / uv cache clean après validation humaine"),
    ),
    (
        "node-cache",
        "low",
        "Cache npm local: vérifier qu'aucun build en cours ne l'utilise, puis envisager un nettoyage npm contrôlé.",
        ("npm cache verify", "npm cache clean --force seulement après validation humaine"),
    ),
    (
        "system-temp",
        "medium",
        "Répertoire temporaire système: inspecter l'âge et les propriétaires; ne supprimer que les fichiers anciens et non ouverts.",
        ("lsof +D <path> sur un périmètre réduit", "tri manuel par âge avant suppression"),
    ),
    (
        "system-logs",
        "medium",
        "Journaux système: rechercher les gros journaux et préférer rotation/vacuum contrôlé à toute suppression brute.",
        ("journalctl --disk-usage", "logrotate -d", "journalctl --vacuum-size=<taille> après validation"),
    ),
    (
        "generic-cache",
        "low",
        "Cache utilisateur générique: inspecter les plus gros sous-dossiers et nettoyer uniquement les caches identifiés.",
        ("du -h --max-depth=1 <path>", "nettoyage ciblé par outil après validation"),
    ),
)


def classify_path(path: str) -> tuple[str, str, str, tuple[str, ...]]:
    normalized = path.rstrip("/")
    if normalized.endswith("/.cache/pip") or "/.cache/pip" in normalized:
        return CATEGORY_RULES[0]
    if normalized.endswith("/.cache/uv") or "/.cache/uv" in normalized:
        return CATEGORY_RULES[0]
    if normalized.endswith("/.npm") or "/.npm" in normalized:
        return CATEGORY_RULES[1]
    if normalized in {"/tmp", "/var/tmp"}:
        return CATEGORY_RULES[2]
    if normalized == "/var/log" or normalized.startswith("/var/log/"):
        return CATEGORY_RULES[3]
    return CATEGORY_RULES[4]


def urgency_for(size_mb: int, disk_used_percent: float) -> str:
    if disk_used_percent >= 85.0 or size_mb >= 2048:
        return "high"
    if disk_used_percent >= 70.0 or size_mb >= 512:
        return "medium"
    return "low"


def build_plan(
    *,
    min_size_mb: int = 100,
    limit: int | None = None,
    candidate_paths: list[Path] | None = None,
) -> dict[str, Any]:
    cleanup_report = cleanup.build_report(candidate_paths or cleanup.DEFAULT_CANDIDATES)
    disk_used = float(cleanup_report["disk"]["used_percent"])
    candidates = cleanup.actionable_candidates(cleanup_report, min_size_mb=min_size_mb, limit=limit)

    review_items: list[dict[str, Any]] = []
    for row in candidates:
        category, risk, rationale, manual_checks = classify_path(row["path"])
        review_items.append(
            {
                "path": row["path"],
                "size_mb": row["size_mb"],
                "category": category,
                "cleanup_risk": risk,
                "urgency": urgency_for(row["size_mb"], disk_used),
                "rationale": rationale,
                "manual_checks": list(manual_checks),
                "allowed_automation": "none",
                "requires_human_validation": True,
            }
        )

    return {
        "schema_version": "cleanup-review-plan-v1",
        "mode": "report-only",
        "source_schema_version": cleanup_report["schema_version"],
        "disk": cleanup_report["disk"],
        "total_candidate_size_mb": cleanup_report["total_candidate_size_mb"],
        "review_item_count": len(review_items),
        "review_items": review_items,
        "guardrails": [
            "Aucune suppression automatique.",
            "Aucun chemin web/serveur n'est inclus dans le plan.",
            "Toute action de nettoyage reste manuelle et validée par Henri.",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan non destructif de revue manuelle des candidats de nettoyage.")
    parser.add_argument("--json", action="store_true", help="Afficher le plan complet en JSON.")
    parser.add_argument("--min-size-mb", type=int, default=100, help="Taille minimale des candidats à planifier.")
    parser.add_argument("--limit", type=int, default=5, help="Nombre maximal de chemins à afficher/planifier.")
    parser.add_argument(
        "--path",
        action="append",
        type=Path,
        dest="paths",
        help="Remplacer les chemins candidats; option répétable.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plan = build_plan(min_size_mb=args.min_size_mb, limit=args.limit, candidate_paths=args.paths)
    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0

    disk = plan["disk"]
    print(
        f"cleanup review plan: disk={disk['used_percent']}% used, "
        f"items={plan['review_item_count']}, mode=report-only"
    )
    for item in plan["review_items"]:
        print(
            f"- {item['urgency']}\t{item['size_mb']} MiB\t{item['path']}\t"
            f"{item['category']}\trisk={item['cleanup_risk']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
