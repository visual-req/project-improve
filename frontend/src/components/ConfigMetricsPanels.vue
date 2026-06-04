<template>
  <a-space direction="vertical" style="width: 100%" :size="12">
    <a-space wrap align="center">
      <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">项目</span>
      <a-select v-model:value="selectedProjectId" style="min-width: 320px">
        <a-select-option v-for="(p, idx) in projects" :key="String(p.id) + ':' + String(idx)" :value="String(p.id)">
          {{ String(p.id) }} · {{ String(p.name || "") }}
        </a-select-option>
      </a-select>
      <a-button type="default" @click="setAllEnabled(true)">全选</a-button>
      <a-button type="default" @click="setAllEnabled(false)">全不选</a-button>
      <a-button type="primary" @click="saveMetricsConfig">保存</a-button>
      <a-button type="default" @click="exportMetricsJson">导出</a-button>
      <a-button type="default" @click="resetToDefault">重置</a-button>
      <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">{{ statusText }}</span>
    </a-space>

    <a-collapse>
      <a-collapse-panel v-for="t in matrix" :key="t.type" :header="t.label">
        <a-row :gutter="[12, 12]">
          <a-col v-for="p in t.phases" :key="p.phase" :xs="24" :md="12" :lg="6">
            <a-card size="small" :title="p.label" style="height: 100%">
              <a-space direction="vertical" style="width: 100%" :size="6">
                <div v-for="it in p.items" :key="it.key" style="display: flex; align-items: flex-start; justify-content: space-between; gap: 8px">
                  <a-checkbox :checked="metricChecked(it.key)" @change="(e) => setMetricChecked(it.key, e && e.target ? e.target.checked : false)">
                    {{ METRIC_LABELS[it.key] || it.key }}
                  </a-checkbox>
                  <a-popover trigger="click" placement="right">
                    <template #content>
                      <div style="max-width: 360px">
                        <div style="font-weight: 600; margin-bottom: 8px">{{ METRIC_LABELS[it.key] || it.key }}</div>
                        <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px; margin-bottom: 4px">含义</div>
                        <div style="margin-bottom: 8px">{{ helpOf(it.key).meaning }}</div>
                        <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px; margin-bottom: 4px">度量方法</div>
                        <div style="margin-bottom: 8px">{{ helpOf(it.key).method }}</div>
                        <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px; margin-bottom: 4px">计算公式</div>
                        <div style="margin-bottom: 8px">{{ helpOf(it.key).formula }}</div>
                        <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px; margin-bottom: 4px">参考值</div>
                        <div>{{ helpOf(it.key).reference }}</div>
                      </div>
                    </template>
                    <a-button size="small" shape="circle" type="default">?</a-button>
                  </a-popover>
                </div>
                <div v-if="!p.items || p.items.length === 0" style="color: rgba(0, 0, 0, 0.45); font-size: 12px">—</div>
              </a-space>
            </a-card>
          </a-col>
        </a-row>
      </a-collapse-panel>
    </a-collapse>
  </a-space>
</template>

<script>
import { computed, ref, watch } from "vue";
import { load } from "js-yaml";

