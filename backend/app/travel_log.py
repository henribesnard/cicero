from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


TRAVEL_LOG_RETENTION_DAYS = 365


@dataclass(frozen=True)
class TravelLogEntry:
    monument_id: str
    scanned_at: str
    score: float
    status: str


class TravelLog:
    """Small deterministic client-side carnet model for USR-1.

    The mobile app can persist these entries locally; the backend keeps this pure
    module to lock the contract and sorting behavior with tests before a real
    mobile persistence layer exists.
    """

    def __init__(self) -> None:
        self._entries: list[TravelLogEntry] = []

    def record_scan(
        self,
        monument_id: str,
        score: float,
        status: str = "matched",
        scanned_at: datetime | str | None = None,
    ) -> dict[str, Any]:
        if not isinstance(monument_id, str) or not monument_id.strip():
            raise ValueError("monument_id is required")
        if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 1:
            raise ValueError("score must be between 0 and 1")
        if status not in {"matched", "low_confidence", "not_found"}:
            raise ValueError("status must be matched, low_confidence or not_found")

        scanned_at_iso = _to_utc_iso(scanned_at)
        entry = TravelLogEntry(
            monument_id=monument_id.strip(),
            scanned_at=scanned_at_iso,
            score=round(float(score), 4),
            status=status,
        )
        self._entries.append(entry)
        return _entry_to_dict(entry)

    def list_scans(self, sort: str = "desc") -> list[dict[str, Any]]:
        if sort not in {"asc", "desc"}:
            raise ValueError("sort must be asc or desc")
        return [
            _entry_to_dict(entry)
            for entry in sorted(
                self._entries,
                key=lambda item: item.scanned_at,
                reverse=sort == "desc",
            )
        ]

    def purge_before(self, cutoff: datetime | str) -> int:
        """Delete carnet entries older than ``cutoff`` and return the count removed.

        SEC-2 requires explicit retention/deletion behavior before any account sync.
        This keeps deletion local, deterministic and easy for the mobile client to run
        on startup or when the user changes privacy settings.
        """
        cutoff_iso = _to_utc_iso(cutoff)
        before_count = len(self._entries)
        self._entries = [entry for entry in self._entries if entry.scanned_at >= cutoff_iso]
        return before_count - len(self._entries)

    def clear(self) -> int:
        """Delete the full local carnet and return the count removed."""
        before_count = len(self._entries)
        self._entries.clear()
        return before_count


def _to_utc_iso(value: datetime | str | None) -> str:
    if value is None:
        value = datetime.now(UTC)
    if isinstance(value, str):
        if not value.strip():
            raise ValueError("scanned_at must be a non-empty ISO timestamp")
        return value
    if not isinstance(value, datetime):
        raise ValueError("scanned_at must be a datetime, ISO string or None")
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _entry_to_dict(entry: TravelLogEntry) -> dict[str, Any]:
    return {
        "monument_id": entry.monument_id,
        "scanned_at": entry.scanned_at,
        "score": entry.score,
        "status": entry.status,
    }
