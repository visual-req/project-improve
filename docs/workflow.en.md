# Workflow

Full Chinese version: [workflow.md](./workflow.md)

Overview:

Inputs (system APIs + config) → data collection & integrity checks → metrics calculation & threshold evaluation → ORID analysis → action planning → report & UI.

## Steps (Skill Prompts)

1) Collect
- Prompt: `skill/prompts/prjmx-collect/01-data-collection.md`
- Outputs: `raw.json`, `data_integrity.json`

2) Metrics
- Prompt: `skill/prompts/prjmx-metrics/02-metrics.md`
- Outputs: `metrics.json`

3) ORID
- Prompt: `skill/prompts/prjmx-orid/03-orid.md`
- Outputs: `report.json` (includes findings + action candidates)

4) Review in UI
- Open `/analysis` and follow the tabs
- Outputs directory:
  - `work/outputs/<project_id>/project-metrics-orid/`
