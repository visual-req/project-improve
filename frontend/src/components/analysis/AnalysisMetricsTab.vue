<template>
  <a-space direction="vertical" style="width: 100%" :size="12">
    <a-button type="primary" @click="requestRunSkill('metrics')">{{ t("analysis.run.metrics") }}</a-button>
    <a-alert v-if="metricsError" type="warning" show-icon :message="metricsError" />
    <a-card size="small" :title="t('analysis.files')">
      <ul style="margin: 0; padding-left: 18px">
        <li>输入：/work/{{ selectedProjectIdModel || "&lt;project_id&gt;" }}/meta/config.yaml</li>
        <li>输入：/work/outputs/{{ selectedProjectIdModel || "&lt;project_id&gt;" }}/project-metrics-orid/raw.json</li>
        <li>输出：/work/outputs/{{ selectedProjectIdModel || "&lt;project_id&gt;" }}/project-metrics-orid/metrics.json</li>
      </ul>
    </a-card>
    <a-card size="small" :title="t('analysis.scope')">
      <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px">
        {{ t("analysis.metrics.selectedCount", { count: enabledMetricKeys.length }) }}{{ enabledMetricKeys.length ? "" : t("analysis.metrics.scopeHint.noneSelected") }}
      </div>
    </a-card>
    <div v-if="!metricsData" style="color: rgba(0, 0, 0, 0.65)">{{ t("analysis.noMetricsYet") }}</div>
    <a-collapse v-else :bordered="false" style="background: transparent">
      <a-collapse-panel key="flow" :header="t('analysis.metrics.group.flow')">
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
      <a-collapse-panel key="plan" :header="t('analysis.metrics.group.plan')">
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
      <a-collapse-panel key="quality" :header="t('analysis.metrics.group.quality')">
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
      <a-collapse-panel key="engineering" :header="t('analysis.metrics.group.engineering')">
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
      <a-collapse-panel v-if="groupedCards.other.length" key="other" :header="t('analysis.metrics.group.other')">
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
import { useI18n } from "../../i18n.js";

