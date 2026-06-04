# クイックスタート

[中文](../zh-CN/getting-started.md) | [日本語](../ja-JP/getting-started.md) | [English](../en-US/getting-started.md)

## できること

- プロジェクト管理 / バグ / Git / CI からデータを収集
- 交付・流動・品質・計画の信頼性・開発効率のメトリクスを算出
- ORID に基づく課題と改善アクションを生成
- Web UI で結果とアクション計画を確認

## 前提

- 設定ファイル：`work/meta/config.yaml`
- API トークンは環境変数で注入（リポジトリに保存しない）
- 各システムの API にアクセス可能

## ブラウザで実行（推奨）

1. ローカルサーバー起動：
   - 一括：`sh scripts/start.sh`
   - もしくは backend のみ：`python3 backend/dev_server.py --port 8000`
2. 開く：`http://localhost:8000/analysis`
3. プロジェクトを選択し、タブ順に実行：
   - データ収集 → 課題発見 → 継続的改善

## Skill prompts で実行

- 入口：`skill/SKILL.md`
- コマンド：
  - `/prjmx:collect` → `skill/prompts/prjmx-collect/01-data-collection.md`
  - `/prjmx:metrics` → `skill/prompts/prjmx-metrics/02-metrics.md`
  - `/prjmx:orid` → `skill/prompts/prjmx-orid/03-orid.md`
  - `/prjmx:report` → `skill/prompts/prjmx-report/04-output-and-frontend.md`

## 生成物

- 推奨ディレクトリ：
  - `work/outputs/<project_id>/project-metrics-orid/`
    - `raw.json`, `data_integrity.json`, `metrics.json`, `report.json`
