#!/usr/bin/env python3
"""Passively inspect ZIP central-directory metadata before extraction."""

from __future__ import annotations

import argparse
import json
import re
import stat
import sys
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path


DRIVE_PREFIX = re.compile(r"^[A-Za-z]:")
DEFAULT_MAX_ENTRIES = 200_000
DEFAULT_MAX_TOTAL_BYTES = 20 * 1024**3
DEFAULT_MAX_FILE_BYTES = 5 * 1024**3
DEFAULT_MAX_RATIO = 1_000.0


@dataclass(frozen=True)
class Finding:
    code: str
    entry: str | None
    detail: str


@dataclass(frozen=True)
class Result:
    status: str
    entries: int
    total_uncompressed_bytes: int
    total_compressed_bytes: int
    findings: tuple[Finding, ...]


def _normalized_name(raw: str) -> tuple[str | None, list[Finding]]:
    findings: list[Finding] = []
    if "\x00" in raw:
        findings.append(Finding("NUL_IN_NAME", raw, "entry name contains a NUL byte"))

    portable = raw.replace("\\", "/")
    if portable.startswith("/") or DRIVE_PREFIX.match(portable):
        findings.append(Finding("ABSOLUTE_PATH", raw, "entry uses an absolute path"))

    is_directory = portable.endswith("/")
    parts = portable.rstrip("/").split("/") if portable.rstrip("/") else []
    if any(part == ".." for part in parts):
        findings.append(Finding("PARENT_TRAVERSAL", raw, "entry contains a '..' component"))
    if any(part == "" for part in parts):
        findings.append(Finding("AMBIGUOUS_PATH", raw, "entry contains an empty path component"))

    clean_parts = [part for part in parts if part not in {"", ".", ".."}]
    normalized = "/".join(clean_parts)
    if is_directory and normalized:
        normalized += "/"
    if not normalized:
        findings.append(Finding("EMPTY_PATH", raw, "entry does not resolve to a file or directory name"))
        return None, findings
    return normalized, findings


def _entry_type(info: zipfile.ZipInfo) -> str:
    mode = (info.external_attr >> 16) & 0xFFFF
    if not mode:
        return "directory" if info.is_dir() else "regular"
    kind = stat.S_IFMT(mode)
    if kind == stat.S_IFDIR:
        return "directory"
    if kind == stat.S_IFREG or kind == 0:
        return "regular"
    if kind == stat.S_IFLNK:
        return "symlink"
    if kind == stat.S_IFCHR:
        return "character-device"
    if kind == stat.S_IFBLK:
        return "block-device"
    if kind == stat.S_IFIFO:
        return "fifo"
    if kind == stat.S_IFSOCK:
        return "socket"
    return "unknown-special"


def inspect_zip(
    archive: Path,
    *,
    max_entries: int = DEFAULT_MAX_ENTRIES,
    max_total_bytes: int = DEFAULT_MAX_TOTAL_BYTES,
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES,
    max_ratio: float = DEFAULT_MAX_RATIO,
) -> Result:
    findings: list[Finding] = []
    seen_exact: set[str] = set()
    seen_folded: dict[str, str] = {}
    total_uncompressed = 0
    total_compressed = 0

    try:
        with zipfile.ZipFile(archive, "r") as zf:
            infos = zf.infolist()
            if len(infos) > max_entries:
                findings.append(
                    Finding("TOO_MANY_ENTRIES", None, f"{len(infos)} exceeds limit {max_entries}")
                )

            for info in infos:
                total_uncompressed += info.file_size
                total_compressed += info.compress_size
                normalized, path_findings = _normalized_name(info.filename)
                findings.extend(path_findings)

                if normalized is not None:
                    if normalized in seen_exact:
                        findings.append(
                            Finding("DUPLICATE_PATH", info.filename, f"duplicate normalized path {normalized!r}")
                        )
                    seen_exact.add(normalized)

                    folded = normalized.casefold()
                    prior = seen_folded.get(folded)
                    if prior is not None and prior != normalized:
                        findings.append(
                            Finding(
                                "CASE_COLLISION",
                                info.filename,
                                f"{normalized!r} collides with {prior!r} on case-insensitive filesystems",
                            )
                        )
                    else:
                        seen_folded[folded] = normalized

                kind = _entry_type(info)
                if kind not in {"regular", "directory"}:
                    findings.append(
                        Finding("SPECIAL_ENTRY", info.filename, f"unsupported entry type: {kind}")
                    )

                if info.flag_bits & 0x1:
                    findings.append(
                        Finding("ENCRYPTED_ENTRY", info.filename, "encrypted entries are not accepted")
                    )

                if info.file_size > max_file_bytes:
                    findings.append(
                        Finding(
                            "FILE_TOO_LARGE",
                            info.filename,
                            f"{info.file_size} bytes exceeds per-file limit {max_file_bytes}",
                        )
                    )

                if info.file_size > 0:
                    if info.compress_size == 0:
                        findings.append(
                            Finding("ZERO_COMPRESSED_SIZE", info.filename, "non-empty entry reports zero compressed bytes")
                        )
                    else:
                        ratio = info.file_size / info.compress_size
                        if ratio > max_ratio:
                            findings.append(
                                Finding(
                                    "COMPRESSION_RATIO",
                                    info.filename,
                                    f"ratio {ratio:.1f}:1 exceeds limit {max_ratio:.1f}:1",
                                )
                            )

    except (OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
        findings.append(Finding("INVALID_ARCHIVE", None, str(exc)))
        return Result("BLOCK", 0, 0, 0, tuple(findings))

    if total_uncompressed > max_total_bytes:
        findings.append(
            Finding(
                "TOTAL_TOO_LARGE",
                None,
                f"{total_uncompressed} bytes exceeds total limit {max_total_bytes}",
            )
        )

    return Result(
        "PASS" if not findings else "BLOCK",
        len(infos),
        total_uncompressed,
        total_compressed,
        tuple(findings),
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect ZIP metadata without extracting or executing archive content."
    )
    parser.add_argument("archive", type=Path)
    parser.add_argument("--max-entries", type=int, default=DEFAULT_MAX_ENTRIES)
    parser.add_argument("--max-total-bytes", type=int, default=DEFAULT_MAX_TOTAL_BYTES)
    parser.add_argument("--max-file-bytes", type=int, default=DEFAULT_MAX_FILE_BYTES)
    parser.add_argument("--max-ratio", type=float, default=DEFAULT_MAX_RATIO)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if min(args.max_entries, args.max_total_bytes, args.max_file_bytes) <= 0 or args.max_ratio <= 0:
        print("limits must be positive", file=sys.stderr)
        return 2

    result = inspect_zip(
        args.archive,
        max_entries=args.max_entries,
        max_total_bytes=args.max_total_bytes,
        max_file_bytes=args.max_file_bytes,
        max_ratio=args.max_ratio,
    )
    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        print(
            f"{result.status}: {result.entries} entries; "
            f"{result.total_uncompressed_bytes} uncompressed bytes; "
            f"{result.total_compressed_bytes} compressed bytes"
        )
        for finding in result.findings:
            where = f" [{finding.entry}]" if finding.entry is not None else ""
            print(f"- {finding.code}{where}: {finding.detail}")
    return 0 if result.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
