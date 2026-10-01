#!/usr/bin/env python3
"""WijSAmen Project Miner v0.1

Local-first scanner for ChatGPT export JSON/JSONL. It preserves raw message text
and source hashes, then derives a separate, explicitly heuristic action inventory.
Nothing is uploaded and no model/API is required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Iterator

DEFAULT_KEYWORDS = [
    "wijsamen", "chatty", "autonoompje", "arty", "continuity", "continuïteit",
    "a52s", "termux", "shizuku", "vulkan", "github", "thing-node", "hive",
    "agent", "llama.cpp", "qwen", "companion", "provenance", "fork",
]

CATEGORY_PATTERNS = {
    "constraint": re.compile(r"\b(nooit|niet|alleen|uitsluitend|moet niet|mag niet|vereist|required|only|never|without)\b", re.I),
    "decision": re.compile(r"\b(besluit|besloten|gekozen|keuze|afgesproken|decision|decided|chosen)\b", re.I),
    "unfinished": re.compile(r"\b(todo|volgende stap|openstaand|nog doen|onaf|unfinished|next step|blocked|blokkade)\b", re.I),
    "artifact": re.compile(r"\b([\w.-]+\.(?:py|sh|md|json|jsonl|zip|kt|java|txt|yml|yaml))\b", re.I),
    "idea": re.compile(r"\b(idee|zou kunnen|kunnen we|concept|hypothese|prototype|idea|could|maybe|perhaps)\b", re.I),
}

FILELIKE_RE = re.compile(r"[\w./-]+\.(?:py|sh|md|json|jsonl|zip|kt|java|txt|yml|yaml)\b", re.I)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()


def json_dump(obj, path: Path) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def iter_input_files(inputs: list[str]) -> Iterator[Path]:
    seen: set[Path] = set()
    for raw in inputs:
        p = Path(raw).expanduser()
        if p.is_dir():
            candidates = sorted([*p.rglob("*.json"), *p.rglob("*.jsonl")])
        else:
            candidates = [p]
        for c in candidates:
            try:
                r = c.resolve()
            except Exception:
                r = c
            if r not in seen and c.is_file():
                seen.add(r)
                yield c


def text_from_content(content) -> str:
    if not isinstance(content, dict):
        return ""
    parts = content.get("parts")
    if isinstance(parts, list):
        out: list[str] = []
        for part in parts:
            if isinstance(part, str):
                out.append(part)
            elif isinstance(part, dict):
                # Keep only explicit textual fields; never serialize binary pointers.
                for key in ("text", "transcript", "caption"):
                    value = part.get(key)
                    if isinstance(value, str) and value.strip():
                        out.append(value)
        return "\n".join(out).strip()
    text = content.get("text")
    return text if isinstance(text, str) else ""


def messages_from_conversation(conv: dict, source: str, source_sha: str) -> Iterator[dict]:
    cid = str(conv.get("conversation_id") or conv.get("id") or "")
    title = str(conv.get("title") or "")
    mapping = conv.get("mapping")
    if isinstance(mapping, dict):
        for node_id, node in mapping.items():
            if not isinstance(node, dict):
                continue
            msg = node.get("message")
            if not isinstance(msg, dict):
                continue
            author = msg.get("author") if isinstance(msg.get("author"), dict) else {}
            role = str(author.get("role") or "unknown")
            text = text_from_content(msg.get("content"))
            if not text:
                continue
            yield {
                "source": source,
                "source_sha256": source_sha,
                "conversation_id": cid,
                "conversation_title": title,
                "node_id": str(node_id),
                "message_id": str(msg.get("id") or node_id),
                "parent_id": node.get("parent"),
                "role": role,
                "created": msg.get("create_time"),
                "model": (msg.get("metadata") or {}).get("model_slug") if isinstance(msg.get("metadata"), dict) else None,
                "text": text,
                "text_sha256": sha256_text(text),
            }
        return

    # Generic JSONL / already-normalized records.
    text = conv.get("text")
    if isinstance(text, str) and text:
        yield {
            "source": source,
            "source_sha256": source_sha,
            "conversation_id": cid,
            "conversation_title": title,
            "node_id": str(conv.get("node_id") or ""),
            "message_id": str(conv.get("message_id") or conv.get("id") or ""),
            "parent_id": conv.get("parent_id"),
            "role": str(conv.get("role") or "unknown"),
            "created": conv.get("created") or conv.get("create_time"),
            "model": conv.get("model"),
            "text": text,
            "text_sha256": sha256_text(text),
        }


def load_records(path: Path) -> tuple[str, list[dict]]:
    data = path.read_bytes()
    source_sha = sha256_bytes(data)
    text = data.decode("utf-8", "replace")
    records: list[dict] = []
    if path.suffix.lower() == ".jsonl":
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict):
                records.append(obj)
        return source_sha, records
    obj = json.loads(text)
    if isinstance(obj, list):
        records = [x for x in obj if isinstance(x, dict)]
    elif isinstance(obj, dict):
        records = [obj]
    return source_sha, records


def classify(text: str) -> list[str]:
    cats = [name for name, pattern in CATEGORY_PATTERNS.items() if pattern.search(text)]
    return cats or ["context"]


def relevant(text: str, keywords: list[str]) -> bool:
    low = text.casefold()
    return any(k.casefold() in low for k in keywords)


def excerpt(text: str, limit: int = 500) -> str:
    one = re.sub(r"\s+", " ", text).strip()
    return one if len(one) <= limit else one[: limit - 1] + "…"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+", help="ChatGPT export JSON/JSONL file(s) or directories")
    ap.add_argument("--out", default=str(Path.home() / "wijsamen-project-audit"))
    ap.add_argument("--keyword", action="append", default=[], help="extra project keyword (repeatable)")
    args = ap.parse_args()

    out = Path(args.out).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    keywords = DEFAULT_KEYWORDS + [k for k in args.keyword if k.strip()]

    raw_path = out / "raw_messages.jsonl"
    inv_path = out / "inventory.jsonl"
    seen_msg: set[tuple[str, str, str]] = set()
    conversations: set[str] = set()
    source_stats: list[dict] = []
    inventory: list[dict] = []
    raw_count = 0

    with raw_path.open("w", encoding="utf-8") as raw_out:
        for path in iter_input_files(args.inputs):
            try:
                source_sha, records = load_records(path)
            except Exception as e:
                source_stats.append({"source": str(path), "error": f"{type(e).__name__}: {e}"})
                continue
            file_messages = 0
            for record in records:
                for msg in messages_from_conversation(record, str(path), source_sha):
                    key = (msg["conversation_id"], msg["message_id"], msg["text_sha256"])
                    if key in seen_msg:
                        continue
                    seen_msg.add(key)
                    raw_out.write(json.dumps(msg, ensure_ascii=False) + "\n")
                    raw_count += 1
                    file_messages += 1
                    conversations.add(msg["conversation_id"] or msg["conversation_title"])
                    if not relevant(msg["text"], keywords):
                        continue
                    cats = classify(msg["text"])
                    item = {
                        "conversation_id": msg["conversation_id"],
                        "conversation_title": msg["conversation_title"],
                        "message_id": msg["message_id"],
                        "role": msg["role"],
                        "created": msg["created"],
                        "categories": cats,
                        "artifact_mentions": sorted(set(FILELIKE_RE.findall(msg["text"]))),
                        "excerpt": excerpt(msg["text"]),
                        "text_sha256": msg["text_sha256"],
                        "source": msg["source"],
                        "source_sha256": msg["source_sha256"],
                        "derivation": "heuristic-v0.1",
                    }
                    inventory.append(item)
            source_stats.append({"source": str(path), "sha256": source_sha, "messages": file_messages})

    with inv_path.open("w", encoding="utf-8") as f:
        for item in inventory:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    counts: dict[str, int] = {}
    for item in inventory:
        for cat in item["categories"]:
            counts[cat] = counts.get(cat, 0) + 1

    stats = {
        "format": "WIJSAMEN-PROJECT-AUDIT/0.1",
        "raw_messages": raw_count,
        "relevant_items": len(inventory),
        "conversation_count": len([x for x in conversations if x]),
        "category_counts": dict(sorted(counts.items())),
        "keywords": keywords,
        "sources": source_stats,
        "policy": {
            "raw_is_separate_from_interpretation": True,
            "no_network": True,
            "no_external_actions": True,
            "heuristics_are_not_facts": True,
        },
    }
    json_dump(stats, out / "stats.json")

    ranked = sorted(
        inventory,
        key=lambda x: (
            "unfinished" not in x["categories"],
            "constraint" not in x["categories"],
            "decision" not in x["categories"],
            str(x.get("created") or ""),
        ),
    )
    lines = [
        "# WijSAmen Project Audit — candidate index",
        "",
        "This file is derived heuristically. Source text remains in `raw_messages.jsonl`;",
        "nothing here silently replaces or overrides the source conversation.",
        "",
        f"- raw messages: {raw_count}",
        f"- relevant candidates: {len(inventory)}",
        f"- conversations represented: {stats['conversation_count']}",
        "",
        "## Candidates",
        "",
    ]
    for i, item in enumerate(ranked[:500], 1):
        cats = ", ".join(item["categories"])
        title = item["conversation_title"] or item["conversation_id"] or "untitled"
        lines += [
            f"### {i}. {title}",
            f"- categories: {cats}",
            f"- role: {item['role']}",
            f"- message: `{item['message_id']}`",
            f"- text sha256: `{item['text_sha256']}`",
            f"- excerpt: {item['excerpt']}",
            "",
        ]
    (out / "action_candidates.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(stats, ensure_ascii=False, indent=2))
    print(f"\nAudit written to: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
