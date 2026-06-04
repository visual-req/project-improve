# O · Objective（客观事实）

目标：从 `metrics` 与 `raw` 中提炼可复核的事实，作为后续分析唯一入口。

## 规则

- 只写事实，不写原因
- 每条事实必须包含：指标/样本 + 数值/数量 + 趋势/对比 + 时间窗
- 允许引用 Top N 异常样本（比如 Aging WIP、Review 延迟、Escaped 缺陷）

## 输出（建议 5–10 条）

每条建议采用模板：

- 事实：{指标名} = {当前值}（{趋势}），阈值 {目标/阈值}（判定 {红/黄/绿}），窗口 {start~end}
- 证据：{来自 metrics 的字段路径或 raw 样本描述}

## 常用事实候选

- 交付/流动：Throughput、Lead Time p50/p75、Cycle Time p50/p75、WIP 平均、Aging WIP Top 10
- 质量：Bug Rate、Reopen Rate、Escaped Defects（含严重度分布）
- 工程效率：PR Lead Time p50/p75、Review Latency p50/p75、Change Size p75、PR↔Issue 关联率
- 计划：Commitment Reliability、Scope Change（added/removed）

## 数据完整性提醒

在输出末尾追加一段简短说明：

- 关键字段缺失会影响哪些事实可信度（引用 `data_integrity`）
