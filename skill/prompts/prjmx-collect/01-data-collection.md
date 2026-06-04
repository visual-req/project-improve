# 数据获取（项目管理 / Bug / Git）

命令指令：`/prjmx:collect`

目标：从配置的系统 API 拉取最小必要数据集，形成可用于度量计算的原始数据，并输出数据完整性诊断。

## 输入

- 配置：`work/meta/config.yaml`
  - 项目管理数据源：`data_source`
  - Bug 数据源：`bug_source`
  - Git 数据源：`git_source`
  - CI 数据源：`ci_source`
- 环境变量：根据每个数据源的 `auth.token_env` 注入 token
- 工作区：
  - 输入：`work/inputs/<project_id>/`（可选：手工导出的 JSON/CSV 或补充数据）
  - 输出：`work/outputs/`（建议：落盘 raw 数据与诊断结果）

## 拉取范围与约束

- 时间窗：默认使用 `metrics.window_days` 或各数据源 `query.since_days`（若存在）
- 只拉取计算指标所需字段；避免全量导出
- 输出中不得包含 token 或任何敏感鉴权信息
- 增量优先：若存在上一份 `raw.json`，优先以其最新时间戳作为 since（减少重复拉取与覆写）

## 项目管理系统（data_source）

最小数据集（按可得性降级）：

- Work item 列表：id/key、标题、类型、创建时间、更新时间、当前状态、负责人、标签、估点/工时
- 状态流转历史：进入/离开状态的时间戳（用于 lead/cycle/wip 计算）
- 迭代信息：sprint/iteration/milestone（用于承诺完成率、范围变更）
- 阻塞信息：blocked 标记/原因（若可得）

输出数据完整性诊断：

- 关键字段缺失率（created、done、status_history、assignee、issue_type、story_points 等）
- 明显异常值（时间逆序、空状态历史、缺失 done 但在 done 状态等）

## Bug 系统（bug_source）

最小数据集：

- Bug 列表：id/key、创建/关闭时间、严重级别、所属版本/模块（如可得）、标签/环境（用于 escaped defects 判定）、状态变更
- Escaped/Production 缺陷：基于 `escaped_defect_labels` 或系统字段（若存在）
- 重开信息：reopen 次数与时间戳（若可得）

输出数据完整性诊断：

- severity 字段可用性（按 `bug_source.query.severity_field`）
- escaped 缺陷识别是否可靠（标签缺失、字段缺失）

## Git 仓库（git_source）

最小数据集：

- commits：提交时间、作者（可匿名化为 id/hash）、变更范围（files/lines 若可得）
- pull requests：创建/合并时间、作者、review 记录、变更大小、关联 issue key（若能从标题/分支提取）
- reviews：review 提交时间、状态（approved/changes requested/commented）

输出数据完整性诊断：

- PR 与 issue 关联率（能否从标题/分支/commit message 提取）
- PR review 数据缺失率

## 持续集成（ci_source）

最小数据集：

- pipeline/workflow 运行记录：触发时间、分支、运行结果（success/failure/cancelled）、耗时
- 构建/集成：用于计算集成频率与成功率
- 代码扫描：用于计算扫描通过率（可按 workflow/job 名区分）

输出数据完整性诊断：

- CI 运行记录可用性（时间窗内是否齐全）
- 代码扫描工作流是否可区分（命名/字段缺失）

## 产物（给下一步消费）

输出一个原始数据对象（JSON in-memory 即可），至少包含：

- `raw.pm_items`（项目管理 work items）
- `raw.bugs`（bug 列表）
- `raw.git`（commits/prs/reviews）
- `data_integrity`（缺失字段、缺失率、异常值、备注）

建议同时落盘到：

- `work/outputs/<project_id>/project-metrics-orid/raw.json`
- `work/outputs/<project_id>/project-metrics-orid/data_integrity.json`
