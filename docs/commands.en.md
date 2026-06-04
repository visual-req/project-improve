# Commands

Full Chinese version: [commands.md](./commands.md)

## Tokens (Environment Variables)

Set env vars based on `auth.token_env` in `work/meta/config.yaml`:

```bash
export PM_API_TOKEN="..."
export BUG_API_TOKEN="..."
export GIT_API_TOKEN="..."
```

## Skill Commands (Chat)

- `/prjmx:collect` → fetch data and generate `raw.json` + `data_integrity.json`
- `/prjmx:metrics` → compute metrics and generate `metrics.json`
- `/prjmx:orid` → generate improvement analysis and `report.json`
- `/prjmx:report` → generate `report.md` (optional)
