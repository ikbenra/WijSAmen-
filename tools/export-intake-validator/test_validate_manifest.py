#!/usr/bin/env python3

import copy
import unittest

from validate_manifest import validate


VALID = {
    "version": 1,
    "source": {
        "provider": "OpenAI",
        "requested_at": "2026-10-19T02:36:00+02:00",
        "completion_signal_at": "2026-10-19T08:00:00+02:00",
        "acquired_at": "2026-10-19T08:05:00+02:00",
    },
    "artifact": {
        "filename": "chatgpt-export-2026-10-19.zip",
        "byte_size": 123456,
        "sha256": "a" * 64,
    },
    "private_storage": {
        "reference": "PRIVATE_ARCHIVE_REFERENCE",
        "readback_byte_size": 123456,
        "readback_sha256": "a" * 64,
    },
    "intake": {
        "state": "READBACK_VERIFIED",
        "content_sensitivity": "PRIVATE",
        "immutable_original": True,
    },
}


class ValidateManifestTests(unittest.TestCase):
    def test_valid_manifest(self):
        self.assertEqual(validate(copy.deepcopy(VALID)), [])

    def test_hash_mismatch_fails(self):
        data = copy.deepcopy(VALID)
        data["private_storage"]["readback_sha256"] = "b" * 64
        self.assertTrue(any("SHA-256" in item for item in validate(data)))

    def test_size_mismatch_fails(self):
        data = copy.deepcopy(VALID)
        data["private_storage"]["readback_byte_size"] = 123455
        self.assertTrue(any("byte size" in item for item in validate(data)))

    def test_non_private_manifest_fails(self):
        data = copy.deepcopy(VALID)
        data["intake"]["content_sensitivity"] = "PUBLIC"
        self.assertTrue(any("PRIVATE" in item for item in validate(data)))

    def test_time_order_fails(self):
        data = copy.deepcopy(VALID)
        data["source"]["acquired_at"] = "2026-10-19T07:59:00+02:00"
        self.assertTrue(any("predates" in item for item in validate(data)))

    def test_timezone_is_required(self):
        data = copy.deepcopy(VALID)
        data["source"]["requested_at"] = "2026-10-19T02:36:00"
        self.assertTrue(any("timezone" in item for item in validate(data)))

    def test_secret_field_fails(self):
        data = copy.deepcopy(VALID)
        data["download_token"] = "synthetic-secret"
        self.assertTrue(any("forbidden" in item for item in validate(data)))

    def test_nested_secret_field_fails(self):
        data = copy.deepcopy(VALID)
        data["private_storage"]["download_url"] = "https://example.invalid/private"
        self.assertTrue(any("$.private_storage.download_url" in item for item in validate(data)))


if __name__ == "__main__":
    unittest.main()
