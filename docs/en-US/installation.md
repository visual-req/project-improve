# Installation

[中文](../zh-CN/installation.md) | [日本語](../ja-JP/installation.md) | [English](../en-US/installation.md)

## Prerequisites

- Node.js (optional, only needed if you want to run the Vite dev server)
- Network access to your PM/Bug/Git/CI APIs
- Tokens injected via environment variables (`token_env` in `work/meta/config.yaml`)

## Workspace Directories

- Inputs: `work/inputs/`
- Outputs: `work/outputs/`

Outputs are written under:
- `work/outputs/<project_id>/project-metrics-orid/`

## Frontend (Optional Vite Dev Server)

```bash
cd frontend
npm install
npm run dev
```
