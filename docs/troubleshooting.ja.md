# トラブルシューティング

中国語版（完全版）：[troubleshooting.md](./troubleshooting.md)

## 画面が開かない / 真っ白になる

- backend の静的サーバーを起動（推奨）：

```bash
sh scripts/start.sh
```

- 開く：
  - `http://127.0.0.1:8001/analysis`（デフォルト）

## 出力ファイルが 404

- 選択したプロジェクトでフローを実行したか確認：
  - データ収集 → `raw.json`
  - 課題発見 → `metrics.json`
  - 継続的改善 → `report.json`
- 出力パスを確認：
  - `work/outputs/<project_id>/project-metrics-orid/`

## トークンが無効 / 取得できない

- `work/meta/config.yaml` の `token_env` と環境変数名が一致しているか
- 必要な API（課題/PR/CI/スキャン）に権限があるか

## unpkg の読み込みに失敗

ブラウザ側 UI は CDN（unpkg）から Vue / Ant Design Vue を読み込みます。

- unpkg にアクセスできるか確認
- 社内ネットワークで遮断される場合は、ローカル依存 + Vite を検討
