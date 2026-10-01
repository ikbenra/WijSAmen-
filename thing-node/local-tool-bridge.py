#!/usr/bin/env python3
"""WijSAmen local tool bridge v0.1.

Loopback-only HTTP bridge exposing a very small read-only allowlist to local agents.
No arbitrary command, path, package or argument is accepted from HTTP input.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
DOCTOR = HERE / "a52s-doctor.sh"
RISH_SAFE = HERE / "rish-safe.sh"
CAPS = Path.home() / "wijsamen-node/state/capabilities.json"

TOOLS = {
    "identity": ["bash", str(RISH_SAFE), "id"],
    "model": ["bash", str(RISH_SAFE), "model"],
    "battery": ["bash", str(RISH_SAFE), "battery"],
    "thermal": ["bash", str(RISH_SAFE), "thermal"],
    "focus": ["bash", str(RISH_SAFE), "focus"],
    "visible": ["bash", str(RISH_SAFE), "visible"],
    "wm": ["bash", str(RISH_SAFE), "wm"],
    "adb_state": ["bash", str(RISH_SAFE), "adb-state"],
    "bluetooth_state": ["bash", str(RISH_SAFE), "bluetooth-state"],
    "asi": ["bash", str(RISH_SAFE), "asi"],
}


def run_fixed(argv: list[str], timeout: int = 12) -> dict:
    try:
        p = subprocess.run(argv, text=True, capture_output=True, timeout=timeout)
        return {
            "ok": p.returncode == 0,
            "returncode": p.returncode,
            "stdout": p.stdout[-20000:],
            "stderr": p.stderr[-5000:],
        }
    except subprocess.TimeoutExpired as e:
        return {"ok": False, "returncode": None, "stdout": e.stdout or "", "stderr": "timeout"}
    except Exception as e:
        return {"ok": False, "returncode": None, "stdout": "", "stderr": f"{type(e).__name__}: {e}"}


def read_caps(refresh: bool = False) -> dict:
    if refresh or not CAPS.exists():
        CAPS.parent.mkdir(parents=True, exist_ok=True)
        run_fixed(["bash", str(DOCTOR), str(CAPS)], timeout=30)
    try:
        return json.loads(CAPS.read_text(encoding="utf-8"))
    except Exception as e:
        return {"error": f"capabilities unavailable: {type(e).__name__}: {e}"}


class Handler(BaseHTTPRequestHandler):
    server_version = "WijSAmenLocalToolBridge/0.1"

    def log_message(self, fmt, *args):
        # Keep HTTP access log local and concise.
        print("bridge:", fmt % args)

    def send_json(self, status: int, obj: dict):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        p = urlparse(self.path)
        if p.path == "/health":
            return self.send_json(200, {
                "ok": True,
                "protocol": "WIJSAMEN-LOCAL-TOOLS/0.1",
                "bind": "loopback-only",
                "read_only": True,
                "tools": sorted(TOOLS),
            })
        if p.path == "/capabilities":
            return self.send_json(200, read_caps(refresh=False))
        if p.path == "/capabilities/refresh":
            return self.send_json(200, read_caps(refresh=True))
        if p.path.startswith("/tool/"):
            name = p.path[len("/tool/"):]
            argv = TOOLS.get(name)
            if argv is None:
                return self.send_json(404, {"ok": False, "error": "tool not in read-only allowlist"})
            return self.send_json(200, {"tool": name, **run_fixed(argv)})
        return self.send_json(404, {"ok": False, "error": "not found"})

    def do_POST(self):
        # There are intentionally no state-changing HTTP methods in v0.1.
        return self.send_json(405, {"ok": False, "error": "read-only bridge; POST disabled"})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=int(os.environ.get("WIJSAMEN_TOOL_PORT", "8091")))
    args = ap.parse_args()
    host = "127.0.0.1"
    srv = ThreadingHTTPServer((host, args.port), Handler)
    print(f"WIJSAMEN local read-only tool bridge: http://{host}:{args.port}")
    print("No arbitrary shell. No non-loopback bind. Ctrl-C stops.")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
