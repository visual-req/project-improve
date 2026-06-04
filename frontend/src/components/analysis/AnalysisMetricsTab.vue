<template>
  <a-space direction="vertical" style="width: 100%" :size="12">
    <a-button type="primary" @click="requestRunSkill('metrics')">执行问题发现</a-button>
    <a-alert v-if="metricsError" type="warning" show-icon :message="metricsError" />
    <a-card size="small" title="输入/输出文件">
      <ul style="margin: 0; padding-left: 18px">
        <li>输入：/work/{{ selectedProjectIdModel || "&lt;project_id&gt;" }}/meta/config.yaml</li>
        <li>输入：/work/outputs/{{ selectedProjectIdModel || "&lt;project_id&gt;" }}/project-metrics-orid/raw.json</li>
        <li>输出：/work/outputs/{{ selectedProjectIdModel || "&lt;project_id&gt;" }}/project-metrics-orid/metrics.json</li>
      </ul>
    </a-card>
    <a-card size="small" title="本次分析范围（按度量指标选择）">
      <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px">
        已选指标：{{ enabledMetricKeys.length }} 个{{ enabledMetricKeys.length ? "" : "（未选择时默认不展示，请先到“度量指标配置”勾选）" }}
      </div>
    </a-card>
    <div v-if="!metricsData" style="color: rgba(0, 0, 0, 0.65)">尚未读取到 metrics.json。</div>
    <a-collapse v-else :bordered="false" style="background: transparent">
      <a-collapse-panel key="flow" header="流动（Flow）">
        <div v-if="groupedCards.flow.length === 0" style="color: rgba(0, 0, 0, 0.45); font-size: 12px">—</div>
        <a-table v-else :columns="metricsTableColumns" :data-source="groupedCards.flow" size="small" :pagination="false">
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'status'">
              <a-tag v-if="record.status" :color="record.status === 'success' ? 'green' : record.status === 'warning' ? 'gold' : 'red'">
                {{ tagText(record.status) }}
              </a-tag>
              <span v-else style="color: rgba(0, 0, 0, 0.45)">—</span>
            </template>
          </template>
        </a-table>
      </a-collapse-panel>
      <a-collapse-panel key="plan" header="计划（Plan）">
        <div v-if="groupedCards.plan.length === 0" style="color: rgba(0, 0, 0, 0.45); font-size: 12px">—</div>
        <a-table v-else :columns="metricsTableColumns" :data-source="groupedCards.plan" size="small" :pagination="false">
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'status'">
              <a-tag v-if="record.status" :color="record.status === 'success' ? 'green' : record.status === 'warning' ? 'gold' : 'red'">
                {{ tagText(record.status) }}
              </a-tag>
              <span v-else style="color: rgba(0, 0, 0, 0.45)">—</span>
            </template>
          </template>
        </a-table>
      </a-collapse-panel>
      <a-collapse-panel key="quality" header="质量（Quality）">
        <div v-if="groupedCards.quality.length === 0" style="color: rgba(0, 0, 0, 0.45); font-size: 12px">—</div>
        <a-table v-else :columns="metricsTableColumns" :data-source="groupedCards.quality" size="small" :pagination="false">
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'status'">
              <a-tag v-if="record.status" :color="record.status === 'success' ? 'green' : record.status === 'warning' ? 'gold' : 'red'">
                {{ tagText(record.status) }}
              </a-tag>
              <span v-else style="color: rgba(0, 0, 0, 0.45)">—</span>
            </template>
          </template>
        </a-table>
      </a-collapse-panel>
      <a-collapse-panel key="engineering" header="工程效率（Engineering）">
        <div v-if="groupedCards.engineering.length === 0" style="color: rgba(0, 0, 0, 0.45); font-size: 12px">—</div>
        <a-table v-else :columns="metricsTableColumns" :data-source="groupedCards.engineering" size="small" :pagination="false">
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'status'">
              <a-tag v-if="record.status" :color="record.status === 'success' ? 'green' : record.status === 'warning' ? 'gold' : 'red'">
                {{ tagText(record.status) }}
              </a-tag>
              <span v-else style="color: rgba(0, 0, 0, 0.45)">—</span>
            </template>
          </template>
        </a-table>
      </a-collapse-panel>
      <a-collapse-panel v-if="groupedCards.other.length" key="other" header="其他">
        <a-table :columns="metricsTableColumns" :data-source="groupedCards.other" size="small" :pagination="false">
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'status'">
              <a-tag v-if="record.status" :color="record.status === 'success' ? 'green' : record.status === 'warning' ? 'gold' : 'red'">
                {{ tagText(record.status) }}
              </a-tag>
              <span v-else style="color: rgba(0, 0, 0, 0.45)">—</span>
            </template>
          </template>
        </a-table>
      </a-collapse-panel>
    </a-collapse>
  </a-space>
