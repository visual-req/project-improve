# Configuration

[中文](../zh-CN/config.md) | [日本語](../ja-JP/config.md) | [English](../en-US/config.md)

This system needs access to multiple systems (project management / defects / Git / CI) to produce auditable metrics. The goal is not only “making it run”, but also keeping metric definitions and data boundaries clear.

## File Locations

- Example: `work/meta/config.example.yaml`
- Actual: `work/meta/config.yaml`

## Multi-Project

One config can include multiple projects (`projects[]`). Each project has an `id`:

- Inputs: `work/inputs/<project_id>/`
- Outputs: `work/outputs/<project_id>/<report_subdir>/`
- Metadata: `work/meta/<project_id>/` (e.g. exported metrics config)

## Tokens & Security (Important)

Do not put tokens directly into `config.yaml`. Use environment variables:

- Set `auth.token_env` in each data source
- Export env vars before running:

```bash
export PM_API_TOKEN="***"
export BUG_API_TOKEN="***"
export GIT_API_TOKEN="***"
export CI_API_TOKEN="***"
```

Recommended: least privilege + regular rotation.

## Typical Data Sources

- Jira: issues + status history (changelog), optional sprint/board data
- Jenkins/CI: builds/runs (timestamp/duration/result), optional quality gates
- Git (GitHub/GitLab): commits, pull requests, reviews
