import os
from datetime import datetime, timezone


def safe_segment(value, fallback):
    raw = str(value or "").strip()
    if not raw:
        return fallback
    cleaned = []
    for ch in raw:
        if ch.isalnum() or ch in {"_", "-", "."}:
            cleaned.append(ch)
        else:
            cleaned.append("_")
    out = "".join(cleaned).strip("._-")[:80]
    return out or fallback


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def repo_root_from_file(file_path):
    return os.path.dirname(os.path.dirname(os.path.abspath(file_path)))
