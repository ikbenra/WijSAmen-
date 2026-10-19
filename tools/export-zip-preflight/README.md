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
