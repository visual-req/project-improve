import json
import os

from utils import safe_segment


def ensure_outputs_dir(cwd, project_id):
    pid = safe_segment(project_id, "unknown")
    base = os.path.join(cwd, "work", "outputs", pid, "project-metrics-orid")
    os.makedirs(base, exist_ok=True)
    return pid, base


def write_output_json(cwd, project_id, filename, payload):
    allowed = {"raw.json", "data_integrity.json", "metrics.json", "report.json"}
    fn = safe_segment(filename, "raw.json")
    if fn not in allowed:
        raise ValueError("unsupported filename")
    pid, base = ensure_outputs_dir(cwd, project_id)
    abs_path = os.path.join(base, fn)
    with open(abs_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return pid, abs_path
