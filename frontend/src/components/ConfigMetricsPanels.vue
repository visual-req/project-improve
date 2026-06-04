<template>
  <a-space direction="vertical" style="width: 100%" :size="12">
    <a-space wrap align="center">
      <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">{{ t("common.project") }}</span>
      <a-select v-model:value="selectedProjectId" style="min-width: 320px">
        <a-select-option v-for="(p, idx) in projects" :key="String(p.id) + ':' + String(idx)" :value="String(p.id)">
          {{ String(p.id) }} · {{ String(p.name || "") }}
        </a-select-option>
      </a-select>
      <a-button type="default" @click="setAllEnabled(true)">{{ t("configMetrics.action.selectAll") }}</a-button>
      <a-button type="default" @click="setAllEnabled(false)">{{ t("configMetrics.action.selectNone") }}</a-button>
      <a-button type="primary" @click="saveMetricsConfig">{{ t("common.save") }}</a-button>
      <a-button type="default" @click="exportMetricsJson">{{ t("common.export") }}</a-button>
      <a-button type="default" @click="resetToDefault">{{ t("common.reset") }}</a-button>
      <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">{{ statusText }}</span>
    </a-space>

    <a-collapse>
      <a-collapse-panel v-for="group in matrix" :key="group.type" :header="group.label">
        <a-row :gutter="[12, 12]">
          <a-col v-for="p in group.phases" :key="p.phase" :xs="24" :md="12" :lg="6">
            <a-card size="small" :title="p.label" style="height: 100%">
              <a-space direction="vertical" style="width: 100%" :size="6">
                <div v-for="it in p.items" :key="it.key" style="display: flex; align-items: flex-start; justify-content: space-between; gap: 8px">
                  <a-checkbox :checked="metricChecked(it.key)" @change="(e) => setMetricChecked(it.key, e && e.target ? e.target.checked : false)">
                    {{ metricLabel(it.key) }}
                  </a-checkbox>
                  <a-popover trigger="click" placement="right">
                    <template #content>
                      <div style="max-width: 360px">
                        <div style="font-weight: 600; margin-bottom: 8px">{{ metricLabel(it.key) }}</div>
                        <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px; margin-bottom: 4px">{{ t("configMetrics.help.meaningTitle") }}</div>
                        <div style="margin-bottom: 8px">{{ helpOf(it.key).meaning }}</div>
                        <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px; margin-bottom: 4px">{{ t("configMetrics.help.methodTitle") }}</div>
                        <div style="margin-bottom: 8px">{{ helpOf(it.key).method }}</div>
                        <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px; margin-bottom: 4px">{{ t("configMetrics.help.formulaTitle") }}</div>
                        <div style="margin-bottom: 8px">{{ helpOf(it.key).formula }}</div>
                        <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px; margin-bottom: 4px">{{ t("configMetrics.help.referenceTitle") }}</div>
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
import { useI18n } from "../i18n.js";

