# コマンド

[中文](../zh-CN/commands.md) | [日本語](../ja-JP/commands.md) | [English](../en-US/commands.md)

## トークン（環境変数）

`work/meta/config.yaml` の `auth.token_env` に合わせて設定：

```bash
export PM_API_TOKEN="..."
export BUG_API_TOKEN="..."
export GIT_API_TOKEN="..."
```

## Skill コマンド（対話）

- `/prjmx:collect` → データ取得、`raw.json` + `data_integrity.json`
- `/prjmx:metrics` → メトリクス算出、`metrics.json`
- `/prjmx:orid` → 改善分析、`report.json`
- `/prjmx:report` → `report.md`（任意）
