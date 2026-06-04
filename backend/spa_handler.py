import http.server
import json
import os
import urllib.parse

from logs import append_log, init_log
from mock_data import build_example_outputs
from outputs import write_output_json


class SpaFallbackHandler(http.server.SimpleHTTPRequestHandler):
    def _write_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(int(status))
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length") or "0")
        raw = self.rfile.read(length) if length > 0 else b""
        try:
            parsed = json.loads(raw.decode("utf-8") or "{}")
        except Exception:
            parsed = None
        return parsed if isinstance(parsed, dict) else {}

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        req_path = parsed.path
        cwd = os.getcwd()

        if req_path == "/api/logs/init":
            body = self._read_json_body()
            project_id = body.get("project_id")
            kind = body.get("kind")
            latest_url = init_log(cwd, project_id, kind)
            return self._write_json(200, {"ok": True, "latest_url": latest_url})

        if req_path == "/api/logs/append":
            body = self._read_json_body()
            project_id = body.get("project_id")
            kind = body.get("kind")
            msg = body.get("message")
            try:
                append_log(cwd, project_id, kind, msg)
            except Exception as e:
                return self._write_json(500, {"ok": False, "error": str(e)})
            return self._write_json(200, {"ok": True})

        if req_path == "/api/outputs/write":
            body = self._read_json_body()
            project_id = body.get("project_id")
            filename = body.get("filename")
            payload = body.get("payload")
            try:
                pid, abs_path = write_output_json(cwd, project_id, filename, payload)
            except Exception as e:
                return self._write_json(400, {"ok": False, "error": str(e)})
            rel = f"/work/outputs/{urllib.parse.quote(pid)}/project-metrics-orid/{urllib.parse.quote(str(filename))}"
            return self._write_json(200, {"ok": True, "path": rel, "abs_path": abs_path})

        return self._write_json(404, {"error": "unknown endpoint", "path": req_path})

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        req_path = parsed.path
        query = urllib.parse.parse_qs(parsed.query or "")

        if req_path.startswith("/work/outputs/"):
            parts = req_path.split("/")
            if len(parts) >= 6 and parts[4] == "project-metrics-orid":
                project_id = (parts[3] or "").strip()
                filename = parts[5]
                local = self.translate_path(req_path)
                if os.path.exists(local) and not os.path.isdir(local):
                    return http.server.SimpleHTTPRequestHandler.do_GET(self)
                if project_id == "example" and filename in {"raw.json", "data_integrity.json", "metrics.json", "report.json"}:
                    data = build_example_outputs(project_id)
                    if filename == "raw.json":
                        return self._write_json(200, data["raw"])
                    if filename == "data_integrity.json":
                        return self._write_json(200, data["data_integrity"])
                    if filename == "metrics.json":
                        return self._write_json(200, data["metrics"])
                    return self._write_json(200, data["report"])

        if req_path.startswith("/mock/"):
            project = (query.get("project", ["example"])[0] or "example").strip()
            data = build_example_outputs(project)
            ds = data["dataset"]
            if req_path == "/mock/jira/issues":
                return self._write_json(200, {"project": project, "issues": ds["issues"], "planning": ds["planning"]})
            if req_path == "/mock/git/commits":
                return self._write_json(200, {"project": project, "commits": ds["commits"]})
            if req_path == "/mock/git/pull_requests":
                return self._write_json(200, {"project": project, "pull_requests": ds["pull_requests"]})
            if req_path == "/mock/ci/runs":
                return self._write_json(200, {"project": project, "runs": ds["runs"]})
            return self._write_json(404, {"error": "unknown mock endpoint", "path": req_path})

        if req_path == "/":
            self.path = "/frontend/index.html"
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        if req_path.startswith("/work/") or req_path.startswith("/docs/") or req_path.startswith("/frontend/"):
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        local = self.translate_path(req_path)
        if os.path.exists(local) and not os.path.isdir(local):
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        self.path = "/frontend/index.html"
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