</template>

<script>
import { computed } from "vue";

export default {
  props: {
    selectedProjectIdModel: { type: String, default: "" },
    requestRunSkill: { type: Function, default: null },
    metricsError: { type: String, default: "" },
    metricsData: { type: [Object, null], default: null },
    enabledMetricKeys: { type: Array, default: () => [] }
  },
  setup(props) {
    function safeNumber(value) {
      const n = typeof value === "number" ? value : Number(value);
      return Number.isFinite(n) ? n : null;
    }

    function formatPercent(value) {
      const n = safeNumber(value);
      if (n === null) return "—";
      return `${Math.round(n * 1000) / 10}%`;
    }

    function formatDays(value) {
      const n = safeNumber(value);
      if (n === null) return "—";
      return `${Math.round(n * 10) / 10} 天`;
    }

    function rrgFromTarget(actual, target, higherIsBetter) {
      const a = safeNumber(actual);
      const t = safeNumber(target);
      if (a === null || t === null) return null;
      if (higherIsBetter) {
        if (a >= t) return "success";
        if (a >= t * 0.9) return "warning";
        return "error";
      }
      if (a <= t) return "success";
      if (a <= t * 1.1) return "warning";
      return "error";
    }

    function tagText(status) {
      if (status === "success") return "达标";
      if (status === "warning") return "关注";
      if (status === "error") return "偏离";
      return "—";
    }

    function pick(obj, path) {
      const parts = String(path || "").split(".").filter(Boolean);
      let cur = obj;
      for (const p of parts) {
        if (!cur || typeof cur !== "object") return undefined;
        cur = cur[p];
      }
      return cur;
    }

    function typeOfMetric(id) {
      const k = String(id || "");
      if (k === "throughput" || k === "wip_avg" || k === "aging_wip" || k.startsWith("lead_time_") || k.startsWith("cycle_time_") || k.startsWith("delivery_cycle_time_"))
        return "flow";
      if (k.includes("commitment") || k.includes("carryover") || k.includes("scope_change") || k.includes("requirement_change")) return "plan";
      if (k.includes("bug") || k.includes("reopen") || k.includes("escaped") || k.includes("defect")) return "quality";
      if (k.startsWith("pr_") || k.startsWith("review_latency") || k.startsWith("ci_") || k.includes("deployment") || k.includes("mttr") || k.includes("code_scan"))
        return "engineering";
      return "other";
    }

    function missingReasonForMetric(id) {
      const k = String(id || "");
      if (k === "throughput") return "暂无数据：可能本窗口内没有已完成（Done）的工作项，或 Jira 数据未成功获取。建议先执行“收集数据”，确认 Jira 工作项数量与状态分布。";
      if (k === "wip_avg" || k === "aging_wip")
        return "暂无数据：可能 Jira 中没有进行中的工作项，或状态/泳道口径未统一，或 Jira 数据获取失败。建议检查 Jira 工作项状态流转与“收集数据”结果。";
      if (k.startsWith("lead_time_") || k.startsWith("cycle_time_") || k.startsWith("delivery_cycle_time_"))
        return "暂无数据：可能本窗口内没有可用于统计的已完成条目，或 Jira 工作项缺少开始/完成时间（状态未流转/未记录变更），或 Jira 获取失败。建议检查 Jira 填写与状态流转口径。";
      if (k.startsWith("pr_lead_time_"))
        return "暂无数据：可能本窗口内没有 PR，或 PR 未合并/缺少创建或合并时间，或 Git 平台数据获取失败。建议检查仓库权限与 PR 数据是否存在。";
      if (k.startsWith("review_latency"))
        return "暂无数据：可能没有评审事件/评审数据未接入，或权限不足导致无法读取评审信息。建议检查评审数据来源与权限配置。";
      if (k.startsWith("ci_"))
        return "暂无数据：可能本窗口内没有 CI 运行记录，或 CI 系统未配置/权限不足导致获取失败。建议检查 CI 数据源配置与收集结果。";
      if (k.includes("code_scan")) return "暂无数据：可能未启用代码扫描门禁，或扫描结果未接入 CI 数据源。建议检查扫描工具与 CI 的集成配置。";
      if (k.includes("bug") || k.includes("reopen") || k.includes("escaped") || k.includes("defect"))
        return "暂无数据：可能缺陷记录不足，或缺陷字段（类型/阶段）未维护，或缺陷系统数据未接入/获取失败。建议检查缺陷口径与数据源配置。";
      if (k.includes("commitment") || k.includes("carryover") || k.includes("scope_change") || k.includes("requirement_change"))
        return "暂无数据：可能迭代计划/范围变更在 Jira 中未维护（缺少 Sprint/版本/变更记录），或相应字段未填写/未接入。建议先完善计划与变更数据口径。";
      return "暂无数据：可能输入数据为空，或数据源获取失败。建议先执行“收集数据”，并检查 Jira/Git/CI/缺陷系统的配置与权限。";
    }

    function analysisFor(id, status, actual, target) {
      const k = String(id || "");
      const s = String(status || "");
      if (actual === null || actual === undefined) return missingReasonForMetric(id);
      if (k.startsWith("lead_time_") || k.startsWith("cycle_time_") || k.startsWith("delivery_cycle_time_")) {
        if (s === "success") return "周期达标，关注波动与分位数尾部；若末期集中上升，优先检查 WIP/等待/评审排队。";
        if (s === "warning") return "略偏慢，优先通过拆小任务、减少并行、缩短评审等待来回拉。";
        if (s === "error") return "明显偏慢，通常是排队与返工叠加；先查泳道阻塞、评审/集成等待与质量门禁。";
        return "结合 WIP、评审等待与质量信号联动判断瓶颈位置。";
      }
      if (k === "wip_avg" || k === "aging_wip") {
        if (s === "success") return "WIP 处于可控范围，继续关注在制老化条目是否集中在某泳道。";
        if (s === "warning" || s === "error") return "WIP 偏高会引发排队与周期上升；建议设 WIP 上限、拉直流程、减少跨泳道等待。";
        return "建议与泳道阻塞/周期指标联动查看。";
      }
      if (k === "bug_rate" || k === "reopen_rate" || k.startsWith("escaped_") || k.includes("defect")) {
        if (s === "success") return "质量信号可接受；继续用缺陷分布/逃逸信号验证门禁是否前置。";
        if (s === "warning" || s === "error") return "质量风险偏高；检查测试策略、门禁阈值、回归覆盖与缺陷反馈闭环。";
        return "建议结合 code_scan/CI 与需求变更联动分析。";
      }
      if (k.startsWith("ci_") || k.includes("code_scan")) {
        if (s === "success") return "工程门禁/CI 表现良好；关注耗时与反馈周期，避免质量门禁成为排队点。";
        if (s === "warning" || s === "error") return "门禁未达标会导致返工与延迟；优先把门禁前置到 PR，并建立修复责任链。";
        return "建议结合 PR 周期与交付周期联动判断。";
      }
      if (k.startsWith("pr_") || k.startsWith("review_latency")) {
        if (s === "success") return "协作与评审节奏良好；继续关注 PR 粒度与末期合并集中。";
        if (s === "warning" || s === "error") return "PR/评审等待偏大；建议拆小 PR、设评审窗口/轮值、限制并行并减少返工。";
        return "建议结合 WIP/周期指标联动分析。";
      }
      if (k === "commitment_reliability" || k === "scope_change" || k.includes("requirement_change")) {
        return "计划类指标用于判断承诺与变更压力；若变更频繁，需在计划/验收口径上形成共识并可视化影响。";
      }
      if (target !== null && target !== undefined) return "结合目标阈值与趋势判断是否需要行动项；优先关注断点与异常波动。";
      return "建议结合趋势与上下游指标联动解释。";
    }

    const METRIC_LABELS = {
      throughput: "吞吐量",
      aging_wip: "老化在制（Aging WIP）",
      lead_time_p50: "交付周期 p50",
      lead_time_p75: "交付周期 p75",
      lead_time_p95: "交付周期 p95",
      cycle_time_p50: "处理周期 p50",
      cycle_time_p75: "处理周期 p75",
      cycle_time_p95: "处理周期 p95",
      wip_avg: "平均在制（WIP）",
      delivery_cycle_time_p50: "测试/交付周期 p50",
      delivery_cycle_time_p75: "测试/交付周期 p75",
      delivery_cycle_time_p95: "测试/交付周期 p95",
      commitment_reliability: "承诺达成率",
      carryover_rate: "结转率",
      scope_change: "范围变更",
      requirement_change_rate: "需求变更率",
      bug_rate: "缺陷率",
      reopen_rate: "重开率",
      requirement_defects: "需求缺陷情况",
      code_defects: "代码缺陷情况",
      review_defects: "评审缺陷",
      test_blockers: "测试阻塞",
      regression_defects: "回归缺陷",
      system_integration_test_defects: "系统集成测试缺陷分析",
      acceptance_test_defects: "验收测试缺陷分析",
      acceptance_fail_rate: "验收失败率",
      escaped_defects: "缺陷逃逸数量",
      escaped_defect_rate: "缺陷逃逸率",
      automated_test_coverage: "自动化测试覆盖率",
      deployment_frequency: "部署频率",
      change_failure_rate: "变更失败率",
      mttr: "平均恢复时间（MTTR）",
      commit_frequency: "提交频率",
      pr_issue_link_rate: "PR ↔ 需求关联率",
      pr_lead_time_p50: "PR 周期 p50",
      pr_lead_time_p75: "PR 周期 p75",
      pr_lead_time_p95: "PR 周期 p95",
      review_latency_p50: "评审等待 p50",
      review_latency_p75: "评审等待 p75",
      review_latency_p95: "评审等待 p95",
      ci_integration_frequency: "持续集成频率",
      ci_success_rate: "CI 成功率",
      ci_duration_p50: "CI 耗时 p50",
      code_scan_pass_rate: "代码扫描通过率",
      oncall_load: "值班负载",
      hotfix_ratio: "紧急修复占比"
    };

    function labelOf(id) {
      const k = String(id || "");
      if (METRIC_LABELS[k]) return METRIC_LABELS[k];
      const m = k.match(/^(delivery_cycle_time|lead_time|cycle_time|pr_lead_time|review_latency|ci_duration)_p(50|75|95)$/);
      if (m) {
        const base = m[1];
        const p = m[2];
        const baseMap = {
          delivery_cycle_time: "测试/交付周期",
          lead_time: "交付周期",
          cycle_time: "处理周期",
          pr_lead_time: "PR 周期",
          review_latency: "评审等待",
          ci_duration: "CI 耗时"
        };
        return `${baseMap[base] || base} p${p}`;
      }
      return `指标（${k}）`;
    }

    function buildRow(id, actual, formatFn, target, higherIsBetter, extraPrefix) {
      const a = actual === undefined ? null : actual;
      const t = target === undefined ? null : target;
      const status = a === null || a === undefined ? null : rrgFromTarget(a, t, higherIsBetter);
      const valueText = formatFn ? formatFn(a) : a === null || a === undefined ? "—" : String(a);
      const extra = extraPrefix ? `${extraPrefix}${t === null || t === undefined ? "—" : t}` : "—";
      return {
        id,
        key: id,
        title: labelOf(id),
        value: valueText,
        status,
        extra,
        analysis: analysisFor(id, status, a, t),
        metric_type: typeOfMetric(id)
      };
    }

    const rows = computed(() => {
      const m = props.metricsData || {};
      const t = (props.metricsData && props.metricsData.targets) || {};
      const selected = Array.isArray(props.enabledMetricKeys) ? props.enabledMetricKeys.map((x) => String(x)) : [];
      const keys = selected.length ? selected : [];
      const out = [];
      for (const id of keys) {
        if (id === "throughput") out.push(buildRow(id, pick(m, "throughput.count"), (v) => (v === null || v === undefined ? "—" : String(v)), null, false, ""));
        else if (id === "wip_avg") out.push(buildRow(id, pick(m, "wip.avg"), (v) => (safeNumber(v) === null ? "—" : safeNumber(v).toFixed(1)), t.wip_limit, false, "上限 ≤ "));
        else if (id === "aging_wip") out.push(buildRow(id, pick(m, "wip.aging_count") ?? pick(m, "wip.aging_wip_count"), (v) => (v === null || v === undefined ? "—" : String(v)), null, false, ""));
        else if (id === "lead_time_p50") out.push(buildRow(id, pick(m, "lead_time_days.p50"), formatDays, t.lead_time_p50_days, false, "目标 ≤ "));
        else if (id === "lead_time_p75") out.push(buildRow(id, pick(m, "lead_time_days.p75"), formatDays, null, false, ""));
        else if (id === "lead_time_p95") out.push(buildRow(id, pick(m, "lead_time_days.p95"), formatDays, null, false, ""));
        else if (id === "cycle_time_p50") out.push(buildRow(id, pick(m, "cycle_time_days.p50"), formatDays, t.cycle_time_p50_days, false, "目标 ≤ "));
        else if (id === "cycle_time_p75") out.push(buildRow(id, pick(m, "cycle_time_days.p75"), formatDays, null, false, ""));
        else if (id === "cycle_time_p95") out.push(buildRow(id, pick(m, "cycle_time_days.p95"), formatDays, null, false, ""));
        else if (id === "pr_lead_time_p50") out.push(buildRow(id, pick(m, "pr_lead_time_days.p50"), formatDays, t.pr_lead_time_p50_days, false, "目标 ≤ "));
        else if (id === "pr_lead_time_p75") out.push(buildRow(id, pick(m, "pr_lead_time_days.p75"), formatDays, null, false, ""));
        else if (id === "pr_lead_time_p95") out.push(buildRow(id, pick(m, "pr_lead_time_days.p95"), formatDays, null, false, ""));
        else if (id === "review_latency_p50") out.push(buildRow(id, pick(m, "review_latency_days.p50"), formatDays, t.review_latency_p50_days, false, "目标 ≤ "));
        else if (id === "review_latency_p75") out.push(buildRow(id, pick(m, "review_latency_days.p75"), formatDays, null, false, ""));
        else if (id === "review_latency_p95") out.push(buildRow(id, pick(m, "review_latency_days.p95"), formatDays, null, false, ""));
        else if (id === "commitment_reliability") out.push(buildRow(id, pick(m, "plan.commitment_reliability"), formatPercent, null, true, ""));
        else if (id === "scope_change") {
          const added = safeNumber(pick(m, "plan.scope_change.added"));
          const removed = safeNumber(pick(m, "plan.scope_change.removed"));
          const value = added === null && removed === null ? "—" : `+${added || 0} / -${removed || 0}`;
          out.push({
            id,
            key: id,
            title: labelOf(id),
            value,
            status: null,
            extra: "迭代内新增 / 移除（如有）",
            analysis: analysisFor(id, null, value === "—" ? null : 0, null),
            metric_type: typeOfMetric(id)
          });
        } else if (id === "bug_rate") out.push(buildRow(id, pick(m, "quality.bug_rate"), formatPercent, t.bug_rate_max, false, "阈值 ≤ "));
        else if (id === "reopen_rate") out.push(buildRow(id, pick(m, "quality.reopen_rate"), formatPercent, t.reopen_rate_max, false, "阈值 ≤ "));
        else if (id === "escaped_defects") out.push(buildRow(id, pick(m, "quality.escaped_defects"), (v) => (v === null || v === undefined ? "—" : String(v)), t.escaped_defects_max, false, "阈值 ≤ "));
        else if (id === "escaped_defect_rate") out.push(buildRow(id, pick(m, "quality.escaped_defect_rate"), formatPercent, t.escaped_defect_rate_max, false, "阈值 ≤ "));
        else if (id === "ci_integration_frequency") out.push(buildRow(id, pick(m, "ci.integration_frequency.count") ?? pick(m, "ci.runs_count"), (v) => (v === null || v === undefined ? "—" : String(v)), null, true, ""));
        else if (id === "ci_success_rate") out.push(buildRow(id, pick(m, "ci.success_rate"), formatPercent, t.ci_success_rate_min, true, "下限 ≥ "));
        else if (id === "code_scan_pass_rate") out.push(buildRow(id, pick(m, "ci.code_scan_pass_rate"), formatPercent, t.code_scan_pass_rate_min, true, "下限 ≥ "));
        else out.push(buildRow(id, pick(m, id), (v) => (v === null || v === undefined ? "—" : String(v)), null, false, ""));
      }
      return out;
    });

    const metricsTableColumns = [
      { title: "指标", dataIndex: "title", key: "title" },
      { title: "值", dataIndex: "value", key: "value", width: 140 },
      { title: "状态", dataIndex: "status", key: "status", width: 90 },
      { title: "说明/目标", dataIndex: "extra", key: "extra", width: 180 },
      { title: "分析结论", dataIndex: "analysis", key: "analysis" }
    ];

    const groupedCards = computed(() => {
      const groups = { flow: [], plan: [], quality: [], engineering: [], other: [] };
      const list = Array.isArray(rows.value) ? rows.value : [];
      for (const c of list) {
        const tp = c && c.metric_type ? String(c.metric_type) : "other";
        if (groups[tp]) groups[tp].push(c);
        else groups.other.push(c);
      }
      return groups;
    });

    return { tagText, groupedCards, metricsTableColumns };
  }
};
</script>
