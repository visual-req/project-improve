# 配置

[中文](../zh-CN/config.md) | [日本語](../ja-JP/config.md) | [English](../en-US/config.md)

本系统需要访问项目管理/缺陷/Git/CI 等多个系统才能得到可复核的度量数据。配置的目的不是“让工具能跑起来”，而是让指标口径与数据边界清晰可控，避免出现“看起来有结论但不可复盘”的情况。

## 配置文件位置

- 示例：`work/meta/config.example.yaml`
- 实际使用：`work/meta/config.yaml`

## 多项目支持

配置文件支持 `projects` 列表，每个项目用 `id` 唯一标识：

- 输入目录：`work/inputs/<project_id>/`
- 输出目录：`work/outputs/<project_id>/<report_subdir>/`
- 元数据目录：`work/meta/<project_id>/`（例如前端导出的 metrics-config.json）

## Token 与安全

### 什么是 Token 访问

Token（访问令牌）通常是各系统提供的“可撤销、可权限控制”的访问凭证，用于替代账号密码进行 API 调用。常见形式包括：

- Bearer Token：HTTP Header 中携带 `Authorization: Bearer <token>`
- Personal Access Token（PAT）：例如 GitHub/GitLab 的 token，本质也是 bearer/token header

### 为什么不要把 token 直接写进配置文件

把 token 明文写入 `config.yaml` 存在高风险：

- 配置文件很容易被误提交到仓库或被分享，造成长期泄露
- token 往往权限很高（可读 PR/代码/流水线甚至写入），泄露影响面大
- token 需要轮换/吊销，明文散落会导致无法统一治理

### 为什么要从命令行/环境变量传递

用命令行设置环境变量（或在 CI 的 secret 管理中注入）是更安全的做法：

- 让“配置（口径/系统地址）”与“密钥（token）”分离，减少泄露面
- 环境变量天然适配本地与 CI，便于不同环境使用不同 token
- 便于轮换：更新环境变量即可，不需要修改配置文件与重新分发

### 推荐做法

不要把 token 明文写入配置；用环境变量注入：

- 在每个数据源的 `auth.token_env` 中指定环境变量名
- 运行时设置环境变量值（例如 `PM_API_TOKEN`）

示例（本地终端）：

```bash
export PM_API_TOKEN="***"
export BUG_API_TOKEN="***"
export GIT_API_TOKEN="***"
export CI_API_TOKEN="***"
```

建议配合最小权限原则（least privilege）：

- 只给读权限（只读 issues/PR/workflows）
- 只给必要范围（限定仓库/组织/项目）
- 定期轮换 token，并在人员变动时及时吊销

## 各系统访问原理（Jira / Jenkins / Git）

本系统的“数据获取”阶段，本质是在时间窗内通过各系统的 HTTP API 拉取结构化数据，然后按 `field_mapping` 统一口径，最后输出原始数据与 `data_integrity` 诊断供后续计算与复盘引用。

通用工作方式：

- 鉴权：把 token 放到 HTTP Header（Bearer/token/basic 等），由 `auth.type` + `auth.token_env` 控制
- 时间窗：用 `metrics.window_days`（或迭代窗口）限制拉取范围，避免全量拉取
- 分页：大多数 API 需要分页（Jira 的 `startAt/maxResults`、GitHub 的 `page/per_page`）
- 字段与展开：为计算 lead/cycle/status history 等指标，通常需要额外字段或展开（例如 Jira changelog）
- 限流与重试：API 可能限流（HTTP 429/403），需要按系统策略做退避重试（实现端应处理）

### Jira（项目管理/缺陷）

典型拉取路径：

- 需求/任务/缺陷列表：JQL Search API（按 `project_key`、`issue_types`、更新时间窗筛选）
- 状态历史：需要 `changelog`（用于计算 cycle/lead、识别返工/重开等信号）
- 迭代/冲刺：如果按 Sprint 口径统计，需要 board/sprint 相关接口（由 `board_id` 辅助定位）

配置里与 Jira 访问相关的关键点：

- `base_url`：你的 Jira 域名与 API 入口
- `query.project_key/board_id/issue_types/done_statuses`：决定查询范围与“完成”口径
- `field_mapping`：把 Jira 字段路径映射到统一字段（时间戳、状态、负责人、story points 等）
- `bug_source.query.escaped_defect_labels`：用标签或字段区分“线上缺陷”（用于缺陷逃逸率）

### Jenkins（CI/构建/扫描）

Jenkins 的数据通常来自 Job/Build 的 JSON API：

- 构建列表：按 Job 在时间窗内枚举 build，读取 `timestamp/duration/result`
- 质量信号：按 Job 命名或参数区分“代码扫描/测试/构建”，统计成功率、频率、扫描通过率等

实践中常见注意点：

- 鉴权方式多样：token/basic、crumb 等；建议使用只读 API token
- Job 命名约定：如果希望区分扫描/测试，需要在 `ci_source` 里配置可识别规则（名称/字段）
- 时区与时间戳：Jenkins 多用毫秒时间戳，需统一到项目时区口径

### Git（GitHub/GitLab 等）

Git 数据主要用于工程效率与协作信号：

- commits：提交频率、活跃度、变更节奏
- pull requests：PR 交付周期（创建→合并）、变更规模（行数/文件数）
- reviews：评审等待/评审耗时（用于 review latency）

实践中常见注意点：

- 分页与限流：Git API 通常限流严格，需要正确分页，并避免无意义全量扫描
- 窗口口径：按 `since_days/window_days` 限制拉取，并保证与指标窗口一致
- 合并策略：不同策略（merge/squash/rebase）会影响“交付点”的识别（配置应写清）

## 配置结构说明

### workspace

- `inputs_dir`：输入根目录（默认 `work/inputs`）
- `outputs_dir`：输出根目录（默认 `work/outputs`）
- `meta_dir`：元数据根目录（默认 `work/meta`）

### active_project_id

默认项目 id。前端与命令触发可用它作为默认选择。

### projects[]

每个项目建议包含：

- `id`：项目唯一 id（用于目录与跨系统映射）
- `name`：项目中文/展示名
- `slug_en`：英文名/slug（用于跨系统匹配与展示）
- `timezone`：时区
- `iteration`：迭代节奏

以及三个数据源（可按需配置/禁用）：

- `data_source`：项目管理系统（需求/任务）
- `bug_source`：Bug 管理系统（缺陷/线上外溢）
- `git_source`：代码仓库（commit/PR/review）
- `ci_source`：持续集成系统（构建频率/成功率/代码扫描通过率）

### output

- `report_subdir`：报告子目录名（建议 `project-metrics-orid`）

实际输出路径建议为：

`work/outputs/<project_id>/<report_subdir>/report.json`

## 常见配置点

- Jira：确认 `project_key`、`board_id`、`done_statuses` 与实际工作流一致
- GitHub：确认 `repo.owner/name` 与 token 权限覆盖 PR 与 review 读取
- Escaped Defects：用 `escaped_defect_labels` 或 severity 字段确保可区分线上缺陷
