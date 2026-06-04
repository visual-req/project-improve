# ワークフロー

中国語版（完全版）：[workflow.md](./workflow.md)

全体像：

入力（各システム API + 設定）→ データ収集と完全性チェック → メトリクス算出と閾値判定 → ORID 分析 → アクション計画 → レポートと UI 表示。

## 手順（Skill Prompts）

1) データ収集
- Prompt：`skill/prompts/prjmx-collect/01-data-collection.md`
- 出力：`raw.json`, `data_integrity.json`

2) 課題発見（メトリクス）
- Prompt：`skill/prompts/prjmx-metrics/02-metrics.md`
- 出力：`metrics.json`

3) 継続的改善（ORID）
- Prompt：`skill/prompts/prjmx-orid/03-orid.md`
- 出力：`report.json`（課題と候補アクション）

4) UI で確認
- `/analysis` を開き、タブ順に実行
- 出力ディレクトリ：
  - `work/outputs/<project_id>/project-metrics-orid/`
