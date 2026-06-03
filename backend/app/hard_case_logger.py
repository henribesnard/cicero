import json
from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


HARD_CASE_STATUSES = {"low_confidence", "not_found"}
ALLOWED_FEEDBACK_LABELS = {"correct", "wrong_monument", "unknown", "poor_angle", "too_dark", "other"}


@dataclass(frozen=True)
class HardCaseRecord:
    scan_id: str
    status: str
    score: float
    created_at: str
    model_version: str
    city_id: str | None
    candidate_monument_id: str | None
    user_feedback: str | None
    notes: str | None


class HardCaseLogger:
    """Deterministic local queue for ML-4 hard recognition cases.

    It intentionally stores metadata only: no photo, no raw embedding, no precise GPS.
    The queue can later feed manual review/reindexing without creating a privacy-heavy
    data collection path on the MVP VPS.
    """

    def __init__(self, max_records: int = 500, storage_path: str | Path | None = None) -> None:
        if not isinstance(max_records, int) or max_records <= 0:
            raise ValueError("max_records must be a positive integer")
        self._max_records = max_records
        self._storage_path = Path(storage_path) if storage_path is not None else None
        self._records: list[HardCaseRecord] = []
        self._load_from_storage()

    def record(
        self,
        *,
        scan_id: str,
        status: str,
        score: float,
        model_version: str,
        city_id: str | None = None,
        candidate_monument_id: str | None = None,
        user_feedback: str | None = None,
        notes: str | None = None,
        created_at: datetime | str | None = None,
    ) -> dict[str, Any]:
        scan_id = _required_text(scan_id, "scan_id")
        model_version = _required_text(model_version, "model_version")
        if status not in HARD_CASE_STATUSES:
            raise ValueError("status must be low_confidence or not_found")
        if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 1:
            raise ValueError("score must be between 0 and 1")
        if user_feedback is not None and user_feedback not in ALLOWED_FEEDBACK_LABELS:
            raise ValueError("user_feedback is not an allowed label")

        record = HardCaseRecord(
            scan_id=scan_id,
            status=status,
            score=round(float(score), 4),
            created_at=_to_utc_iso(created_at),
            model_version=model_version,
            city_id=_optional_text(city_id, "city_id"),
            candidate_monument_id=_optional_text(candidate_monument_id, "candidate_monument_id"),
            user_feedback=user_feedback,
            notes=_optional_text(notes, "notes"),
        )
        self._records.append(record)
        overflow = len(self._records) - self._max_records
        if overflow > 0:
            self._records = self._records[overflow:]
        self._persist()
        return _record_to_dict(record)

    def list_records(self, status: str | None = None) -> list[dict[str, Any]]:
        if status is not None and status not in HARD_CASE_STATUSES:
            raise ValueError("status filter must be low_confidence or not_found")
        records = self._records if status is None else [record for record in self._records if record.status == status]
        return [_record_to_dict(record) for record in records]

    def annotate(self, scan_id: str, *, user_feedback: str, notes: str | None = None) -> dict[str, Any]:
        """Attach human-review feedback to an existing hard case without raw signals."""
        scan_id = _required_text(scan_id, "scan_id")
        if user_feedback not in ALLOWED_FEEDBACK_LABELS:
            raise ValueError("user_feedback is not an allowed label")
        notes = _optional_text(notes, "notes")

        for index, record in enumerate(self._records):
            if record.scan_id == scan_id:
                annotated = HardCaseRecord(
                    scan_id=record.scan_id,
                    status=record.status,
                    score=record.score,
                    created_at=record.created_at,
                    model_version=record.model_version,
                    city_id=record.city_id,
                    candidate_monument_id=record.candidate_monument_id,
                    user_feedback=user_feedback,
                    notes=notes,
                )
                self._records[index] = annotated
                self._persist()
                return _record_to_dict(annotated)

        raise KeyError("Hard case not found")

    def export_retraining_batch(self) -> dict[str, Any]:
        counts = {status: 0 for status in sorted(HARD_CASE_STATUSES)}
        feedback_counts = {label: 0 for label in sorted(ALLOWED_FEEDBACK_LABELS)}
        review_records: list[dict[str, Any]] = []
        for record in self._records:
            counts[record.status] += 1
            if record.user_feedback is not None:
                feedback_counts[record.user_feedback] += 1
            review_records.append(
                {
                    **_record_to_dict(record),
                    "review_priority": _review_priority(record),
                }
            )

        return {
            "schema_version": "hard-cases-v1",
            "record_count": len(self._records),
            "counts_by_status": counts,
            "counts_by_feedback": feedback_counts,
            "review_queue": sorted(
                review_records,
                key=lambda record: (-record["review_priority"], record["created_at"], record["scan_id"]),
            ),
            "privacy": {
                "stores_raw_image": False,
                "stores_raw_embedding": False,
                "stores_precise_location": False,
            },
            "records": deepcopy(self.list_records()),
        }

    def clear(self) -> int:
        removed = len(self._records)
        self._records.clear()
        self._persist()
        return removed

    def _load_from_storage(self) -> None:
        if self._storage_path is None or not self._storage_path.exists():
            return

        loaded: list[HardCaseRecord] = []
        for line in self._storage_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            payload = json.loads(line)
            loaded.append(_record_from_dict(payload))

        overflow = len(loaded) - self._max_records
        self._records = loaded[overflow:] if overflow > 0 else loaded

    def _persist(self) -> None:
        if self._storage_path is None:
            return

        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        content = "".join(
            json.dumps(_record_to_dict(record), ensure_ascii=False, sort_keys=True) + "\n" for record in self._records
        )
        self._storage_path.write_text(content, encoding="utf-8")


