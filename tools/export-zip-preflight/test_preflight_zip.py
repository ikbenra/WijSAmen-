#!/usr/bin/env python3

import stat
import tempfile
import unittest
import zipfile
from pathlib import Path

from preflight_zip import inspect_zip


def write_zip(path: Path, entries: list[tuple[str | zipfile.ZipInfo, bytes]]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, payload in entries:
            zf.writestr(name, payload)


class ZipPreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def result(self, entries, **limits):
        archive = self.root / "sample.zip"
        write_zip(archive, entries)
        return inspect_zip(archive, **limits)

    def test_regular_archive_passes(self):
        result = self.result([("conversations.json", b"[]"), ("assets/readme.txt", b"ok")])
        self.assertEqual(result.status, "PASS")

    def test_parent_traversal_blocks(self):
        result = self.result([("../outside.txt", b"no")])
        self.assertIn("PARENT_TRAVERSAL", {item.code for item in result.findings})

    def test_absolute_path_blocks(self):
        result = self.result([("/absolute.txt", b"no")])
        self.assertIn("ABSOLUTE_PATH", {item.code for item in result.findings})

    def test_windows_drive_path_blocks(self):
        result = self.result([("C:\\outside.txt", b"no")])
        self.assertIn("ABSOLUTE_PATH", {item.code for item in result.findings})

    def test_symlink_blocks(self):
        link = zipfile.ZipInfo("link")
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        result = self.result([(link, b"target")])
        self.assertIn("SPECIAL_ENTRY", {item.code for item in result.findings})

    def test_duplicate_normalized_path_blocks(self):
        result = self.result([("folder/file.txt", b"one"), ("folder/file.txt", b"two")])
        self.assertIn("DUPLICATE_PATH", {item.code for item in result.findings})

    def test_file_directory_target_collision_blocks(self):
        result = self.result([("node", b"file"), ("node/", b"")])
        self.assertIn("DUPLICATE_PATH", {item.code for item in result.findings})

    def test_case_collision_blocks(self):
        result = self.result([("Data.json", b"one"), ("data.json", b"two")])
        self.assertIn("CASE_COLLISION", {item.code for item in result.findings})

    def test_file_size_limit_blocks(self):
        result = self.result([("large.txt", b"12345")], max_file_bytes=4)
        self.assertIn("FILE_TOO_LARGE", {item.code for item in result.findings})

    def test_total_size_limit_blocks(self):
        result = self.result([("a", b"123"), ("b", b"456")], max_total_bytes=5)
        self.assertIn("TOTAL_TOO_LARGE", {item.code for item in result.findings})

    def test_compression_ratio_limit_blocks(self):
        result = self.result([("dense.txt", b"A" * 20_000)], max_ratio=2.0)
        self.assertIn("COMPRESSION_RATIO", {item.code for item in result.findings})

    def test_invalid_archive_blocks(self):
        archive = self.root / "not-a-zip.zip"
        archive.write_bytes(b"not a zip")
        result = inspect_zip(archive)
        self.assertEqual(result.status, "BLOCK")
        self.assertIn("INVALID_ARCHIVE", {item.code for item in result.findings})


if __name__ == "__main__":
    unittest.main()
