from copy import deepcopy
from datetime import UTC, datetime
from typing import Any


class OfflinePackageRegistry:
    """Local client-side registry for downloaded city packages.

    OFF-3 needs deterministic package management before the mobile UI is wired:
    list installed cities, display storage usage, flag available updates and delete
    downloaded city bundles without touching account/server data.
    """

    def __init__(self, storage_quota_bytes: int | None = None) -> None:
        if storage_quota_bytes is not None and storage_quota_bytes < 0:
            raise ValueError("storage_quota_bytes must be positive")
        self._storage_quota_bytes = storage_quota_bytes
        self._installed: dict[str, dict[str, Any]] = {}

    def install(
        self,
        bundle: dict[str, Any],
        *,
        size_bytes: int,
        installed_at: datetime | str | None = None,
    ) -> dict[str, Any]:
        city_id = _required_text(bundle, "city_id")
        package_version = _required_text(bundle, "package_version")
        model_version = _required_text(bundle, "model_version")
        lang = _required_text(bundle, "lang")
        if not isinstance(size_bytes, int) or size_bytes <= 0:
            raise ValueError("size_bytes must be a positive integer")

        current_size = self._installed.get(city_id, {}).get("size_bytes", 0)
        projected_usage = self.storage_usage()["used_bytes"] - current_size + size_bytes
        if self._storage_quota_bytes is not None and projected_usage > self._storage_quota_bytes:
            raise ValueError("storage quota exceeded")

        manifest = {
            "city_id": city_id,
            "package_version": package_version,
            "model_version": model_version,
            "lang": lang,
            "size_bytes": size_bytes,
            "installed_at": _to_utc_iso(installed_at),
            "monument_count": len(bundle.get("monument_cards", [])),
            "update_available": False,
        }
        self._installed[city_id] = manifest
        return deepcopy(manifest)

    def list_installed(self) -> list[dict[str, Any]]:
        return [deepcopy(package) for package in sorted(self._installed.values(), key=lambda item: item["city_id"])]

    def storage_usage(self) -> dict[str, int | None]:
        used_bytes = sum(package["size_bytes"] for package in self._installed.values())
        quota = self._storage_quota_bytes
        return {
            "used_bytes": used_bytes,
            "quota_bytes": quota,
            "available_bytes": None if quota is None else max(0, quota - used_bytes),
        }

    def mark_update_available(self, city_id: str, latest_package_version: str) -> dict[str, Any]:
        package = self._get_installed(city_id)
        if not isinstance(latest_package_version, str) or not latest_package_version.strip():
            raise ValueError("latest_package_version must be a non-empty string")

        package["update_available"] = latest_package_version != package["package_version"]
        if package["update_available"]:
            package["latest_package_version"] = latest_package_version
        else:
            package.pop("latest_package_version", None)
        return deepcopy(package)

    def delete(self, city_id: str) -> dict[str, Any]:
        self._get_installed(city_id)
        return self._installed.pop(city_id)

    def _get_installed(self, city_id: str) -> dict[str, Any]:
        if city_id not in self._installed:
            raise KeyError("city package is not installed")
        return self._installed[city_id]


def _required_text(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return value.strip()


def _to_utc_iso(value: datetime | str | None) -> str:
    if value is None:
        value = datetime.now(UTC)
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, str) and value.strip():
        return value.strip()
    raise ValueError("installed_at must be a datetime, ISO string or None")
