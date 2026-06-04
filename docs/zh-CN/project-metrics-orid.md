# 项目度量 · ORID 持续改进（说明）

[中文](../zh-CN/project-metrics-orid.md) | [日本語](../ja-JP/project-metrics-orid.md) | [English](../en-US/project-metrics-orid.md)

## 目标

通过项目管理系统 API 拉取数据，计算核心交付/质量/计划指标，并用 ORID（Objective/Reflective/Interpretive/Decisional）形成可执行的持续改进闭环。

## 配置

- 配置文件：`work/meta/config.yaml`
- 鉴权：建议通过环境变量提供 token（由 `token_env` 指定）

## 产物

建议将分析产物落盘到：

- `work/outputs/<project_id>/project-metrics-orid/report.md`
- `work/outputs/<project_id>/project-metrics-orid/report.json`

其中 `report.json` 供前端页面展示。

## report.json 建议结构

```json
{
  "data_integrity": {
    "missing_fields": [],
    "missing_rate": {},
    "notes": []
  },
  "metrics": {
    "window": { "days": 30, "start": "2026-05-05", "end": "2026-06-04" },
    "throughput": { "count": 42 },
    "lead_time_days": { "p50": 6.2, "p75": 9.1, "p95": 18.4 },
    "cycle_time_days": { "p50": 2.7, "p75": 4.3, "p95": 10.2 },
    "wip": { "avg": 9.3, "limit": 10 },
    "quality": { "bug_rate": 0.18, "reopen_rate": 0.06, "escaped_defects": 1 },
    "plan": { "commitment_reliability": 0.82, "scope_change": { "added": 6, "removed": 2 } }
  },
  "issues": [
    { "title": "在制过多导致流动变慢", "evidence": ["WIP 平均 12.1 > 10", "cycle time p75 上升"], "severity": "high" }
  ],
  "orid": {
    "objective": [],
    "reflective": [],
    "interpretive": [],
    "decisional": []
  },
  "root_cause_map": {
    "version": 1,
    "project_id": "proj-123",
    "phenomena": []
  },
  "actions": [
    {
      "id": "A-001",
      "problem": "在制过多导致流动变慢",
      "cause": "评审列 WIP 超限且缺少清理机制",
      "solution": "限制评审列 WIP，并建立每日清理机制",
      "discovered_date": "2026-06-04",
      "due_date": "2026-06-18",
      "completed_date": null,
      "expected_effect": "cycle time p50 <= 3 天；评审列 WIP <= 5",
      "acceptance_method": "连续 2 个窗口 cycle time p50 满足阈值；看板检查评审列 WIP",
      "owner_role": "Tech Lead"
    }
  ]
}
```

## 前端展示

启动 `frontend/`（Vue + Ant Design Vue），将 `report.json` 内容粘贴或通过文件导入，即可查看：

- 度量数据概览与趋势提示
- 发现的问题与证据
- ORID 根因分析过程
- 根因思维导图（含权重）
- 解决方案与行动项
- 任务排期计划（按截止日期排序）
