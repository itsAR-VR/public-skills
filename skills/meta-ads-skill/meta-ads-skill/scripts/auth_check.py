#!/usr/bin/env python3
"""Diagnose whether the local Meta Ads OAuth database contains a usable token."""

from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import unquote


DEFAULT_DATABASE_URL = "sqlite:///.meta-ads-mcp/oauth.db"

TOKEN_NAME_HINTS = ("token", "credential", "secret")
TABLE_NAME_HINTS = ("token", "oauth", "auth", "credential", "session", "facebook")
GENERIC_VALUE_COLUMNS = {"value", "data", "payload"}

STATUS_COLUMN_HINTS = {"status", "state"}
VALIDITY_COLUMN_HINTS = {"is_valid", "valid", "active", "enabled"}
EXPIRY_COLUMN_HINTS = {
    "expires_at",
    "expires_on",
    "expires",
    "expires_at_utc",
    "token_expires_at",
    "access_token_expires_at",
}
INVALID_STATUS_VALUES = {
    "inactive",
    "disabled",
    "invalid",
    "expired",
    "revoked",
    "missing",
    "pending",
    "failed",
    "error",
    "unauthorized",
}
ACTIVE_STATUS_VALUES = {
    "active",
    "valid",
    "connected",
    "authenticated",
    "authorized",
}
INVALID_MARKER_COLUMNS = {
    "revoked_at",
    "revoked_on",
    "deleted_at",
    "deleted_on",
    "disabled_at",
    "disabled_on",
}


@dataclass
class TokenCheckResult:
    valid: bool
    reason: str


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        try:
            value = value.decode("utf-8")
        except UnicodeDecodeError:
            return ""
    return str(value).strip().lower()


def _is_truthy(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, bytes):
        return len(value) > 0
    text = str(value).strip().lower()
    return text not in {"", "0", "false", "no", "off", "null", "none"}


def _parse_expiry(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        dt = value
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    if isinstance(value, (int, float)):
        timestamp = float(value)
        if abs(timestamp) > 10_000_000_000:
            timestamp /= 1000.0
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)

    text = str(value).strip()
    if not text:
        return None
    try:
        timestamp = float(text)
    except ValueError:
        try:
            dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    if abs(timestamp) > 10_000_000_000:
        timestamp /= 1000.0
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _sqlite_path_from_url(database_url: str | None) -> Path | None:
    if not database_url:
        return None
    database_url = database_url.strip()
    if database_url in {":memory:", "sqlite:///:memory:"}:
        return None
    if database_url.startswith("sqlite:////"):
        raw_path = "/" + unquote(database_url[len("sqlite:////") :].split("?", 1)[0].split("#", 1)[0])
        if raw_path == "/":
            return None
        return Path(raw_path)
    if database_url.startswith("sqlite:///"):
        raw_path = unquote(database_url[len("sqlite:///") :].split("?", 1)[0].split("#", 1)[0])
        if not raw_path:
            return None
        return Path(raw_path)
    if database_url.startswith("sqlite://"):
        raw_path = unquote(database_url[len("sqlite://") :].split("?", 1)[0].split("#", 1)[0])
        if not raw_path:
            return None
        return Path(raw_path)
    return Path(database_url)


def _candidate_database_paths(database_url: str | None) -> list[Path]:
    path = _sqlite_path_from_url(database_url)
    if path is None:
        return []

    candidates: list[Path] = []
    if path.is_absolute():
        candidates.append(path)
    else:
        script_dir = Path(__file__).resolve().parent
        candidates.extend(
            [
                Path.cwd() / path,
                script_dir / path,
            ]
        )
        candidates.extend(parent / path for parent in script_dir.parents)
        candidates.append(path)

    deduped: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate.resolve(strict=False))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(candidate)
    return deduped


def _column_matches_hint(column_name: str, hints: tuple[str, ...]) -> bool:
    lowered = column_name.lower()
    return any(hint in lowered for hint in hints)


def _table_is_auth_related(table_name: str) -> bool:
    lowered = table_name.lower()
    return any(hint in lowered for hint in TABLE_NAME_HINTS)


