#!/usr/bin/env python3
"""Validate a private ChatGPT-export intake manifest without opening the archive."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ALLOWED_STATES = (
    "REQUESTED",
    "COMPLETION_SIGNAL_VERIFIED",
    "ACQUIRED",
    "HASHED",
    "STORED_PRIVATE",
    "READBACK_VERIFIED",
    "INTAKE_READY",
)


def _timestamp(value: object, field: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str) or not value:
        errors.append(f"{field} must be a non-empty ISO-8601 timestamp")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{field} is not a valid ISO-8601 timestamp")
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        errors.append(f"{field} must include a timezone offset")
        return None
    return parsed


def _forbidden_paths(value: object, prefix: str = "$") -> list[str]:
    forbidden = {"download_url", "download_token", "email_body", "chat_content"}
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}"
            if key in forbidden:
                found.append(path)
            found.extend(_forbidden_paths(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_forbidden_paths(child, f"{prefix}[{index}]"))
    return found


def validate(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest root must be an object"]

    if data.get("version") != 1:
        errors.append("version must equal 1")

    source = data.get("source")
    artifact = data.get("artifact")
    storage = data.get("private_storage")
    intake = data.get("intake")
    for name, value in (
        ("source", source),
        ("artifact", artifact),
        ("private_storage", storage),
        ("intake", intake),
    ):
        if not isinstance(value, dict):
            errors.append(f"{name} must be an object")

    if errors:
        return errors

    if source.get("provider") != "OpenAI":
        errors.append("source.provider must equal OpenAI")

    requested = _timestamp(source.get("requested_at"), "source.requested_at", errors)
    completed = _timestamp(
        source.get("completion_signal_at"), "source.completion_signal_at", errors
    )
    acquired = _timestamp(source.get("acquired_at"), "source.acquired_at", errors)
    if requested and completed and completed < requested:
        errors.append("completion signal predates the request")
    if completed and acquired and acquired < completed:
        errors.append("acquisition predates the completion signal")

    filename = artifact.get("filename")
    if not isinstance(filename, str) or not filename.lower().endswith(".zip"):
        errors.append("artifact.filename must identify a ZIP file")

    byte_size = artifact.get("byte_size")
    readback_size = storage.get("readback_byte_size")
    if not isinstance(byte_size, int) or isinstance(byte_size, bool) or byte_size <= 0:
        errors.append("artifact.byte_size must be a positive integer")
    if not isinstance(readback_size, int) or isinstance(readback_size, bool) or readback_size <= 0:
        errors.append("private_storage.readback_byte_size must be a positive integer")
    if isinstance(byte_size, int) and isinstance(readback_size, int) and byte_size != readback_size:
        errors.append("readback byte size does not match the acquired artifact")

    digest = artifact.get("sha256")
    readback_digest = storage.get("readback_sha256")
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        errors.append("artifact.sha256 must be 64 lowercase hexadecimal characters")
    if not isinstance(readback_digest, str) or not SHA256_RE.fullmatch(readback_digest):
        errors.append("private_storage.readback_sha256 must be 64 lowercase hexadecimal characters")
    if isinstance(digest, str) and isinstance(readback_digest, str) and digest != readback_digest:
        errors.append("readback SHA-256 does not match the acquired artifact")

    reference = storage.get("reference")
    if not isinstance(reference, str) or not reference.strip():
        errors.append("private_storage.reference must be a non-empty private locator")

    state = intake.get("state")
    if state not in ALLOWED_STATES:
        errors.append("intake.state is not recognized")
    if intake.get("content_sensitivity") != "PRIVATE":
        errors.append("intake.content_sensitivity must equal PRIVATE")
    if intake.get("immutable_original") is not True:
        errors.append("intake.immutable_original must be true")
    if state in {"READBACK_VERIFIED", "INTAKE_READY"}:
        if byte_size != readback_size or digest != readback_digest:
            errors.append(f"{state} requires matching size and SHA-256 readback")

    present = sorted(_forbidden_paths(data))
    if present:
        errors.append("forbidden secret/content fields: " + ", ".join(present))

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {Path(argv[0]).name} PRIVATE_MANIFEST.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1

    errors = validate(data)
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID: private export artifact and readback agree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
