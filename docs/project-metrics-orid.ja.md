# プロジェクトメトリクス · ORID 継続的改善

中国語版（完全版）：[project-metrics-orid.md](./project-metrics-orid.md)

## 目的

各システムからデータを取得し、主要メトリクスを算出し、ORID に基づく改善ループを実行可能な計画として出力します。

## 設定

- `work/meta/config.yaml`
- トークンは環境変数（`token_env`）で注入

## 生成物

以下に出力します：

- `work/outputs/<project_id>/project-metrics-orid/report.json`
- `work/outputs/<project_id>/project-metrics-orid/report.md`（任意）

`report.json` は Web UI で利用します。

## UI

`/analysis` で以下を確認できます：

- メトリクスと課題
- ORID 分析と候補アクション
- アクション計画へ追加し継続的に追跡
