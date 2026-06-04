"""Report Cicero's lightweight privacy/retention controls for SEC-2.

This script is intentionally read-only: it imports the in-repo contracts and emits a
small JSON report that can be attached to a release checklist or support response.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def _ensure_app_importable() -> None:
    import sys

    root = str(ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)


def build_report() -> dict[str, Any]:
    _ensure_app_importable()

    from app.hard_case_logger import HardCaseLogger
    from app.main import CHAT_HISTORY_MAX_MESSAGES, CHAT_HISTORY_RETENTION, HARD_CASE_LOGGER
    from app.travel_log import TRAVEL_LOG_RETENTION_DAYS, TravelLog

    hard_case_probe = HardCaseLogger(max_records=HARD_CASE_LOGGER._max_records)  # noqa: SLF001 - operational report.
    empty_export = hard_case_probe.export_retraining_batch()

    controls = {
        "chat": {
            "retention": CHAT_HISTORY_RETENTION,
            "max_context_messages_used": CHAT_HISTORY_MAX_MESSAGES,
            "server_persists_conversation_history": False,
            "deletion_action": "session ends on client / no server-side chat store to erase in MVP",
        },
        "travel_log": {
            "retention_days": TRAVEL_LOG_RETENTION_DAYS,
            "storage_scope": "client_side_local_model",
            "supports_selective_retention_purge": hasattr(TravelLog, "purge_before"),
            "supports_full_user_deletion": hasattr(TravelLog, "clear"),
        },
        "hard_cases": {
            "max_records": HARD_CASE_LOGGER._max_records,  # noqa: SLF001 - operational report.
            "supports_full_user_deletion": hasattr(HardCaseLogger, "clear"),
            "privacy_flags": empty_export["privacy"],
            "stores_metadata_only": not any(empty_export["privacy"].values()),
        },
    }

    readiness = {
        "sec_2_minimum_controls_present": all(
            [
                controls["chat"]["retention"] == "session_only_client_side",
                controls["travel_log"]["supports_selective_retention_purge"],
                controls["travel_log"]["supports_full_user_deletion"],
                controls["hard_cases"]["supports_full_user_deletion"],
                controls["hard_cases"]["stores_metadata_only"],
            ]
        ),
        "manual_review_required_before_production": [
            "map these code-level controls to the public privacy policy wording",
            "define authenticated user identity flow before remote account sync",
            "document operational SLA for data deletion requests",
        ],
    }

    return {"schema_version": "privacy-retention-controls-v1", "controls": controls, "readiness": readiness}


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit a read-only SEC-2 privacy/retention controls report.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args()
    print(json.dumps(build_report(), ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=True))


if __name__ == "__main__":
    main()
