# Manual

## 文件与目录

- Skill：`skill/SKILL.md`
- Prompts：`skill/prompts/`
- 配置：`work/meta/config.yaml`
- 前端：`frontend/`（Vue + Ant Design Vue）
- 输出（建议）：`work/outputs/<project_id>/project-metrics-orid/`

## 前端操作（URL 与页面）

前端使用 History 路由，每个页面都有固定 URL（不使用 `?page=` 或 `#`，且 URL 不包含 `frontend` 前缀）：

- 项目分析页：`/analysis`
- 系统访问配置：`/config/system`
- 度量指标配置：`/config/metrics`
- 理念：`/concept`
- 项目管理：`/projects`
- 行动项管理：`/actions`

启动命令请统一参考 [getting-started.md](file:///Users/stephenwang/Documents/trae_projects/project-improve/docs/getting-started.md#L57-L86)。

### 1) 项目管理

在“项目管理”页：

- 新增/修改/删除项目（至少填写 `id`、名称、英文名）
- 选择当前项目（后续执行与行动项管理会复用该选择）

### 2) 执行数据收集 → 指标 → ORID

在“项目分析页”按 Tab 顺序执行：

1. 收集数据：生成 `raw.json` 与 `data_integrity.json`
2. 问题发现：生成 `metrics.json`
3. 持续改进：生成 `report.json`（用于前端展示与行动项候选）

执行时页面会显示遮罩与进度条，并在输出文件生成后自动刷新状态。

### 3) 行动项管理与历史

在“行动项管理”页：

- 从 `report.json.actions` 加载候选行动项
- 选择哪些纳入行动计划，并维护负责人、开始时间、状态、进度、实际效果等字段
- 点击“保存改进快照”，将当下的关键指标 + 行动项完成情况留存为历史记录

历史记录会在“项目管理”页展示，并给出关键指标的前后对比摘要。

## 配置说明（work/meta/config.yaml）

### data_source（项目管理）

- `system`：jira/linear/gitlab/azure_devops/custom
- `base_url`：API 域名或入口
- `auth`：鉴权方式与 `token_env`
- `query`：项目范围（project_key/board_id/issue_types/done_statuses 等）

### bug_source（Bug 管理）

- `system`：jira/bugzilla/zentao/gitlab/custom（示例）
- `escaped_defect_labels`：识别线上缺陷的标签集合（可按你们约定调整）
- `severity_field`：严重级别字段路径（如 `priority.name`）

### git_source（代码仓库）

- `system`：github/gitlab/bitbucket/custom
- `base_url`：API 域名或入口
- `auth`：鉴权方式与 `token_env`
- `repo`：owner/name/default_branch
- `query.include`：需要拉取的对象（commits/pull_requests/reviews）

### field_mapping（字段映射）

用于不同系统字段差异的兼容，建议你按实际 API 响应做映射与校准。

### metrics（口径与阈值）

- `window_days`：默认分析时间窗
- `wip_statuses`：在制状态集合
- `lead_time` / `cycle_time`：定义起止事件
- `percentiles`：分位数集合（p50/p75/p95）
- `targets`：阈值（用于红黄绿判定）

## 输出结构

### report.json（用于前端）

建议包含字段：

- `project`
- `data_integrity`
- `metrics`
- `issues`
- `orid`
- `actions`

### report.md（用于汇报/复盘）

建议章节：

- 数据来源与窗口
- 指标与趋势（含红黄绿）
- 问题清单（证据）
- ORID 分析过程
- 行动项与排期（负责人、验收标准、风险、依赖）

## 常见问题

- token 无效：确认环境变量名与 `token_env` 一致；确认 token 权限覆盖所需 API 范围
- 数据缺失：优先检查字段映射与查询条件；必要时在 `data_integrity` 中标注缺失与影响
- 指标口径争议：把口径写进 `metrics`，并在 `report.md` 明确状态集合/过滤规则
