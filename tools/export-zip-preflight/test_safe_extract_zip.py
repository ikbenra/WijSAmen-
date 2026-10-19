#!/usr/bin/env python3

import hashlib
import os
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path

from safe_extract_zip import ExtractionBlocked, safe_extract


class SafeExtractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def archive(self, entries, *, compression=zipfile.ZIP_DEFLATED):
        path = self.root / "sample.zip"
        with zipfile.ZipFile(path, "w", compression=compression) as zf:
            for name, payload in entries:
                zf.writestr(name, payload)
        return path

    def test_extracts_to_new_directory_with_inventory(self):
        archive = self.archive([("conversations.json", b"[]"), ("assets/note.txt", b"hello")])
        destination = self.root / "out"
        result = safe_extract(archive, destination)
        self.assertEqual(result.status, "EXTRACTED_VERIFIED")
        self.assertEqual((destination / "assets/note.txt").read_bytes(), b"hello")
        inventory = {item.path: item for item in result.inventory}
        self.assertEqual(inventory["assets/note.txt"].sha256, hashlib.sha256(b"hello").hexdigest())

    def test_existing_destination_is_preserved(self):
        archive = self.archive([("file.txt", b"new")])
        destination = self.root / "out"
        destination.mkdir()
        sentinel = destination / "sentinel.txt"
        sentinel.write_text("keep", encoding="utf-8")
        with self.assertRaises(ExtractionBlocked):
            safe_extract(archive, destination)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_traversal_is_blocked_without_destination(self):
        archive = self.archive([("../outside.txt", b"no")])
        destination = self.root / "out"
        with self.assertRaises(ExtractionBlocked):
            safe_extract(archive, destination)
        self.assertFalse(destination.exists())

    def test_symlink_is_blocked(self):
        link = zipfile.ZipInfo("link")
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        archive = self.archive([(link, b"target")])
        with self.assertRaises(ExtractionBlocked):
            safe_extract(archive, self.root / "out")

    def test_executable_permission_is_not_preserved(self):
        executable = zipfile.ZipInfo("run.sh")
        executable.create_system = 3
        executable.external_attr = (stat.S_IFREG | 0o755) << 16
        archive = self.archive([(executable, b"#!/bin/sh\nexit 0\n")])
        destination = self.root / "out"
        safe_extract(archive, destination)
        mode = stat.S_IMODE((destination / "run.sh").stat().st_mode)
        self.assertEqual(mode, 0o600)

    def test_crc_failure_leaves_no_destination_or_partial_directory(self):
        archive = self.archive([("file.txt", b"ORIGINAL")], compression=zipfile.ZIP_STORED)
        raw = archive.read_bytes()
        offset = raw.index(b"ORIGINAL")
        archive.write_bytes(raw[:offset] + b"XRIGINAL" + raw[offset + 8 :])
        destination = self.root / "out"
        with self.assertRaises(zipfile.BadZipFile):
            safe_extract(archive, destination)
        self.assertFalse(destination.exists())
        self.assertEqual(list(self.root.glob(".out.partial-*")), [])


if __name__ == "__main__":
    unittest.main()
