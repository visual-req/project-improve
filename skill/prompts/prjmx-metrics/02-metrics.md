# 指标计算（度量口径 + 公式 + 趋势 + 红黄绿）

命令指令：`/prjmx:metrics`

目标：基于数据获取步骤的 raw 数据计算核心指标，并明确口径、公式、趋势与阈值判定。

## 输入

- 原始数据：`raw.pm_items`、`raw.bugs`、`raw.git`
- 配置：`work/meta/config.yaml`
  - `metrics`（时间窗、状态集合、percentiles、targets）
  - `field_mapping`（字段映射）

## 统一口径

- 时间窗：`metrics.window_days`
- 完成态：项目管理的 done 状态集合（由数据源 query.done_statuses 或字段映射推断）
- WIP 状态：`metrics.wip_statuses`
- Lead Time：从 `metrics.lead_time.start` 到 `metrics.lead_time.end`
- Cycle Time：从 `metrics.cycle_time.start` 到 `metrics.cycle_time.end`
- 增量对比：若存在上一份 `report.json` 或 `metrics.json`，优先输出“与上次窗口的差异/趋势”而不是只给单点数值

## 指标集合（至少覆盖）

### 交付与流动

- Throughput：时间窗内完成的 work items 数
- Lead Time：从创建到完成（p50/p75/p95）
- Cycle Time：从开始处理中到完成（p50/p75/p95）
- WIP：时间窗内平均在制数量（基于 WIP 状态集合）
- Aging WIP：在制超过阈值的条目列表（阈值可取 lead/cycle 的 p75 或固定天数）

### 质量（结合 Bug 系统）

- 缺陷率：Bug 完成数 / 总完成数（同窗）
- Escaped Defects：线上/生产缺陷数量（按 bug_source 口径）
- Reopen Rate：被重开比例（项目管理或 bug 系统二者择优）

### 计划可靠性（如有迭代承诺）

- Commitment Reliability：承诺项中按期完成比例
- Scope Change：迭代内新增/移除项

### 工程效率（结合 Git）

- PR Lead Time：PR 创建到合并（p50/p75/p95）
- Review Latency：PR 创建到首个 review 的时间（p50/p75/p95）
- Change Size：PR 变更大小分布（files/lines 若可得）

### 持续集成（结合 CI）

- Integration Frequency：时间窗内 CI 构建/集成流水线运行次数（可换算为每日/每周频率）
- CI Success Rate：成功运行次数 / 总运行次数（排除 cancelled 可选）
- Code Scan Pass Rate：代码扫描通过次数 / 扫描运行次数
- CI Duration：流水线耗时分布（p50/p75/p95，可选）

## 对每个指标输出（必须）

- 定义（状态集合/过滤规则/时间窗）
- 计算方法（公式或清晰伪代码）
- 当前值
- 趋势（对比上一窗口或上一迭代；若无历史则标注不可计算）
- 阈值判定（targets）：红/黄/绿与原因

## 产物（给下一步消费）

构造 `metrics` 对象，包含：

- `metrics.window`（start/end/days）
- `metrics.*`（各指标数据）
- `metrics.targets`（用于判定的目标/阈值）

建议落盘到：

- `work/outputs/<project_id>/project-metrics-orid/metrics.json`
