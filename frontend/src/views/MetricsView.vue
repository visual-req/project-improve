<template>
  <div v-if="!data" style="color: rgba(0, 0, 0, 0.65)">尚未导入数据。</div>
  <div v-else>
    <a-space style="margin-bottom: 12px" wrap>
      <a-tag color="blue">窗口：{{ windowText }}</a-tag>
      <a-tag color="blue">项目：{{ projectName }}</a-tag>
    </a-space>
    <a-row :gutter="[12, 12]">
      <a-col v-for="c in cards" :key="c.key" :xs="24" :sm="12" :lg="8">
        <a-card size="small">
          <template #title>
            <a-space>
              <span>{{ c.key }}</span>
              <a-tag v-if="c.status" :color="c.status === 'success' ? 'green' : c.status === 'warning' ? 'gold' : 'red'">
                {{ tagText(c.status) }}
              </a-tag>
            </a-space>
          </template>
          <a-statistic :value="c.value" />
          <div style="margin-top: 6px; color: rgba(0, 0, 0, 0.65); font-size: 12px">{{ c.extra }}</div>
        </a-card>
      </a-col>
    </a-row>
    <a-divider />
    <a-typography-title :level="5" style="margin-top: 0">数据完整性</a-typography-title>
    <a-typography-paragraph style="margin-bottom: 0">
      <pre style="margin: 0; white-space: pre-wrap">{{ JSON.stringify((data && data.data_integrity) || {}, null, 2) }}</pre>
    </a-typography-paragraph>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  data: { type: Object, default: null },
  metricsConfig: { type: Object, default: null }
});

const metrics = computed(() => (props.data && props.data.metrics) || {});
const targets = computed(() => metrics.value.targets || {});
const enabled = computed(() => (props.metricsConfig && props.metricsConfig.enabled) || {});

const projectName = computed(() => (props.data && props.data.project && props.data.project.name) || "—");
const windowText = computed(() => {
  const w = metrics.value.window || {};
  if (w.start && w.end) return `${String(w.start).slice(0, 10)} ~ ${String(w.end).slice(0, 10)}`;
  if (w.days) return `${w.days} 天`;
  return "—";
});

function safeNumber(value) {
  const n = typeof value === "number" ? value : Number(value);
  return Number.isFinite(n) ? n : null;
}

function rrgFromTarget(value, target, higherIsBetter = false) {
  const v = safeNumber(value);
  const t = safeNumber(target);
  if (v === null || t === null) return null;
  if (higherIsBetter) {
    if (v >= t) return "success";
    if (v >= t * 0.9) return "warning";
    return "error";
  }
  if (v <= t) return "success";
  if (v <= t * 1.1) return "warning";
  return "error";
}

function tagText(status) {
  if (status === "success") return "绿";
  if (status === "warning") return "黄";
  if (status === "error") return "红";
  return "—";
}

