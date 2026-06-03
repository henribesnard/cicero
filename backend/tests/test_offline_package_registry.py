from app.offline import build_offline_bundle
from app.offline_package_registry import OfflinePackageRegistry


def test_install_city_package_tracks_storage_and_update_status() -> None:
    registry = OfflinePackageRegistry(storage_quota_bytes=50_000_000)
    bundle = build_offline_bundle("paris", lang="fr")

    installed = registry.install(bundle, size_bytes=24_576_000, installed_at="2026-06-03T09:00:00Z")

    assert installed == {
        "city_id": "paris",
        "package_version": "2026.06.03-1",
        "model_version": "vision-lite-1.0.0",
        "lang": "fr",
        "size_bytes": 24_576_000,
        "installed_at": "2026-06-03T09:00:00Z",
        "monument_count": 1,
        "update_available": False,
    }
    assert registry.storage_usage() == {
        "used_bytes": 24_576_000,
        "quota_bytes": 50_000_000,
        "available_bytes": 25_424_000,
    }
    assert registry.list_installed() == [installed]

    marked = registry.mark_update_available("paris", latest_package_version="2026.06.10-1")

    assert marked["update_available"] is True
    assert marked["latest_package_version"] == "2026.06.10-1"


def test_delete_city_package_removes_installed_bundle_and_frees_storage() -> None:
    registry = OfflinePackageRegistry(storage_quota_bytes=30_000_000)
    registry.install(build_offline_bundle("paris"), size_bytes=24_576_000, installed_at="2026-06-03T09:00:00Z")

    removed = registry.delete("paris")

    assert removed["city_id"] == "paris"
    assert removed["size_bytes"] == 24_576_000
    assert registry.list_installed() == []
    assert registry.storage_usage()["used_bytes"] == 0


def test_install_rejects_packages_over_storage_quota() -> None:
    registry = OfflinePackageRegistry(storage_quota_bytes=1_000)

    try:
        registry.install(build_offline_bundle("paris"), size_bytes=24_576_000)
    except ValueError as exc:
        assert str(exc) == "storage quota exceeded"
    else:
        raise AssertionError("expected quota rejection")


def test_delete_and_update_unknown_city_are_explicit_errors() -> None:
    registry = OfflinePackageRegistry()

    for action in (lambda: registry.delete("unknown"), lambda: registry.mark_update_available("unknown", "2026.06.10-1")):
        try:
            action()
        except KeyError as exc:
            assert str(exc).strip("'") == "city package is not installed"
        else:
            raise AssertionError("expected missing installed package rejection")
