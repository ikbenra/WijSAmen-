#!/usr/bin/env python3
"""Extract a preflight-approved ZIP into a new directory with bounded writes."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path

from preflight_zip import (
    DEFAULT_MAX_ENTRIES,
    DEFAULT_MAX_FILE_BYTES,
    DEFAULT_MAX_RATIO,
    DEFAULT_MAX_TOTAL_BYTES,
    inspect_zip,
    normalized_entry_name,
)


CHUNK_BYTES = 1024 * 1024


class ExtractionBlocked(RuntimeError):
    """Raised when extraction cannot complete without weakening a safety invariant."""


@dataclass(frozen=True)
class InventoryEntry:
    path: str
    byte_size: int
    sha256: str


@dataclass(frozen=True)
class ExtractionResult:
    status: str
    destination: str
    file_count: int
    total_bytes: int
    inventory: tuple[InventoryEntry, ...]


def _open_new_regular_file(path: Path):
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    return os.fdopen(descriptor, "wb")


def safe_extract(
    archive: Path,
    destination: Path,
    *,
    max_entries: int = DEFAULT_MAX_ENTRIES,
    max_total_bytes: int = DEFAULT_MAX_TOTAL_BYTES,
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES,
    max_ratio: float = DEFAULT_MAX_RATIO,
) -> ExtractionResult:
    archive = archive.resolve()
    destination = destination.resolve(strict=False)
    parent = destination.parent

    if destination.exists():
        raise ExtractionBlocked("destination already exists; refusing to merge or overwrite")
    if not parent.is_dir():
        raise ExtractionBlocked("destination parent must already exist")

    preflight = inspect_zip(
        archive,
        max_entries=max_entries,
        max_total_bytes=max_total_bytes,
        max_file_bytes=max_file_bytes,
        max_ratio=max_ratio,
    )
    if preflight.status != "PASS":
        codes = ", ".join(sorted({item.code for item in preflight.findings}))
        raise ExtractionBlocked(f"ZIP preflight blocked extraction: {codes}")

    staging = Path(tempfile.mkdtemp(prefix=f".{destination.name}.partial-", dir=parent))
    os.chmod(staging, 0o700)
    inventory: list[InventoryEntry] = []
    total_written = 0

    try:
        root = staging.resolve()
        with zipfile.ZipFile(archive, "r") as zf:
            for info in zf.infolist():
                normalized, findings = normalized_entry_name(info.filename)
                if normalized is None or findings:
                    raise ExtractionBlocked("entry path changed after successful preflight")

                relative = normalized.rstrip("/")
                target = staging.joinpath(*relative.split("/"))
                resolved_target = target.resolve(strict=False)
                if not resolved_target.is_relative_to(root):
                    raise ExtractionBlocked("resolved entry escaped the staging directory")

                if info.is_dir() or normalized.endswith("/"):
                    target.mkdir(mode=0o700, parents=True, exist_ok=True)
                    os.chmod(target, 0o700)
                    continue

                target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
                digest = hashlib.sha256()
                file_written = 0
                with zf.open(info, "r") as source, _open_new_regular_file(target) as sink:
                    while True:
                        chunk = source.read(CHUNK_BYTES)
                        if not chunk:
                            break
                        file_written += len(chunk)
                        total_written += len(chunk)
                        if file_written > max_file_bytes:
                            raise ExtractionBlocked("actual file bytes exceeded the configured limit")
                        if total_written > max_total_bytes:
                            raise ExtractionBlocked("actual total bytes exceeded the configured limit")
                        digest.update(chunk)
                        sink.write(chunk)

                if file_written != info.file_size:
                    raise ExtractionBlocked("actual file size did not match central-directory metadata")
                os.chmod(target, 0o600)
                inventory.append(
                    InventoryEntry(relative, file_written, digest.hexdigest())
                )

        if destination.exists():
            raise ExtractionBlocked("destination appeared during extraction; refusing to replace it")
        os.rename(staging, destination)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise

    return ExtractionResult(
        "EXTRACTED_VERIFIED",
        str(destination),
        len(inventory),
        total_written,
        tuple(inventory),
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Preflight and extract a ZIP into a fresh directory without executing content."
    )
    parser.add_argument("archive", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--max-entries", type=int, default=DEFAULT_MAX_ENTRIES)
    parser.add_argument("--max-total-bytes", type=int, default=DEFAULT_MAX_TOTAL_BYTES)
    parser.add_argument("--max-file-bytes", type=int, default=DEFAULT_MAX_FILE_BYTES)
    parser.add_argument("--max-ratio", type=float, default=DEFAULT_MAX_RATIO)
    parser.add_argument("--json", action="store_true", help="print the private file inventory as JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if min(args.max_entries, args.max_total_bytes, args.max_file_bytes) <= 0 or args.max_ratio <= 0:
        print("limits must be positive", file=sys.stderr)
        return 2
    try:
        result = safe_extract(
            args.archive,
            args.destination,
            max_entries=args.max_entries,
            max_total_bytes=args.max_total_bytes,
            max_file_bytes=args.max_file_bytes,
            max_ratio=args.max_ratio,
        )
    except (ExtractionBlocked, OSError, zipfile.BadZipFile, RuntimeError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        print(
            f"{result.status}: {result.file_count} regular files; "
            f"{result.total_bytes} bytes; destination created"
        )
        print("Inventory paths and SHA-256 values are available only with --json; keep that output private.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
