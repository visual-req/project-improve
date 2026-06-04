# Commands

本项目不强制绑定某个 CLI；这里的 “Commands” 指最常用的操作指令与对话触发方式。

## 环境变量（Token）

按 `work/meta/config.yaml` 中各数据源 `auth.token_env` 设置：

```bash
export PM_API_TOKEN="..."
export BUG_API_TOKEN="..."
export GIT_API_TOKEN="..."
```

## 文件入口

- Skill：`skill/SKILL.md`
- Prompts：`skill/prompts/`
- 配置：`work/meta/config.yaml`
- 前端：`frontend/`

## 对话触发（示例）

- `/prjmx:collect`：拉取项目管理、bug、git 数据，并输出 data_integrity。
- `/prjmx:metrics`：计算 lead/cycle/wip、质量指标、PR 指标，并给出红黄绿。
- `/prjmx:orid`：基于指标做 ORID 分析，给出原因假设与反证。
- `/prjmx:report`：生成 report.md/report.json，并给出行动项排期表。

## 打开前端

启动前端工程并导入/粘贴 `work/outputs/<project_id>/project-metrics-orid/report.json`：

```bash
cd frontend
npm install
npm run dev
```
