# インストール

[中文](../zh-CN/installation.md) | [日本語](../ja-JP/installation.md) | [English](../en-US/installation.md)

## 前提

- Node.js（Vite の dev server を使う場合のみ必要）
- PM/Bug/Git/CI の API にアクセス可能
- トークンは環境変数で注入（`work/meta/config.yaml` の `token_env`）

## ワークスペース

- 入力：`work/inputs/`
- 出力：`work/outputs/`

出力は以下に生成されます：
- `work/outputs/<project_id>/project-metrics-orid/`

## フロントエンド（任意：Vite dev server）

```bash
cd frontend
npm install
npm run dev
```