const cards = computed(() => {
  const m = metrics.value;
  const t = targets.value;

  const leadP50 = m.lead_time_days && m.lead_time_days.p50;
  const cycleP50 = m.cycle_time_days && m.cycle_time_days.p50;
  const wipAvg = m.wip && m.wip.avg;
  const throughput = m.throughput && m.throughput.count;
  const bugRate = m.quality && m.quality.bug_rate;
  const reopenRate = m.quality && m.quality.reopen_rate;
  const escaped = m.quality && m.quality.escaped_defects;
  const prP50 = m.pr_lead_time_days && m.pr_lead_time_days.p50;
  const reviewP50 = m.review_latency_days && m.review_latency_days.p50;
  const ci = m.ci || {};
  const ciRuns = (ci.integration_frequency && ci.integration_frequency.count) ?? ci.runs_count ?? null;
  const ciSuccessRate = ci.success_rate ?? null;
  const codeScanPassRate = ci.code_scan_pass_rate ?? ci.scan_pass_rate ?? null;

  const all = [
    { id: "throughput", key: "Throughput", value: throughput ?? "—", extra: "完成数量", status: null },
    {
      id: "lead_time_p50",
      key: "Lead Time p50",
      value: safeNumber(leadP50) === null ? "—" : `${safeNumber(leadP50).toFixed(1)} 天`,
      extra: `目标 ≤ ${t.lead_time_p50_days ?? "—"}`,
      status: rrgFromTarget(leadP50, t.lead_time_p50_days, false)
    },
    {
      id: "cycle_time_p50",
      key: "Cycle Time p50",
      value: safeNumber(cycleP50) === null ? "—" : `${safeNumber(cycleP50).toFixed(1)} 天`,
      extra: `目标 ≤ ${t.cycle_time_p50_days ?? "—"}`,
      status: rrgFromTarget(cycleP50, t.cycle_time_p50_days, false)
    },
    {
      id: "wip_avg",
      key: "WIP 平均",
      value: safeNumber(wipAvg) === null ? "—" : safeNumber(wipAvg).toFixed(1),
      extra: `上限 ≤ ${t.wip_limit ?? "—"}`,
      status: rrgFromTarget(wipAvg, t.wip_limit, false)
    },
    {
      id: "bug_rate",
      key: "Bug Rate",
      value: safeNumber(bugRate) === null ? "—" : `${(safeNumber(bugRate) * 100).toFixed(0)}%`,
      extra: `阈值 ≤ ${t.bug_rate_max ?? "—"}`,
      status: rrgFromTarget(bugRate, t.bug_rate_max, false)
    },
    {
      id: "reopen_rate",
      key: "重开率",
      value: safeNumber(reopenRate) === null ? "—" : `${(safeNumber(reopenRate) * 100).toFixed(0)}%`,
      extra: `阈值 ≤ ${t.reopen_rate_max ?? "—"}`,
      status: rrgFromTarget(reopenRate, t.reopen_rate_max, false)
    },
    {
      id: "escaped_defects",
      key: "缺陷逃逸率",
      value: escaped ?? "—",
      extra: `阈值 ≤ ${t.escaped_defects_max ?? "—"}`,
      status: rrgFromTarget(escaped, t.escaped_defects_max, false)
    },
    {
      id: "pr_lead_time_p50",
      key: "PR Lead Time p50",
      value: safeNumber(prP50) === null ? "—" : `${safeNumber(prP50).toFixed(1)} 天`,
      extra: `目标 ≤ ${t.pr_lead_time_p50_days ?? "—"}`,
      status: rrgFromTarget(prP50, t.pr_lead_time_p50_days, false)
    },
    {
      id: "review_latency_p50",
      key: "Review Latency p50",
      value: safeNumber(reviewP50) === null ? "—" : `${safeNumber(reviewP50).toFixed(1)} 天`,
      extra: `目标 ≤ ${t.review_latency_p50_days ?? "—"}`,
      status: rrgFromTarget(reviewP50, t.review_latency_p50_days, false)
    },
    {
      id: "ci_integration_frequency",
      key: "Integration Frequency",
      value: ciRuns === null ? "—" : String(ciRuns),
      extra: "CI 运行次数（窗口内）",
      status: null
    },
    {
      id: "ci_success_rate",
      key: "CI Success Rate",
      value: safeNumber(ciSuccessRate) === null ? "—" : `${(safeNumber(ciSuccessRate) * 100).toFixed(0)}%`,
      extra: `下限 ≥ ${t.ci_success_rate_min ?? "—"}`,
      status: rrgFromTarget(ciSuccessRate, t.ci_success_rate_min, true)
    },
    {
      id: "code_scan_pass_rate",
      key: "Code Scan Pass Rate",
      value: safeNumber(codeScanPassRate) === null ? "—" : `${(safeNumber(codeScanPassRate) * 100).toFixed(0)}%`,
      extra: `下限 ≥ ${t.code_scan_pass_rate_min ?? "—"}`,
      status: rrgFromTarget(codeScanPassRate, t.code_scan_pass_rate_min, true)
    }
  ];
  return all.filter((c) => enabled.value[c.id] !== false);
});
</script>