export default {
  setup() {
    async function fetchProjectsRegistry() {
      try {
        const res = await fetch("/work/meta/config.yaml", { cache: "no-store" });
        if (!res.ok) return [];
        const text = await res.text();
        const obj = load(text);
        return obj && Array.isArray(obj.projects) ? obj.projects : [];
      } catch {
        return [];
      }
    }

    function downloadText(filename, text, mime) {
      const blob = new Blob([text], { type: (mime || "text/plain") + ";charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    }

const METRIC_CATALOG = [
  { key: "throughput", label: "吞吐量", type: "flow", phase: "plan" },
  { key: "wip_avg", label: "平均在制（WIP）", type: "flow", phase: "plan" },
  { key: "aging_wip", label: "老化在制（Aging WIP）", type: "flow", phase: "plan" },
  { key: "lead_time_p50", label: "交付周期 p50", type: "flow", phase: "plan" },
  { key: "lead_time_p75", label: "交付周期 p75", type: "flow", phase: "plan" },
  { key: "lead_time_p95", label: "交付周期 p95", type: "flow", phase: "plan" },
  { key: "cycle_time_p50", label: "处理周期 p50", type: "flow", phase: "dev" },
  { key: "cycle_time_p75", label: "处理周期 p75", type: "flow", phase: "dev" },
  { key: "cycle_time_p95", label: "处理周期 p95", type: "flow", phase: "dev" },
  { key: "review_latency_p50", label: "评审等待 p50", type: "engineering", phase: "dev" },
  { key: "review_latency_p75", label: "评审等待 p75", type: "engineering", phase: "dev" },
  { key: "review_latency_p95", label: "评审等待 p95", type: "engineering", phase: "dev" },
  { key: "pr_lead_time_p50", label: "PR 周期 p50", type: "engineering", phase: "dev" },
  { key: "pr_lead_time_p75", label: "PR 周期 p75", type: "engineering", phase: "dev" },
  { key: "pr_lead_time_p95", label: "PR 周期 p95", type: "engineering", phase: "dev" },
  { key: "change_size", label: "变更规模", type: "engineering", phase: "dev" },
  { key: "deployment_frequency", label: "发布频率", type: "flow", phase: "test" },
  { key: "delivery_batch_size", label: "交付批量", type: "flow", phase: "test" },
  { key: "delivery_cycle_time_p50", label: "交付周期（测试/交付）p50", type: "flow", phase: "test" },
  { key: "delivery_cycle_time_p75", label: "交付周期（测试/交付）p75", type: "flow", phase: "test" },
  { key: "delivery_cycle_time_p95", label: "交付周期（测试/交付）p95", type: "flow", phase: "test" },
  { key: "mttr", label: "平均恢复时间（MTTR）", type: "flow", phase: "run" },
  { key: "change_failure_rate", label: "变更失败率", type: "flow", phase: "run" },
  { key: "commitment_reliability", label: "承诺达成率", type: "plan", phase: "plan" },
  { key: "scope_change", label: "范围变更", type: "plan", phase: "plan" },
  { key: "iteration_throughput", label: "迭代吞吐率", type: "plan", phase: "plan" },
  { key: "iteration_completion_rate", label: "迭代完成率", type: "plan", phase: "plan" },
  { key: "carryover_rate", label: "迭代结转率", type: "plan", phase: "plan" },
  { key: "wip_limit_adherence", label: "WIP 上限执行率", type: "plan", phase: "dev" },
  { key: "blocked_ratio", label: "阻塞占比", type: "plan", phase: "dev" },
  { key: "ontime_delivery_rate", label: "按期交付率", type: "plan", phase: "test" },
  { key: "rework_ratio", label: "返工比例", type: "plan", phase: "test" },
  { key: "requirement_change_rate", label: "需求变更率", type: "plan", phase: "test" },
  { key: "online_commitment_deviation", label: "线上承诺偏差", type: "plan", phase: "run" },
  { key: "sla", label: "SLA 达成情况", type: "plan", phase: "run" },
  { key: "requirement_defects", label: "需求缺陷情况", type: "quality", phase: "plan" },
  { key: "code_defects", label: "代码缺陷情况", type: "quality", phase: "dev" },
  { key: "automated_test_coverage", label: "自动化测试覆盖率", type: "quality", phase: "test" },
  { key: "bug_rate", label: "缺陷率（Bug Rate）", type: "quality", phase: "plan" },
  { key: "reopen_rate", label: "重开率", type: "quality", phase: "test" },
  { key: "review_defects", label: "评审缺陷", type: "quality", phase: "dev" },
  { key: "test_blockers", label: "测试阻塞", type: "quality", phase: "dev" },
  { key: "regression_defects", label: "回归缺陷", type: "quality", phase: "test" },
  { key: "system_integration_test_defects", label: "系统集成测试缺陷分析", type: "quality", phase: "test" },
  { key: "acceptance_test_defects", label: "验收测试缺陷分析", type: "quality", phase: "test" },
  { key: "acceptance_fail_rate", label: "验收失败率", type: "quality", phase: "test" },
  { key: "escaped_defects", label: "缺陷逃逸数量", type: "quality", phase: "run" },
  { key: "escaped_defect_rate", label: "缺陷逃逸率", type: "quality", phase: "run" },
  { key: "prod_defect_severity", label: "生产缺陷严重度", type: "quality", phase: "run" },
  { key: "commit_frequency", label: "提交频率", type: "engineering", phase: "plan" },
  { key: "pr_issue_link_rate", label: "PR ↔ 需求关联率", type: "engineering", phase: "plan" },
  { key: "ci_integration_frequency", label: "持续集成频率", type: "engineering", phase: "test" },
  { key: "ci_success_rate", label: "CI 成功率", type: "engineering", phase: "test" },
  { key: "code_scan_pass_rate", label: "代码扫描通过率", type: "engineering", phase: "test" },
  { key: "ci_duration_p50", label: "CI 耗时 p50", type: "engineering", phase: "test" },
  { key: "oncall_load", label: "值班负载", type: "engineering", phase: "run" },
  { key: "hotfix_ratio", label: "紧急修复占比", type: "engineering", phase: "run" }
];

const METRIC_KEYS = Array.from(new Set(METRIC_CATALOG.map((x) => x.key)));
const METRIC_LABELS = METRIC_CATALOG.reduce((acc, x) => {
  acc[x.key] = x.label;
  return acc;
}, {});

const PHASE_LABELS = { plan: "需求/计划", dev: "开发/评审", test: "测试/交付", run: "线上/运行" };
const TYPE_LABELS = { flow: "流动", plan: "计划", quality: "质量", engineering: "工程效率" };

function defaultEnabledMap() {
  const m = {};
  METRIC_KEYS.forEach((k) => (m[k] = false));
  [
    "throughput",
    "wip_avg",
    "aging_wip",
    "lead_time_p50",
    "cycle_time_p50",
    "review_latency_p50",
    "pr_lead_time_p50",
    "deployment_frequency",
    "change_failure_rate",
    "mttr",
    "delivery_cycle_time_p50",
    "commitment_reliability",
    "carryover_rate",
    "requirement_change_rate",
    "bug_rate",
    "system_integration_test_defects",
    "acceptance_test_defects",
    "escaped_defects",
    "escaped_defect_rate",
    "automated_test_coverage",
    "ci_success_rate",
    "code_scan_pass_rate"
  ].forEach((k) => {
    if (m[k] !== undefined) m[k] = true;
  });
  return m;
}

const METRIC_HELP = {
  throughput: { meaning: "时间窗内完成的工作项数量。", method: "统计 metrics.throughput.count。", formula: "吞吐量 = 完成条目数。", reference: "更关注趋势。" },
  wip_avg: {
    meaning: "时间窗内平均在制数量。",
    method: "统计处于 WIP 状态集合中的条目数量并求平均。",
    formula: "WIP_avg = 在制数量时间平均。",
    reference: "可用看板 WIP 上限作参考。"
  },
  lead_time_p50: {
    meaning: "从创建到完成的交付周期中位数。",
    method: "created→done 的天数分布取 p50。",
    formula: "交付周期 = done_at - created_at。",
    reference: "用团队承诺周期作参考。"
  },
  cycle_time_p50: {
    meaning: "从开始处理到完成的处理周期中位数。",
    method: "in_progress→done 的天数分布取 p50。",
    formula: "处理周期 = done_at - in_progress_at。",
    reference: "与 WIP/评审等待联动解读。"
  },
  bug_rate: {
    meaning: "缺陷率：时间窗内 Bug 完成数占比。",
    method: "统计 bug 完成数与总完成数。",
    formula: "缺陷率 = BugsDone / AllDone。",
    reference: "结合返工与变更规模综合看。"
  },
  escaped_defects: {
    meaning: "线上逃逸缺陷数量。",
    method: "按 bug_source 规则识别生产缺陷。",
    formula: "count(线上缺陷)。",
    reference: "建议结合严重度与趋势。"
  },
  automated_test_coverage: {
    meaning: "自动化测试覆盖率。",
    method: "从测试平台/CI 获取覆盖率。",
    formula: "覆盖率 = 覆盖项 / 总项。",
    reference: "结合回归成本与缺陷综合评估。"
  },
  requirement_defects: {
    meaning: "需求缺陷情况（按团队口径）。",
    method: "需求澄清/返工/验收失败/需求变更等信号。",
    formula: "按口径定义。",
    reference: "先统一口径再做趋势。"
  },
  code_defects: {
    meaning: "代码缺陷情况（按团队口径）。",
    method: "代码扫描问题、评审缺陷、缺陷密度等。",
    formula: "按口径定义。",
    reference: "与变更规模联动解读。"
  },
  system_integration_test_defects: {
    meaning: "系统集成测试阶段暴露的缺陷分布与成因画像（不是单一数量）。",
    method: "从缺陷系统中按阶段/标签/发现环节统计（SIT），结合模块、责任域、缺陷类型聚类分析。",
    formula: "可拆为：SIT缺陷数量、SIT缺陷占比、SIT缺陷Top原因/模块分布。",
    reference: "用于定位：集成接口、环境一致性、契约测试缺失、跨团队协作接口不清等问题。"
  },
  acceptance_test_defects: {
    meaning: "验收测试阶段暴露的缺陷分布与成因画像（不是单一数量）。",
    method: "从缺陷系统中按阶段/标签/发现环节统计（UAT/验收），结合需求变更、验收口径、测试用例覆盖进行联动分析。",
    formula: "可拆为：验收缺陷数量、验收缺陷占比、验收失败原因Top（需求/口径/实现/数据/环境）。",
    reference: "用于定位：验收标准不清、需求澄清不足、回归覆盖不足、数据/权限/环境差异导致的问题。"
  }
};

function helpOf(key) {
  const k = String(key);
  const label = METRIC_LABELS[k] || k;
  return (
    METRIC_HELP[k] || {
      meaning: `指标：${label}。用于辅助定位流程/质量/工程效率方面的阻碍点。`,
      method: "按团队口径从项目管理系统、代码仓库、CI/CD、缺陷系统等数据源聚合计算。",
      formula: "按口径定义（可先用趋势分析，再逐步细化公式）。",
      reference: "更关注趋势与断点；结合看板/PR/CI 证据做联动解释。"
    }
  );
}

    const statusText = ref("");
    const fallbackProjects = [{ id: "example", name: "example-project", slug_en: "example-project" }];
    const projects = ref(fallbackProjects);
    const selectedProjectId = ref("example");

const metricsConfig = ref({ enabled: defaultEnabledMap() });
const matrix = computed(() => {
  const byType = { flow: [], plan: [], quality: [], engineering: [] };
  METRIC_CATALOG.forEach((m) => {
    const t = m.type || "flow";
    byType[t] = byType[t] || [];
    byType[t].push(m);
  });
  const types = Object.keys(TYPE_LABELS).map((t) => ({ type: t, label: TYPE_LABELS[t] }));
  const phases = Object.keys(PHASE_LABELS).map((p) => ({ phase: p, label: PHASE_LABELS[p] }));
  return types.map((t) => ({
    ...t,
    phases: phases.map((p) => ({ ...p, items: (byType[t.type] || []).filter((x) => x.phase === p.phase) }))
  }));
});

    async function loadProjects() {
      const loaded = await fetchProjectsRegistry();
      projects.value = Array.isArray(loaded) && loaded.length ? loaded : fallbackProjects;
      const first = projects.value[0];
      selectedProjectId.value = (first && String(first.id)) || "example";
    }

function resetMetricsConfig() {
  metricsConfig.value = { enabled: defaultEnabledMap() };
}

function metricChecked(key) {
  const k = String(key);
  return metricsConfig.value && metricsConfig.value.enabled ? metricsConfig.value.enabled[k] === true : false;
}

function setMetricChecked(key, checked) {
  const k = String(key);
  if (!metricsConfig.value || typeof metricsConfig.value !== "object") metricsConfig.value = { enabled: {} };
  if (!metricsConfig.value.enabled || typeof metricsConfig.value.enabled !== "object") metricsConfig.value.enabled = {};
  metricsConfig.value.enabled[k] = !!checked;
}

function setAllEnabled(on) {
  const next = defaultEnabledMap();
  METRIC_KEYS.forEach((k) => {
    next[k] = !!on;
  });
  metricsConfig.value = { enabled: next };
}

function exportMetricsJson() {
  const pid = selectedProjectId.value || "example";
  const payload = { enabled: { ...defaultEnabledMap(), ...((metricsConfig.value && metricsConfig.value.enabled) || {}) } };
  downloadText("metrics.json", JSON.stringify(payload, null, 2), "application/json");
  statusText.value = `已导出 metrics.json（放到 work/${pid}/meta/metrics.json）`;
}

function saveMetricsConfig() {
  const pid = String(selectedProjectId.value || "").trim() || "example";
  const payload = { enabled: { ...defaultEnabledMap(), ...((metricsConfig.value && metricsConfig.value.enabled) || {}) } };
  try {
    window.localStorage.setItem(`prjmx.metricsConfig.${pid}`, JSON.stringify(payload));
    statusText.value = "已保存（本地）";
  } catch {
    statusText.value = "保存失败";
  }
}

function loadMetricsConfigFromStorage() {
  const pid = String(selectedProjectId.value || "").trim() || "example";
  try {
    const raw = window.localStorage.getItem(`prjmx.metricsConfig.${pid}`);
    if (!raw) return false;
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object") return false;
    if (!parsed.enabled || typeof parsed.enabled !== "object") return false;
    metricsConfig.value = { enabled: { ...defaultEnabledMap(), ...parsed.enabled } };
    return true;
  } catch {
    return false;
  }
}

function resetToDefault() {
  const pid = String(selectedProjectId.value || "").trim() || "example";
  resetMetricsConfig();
  try {
    window.localStorage.removeItem(`prjmx.metricsConfig.${pid}`);
  } catch {}
  statusText.value = "已重置为默认";
}

    watch(selectedProjectId, () => {
      if (!loadMetricsConfigFromStorage()) resetMetricsConfig();
    });
    loadProjects().then(() => {
      if (!loadMetricsConfigFromStorage()) resetMetricsConfig();
    });

    return {
      statusText,
      projects,
      selectedProjectId,
      matrix,
      METRIC_LABELS,
      metricChecked,
      setMetricChecked,
      setAllEnabled,
      saveMetricsConfig,
      resetToDefault,
      exportMetricsJson,
      helpOf
    };
  }
};
</script>
