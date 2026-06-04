# 项目ORID持续改进

持续改进之所以重要，是因为项目交付的真实瓶颈往往不是“某个点做得不够努力”，而是系统性的流动问题（等待、返工、信息不对称、过大变更、质量回流）。如果没有持续改进：
- 指标会停留在“看到了”，但无法形成可验收的行动
- 复盘会容易变成口号、归因或一轮轮重复同样的问题
- 团队能力与交付稳定性难以累积，问题只会在不同迭代以不同形式反复出现

本仓库包含一个用于“项目度量数据获取 → 指标分析 → 基于 ORID 的持续改进闭环”的 skill，以及一个用于展示分析结果的前端工程（Vue + Ant Design Vue）。

## Language

- 中文（当前）：[README.md](./README.md)
- English: [README.en.md](./README.en.md)
- 日本語: [README.ja.md](./README.ja.md)

## 阅读入口

- 快速开始（必读）：[docs/getting-started.md](./docs/getting-started.md)
- 首次配置（必读）：[docs/config.md](./docs/config.md)
- 使用手册（建议先看）：[docs/manual.md](./docs/manual.md)
- 常见问题（遇到报错先看）：[docs/troubleshooting.md](./docs/troubleshooting.md)
- English docs: [docs/getting-started.en.md](./docs/getting-started.en.md)
- 日本語 docs: [docs/getting-started.ja.md](./docs/getting-started.ja.md)
- 总入口（Skill）：[skill/SKILL.md](./skill/SKILL.md)
- 概念与方法论（ORID/PDCA/反模式/行动项）：[docs/concept.md](./docs/concept.md)
- 指标体系与分组：[docs/metrics.md](./docs/metrics.md)
- 工作流说明：[docs/workflow.md](./docs/workflow.md)
- 命令说明：[docs/commands.md](./docs/commands.md)

## 快速启动

### 方式 A：通过 start.sh 一键启动（推荐）

```bash
sh scripts/start.sh
```

启动后打开：

- `http://127.0.0.1:8001/analysis`

如需修改端口：

```bash
BACKEND_PORT=8002 sh scripts/start.sh
```

### 方式 B：手动启动（仅用 Python）

```bash
python3 backend/dev_server.py --port 8001
```

然后打开：

- `http://127.0.0.1:8001/analysis`

### 方式 C：通过 IDE 交互指令启动

- 在 Trae IDE 的对话框输入：`启动前后端`
- IDE 会执行 `sh scripts/start.sh` 并返回可访问的页面地址（包含 `/analysis`）

### 工作区要求

- 工作区配置：`work/meta/config.yaml`
- 报告（按项目编号/ID）：`work/outputs/<project_id>/project-metrics-orid/report.json`

页面会在选择项目后自动尝试读取对应的 `report.json` 并渲染结果。

## Skill 说明

- Skill 位置：`skill/SKILL.md`
- 指令拆分：`skill/prompts/`
- 配置文件：`work/meta/config.yaml`

### 谁应该用

- 研发负责人/Tech Lead：用指标与根因树把“改进”落到可验收的行动项与排期
- Scrum Master/项目经理：用计划可靠性与流动指标发现协作瓶颈与流程问题
- QA/质量负责人：用质量与回归/线上缺陷信号定位风险点并闭环

### 什么频率用

- 每周 1 次（滚动 30 天窗口）或每个迭代结束 1 次（更适合做复盘与改进承诺）

### 怎么用（闭环步骤）

- 数据收集：`/prjmx:collect`
- 指标与问题发现：`/prjmx:metrics`
- ORID 分析与根因图：`/prjmx:orid`
- 汇总报告（供前端展示）：`/prjmx:report`

每步都以 `work/meta/config.yaml` 为配置入口，产物落在：

- `work/outputs/<project_id>/project-metrics-orid/`

## 输出与展示

- 建议输出目录：`work/outputs/<project_id>/project-metrics-orid/`
  - `report.md`
  - `report.json`
- 前端工程：`frontend/`
  - 直接通过 `python3 -m http.server` 访问即可（无需安装前端依赖）
