# プロジェクトORID 継続的改善

このリポジトリは以下を提供します：
- Skill によるワークフロー実行：**データ収集 → メトリクス/課題発見 → ORID による継続的改善**
- 結果閲覧とアクション計画管理のための軽量 Web UI（Vue + Ant Design Vue）

## 言語

- 日本語（このファイル）
- [简体中文](./README.md)
- [English](./README.en.md)

## 先に読む

- クイックスタート： [docs/getting-started.ja.md](./docs/getting-started.ja.md)
- 設定： [docs/config.ja.md](./docs/config.ja.md)
- マニュアル： [docs/manual.ja.md](./docs/manual.ja.md)
- トラブルシューティング： [docs/troubleshooting.ja.md](./docs/troubleshooting.ja.md)

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