def _row_has_token_value(table_name: str, row: Mapping[str, Any]) -> tuple[bool, str | None]:
    table_is_auth_related = _table_is_auth_related(table_name)

    for column_name, value in row.items():
        lowered = column_name.lower()
        if _column_matches_hint(lowered, TOKEN_NAME_HINTS):
            if _is_truthy(value):
                return True, column_name
        elif table_is_auth_related and lowered in GENERIC_VALUE_COLUMNS and _is_truthy(value):
            return True, column_name

    return False, None


def _row_status_reason(table_name: str, row: Mapping[str, Any]) -> TokenCheckResult | None:
    token_present, token_column = _row_has_token_value(table_name, row)
    if not token_present:
        return None

    now = datetime.now(timezone.utc)
    explicit_valid = False

    for column_name, value in row.items():
        lowered = column_name.lower()
        text = _normalize_text(value)

        if lowered in INVALID_MARKER_COLUMNS and _is_truthy(value):
            return TokenCheckResult(False, f"{table_name}.{column_name} is set")

        if lowered in STATUS_COLUMN_HINTS:
            if text in INVALID_STATUS_VALUES:
                return TokenCheckResult(False, f"{table_name}.{column_name}={value!r}")
            if text in ACTIVE_STATUS_VALUES:
                explicit_valid = True

        if lowered in VALIDITY_COLUMN_HINTS:
            if not _is_truthy(value):
                return TokenCheckResult(False, f"{table_name}.{column_name}={value!r}")
            explicit_valid = True

        if lowered in EXPIRY_COLUMN_HINTS:
            expiry = _parse_expiry(value)
            if expiry is not None:
                if expiry <= now:
                    return TokenCheckResult(False, f"{table_name}.{column_name}={value!r}")
                explicit_valid = True

    if explicit_valid or token_present:
        return TokenCheckResult(True, f"Found token in {table_name}.{token_column}")

    return None


def _validate_token_database(db_path: Path) -> TokenCheckResult:
    try:
        with sqlite3.connect(db_path) as connection:
            connection.row_factory = sqlite3.Row
            table_rows = connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
            ).fetchall()

            if not table_rows:
                return TokenCheckResult(False, "The OAuth database does not contain any user tables.")

            token_row_found = False
            last_failure: TokenCheckResult | None = None

            for table_row in table_rows:
                table_name = table_row[0]
                table_info = connection.execute(
                    f"PRAGMA table_info({_quote_identifier(table_name)})"
                ).fetchall()
                if not table_info:
                    continue

                rows = connection.execute(f"SELECT * FROM {_quote_identifier(table_name)}")
                for row in rows:
                    row_dict = {key: row[key] for key in row.keys()}
                    status = _row_status_reason(table_name, row_dict)
                    if status is None:
                        continue
                    token_row_found = True
                    if status.valid:
                        return status
                    last_failure = status

            if token_row_found:
                return last_failure or TokenCheckResult(False, "A token row was found, but it is not usable.")

            return TokenCheckResult(False, "No token-bearing rows were found in the OAuth database.")
    except sqlite3.Error as exc:
        return TokenCheckResult(False, f"Could not read the OAuth database: {exc}")


def _print_auth_remediation() -> None:
    print("Please authenticate to continue.")
    print("Action Plan:")
    print(
        "1. Ensure the local OAuth web server is running: python src/auth/run_web_server.py"
    )
    print("2. Visit http://localhost:8000/auth/facebook in your web browser")
    print("3. Grant the requested permissions")
    print("4. Return here once authentication is complete")


def check_auth_status():
    print("Checking Meta Ads API authentication token...")
    database_url = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL).strip()
    candidate_paths = _candidate_database_paths(database_url)

    if not candidate_paths:
        print("Error: No SQLite OAuth database path could be determined.")
        _print_auth_remediation()
        return False

    checked_any_database = False
    last_result: TokenCheckResult | None = None

    for db_path in candidate_paths:
        if not db_path.exists():
            continue
        checked_any_database = True
        last_result = _validate_token_database(db_path)
        if last_result.valid:
            print("Authentication successful! Token is valid.")
            return True

    if not checked_any_database:
        print(f"Error: OAuth database not found at {candidate_paths[0]}.")
    else:
        reason = last_result.reason if last_result else "No valid access token found."
        print(f"Error: No valid access token found. {reason}")

    _print_auth_remediation()
    return False


if __name__ == "__main__":
    check_auth_status()