export default {
  props: {
    selectedProjectIdModel: { type: String, default: "" },
    requestRunSkill: { type: Function, default: null },
    metricsError: { type: String, default: "" },
    metricsData: { type: [Object, null], default: null },
    enabledMetricKeys: { type: Array, default: () => [] }
  },
  setup(props) {
    const { t } = useI18n();
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
      return t("unit.days", { n: Math.round(n * 10) / 10 });
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
      if (status === "success") return t("analysis.metrics.status.success");
      if (status === "warning") return t("analysis.metrics.status.warning");
      if (status === "error") return t("analysis.metrics.status.error");
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
      if (k === "throughput") return t("analysis.metrics.missing.throughput");
      if (k === "wip_avg" || k === "aging_wip") return t("analysis.metrics.missing.wip");
      if (k.startsWith("lead_time_") || k.startsWith("cycle_time_") || k.startsWith("delivery_cycle_time_")) return t("analysis.metrics.missing.leadTime");
      if (k.startsWith("pr_lead_time_")) return t("analysis.metrics.missing.prLeadTime");
      if (k.startsWith("review_latency")) return t("analysis.metrics.missing.reviewLatency");
      if (k.startsWith("ci_")) return t("analysis.metrics.missing.ci");
      if (k.includes("code_scan")) return t("analysis.metrics.missing.codeScan");
      if (k.includes("bug") || k.includes("reopen") || k.includes("escaped") || k.includes("defect")) return t("analysis.metrics.missing.defects");
      if (k.includes("commitment") || k.includes("carryover") || k.includes("scope_change") || k.includes("requirement_change")) return t("analysis.metrics.missing.plan");
      return t("analysis.metrics.missing.generic");
    }

    function analysisFor(id, status, actual, target) {
      const k = String(id || "");
      const s = String(status || "");
      if (actual === null || actual === undefined) return missingReasonForMetric(id);
      if (k.startsWith("lead_time_") || k.startsWith("cycle_time_") || k.startsWith("delivery_cycle_time_")) {
        if (s === "success") return t("analysis.metrics.analysis.leadTime.success");
        if (s === "warning") return t("analysis.metrics.analysis.leadTime.warning");
        if (s === "error") return t("analysis.metrics.analysis.leadTime.error");
        return t("analysis.metrics.analysis.leadTime.generic");
      }
      if (k === "wip_avg" || k === "aging_wip") {
        if (s === "success") return t("analysis.metrics.analysis.wip.success");
        if (s === "warning" || s === "error") return t("analysis.metrics.analysis.wip.warning");
        return t("analysis.metrics.analysis.wip.generic");
      }
      if (k === "bug_rate" || k === "reopen_rate" || k.startsWith("escaped_") || k.includes("defect")) {
        if (s === "success") return t("analysis.metrics.analysis.quality.success");
        if (s === "warning" || s === "error") return t("analysis.metrics.analysis.quality.warning");
        return t("analysis.metrics.analysis.quality.generic");
      }
      if (k.startsWith("ci_") || k.includes("code_scan")) {
        if (s === "success") return t("analysis.metrics.analysis.ci.success");
        if (s === "warning" || s === "error") return t("analysis.metrics.analysis.ci.warning");
        return t("analysis.metrics.analysis.ci.generic");
      }
      if (k.startsWith("pr_") || k.startsWith("review_latency")) {
        if (s === "success") return t("analysis.metrics.analysis.pr.success");
        if (s === "warning" || s === "error") return t("analysis.metrics.analysis.pr.warning");
        return t("analysis.metrics.analysis.pr.generic");
      }
      if (k === "commitment_reliability" || k === "scope_change" || k.includes("requirement_change")) {
        return t("analysis.metrics.analysis.plan.generic");
      }
      if (target !== null && target !== undefined) return t("analysis.metrics.analysis.target.generic");
      return t("analysis.metrics.analysis.generic");
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
      const localized = t(`metric.${k}`);
      if (localized && localized !== `metric.${k}`) return localized;
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
        const localizedBase = t(`metricBase.${base}`);
        const baseText = localizedBase && localizedBase !== `metricBase.${base}` ? localizedBase : baseMap[base] || base;
        return `${baseText} p${p}`;
      }
      const fallback = t("analysis.metrics.metricFallback", { key: k });
      return fallback && fallback !== "analysis.metrics.metricFallback" ? fallback : `Metric (${k})`;
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
        else if (id === "wip_avg") out.push(buildRow(id, pick(m, "wip.avg"), (v) => (safeNumber(v) === null ? "—" : safeNumber(v).toFixed(1)), t.wip_limit, false, t("analysis.metrics.extra.upperLimit")));
        else if (id === "aging_wip") out.push(buildRow(id, pick(m, "wip.aging_count") ?? pick(m, "wip.aging_wip_count"), (v) => (v === null || v === undefined ? "—" : String(v)), null, false, ""));
        else if (id === "lead_time_p50") out.push(buildRow(id, pick(m, "lead_time_days.p50"), formatDays, t.lead_time_p50_days, false, t("analysis.metrics.extra.targetLE")));
        else if (id === "lead_time_p75") out.push(buildRow(id, pick(m, "lead_time_days.p75"), formatDays, null, false, ""));
        else if (id === "lead_time_p95") out.push(buildRow(id, pick(m, "lead_time_days.p95"), formatDays, null, false, ""));
        else if (id === "cycle_time_p50") out.push(buildRow(id, pick(m, "cycle_time_days.p50"), formatDays, t.cycle_time_p50_days, false, t("analysis.metrics.extra.targetLE")));
        else if (id === "cycle_time_p75") out.push(buildRow(id, pick(m, "cycle_time_days.p75"), formatDays, null, false, ""));
        else if (id === "cycle_time_p95") out.push(buildRow(id, pick(m, "cycle_time_days.p95"), formatDays, null, false, ""));
        else if (id === "pr_lead_time_p50") out.push(buildRow(id, pick(m, "pr_lead_time_days.p50"), formatDays, t.pr_lead_time_p50_days, false, t("analysis.metrics.extra.targetLE")));
        else if (id === "pr_lead_time_p75") out.push(buildRow(id, pick(m, "pr_lead_time_days.p75"), formatDays, null, false, ""));
        else if (id === "pr_lead_time_p95") out.push(buildRow(id, pick(m, "pr_lead_time_days.p95"), formatDays, null, false, ""));
        else if (id === "review_latency_p50") out.push(buildRow(id, pick(m, "review_latency_days.p50"), formatDays, t.review_latency_p50_days, false, t("analysis.metrics.extra.targetLE")));
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
            extra: t("analysis.metrics.extra.scopeChangeNote"),
            analysis: analysisFor(id, null, value === "—" ? null : 0, null),
            metric_type: typeOfMetric(id)
          });
        } else if (id === "bug_rate") out.push(buildRow(id, pick(m, "quality.bug_rate"), formatPercent, t.bug_rate_max, false, t("analysis.metrics.extra.thresholdLE")));
        else if (id === "reopen_rate") out.push(buildRow(id, pick(m, "quality.reopen_rate"), formatPercent, t.reopen_rate_max, false, t("analysis.metrics.extra.thresholdLE")));
        else if (id === "escaped_defects") out.push(buildRow(id, pick(m, "quality.escaped_defects"), (v) => (v === null || v === undefined ? "—" : String(v)), t.escaped_defects_max, false, t("analysis.metrics.extra.thresholdLE")));
        else if (id === "escaped_defect_rate") out.push(buildRow(id, pick(m, "quality.escaped_defect_rate"), formatPercent, t.escaped_defect_rate_max, false, t("analysis.metrics.extra.thresholdLE")));
        else if (id === "ci_integration_frequency") out.push(buildRow(id, pick(m, "ci.integration_frequency.count") ?? pick(m, "ci.runs_count"), (v) => (v === null || v === undefined ? "—" : String(v)), null, true, ""));
        else if (id === "ci_success_rate") out.push(buildRow(id, pick(m, "ci.success_rate"), formatPercent, t.ci_success_rate_min, true, t("analysis.metrics.extra.lowerLimit")));
        else if (id === "code_scan_pass_rate") out.push(buildRow(id, pick(m, "ci.code_scan_pass_rate"), formatPercent, t.code_scan_pass_rate_min, true, t("analysis.metrics.extra.lowerLimit")));
        else out.push(buildRow(id, pick(m, id), (v) => (v === null || v === undefined ? "—" : String(v)), null, false, ""));
      }
      return out;
    });

    const metricsTableColumns = computed(() => [
      { title: t("analysis.metrics.table.metric"), dataIndex: "title", key: "title" },
      { title: t("analysis.metrics.table.value"), dataIndex: "value", key: "value", width: 140 },
      { title: t("analysis.metrics.table.status"), dataIndex: "status", key: "status", width: 90 },
      { title: t("analysis.metrics.table.extra"), dataIndex: "extra", key: "extra", width: 180 },
      { title: t("analysis.metrics.table.analysis"), dataIndex: "analysis", key: "analysis" }
    ]);

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

    return { t, tagText, groupedCards, metricsTableColumns };
  }
};
</script>
