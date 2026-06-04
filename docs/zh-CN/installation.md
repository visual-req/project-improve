# 安装

[中文](../zh-CN/installation.md) | [日本語](../ja-JP/installation.md) | [English](../en-US/installation.md)

## 前置依赖

- Node.js（用于前端工程）
- 可访问的项目管理系统 / Bug 系统 / Git 仓库 API
- Token 通过环境变量注入（见 `work/meta/config.yaml` 的 `token_env`）

## 工作区目录

- 输入：`work/inputs/`
- 输出：`work/outputs/`

报告与数据文件统一放到输出目录下（例如 `work/outputs/<project_id>/project-metrics-orid/`）。

## npx（本地）

仓库内置了一个轻量 CLI，便于初始化项目工作目录与启动前端：

```bash
npx . init --project-id <project_id>
npx . frontend
```

## 前端安装与运行

```bash
cd frontend
npm install
npm run dev
```

构建与预览（可选）：

```bash
cd frontend
npm run build
npm run preview
```
