# 設定

[中文](../zh-CN/config.md) | [日本語](../ja-JP/config.md) | [English](../en-US/config.md)

本システムは複数のシステム（プロジェクト管理 / 欠陥 / Git / CI）へアクセスして、復盤可能なメトリクスを生成します。目的は「動かすこと」だけでなく、指標の口径とデータ境界を明確に保つことです。

## ファイル配置

- サンプル：`work/meta/config.example.yaml`
- 実運用：`work/meta/config.yaml`

## 複数プロジェクト

1 つの設定に `projects[]` を含められます。各プロジェクトは `id` で識別します。

- 入力：`work/inputs/<project_id>/`
- 出力：`work/outputs/<project_id>/<report_subdir>/`
- メタ：`work/meta/<project_id>/`

## トークンと安全性（重要）

トークンを `config.yaml` に直接書かないでください。環境変数で注入します。

- 各データソースの `auth.token_env` に環境変数名を設定
- 実行前に環境変数を設定：

```bash
export PM_API_TOKEN="***"
export BUG_API_TOKEN="***"
export GIT_API_TOKEN="***"
export CI_API_TOKEN="***"
```

推奨：最小権限 + 定期ローテーション。

## 代表的なデータソース

- Jira：課題 + ステータス履歴（changelog）、必要に応じて sprint/board
- Jenkins/CI：ビルド/実行（timestamp/duration/result）、必要に応じて品質ゲート
- Git（GitHub/GitLab）：commit、PR、レビュー