def _required_text(value: object, key: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return value.strip()


def _optional_text(value: object, key: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string when provided")
    return value.strip()


def _to_utc_iso(value: datetime | str | None) -> str:
    if value is None:
        value = datetime.now(UTC)
    if isinstance(value, str):
        if not value.strip():
            raise ValueError("created_at must be a non-empty ISO timestamp")
        return value.strip()
    if not isinstance(value, datetime):
        raise ValueError("created_at must be a datetime, ISO string or None")
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _record_to_dict(record: HardCaseRecord) -> dict[str, Any]:
    return {
        "scan_id": record.scan_id,
        "status": record.status,
        "score": record.score,
        "created_at": record.created_at,
        "model_version": record.model_version,
        "city_id": record.city_id,
        "candidate_monument_id": record.candidate_monument_id,
        "user_feedback": record.user_feedback,
        "notes": record.notes,
    }


def _record_from_dict(payload: object) -> HardCaseRecord:
    if not isinstance(payload, dict):
        raise ValueError("hard-case JSONL entries must be objects")

    scan_id = _required_text(payload.get("scan_id"), "scan_id")
    status = payload.get("status")
    if status not in HARD_CASE_STATUSES:
        raise ValueError("status must be low_confidence or not_found")

    score = payload.get("score")
    if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 1:
        raise ValueError("score must be between 0 and 1")

    user_feedback = payload.get("user_feedback")
    if user_feedback is not None and user_feedback not in ALLOWED_FEEDBACK_LABELS:
        raise ValueError("user_feedback is not an allowed label")

    return HardCaseRecord(
        scan_id=scan_id,
        status=status,
        score=round(float(score), 4),
        created_at=_required_text(payload.get("created_at"), "created_at"),
        model_version=_required_text(payload.get("model_version"), "model_version"),
        city_id=_optional_text(payload.get("city_id"), "city_id"),
        candidate_monument_id=_optional_text(payload.get("candidate_monument_id"), "candidate_monument_id"),
        user_feedback=user_feedback,
        notes=_optional_text(payload.get("notes"), "notes"),
    )


def _review_priority(record: HardCaseRecord) -> int:
    """Score manual-review value from 0..100 without storing private raw signals."""
    priority = 45 if record.status == "not_found" else 25
    priority += round((1 - record.score) * 25)

    if record.user_feedback in {"wrong_monument", "unknown"}:
        priority += 20
    elif record.user_feedback in {"poor_angle", "too_dark"}:
        priority += 10

    if record.city_id is not None:
        priority += 5
    if record.candidate_monument_id is not None:
        priority += 5
    return min(priority, 100)
