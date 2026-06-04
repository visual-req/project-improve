---
name: "project-metrics-orid"
description: "获取项目相关数据（项目管理/bug/git）并计算度量指标，基于ORID输出持续改进闭环与行动排期。按 skill/prompts/ 下的指令分步执行。"
---

# 项目度量 · ORID 持续改进（Skill）

本 Skill 的执行指令已按阶段拆分到 `skill/prompts/` 目录。运行时按顺序使用这些指令完成：数据获取 → 指标计算 → ORID 分析 → 行动排期与产物落盘。

## 配置

- 配置文件：`work/meta/config.yaml`
- token 通过环境变量提供（由配置中的 `token_env` 指定）

## Prompts（按顺序）

1. `/prjmx:collect` → `skill/prompts/prjmx-collect/01-data-collection.md`
2. `/prjmx:metrics` → `skill/prompts/prjmx-metrics/02-metrics.md`
3. `/prjmx:orid` → `skill/prompts/prjmx-orid/03-orid.md`
4. `/prjmx:report` → `skill/prompts/prjmx-report/04-output-and-frontend.md`

## 产物

- `work/outputs/<project_id>/project-metrics-orid/report.md`
- `work/outputs/<project_id>/project-metrics-orid/report.json`

前端工程 `frontend/` 通过导入/粘贴 `report.json` 展示度量数据、问题、ORID 过程、解决方案与任务排期计划。

## 前端（Vue + Ant Design Vue）

- 目录：`frontend/`
- 启动：

```bash
cd frontend
npm install
npm run dev
```

打开页面后导入/粘贴 `work/outputs/<project_id>/project-metrics-orid/report.json` 即可展示。
