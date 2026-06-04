def build_example_dataset(project_id):
    issues = []
    sprint_start = "2026-05-01"
    sprint_end = "2026-05-10"
    sprint_total_points = 30
    for i in range(1, 13):
        status = "Done" if i % 5 == 0 else ("Review" if i % 4 == 0 else ("In Progress" if i % 3 == 0 else "To Do"))
        created_at = "2026-05-01"
        started_at = "2026-05-03" if status in {"In Progress", "Review", "Done"} else ""
        done_at = "2026-05-08" if status == "Done" else ""
        due_date = "2026-05-10"
        history = [{"status": "To Do", "at": created_at}]
        if started_at:
            history.append({"status": "In Progress", "at": started_at})
        if status == "Review":
            history.append({"status": "Review", "at": "2026-05-06"})
        if done_at:
            history.append({"status": "Done", "at": done_at})
        issues.append(
            {
                "key": f"{str(project_id).upper()}-{100+i}",
                "type": "Story" if i % 4 else "Bug",
                "summary": f"示例需求/缺陷 {i}",
                "status": status,
                "assignee": "dev-a" if i % 2 == 0 else "dev-b",
                "story_points": 1 if i % 4 else 3,
                "labels": ["mock", "example"],
                "created_at": created_at,
                "updated_at": "2026-05-10",
                "started_at": started_at,
                "done_at": done_at,
                "due_date": due_date,
                "status_history": history,
            }
        )

    commits = []
    for i in range(1, 15):
        commits.append(
            {
                "sha": f"deadbeef{i:02d}",
                "author": "dev-a" if i % 2 else "dev-b",
                "date": f"2026-05-{i:02d}T10:00:00Z",
                "message": f"mock commit {i}: refactor/test/feature",
                "files_changed": (i % 5) + 1,
            }
        )

    pull_requests = []
    for i in range(1, 9):
        pull_requests.append(
            {
                "id": i,
                "title": f"PR {i}: 示例改动",
                "author": "dev-a" if i % 2 else "dev-b",
                "state": "merged" if i % 3 else "open",
                "created_at": f"2026-05-{i:02d}T09:00:00Z",
                "merged_at": None if i % 3 == 0 else f"2026-05-{i:02d}T18:00:00Z",
                "additions": 50 + i * 3,
                "deletions": 20 + i,
                "reviews": [{"reviewer": "dev-c", "state": "approved"}] if i % 2 else [],
            }
        )

    runs = []
    for i in range(1, 11):
        runs.append(
            {
                "id": i,
                "pipeline": "ci",
                "status": "success" if i % 6 else "failed",
                "duration_seconds": 300 + i * 18,
                "created_at": f"2026-05-{i:02d}T12:00:00Z",
            }
        )

    burndown = []
    for d in range(0, 10):
        date = f"2026-05-{1+d:02d}"
        ideal_remaining = max(0, sprint_total_points - int(round((sprint_total_points / 9) * d)))
        drift = 2 if d >= 5 else 0
        actual_remaining = max(0, ideal_remaining + drift)
        burndown.append({"date": date, "ideal_remaining_points": ideal_remaining, "remaining_points": actual_remaining})

    gantt_tasks = [
        {"id": "T-1", "name": "需求澄清与拆分", "planned_start": "2026-05-01", "planned_end": "2026-05-02", "actual_end": "2026-05-02"},
        {"id": "T-2", "name": "实现与自测", "planned_start": "2026-05-03", "planned_end": "2026-05-06", "actual_end": "2026-05-07"},
        {"id": "T-3", "name": "联调与回归", "planned_start": "2026-05-06", "planned_end": "2026-05-09", "actual_end": ""},
    ]

    planning = {
        "sprint": {"start_date": sprint_start, "end_date": sprint_end, "total_points": sprint_total_points},
        "burndown": {"series": burndown},
        "gantt": {"tasks": gantt_tasks},
    }

    return {"issues": issues, "commits": commits, "pull_requests": pull_requests, "runs": runs, "planning": planning}


