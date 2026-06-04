from tools.report_privacy_retention_controls import build_report


def test_privacy_retention_report_exposes_sec_2_controls() -> None:
    report = build_report()

    assert report["schema_version"] == "privacy-retention-controls-v1"
    assert report["readiness"]["sec_2_minimum_controls_present"] is True

    chat = report["controls"]["chat"]
    assert chat["retention"] == "session_only_client_side"
    assert chat["server_persists_conversation_history"] is False
    assert chat["max_context_messages_used"] == 12

    travel_log = report["controls"]["travel_log"]
    assert travel_log["retention_days"] == 365
    assert travel_log["supports_selective_retention_purge"] is True
    assert travel_log["supports_full_user_deletion"] is True

    hard_cases = report["controls"]["hard_cases"]
    assert hard_cases["max_records"] == 500
    assert hard_cases["supports_full_user_deletion"] is True
    assert hard_cases["stores_metadata_only"] is True
    assert hard_cases["privacy_flags"] == {
        "stores_raw_image": False,
        "stores_raw_embedding": False,
        "stores_precise_location": False,
    }
