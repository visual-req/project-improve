# プロジェクトORID 継続的改善

[中文](./README.md) | [English](./README.en-US.md) | [日本語](./README.ja-JP.md)

このリポジトリは以下を提供します：
- Skill によるワークフロー実行：**データ収集 → メトリクス/課題発見 → ORID による継続的改善**
- 結果閲覧とアクション計画管理のための軽量 Web UI（Vue + Ant Design Vue）

## 先に読む

- クイックスタート： [docs/ja-JP/getting-started.md](./docs/ja-JP/getting-started.md)
- 設定： [docs/ja-JP/config.md](./docs/ja-JP/config.md)
- マニュアル： [docs/ja-JP/manual.md](./docs/ja-JP/manual.md)
- トラブルシューティング： [docs/ja-JP/troubleshooting.md](./docs/ja-JP/troubleshooting.md)

## 起動

```bash
sh scripts/start.sh
```

ブラウザで開く：
- http://127.0.0.1:8001/analysis

ポート変更：

```bash
BACKEND_PORT=8002 sh scripts/start.sh
```