def build_example_metrics(dataset):
    issues = dataset.get("issues") or []
    runs = dataset.get("runs") or []
    prs = dataset.get("pull_requests") or []
    done_issues = [x for x in issues if str((x or {}).get("status")) == "Done"]
    in_progress_issues = [x for x in issues if str((x or {}).get("status")) == "In Progress"]
    bug_done = len([x for x in done_issues if str((x or {}).get("type")) == "Bug"])
    total_done = len(done_issues) or 1
    ci_ok = len([x for x in runs if str((x or {}).get("status")) == "success"])
    ci_rate = ci_ok / len(runs) if runs else 1
    merged_prs = len([x for x in prs if str((x or {}).get("state")) == "merged"])
    return {
        "window": "mock:30d",
        "throughput": {"count": len(done_issues)},
        "wip": {"avg": len(in_progress_issues), "aging_count": max(0, len(in_progress_issues) - 2)},
        "lead_time_days": {"p50": 5, "p75": 7, "p95": 12},
        "cycle_time_days": {"p50": 2, "p75": 3, "p95": 6},
        "pr_lead_time_days": {"p50": 1.2, "p75": 2.1, "p95": 4.8},
        "review_latency_days": {"p50": 0.4, "p75": 0.9, "p95": 1.8},
        "plan": {"commitment_reliability": 0.78, "scope_change": {"added": 2, "removed": 1}},
        "quality": {
            "bug_rate": bug_done / total_done,
            "reopen_rate": 0.06,
            "escaped_defects": 1,
            "escaped_defect_rate": 1 / total_done,
        },
        "ci": {"integration_frequency": {"count": len(runs)}, "success_rate": ci_rate, "code_scan_pass_rate": 0.93},
        "targets": {
            "lead_time_p50_days": 7,
            "cycle_time_p50_days": 3,
            "wip_limit": 10,
            "bug_rate_max": 0.1,
            "reopen_rate_max": 0.1,
            "escaped_defects_max": 2,
            "ci_success_rate_min": 0.9,
            "code_scan_pass_rate_min": 0.95,
        },
        "mock_details": {"done_items": len(done_issues), "wip_items": len(in_progress_issues), "merged_prs": merged_prs},
    }


def build_example_report(project_id, metrics, dataset):
    issues = dataset.get("issues") or []
    runs = dataset.get("runs") or []
    prs = dataset.get("pull_requests") or []
    done_issues = [x for x in issues if str((x or {}).get("status")) == "Done"]
    in_progress_issues = [x for x in issues if str((x or {}).get("status")) == "In Progress"]
    ci_ok = len([x for x in runs if str((x or {}).get("status")) == "success"])
    ci_rate = ci_ok / len(runs) if runs else 1
    merged_prs = len([x for x in prs if str((x or {}).get("state")) == "merged"])
    return {
        "mode": "mock",
        "project": project_id,
        "metrics": metrics,
        "orid": {
            "objective": [
                f"完成 {len(done_issues)} 个条目（Done），在制 {len(in_progress_issues)} 个（In Progress）",
                f"流水线成功率 {int(round(ci_rate * 100))}%，合并请求 {merged_prs} 个",
            ],
            "reflective": ["迭代中后期出现提交/合并集中，评审与集成可能存在排队", "质量门禁未达标导致返工风险上升"],
            "interpretive": ["任务拆分偏大导致合并慢", "评审等待与 CI 波动导致反馈不连续", "质量门禁阈值未固化导致缺陷回流"],
            "decisional": ["把行动项纳入计划并设定验收/负责人，下一窗口验证 lead time 与门禁趋势"],
        },
        "actions": [
            {
                "id": "A-1",
                "problem": "交付节奏不稳定，出现集中合并",
                "cause": "任务拆分偏大 + 评审等待",
                "solution": "把需求拆到 1 天内可合并粒度；设置每日评审窗口；限制在制数量",
                "due_date": "",
                "expected_effect": "降低合并请求周期，减少末期堆积",
                "acceptance_method": "下个窗口合并请求周期下降，评审等待下降",
                "owner_role": "研发负责人",
            },
            {
                "id": "A-2",
                "problem": "代码扫描通过率偏低",
                "cause": "门禁未前置 + 修复缺少明确责任链",
                "solution": "合并请求阶段强制扫描门禁；为阻断级问题建立修复时限；引入智能辅助定位与修复草稿",
                "due_date": "",
                "expected_effect": "提升代码扫描通过率，减少返工",
                "acceptance_method": "下个窗口代码扫描通过率达到目标且无新增阻断级问题",
                "owner_role": "质量/研发",
            },
        ],
    }


def build_example_outputs(project_id):
    ds = build_example_dataset(project_id)
    metrics = build_example_metrics(ds)
    raw = {
        "mode": "mock",
        "project": project_id,
        "sources": {"jira": {"issues": ds["issues"]}, "git": {"commits": ds["commits"], "pull_requests": ds["pull_requests"]}, "ci": {"runs": ds["runs"]}},
        "planning": ds["planning"],
    }
    integrity = {
        "ok": True,
        "mode": "mock",
        "project": project_id,
        "sources": {"jira_issues": len(ds["issues"]), "git_commits": len(ds["commits"]), "git_pull_requests": len(ds["pull_requests"]), "ci_runs": len(ds["runs"])},
    }
    report = build_example_report(project_id, metrics, ds)
    return {"raw": raw, "data_integrity": integrity, "metrics": {"mode": "mock", "project": project_id, "metrics": metrics}, "report": report, "dataset": ds}
