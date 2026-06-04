import os
import urllib.parse
from datetime import datetime, timezone

from utils import now_iso, safe_segment


def ensure_logs_dir(cwd):
    base = os.path.join(cwd, "work", "logs")
    os.makedirs(base, exist_ok=True)
    return base


def log_paths(cwd, project_id, kind):
    pid = safe_segment(project_id, "unknown")
    k = safe_segment(kind, "run")
    base = ensure_logs_dir(cwd)
    dir_path = os.path.join(base, pid)
    os.makedirs(dir_path, exist_ok=True)
    latest = os.path.join(dir_path, f"latest-{k}.log")
    return pid, k, dir_path, latest


def init_log(cwd, project_id, kind):
    pid, k, dir_path, latest = log_paths(cwd, project_id, kind)
    if os.path.exists(latest) and not os.path.isdir(latest):
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        archive = os.path.join(dir_path, f"run-{k}-{ts}.log")
        try:
            os.rename(latest, archive)
        except OSError:
            pass
    with open(latest, "w", encoding="utf-8") as f:
        f.write(f"[{now_iso()}] init project={pid} kind={k}\n")
    return f"/work/logs/{urllib.parse.quote(pid)}/latest-{urllib.parse.quote(k)}.log"


def append_log(cwd, project_id, kind, message):
    pid, k, _, latest = log_paths(cwd, project_id, kind)
    line = str(message or "").rstrip("\n")
    if not line:
        return
    with open(latest, "a", encoding="utf-8") as f:
        f.write(f"[{now_iso()}] {line}\n")
