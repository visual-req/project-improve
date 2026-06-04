# Troubleshooting

Full Chinese version: [troubleshooting.md](./troubleshooting.md)

## The UI is blank / cannot open

- Start the backend static server (recommended):

```bash
sh scripts/start.sh
```

- Open:
  - `http://127.0.0.1:8001/analysis` (default)

## Output files return 404

- Ensure you have run the workflow for the selected project:
  - Collect → generates `raw.json`
  - Insights → generates `metrics.json`
  - Improvement → generates `report.json`
- Verify the output path:
  - `work/outputs/<project_id>/project-metrics-orid/`

## Token invalid / cannot fetch data

- Ensure env var names match `token_env` in `work/meta/config.yaml`
- Ensure token permissions cover required APIs (issues/PR/CI runs/scans)

## unpkg resources fail to load

The browser-side UI loads Vue/Ant Design Vue from CDN (unpkg).

- Ensure network access to unpkg
- If blocked by corporate network, consider local dependency install + Vite build
