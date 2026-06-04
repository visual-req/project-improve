# 快速开始

[中文](../zh-CN/getting-started.md) | [日本語](../ja-JP/getting-started.md) | [English](../en-US/getting-started.md)

## 你将获得什么

- 从项目管理系统 / Bug 系统 / Git 仓库汇总项目度量数据
- 计算交付、流动、质量、计划可靠性、工程效率等指标
- 基于 ORID 输出问题、根因假设、改进决策与行动排期
- 用前端工程展示 `report.json`

## 前置条件

- 已配置 `work/meta/config.yaml`
- 已准备 API Token，并以环境变量方式注入（避免明文写入仓库）
- 有可访问的项目管理系统、Bug 系统、代码仓库 API

## 1) 配置

- 配置文件：`work/meta/config.yaml`
- 关键配置段：
  - `data_source`：项目管理系统数据源
  - `bug_source`：Bug 管理系统数据源
  - `git_source`：代码仓库数据源
  - `metrics`：时间窗、阈值、口径

## 工作区目录

- 输入：`work/inputs/`
- 输出：`work/outputs/`

## 2) 设置环境变量

按配置中的 `token_env` 设置（示例）：

```bash
export PM_API_TOKEN="..."
export BUG_API_TOKEN="..."
export GIT_API_TOKEN="..."
```

## 通过前端页面进行配置（可选）

前端提供“配置”入口用于：

- 读取/查看 `work/meta/config.yaml`（通过导入/导出 YAML 的方式）
- 选择项目 id，并复制对应命令（`/prjmx:* project_id=...`）
- 勾选“度量展示配置”（会导出 `metrics-config.<project_id>.json`，建议保存到 `work/meta/<project_id>/metrics-config.json`）

## 网页执行方式（推荐）

在浏览器中完成“收集数据 → 指标 → ORID/报告”的全流程：

1. 启动（任选其一）：
   - 一键：`sh scripts/start.sh`
   - 或仅启动本地静态服务：`python3 backend/dev_server.py --port 8000`
2. 打开：`http://localhost:8000/analysis`
3. 选择项目后，按页面中的 Tab 顺序执行，并等待对应输出文件生成（`raw.json`、`metrics.json`、`report.json` 等）

## 3) 按 prompts 执行（在对话中逐步使用）

- Skill 入口：`skill/SKILL.md`
- 指令目录：`skill/prompts/`
  1. `/prjmx:collect` → `prjmx-collect/01-data-collection.md`
  2. `/prjmx:metrics` → `prjmx-metrics/02-metrics.md`
  3. `/prjmx:orid` → `prjmx-orid/03-orid.md`
  4. `/prjmx:report` → `prjmx-report/04-output-and-frontend.md`

## 4) 查看产物与前端展示

- 产物目录（建议）：`work/outputs/<project_id>/project-metrics-orid/`
  - `report.md`
  - `report.json`
- 前端工程：`frontend/`（Vue + Ant Design Vue）
  - 启动（前端开发服务器）：

```bash
cd frontend
npm install
npm run dev
```

  - 打开：`http://127.0.0.1:5173/analysis`

- 后端（本项目的本地静态服务 + SPA fallback，用于根路径路由刷新不 404）：

```bash
python3 backend/dev_server.py --port 8000
```

  - 打开：`http://localhost:8000/analysis`

- 一键启动（同时启动后端静态服务 + 前端开发服务器）：

```bash
sh scripts/start.sh
```
