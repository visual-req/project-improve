# Manual

[中文](../zh-CN/manual.md) | [日本語](../ja-JP/manual.md) | [English](../en-US/manual.md)

## Files & Directories

- Skill entry: `skill/SKILL.md`
- Prompts: `skill/prompts/`
- Workspace config: `work/meta/config.yaml`
- Frontend: `frontend/` (Vue + Ant Design Vue, browser-side SFC loader)
- Outputs (recommended): `work/outputs/<project_id>/project-metrics-orid/`

## Web UI Pages (URLs)

The UI uses History routing:

- Analysis: `/analysis`
- System access config: `/config/system`
- Metrics config: `/config/metrics`
- Concepts: `/concept`
- Project management: `/projects`
- Action plan: `/actions`

Startup commands: see [getting-started.en.md](./getting-started.en.md).

## Typical Workflow

1. Project management: create/select a project (id/name/slug/timezone)
2. Analysis (run tabs in order):
   - Collect: generates `raw.json` and `data_integrity.json`
   - Insights: generates `metrics.json`
   - Improvement: generates `report.json` (action candidates)
3. Improvement → Candidate actions:
   - Review action candidates in the Analysis page
   - Add selected candidates to the Action Plan
4. Action Plan page:
   - Maintain owner/status/progress/dates/actual impact
   - Save improvement snapshots for history comparison
