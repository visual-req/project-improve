# Project Metrics · ORID Continuous Improvement

[中文](../zh-CN/project-metrics-orid.md) | [日本語](../ja-JP/project-metrics-orid.md) | [English](../en-US/project-metrics-orid.md)

## Goal

Fetch data from project systems, compute key metrics, and generate an ORID-based improvement loop with actionable plans.

## Config

- `work/meta/config.yaml`
- Tokens via env vars (see `token_env`)

## Outputs

Write outputs to:

- `work/outputs/<project_id>/project-metrics-orid/report.json`
- `work/outputs/<project_id>/project-metrics-orid/report.md` (optional)

`report.json` is used by the web UI.

## UI

Open `/analysis` to:

- Review metrics and findings
- See ORID analysis and candidate actions
- Add actions into the Action Plan for ongoing tracking
