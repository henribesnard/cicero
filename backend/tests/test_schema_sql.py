from pathlib import Path
import re


def test_schema_sql_contains_expected_tables() -> None:
    sql_path = Path(__file__).resolve().parents[1] / "sql" / "001_init.sql"
    sql = sql_path.read_text(encoding="utf-8")

    expected_tables = ["cities", "monuments", "media", "monument_i18n"]
    for table in expected_tables:
        pattern = rf"\bCREATE\s+TABLE\s+{re.escape(table)}\b"
        assert re.search(pattern, sql, flags=re.IGNORECASE), (
            f"Missing CREATE TABLE for '{table}' in {sql_path}"
        )
