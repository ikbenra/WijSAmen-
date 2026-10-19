# Export ZIP Preflight

Passive central-directory inspection for a privately stored ChatGPT export ZIP. The tool does not extract, execute, upload or modify archive content.

## Use

Run only after the original ZIP has been stored privately and its size/SHA-256 readback has matched the private manifest:

```sh
python preflight_zip.py /private/path/chatgpt-export.zip
```

Machine-readable output:

```sh
python preflight_zip.py --json /private/path/chatgpt-export.zip
```

The default policy blocks:

- absolute paths, parent traversal and ambiguous empty paths;
- duplicate normalized paths and case-fold collisions;
- symlinks, devices, FIFOs, sockets and unknown special entries;
- encrypted entries;
- oversized entry counts, individual files or total expansion;
- extreme compression ratios and malformed ZIP structures.

Limits are explicit CLI options so an unusually large legitimate export can be reviewed rather than silently accepted.

## Test

```sh
python -m unittest -v test_preflight_zip.py
python -m py_compile preflight_zip.py test_preflight_zip.py
```

A `PASS` is only an extraction-safety precondition. It does not prove source authenticity, archive completeness, benign file contents, matching SHA-256, private sharing state or successful continuity import. Keep every real archive, manifest, filename inventory and private storage locator outside this public repository.

## Bounded extraction

Only after the original ZIP readback, private-manifest validation and preflight all pass:

```sh
python safe_extract_zip.py /private/path/chatgpt-export.zip /private/path/new-import-directory
```

The destination and its parent must be explicitly chosen; the parent must already exist and the destination must not. Extraction happens in a private staging directory and is renamed only after every regular file has been streamed, CRC-checked, size-checked and SHA-256 inventoried. On an error, the generated partial directory is removed. Archived executable permissions and timestamps are not restored.

Default output contains only counts. `--json` prints paths and digests and must remain private. The tool never executes extracted content and never imports it into a continuity system.
