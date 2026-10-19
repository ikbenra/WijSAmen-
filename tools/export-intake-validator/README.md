# Export Intake Validator

Small standard-library validator for the private manifest described by the [ChatGPT Export Intake Gate](../../docs/CHATGPT_EXPORT_INTAKE.md).

It checks only metadata and readback invariants. It does **not** open, extract, upload or execute the export archive.

## Use

Keep the real manifest private. From this directory:

```sh
python validate_manifest.py /private/path/export-intake-manifest.json
```

Exit code `0` means the required fields are present and artifact/readback size plus SHA-256 agree. It does not prove that the archive is complete, authentic or safely imported.

Run the synthetic tests with:

```sh
python -m unittest -v test_validate_manifest.py
```

`manifest.example.json` contains placeholders only. Never commit a real manifest, storage locator, download URL, token, email body or chat content.
