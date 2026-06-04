# Getting Started

Full Chinese version: [getting-started.md](./getting-started.md)

## What You Get

- Collect project data from project management / bug / Git / CI systems
- Compute delivery, flow, quality, planning reliability, and engineering efficiency metrics
- Generate ORID-based findings and improvement actions
- Review results in the web UI (`report.json`, action candidates, action plan)

## Prerequisites

- A workspace config file: `work/meta/config.yaml`
- API tokens provided via environment variables (do not commit tokens to the repo)
- Network access to your systems’ APIs

## Run in the Browser (Recommended)

1. Start local server:
   - One command: `sh scripts/start.sh`
   - Or backend only: `python3 backend/dev_server.py --port 8000`
2. Open: `http://localhost:8000/analysis`
3. Select a project and run tabs in order:
   - Collect → Metrics/Insights → Improvement

## Run via Skill Prompts

- Entry: `skill/SKILL.md`
- Commands:
  - `/prjmx:collect` → `skill/prompts/prjmx-collect/01-data-collection.md`
  - `/prjmx:metrics` → `skill/prompts/prjmx-metrics/02-metrics.md`
  - `/prjmx:orid` → `skill/prompts/prjmx-orid/03-orid.md`
  - `/prjmx:report` → `skill/prompts/prjmx-report/04-output-and-frontend.md`

## Outputs

- Recommended output directory:
  - `work/outputs/<project_id>/project-metrics-orid/`
    - `raw.json`, `data_integrity.json`, `metrics.json`, `report.json`
