# マニュアル

[中文](../zh-CN/manual.md) | [日本語](../ja-JP/manual.md) | [English](../en-US/manual.md)

## ファイル/ディレクトリ

- Skill 入口：`skill/SKILL.md`
- Prompts：`skill/prompts/`
- 設定：`work/meta/config.yaml`
- フロント：`frontend/`（Vue + Ant Design Vue、ブラウザ側 SFC ローダー）
- 出力（推奨）：`work/outputs/<project_id>/project-metrics-orid/`

## Web UI のページ（URL）

History ルーティングを使用します：

- 分析：`/analysis`
- システム接続設定：`/config/system`
- メトリクス設定：`/config/metrics`
- コンセプト：`/concept`
- プロジェクト管理：`/projects`
- アクション計画：`/actions`

起動方法： [getting-started.ja.md](./getting-started.ja.md) を参照してください。

## 基本フロー

1. プロジェクト管理：プロジェクトを作成/選択（id/name/slug/timezone）
2. 分析（タブ順に実行）：
   - データ収集：`raw.json` と `data_integrity.json`
   - 課題発見：`metrics.json`
   - 継続的改善：`report.json`（候補アクション）
3. 継続的改善 → 候補アクション：
   - 分析ページで候補を確認
   - 必要なものをアクション計画へ追加
4. アクション計画ページ：
   - 担当/状態/進捗/日付/実績効果を継続的に更新
   - 改善スナップショットを保存し履歴比較