export default {
  setup() {
    const { t, locale } = useI18n();
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
  { key: "throughput", type: "flow", phase: "plan" },
  { key: "wip_avg", type: "flow", phase: "plan" },
  { key: "aging_wip", type: "flow", phase: "plan" },
  { key: "lead_time_p50", type: "flow", phase: "plan" },
  { key: "lead_time_p75", type: "flow", phase: "plan" },
  { key: "lead_time_p95", type: "flow", phase: "plan" },
  { key: "cycle_time_p50", type: "flow", phase: "dev" },
  { key: "cycle_time_p75", type: "flow", phase: "dev" },
  { key: "cycle_time_p95", type: "flow", phase: "dev" },
  { key: "review_latency_p50", type: "engineering", phase: "dev" },
  { key: "review_latency_p75", type: "engineering", phase: "dev" },
  { key: "review_latency_p95", type: "engineering", phase: "dev" },
  { key: "pr_lead_time_p50", type: "engineering", phase: "dev" },
  { key: "pr_lead_time_p75", type: "engineering", phase: "dev" },
  { key: "pr_lead_time_p95", type: "engineering", phase: "dev" },
  { key: "change_size", type: "engineering", phase: "dev" },
  { key: "deployment_frequency", type: "flow", phase: "test" },
  { key: "delivery_batch_size", type: "flow", phase: "test" },
  { key: "delivery_cycle_time_p50", type: "flow", phase: "test" },
  { key: "delivery_cycle_time_p75", type: "flow", phase: "test" },
  { key: "delivery_cycle_time_p95", type: "flow", phase: "test" },
  { key: "mttr", type: "flow", phase: "run" },
  { key: "change_failure_rate", type: "flow", phase: "run" },
  { key: "commitment_reliability", type: "plan", phase: "plan" },
  { key: "scope_change", type: "plan", phase: "plan" },
  { key: "iteration_throughput", type: "plan", phase: "plan" },
  { key: "iteration_completion_rate", type: "plan", phase: "plan" },
  { key: "carryover_rate", type: "plan", phase: "plan" },
  { key: "wip_limit_adherence", type: "plan", phase: "dev" },
  { key: "blocked_ratio", type: "plan", phase: "dev" },
  { key: "ontime_delivery_rate", type: "plan", phase: "test" },
  { key: "rework_ratio", type: "plan", phase: "test" },
  { key: "requirement_change_rate", type: "plan", phase: "test" },
  { key: "online_commitment_deviation", type: "plan", phase: "run" },
  { key: "sla", type: "plan", phase: "run" },
  { key: "requirement_defects", type: "quality", phase: "plan" },
  { key: "code_defects", type: "quality", phase: "dev" },
  { key: "automated_test_coverage", type: "quality", phase: "test" },
  { key: "bug_rate", type: "quality", phase: "plan" },
  { key: "reopen_rate", type: "quality", phase: "test" },
  { key: "review_defects", type: "quality", phase: "dev" },
  { key: "test_blockers", type: "quality", phase: "dev" },
  { key: "regression_defects", type: "quality", phase: "test" },
  { key: "system_integration_test_defects", type: "quality", phase: "test" },
  { key: "acceptance_test_defects", type: "quality", phase: "test" },
  { key: "acceptance_fail_rate", type: "quality", phase: "test" },
  { key: "escaped_defects", type: "quality", phase: "run" },
  { key: "escaped_defect_rate", type: "quality", phase: "run" },
  { key: "prod_defect_severity", type: "quality", phase: "run" },
  { key: "commit_frequency", type: "engineering", phase: "plan" },
  { key: "pr_issue_link_rate", type: "engineering", phase: "plan" },
  { key: "ci_integration_frequency", type: "engineering", phase: "test" },
  { key: "ci_success_rate", type: "engineering", phase: "test" },
  { key: "code_scan_pass_rate", type: "engineering", phase: "test" },
  { key: "ci_duration_p50", type: "engineering", phase: "test" },
  { key: "oncall_load", type: "engineering", phase: "run" },
  { key: "hotfix_ratio", type: "engineering", phase: "run" }
];

const METRIC_KEYS = Array.from(new Set(METRIC_CATALOG.map((x) => x.key)));
const METRIC_LABELS_ZH = {
  throughput: "吞吐量",
  wip_avg: "平均在制（WIP）",
  aging_wip: "老化在制（Aging WIP）",
  lead_time_p50: "交付周期 p50",
  lead_time_p75: "交付周期 p75",
  lead_time_p95: "交付周期 p95",
  cycle_time_p50: "处理周期 p50",
  cycle_time_p75: "处理周期 p75",
  cycle_time_p95: "处理周期 p95",
  review_latency_p50: "评审等待 p50",
  review_latency_p75: "评审等待 p75",
  review_latency_p95: "评审等待 p95",
  pr_lead_time_p50: "PR 周期 p50",
  pr_lead_time_p75: "PR 周期 p75",
  pr_lead_time_p95: "PR 周期 p95",
  change_size: "变更规模",
  deployment_frequency: "发布频率",
  delivery_batch_size: "交付批量",
  delivery_cycle_time_p50: "交付周期（测试/交付）p50",
  delivery_cycle_time_p75: "交付周期（测试/交付）p75",
  delivery_cycle_time_p95: "交付周期（测试/交付）p95",
  mttr: "平均恢复时间（MTTR）",
  change_failure_rate: "变更失败率",
  commitment_reliability: "承诺达成率",
  scope_change: "范围变更",
  iteration_throughput: "迭代吞吐率",
  iteration_completion_rate: "迭代完成率",
  carryover_rate: "迭代结转率",
  wip_limit_adherence: "WIP 上限执行率",
  blocked_ratio: "阻塞占比",
  ontime_delivery_rate: "按期交付率",
  rework_ratio: "返工比例",
  requirement_change_rate: "需求变更率",
  online_commitment_deviation: "线上承诺偏差",
  sla: "SLA 达成情况",
  requirement_defects: "需求缺陷情况",
  code_defects: "代码缺陷情况",
  automated_test_coverage: "自动化测试覆盖率",
  bug_rate: "缺陷率（Bug Rate）",
  reopen_rate: "重开率",
  review_defects: "评审缺陷",
  test_blockers: "测试阻塞",
  regression_defects: "回归缺陷",
  system_integration_test_defects: "系统集成测试缺陷分析",
  acceptance_test_defects: "验收测试缺陷分析",
  acceptance_fail_rate: "验收失败率",
  escaped_defects: "缺陷逃逸数量",
  escaped_defect_rate: "缺陷逃逸率",
  prod_defect_severity: "生产缺陷严重度",
  commit_frequency: "提交频率",
  pr_issue_link_rate: "PR ↔ 需求关联率",
  ci_integration_frequency: "持续集成频率",
  ci_success_rate: "CI 成功率",
  code_scan_pass_rate: "代码扫描通过率",
  ci_duration_p50: "CI 耗时 p50",
  oncall_load: "值班负载",
  hotfix_ratio: "紧急修复占比"
};

const METRIC_LABELS_JA = {
  throughput: "スループット",
  wip_avg: "平均WIP",
  aging_wip: "老化WIP（Aging WIP）",
  lead_time_p50: "リードタイム p50",
  lead_time_p75: "リードタイム p75",
  lead_time_p95: "リードタイム p95",
  cycle_time_p50: "サイクルタイム p50",
  cycle_time_p75: "サイクルタイム p75",
  cycle_time_p95: "サイクルタイム p95",
  review_latency_p50: "レビュー待ち p50",
  review_latency_p75: "レビュー待ち p75",
  review_latency_p95: "レビュー待ち p95",
  pr_lead_time_p50: "PRサイクル p50",
  pr_lead_time_p75: "PRサイクル p75",
  pr_lead_time_p95: "PRサイクル p95",
  change_size: "変更規模",
  deployment_frequency: "デプロイ頻度",
  delivery_batch_size: "配信バッチサイズ",
  delivery_cycle_time_p50: "配信サイクル（テスト/配信）p50",
  delivery_cycle_time_p75: "配信サイクル（テスト/配信）p75",
  delivery_cycle_time_p95: "配信サイクル（テスト/配信）p95",
  mttr: "MTTR",
  change_failure_rate: "変更失敗率",
  commitment_reliability: "コミット達成率",
  scope_change: "スコープ変更",
  iteration_throughput: "イテレーションスループット",
  iteration_completion_rate: "イテレーション完了率",
  carryover_rate: "持ち越し率",
  wip_limit_adherence: "WIP上限遵守率",
  blocked_ratio: "ブロック比率",
  ontime_delivery_rate: "期日通り配信率",
  rework_ratio: "手戻り比率",
  requirement_change_rate: "要件変更率",
  online_commitment_deviation: "本番コミット偏差",
  sla: "SLA達成",
  requirement_defects: "要件欠陥",
  code_defects: "コード欠陥",
  automated_test_coverage: "自動テストカバレッジ",
  bug_rate: "欠陥率（Bug Rate）",
  reopen_rate: "再オープン率",
  review_defects: "レビュー欠陥",
  test_blockers: "テストブロッカー",
  regression_defects: "回帰欠陥",
  system_integration_test_defects: "SIT欠陥分析",
  acceptance_test_defects: "UAT欠陥分析",
  acceptance_fail_rate: "受入失敗率",
  escaped_defects: "逃逸欠陥数",
  escaped_defect_rate: "逃逸欠陥率",
  prod_defect_severity: "本番欠陥重大度",
  commit_frequency: "コミット頻度",
  pr_issue_link_rate: "PR↔課題関連率",
  ci_integration_frequency: "CI統合頻度",
  ci_success_rate: "CI成功率",
  code_scan_pass_rate: "コードスキャン通過率",
  ci_duration_p50: "CI所要時間 p50",
  oncall_load: "オンコール負荷",
  hotfix_ratio: "緊急修正比率"
};

const METRIC_LABELS_EN = {
  throughput: "Throughput",
  wip_avg: "Avg WIP",
  aging_wip: "Aging WIP",
  lead_time_p50: "Lead Time p50",
  lead_time_p75: "Lead Time p75",
  lead_time_p95: "Lead Time p95",
  cycle_time_p50: "Cycle Time p50",
  cycle_time_p75: "Cycle Time p75",
  cycle_time_p95: "Cycle Time p95",
  review_latency_p50: "Review Latency p50",
  review_latency_p75: "Review Latency p75",
  review_latency_p95: "Review Latency p95",
  pr_lead_time_p50: "PR Lead Time p50",
  pr_lead_time_p75: "PR Lead Time p75",
  pr_lead_time_p95: "PR Lead Time p95",
  change_size: "Change Size",
  deployment_frequency: "Deployment Frequency",
  delivery_batch_size: "Delivery Batch Size",
  delivery_cycle_time_p50: "Delivery Cycle Time (Test/Delivery) p50",
  delivery_cycle_time_p75: "Delivery Cycle Time (Test/Delivery) p75",
  delivery_cycle_time_p95: "Delivery Cycle Time (Test/Delivery) p95",
  mttr: "MTTR",
  change_failure_rate: "Change Failure Rate",
  commitment_reliability: "Commitment Reliability",
  scope_change: "Scope Change",
  iteration_throughput: "Iteration Throughput",
  iteration_completion_rate: "Iteration Completion Rate",
  carryover_rate: "Carryover Rate",
  wip_limit_adherence: "WIP Limit Adherence",
  blocked_ratio: "Blocked Ratio",
  ontime_delivery_rate: "On-time Delivery Rate",
  rework_ratio: "Rework Ratio",
  requirement_change_rate: "Requirement Change Rate",
  online_commitment_deviation: "Online Commitment Deviation",
  sla: "SLA Achievement",
  requirement_defects: "Requirement Defects",
  code_defects: "Code Defects",
  automated_test_coverage: "Automated Test Coverage",
  bug_rate: "Bug Rate",
  reopen_rate: "Reopen Rate",
  review_defects: "Review Defects",
  test_blockers: "Test Blockers",
  regression_defects: "Regression Defects",
  system_integration_test_defects: "SIT Defects Analysis",
  acceptance_test_defects: "UAT Defects Analysis",
  acceptance_fail_rate: "Acceptance Fail Rate",
  escaped_defects: "Escaped Defects",
  escaped_defect_rate: "Escaped Defect Rate",
  prod_defect_severity: "Prod Defect Severity",
  commit_frequency: "Commit Frequency",
  pr_issue_link_rate: "PR ↔ Issue Link Rate",
  ci_integration_frequency: "CI Integration Frequency",
  ci_success_rate: "CI Success Rate",
  code_scan_pass_rate: "Code Scan Pass Rate",
  ci_duration_p50: "CI Duration p50",
  oncall_load: "On-call Load",
  hotfix_ratio: "Hotfix Ratio"
};

function currentLocale() {
  const v = locale && locale.value ? String(locale.value) : "zh-CN";
  return v === "ja-JP" || v === "en-US" || v === "zh-CN" ? v : "zh-CN";
}

function metricLabel(key) {
  const k = String(key || "");
  const lc = currentLocale();
  if (lc === "ja-JP") return METRIC_LABELS_JA[k] || METRIC_LABELS_ZH[k] || k;
  if (lc === "en-US") return METRIC_LABELS_EN[k] || METRIC_LABELS_ZH[k] || k;
  return METRIC_LABELS_ZH[k] || k;
}

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
  const label = metricLabel(k);
  const lc = currentLocale();
  if (lc === "en-US") {
    return (
      {
        throughput: {
          meaning: "Number of completed items in the window.",
          method: "Use metrics.throughput.count.",
          formula: "Throughput = count(completed items).",
          reference: "Focus on trend."
        },
        wip_avg: {
          meaning: "Average work-in-progress in the window.",
          method: "Count items in WIP statuses over time and average.",
          formula: "Avg WIP = time-average(WIP count).",
          reference: "Use WIP limit as a reference."
        },
        lead_time_p50: {
          meaning: "Median lead time from created to done.",
          method: "Compute created→done duration distribution and take p50.",
          formula: "Lead time = done_at - created_at.",
          reference: "Compare with team expectation/commitment."
        },
        cycle_time_p50: {
          meaning: "Median cycle time from started to done.",
          method: "Compute in_progress→done duration distribution and take p50.",
          formula: "Cycle time = done_at - in_progress_at.",
          reference: "Interpret with WIP and review latency."
        },
        bug_rate: {
          meaning: "Share of bug completions in the window.",
          method: "Count completed bugs and total completions.",
          formula: "Bug rate = BugsDone / AllDone.",
          reference: "Interpret with change size and rework."
        },
        escaped_defects: {
          meaning: "Number of escaped (production) defects.",
          method: "Identify production defects via bug_source rules.",
          formula: "Escaped defects = count(prod defects).",
          reference: "Track severity and trend."
        },
        automated_test_coverage: {
          meaning: "Automated test coverage level.",
          method: "Fetch coverage from test platform/CI.",
          formula: "Coverage = covered / total.",
          reference: "Assess together with regression cost."
        },
        system_integration_test_defects: {
          meaning: "Defects exposed in system integration test (distribution, not just count).",
          method: "Group SIT defects by module/type/cause/ownership and analyze patterns.",
          formula: "Break down into: count, ratio, top causes/modules.",
          reference: "Helps locate integration, environment parity, missing contract tests, cross-team interface issues."
        },
        acceptance_test_defects: {
          meaning: "Defects exposed in acceptance/UAT (distribution, not just count).",
          method: "Group UAT defects by cause, link with requirement changes and acceptance criteria.",
          formula: "Break down into: count, ratio, top acceptance failure reasons.",
          reference: "Helps locate unclear criteria, insufficient clarification, regression gaps, data/permission/environment differences."
        }
      }[k] || {
        meaning: `Metric: ${label}. Used to locate bottlenecks in flow/quality/engineering.`,
        method: "Aggregate from PM / Git / CI / bug systems based on your team definition.",
        formula: "Depends on definition; start with trends and refine later.",
        reference: "Focus on trend and breakpoints; connect with evidence (board/PR/CI)."
      }
    );
  }
  if (lc === "ja-JP") {
    return (
      {
        throughput: {
          meaning: "期間内に完了した作業項目数。",
          method: "metrics.throughput.count を利用。",
          formula: "スループット = 完了件数。",
          reference: "傾向を見る。"
        },
        wip_avg: {
          meaning: "期間内の平均WIP。",
          method: "WIPステータスの件数を時系列で平均化。",
          formula: "平均WIP = WIP件数の時間平均。",
          reference: "WIP上限を参考にする。"
        },
        lead_time_p50: {
          meaning: "作成→完了のリードタイム中央値。",
          method: "created→done の分布から p50 を取る。",
          formula: "Lead time = done_at - created_at。",
          reference: "チームの期待/コミットと比較。"
        },
        cycle_time_p50: {
          meaning: "着手→完了のサイクルタイム中央値。",
          method: "in_progress→done の分布から p50 を取る。",
          formula: "Cycle time = done_at - in_progress_at。",
          reference: "WIP/レビュー待ちと合わせて解釈。"
        },
        bug_rate: {
          meaning: "期間内のBug完了比率。",
          method: "Bug完了数と総完了数を集計。",
          formula: "Bug rate = BugsDone / AllDone。",
          reference: "変更規模や手戻りと合わせて見る。"
        },
        escaped_defects: {
          meaning: "本番逃逸欠陥数。",
          method: "bug_source のルールで本番欠陥を識別。",
          formula: "Escaped defects = count(prod defects)。",
          reference: "重大度と傾向を追う。"
        },
        automated_test_coverage: {
          meaning: "自動テストカバレッジ。",
          method: "テスト基盤/CIから取得。",
          formula: "Coverage = covered / total。",
          reference: "回帰コストと合わせて評価。"
        },
        system_integration_test_defects: {
          meaning: "SITで検出された欠陥の分布（件数だけでなく原因/偏り）。",
          method: "SIT欠陥をモジュール/種類/原因で分類しパターン分析。",
          formula: "件数・比率・Top原因/モジュールの内訳。",
          reference: "統合、環境差、契約テスト不足、クロスチームIFの課題を特定。"
        },
        acceptance_test_defects: {
          meaning: "UAT/受入で検出された欠陥の分布（件数だけでなく原因/偏り）。",
          method: "受入欠陥を原因で分類し、要件変更/受入基準/回帰網羅と連動分析。",
          formula: "件数・比率・受入失敗理由Topの内訳。",
          reference: "基準不明確、要件明確化不足、回帰不足、データ/権限/環境差を特定。"
        }
      }[k] || {
        meaning: `指標：${label}。フロー/品質/開発効率のボトルネック特定に使います。`,
        method: "PM/Git/CI/欠陥システムから、チーム定義に従って集計します。",
        formula: "定義に依存。まずは傾向から始め、必要に応じて詳細化。",
        reference: "傾向と変化点を重視し、ボード/PR/CIなどの証拠と合わせて解釈。"
      }
    );
  }
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
  const types = ["flow", "plan", "quality", "engineering"].map((tp) => ({ type: tp, label: t(`configMetrics.type.${tp}`) }));
  const phases = ["plan", "dev", "test", "run"].map((ph) => ({ phase: ph, label: t(`configMetrics.phase.${ph}`) }));
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
  statusText.value = t("configMetrics.status.exported", { pid });
}

function saveMetricsConfig() {
  const pid = String(selectedProjectId.value || "").trim() || "example";
  const payload = { enabled: { ...defaultEnabledMap(), ...((metricsConfig.value && metricsConfig.value.enabled) || {}) } };
  try {
    window.localStorage.setItem(`prjmx.metricsConfig.${pid}`, JSON.stringify(payload));
    statusText.value = t("configMetrics.status.savedLocal");
  } catch {
    statusText.value = t("configMetrics.status.saveFailed");
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
  statusText.value = t("configMetrics.status.resetDefault");
}

    watch(selectedProjectId, () => {
      if (!loadMetricsConfigFromStorage()) resetMetricsConfig();
    });
    loadProjects().then(() => {
      if (!loadMetricsConfigFromStorage()) resetMetricsConfig();
    });

    return {
      t,
      statusText,
      projects,
      selectedProjectId,
      matrix,
      metricLabel,
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
