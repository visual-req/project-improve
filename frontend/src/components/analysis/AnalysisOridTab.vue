<template>
  <a-space direction="vertical" style="width: 100%" :size="12">
    <a-button type="primary" @click="requestRunSkill('orid')">{{ t("analysis.run.orid") }}</a-button>
    <a-alert v-if="oridError" type="warning" show-icon :message="oridError" />
    <a-card size="small" :title="t('analysis.files')">
      <ul style="margin: 0; padding-left: 18px">
        <li>{{ t("analysis.orid.files.inputWorkspace") }}</li>
        <li>{{ t("analysis.orid.files.inputMetrics") }}</li>
        <li>{{ t("analysis.orid.files.outputReport") }}</li>
      </ul>
    </a-card>

    <a-card size="small" :title="t('analysis.orid.signalsTitle')">
      <a-space direction="vertical" style="width: 100%" :size="10">
        <div>
          <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px; margin-bottom: 6px">{{ t("analysis.orid.signalSectionTitle") }}</div>
          <a-space wrap>
            <a-tag v-for="tag in signalTags" :key="tag.key" :color="tag.color">{{ tag.text }}</a-tag>
          </a-space>
        </div>

        <div>
          <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px; margin-bottom: 6px">{{ t("analysis.orid.metricInterpretTitle") }}</div>
          <div v-if="metricInterpretRows.length === 0" style="color: rgba(0, 0, 0, 0.45); font-size: 12px">{{ t("common.none") }}</div>
          <a-table
            v-else
            :columns="metricInterpretColumns"
            :data-source="metricInterpretRows"
            size="small"
            :pagination="{ pageSize: 6 }"
            :scroll="{ x: 900 }"
          />
        </div>
      </a-space>
    </a-card>
    <div v-if="!reportData" style="color: rgba(0, 0, 0, 0.65)">{{ t("analysis.noReportYet") }}</div>
    <a-alert v-else type="success" show-icon :message="t('analysis.reportReady')" />

    <a-card v-if="reportData" size="small" :title="t('analysis.orid.linksTitle')">
      <div v-if="linkRows.length === 0" style="color: rgba(0, 0, 0, 0.45); font-size: 12px">{{ t("common.none") }}</div>
      <a-table v-else :columns="linkColumns" :data-source="linkRows" size="small" :pagination="{ pageSize: 6 }" :scroll="{ x: 900 }">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'metrics'">
            <a-space wrap>
              <a-tag v-for="m in record.metrics" :key="m.key" color="blue">{{ m.label }}：{{ m.value }}</a-tag>
            </a-space>
          </template>
        </template>
      </a-table>
    </a-card>

    <a-card v-if="reportData" size="small" :title="t('analysis.actionCandidates')">
      <a-space wrap align="center" style="margin-bottom: 10px">
        <a-button type="primary" :disabled="selectedKeys.length === 0" @click="addSelectedActionsToPlan">{{ t("analysis.orid.addSelectedToPlan") }}</a-button>
        <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">{{ t("analysis.orid.addSelectedHint") }}</span>
      </a-space>
      <div v-if="actionCandidates.length === 0" style="color: rgba(0, 0, 0, 0.65)">{{ t("common.none") }}</div>
      <a-table
        v-else
        :row-selection="rowSelection"
        :columns="columns"
        :data-source="actionCandidates"
        size="small"
        :pagination="{ pageSize: 6 }"
        :scroll="{ x: 1650 }"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-button type="link" size="small" @click="openDetail(record)">{{ t("common.detail") }}</a-button>
          </template>
        </template>
      </a-table>
    </a-card>

    <a-drawer v-model:visible="detailVisible" :title="t('plan.item.detail')" width="560">
      <div v-if="!detailRecord" style="color: rgba(0, 0, 0, 0.45)">{{ t("common.none") }}</div>
      <a-space v-else direction="vertical" style="width: 100%" :size="12">
        <a-card size="small" :title="t('analysis.orid.section.overview')">
          <a-space wrap>
            <a-tag color="blue">{{ detailRecord.id || t("common.none") }}</a-tag>
            <a-tag :color="statusColor(detailRecord.status)">{{ statusText(detailRecord.status) }}</a-tag>
            <a-tag :color="severityColor(detailRecord.severity)">{{ t("analysis.orid.tag.severity", { v: severityText(detailRecord.severity) }) }}</a-tag>
            <a-tag color="default">{{ t("analysis.orid.tag.owner", { v: detailRecord.owner_role || t('common.none') }) }}</a-tag>
            <a-tag v-if="detailAlreadyAdded" color="green">{{ t("analysis.addedToPlan") }}</a-tag>
          </a-space>
          <a-descriptions size="small" :column="2" bordered style="margin-top: 10px">
            <a-descriptions-item :label="t('analysis.orid.field.discoveredAt')">{{ detailRecord.discovered_at || t("common.none") }}</a-descriptions-item>
            <a-descriptions-item :label="t('analysis.orid.field.startDate')">{{ detailRecord.start_date || t("common.none") }}</a-descriptions-item>
            <a-descriptions-item :label="t('analysis.orid.field.dueDate')">{{ detailRecord.due_date || t("common.none") }}</a-descriptions-item>
            <a-descriptions-item :label="t('analysis.orid.field.completedDate')">{{ detailRecord.completed_date || t("common.none") }}</a-descriptions-item>
          </a-descriptions>
        </a-card>

        <a-card size="small" :title="t('analysis.orid.section.problemCause')">
          <a-space direction="vertical" style="width: 100%" :size="8">
            <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px">{{ t("analysis.orid.field.problem") }}</div>
            <div style="white-space: pre-wrap">{{ detailRecord.problem || t("common.none") }}</div>
            <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px">{{ t("analysis.orid.field.cause") }}</div>
            <div style="white-space: pre-wrap">{{ detailRecord.cause || t("common.none") }}</div>
          </a-space>
        </a-card>

        <a-card size="small" :title="t('analysis.orid.section.solution')">
          <a-space direction="vertical" style="width: 100%" :size="8">
            <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px">{{ t("analysis.orid.field.solution") }}</div>
            <div style="white-space: pre-wrap">{{ detailRecord.solution || t("common.none") }}</div>
            <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px">{{ t("analysis.orid.field.expectedEffect") }}</div>
            <div style="white-space: pre-wrap">{{ detailRecord.expected_effect || t("common.none") }}</div>
            <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px">{{ t("analysis.orid.field.acceptanceMethod") }}</div>
            <div style="white-space: pre-wrap">{{ detailRecord.acceptance_method || t("common.none") }}</div>
          </a-space>
        </a-card>

        <a-card size="small" :title="t('analysis.orid.section.evidence')">
          <div v-if="detailLinks.length === 0" style="color: rgba(0, 0, 0, 0.45); font-size: 12px">{{ t("common.none") }}</div>
          <a-space v-else direction="vertical" style="width: 100%" :size="8">
            <a-table :columns="detailLinkColumns" :data-source="detailLinks" size="small" :pagination="false" :scroll="{ x: 900 }" />
            <a-space wrap>
              <a-tag v-for="tag in signalTags" :key="`d_${tag.key}`" :color="tag.color">{{ tag.text }}</a-tag>
            </a-space>
            <div v-if="oridHints.length" style="color: rgba(0, 0, 0, 0.65); font-size: 12px">
              {{ t("analysis.orid.oridHints", { items: oridHints.join('；') }) }}
            </div>
          </a-space>
        </a-card>
      </a-space>

      <template #footer>
        <a-space direction="vertical" style="width: 100%" :size="8">
          <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px">
            {{ t("analysis.addToPlanHelp") }}
          </div>
          <a-space style="width: 100%" align="center" :size="10">
            <a-button type="default" @click="detailVisible = false">{{ t("common.close") }}</a-button>
            <a-button type="primary" :disabled="detailAlreadyAdded" @click="addDetailToPlan">{{ t("analysis.addToPlan") }}</a-button>
            <span v-if="detailAlreadyAdded" style="color: rgba(0, 0, 0, 0.45); font-size: 12px">{{ t("analysis.addedToPlanHint") }}</span>
          </a-space>
        </a-space>
      </template>
    </a-drawer>
  </a-space>
</template>

<script>
import { computed, ref } from "vue";
import { message } from "ant-design-vue";
import { useI18n } from "../../i18n.js";

export default {
  props: {
    selectedProjectIdModel: { type: String, default: "" },
    requestRunSkill: { type: Function, default: null },
    oridError: { type: String, default: "" },
    reportData: { type: [Object, null], default: null },
    metricsData: { type: [Object, null], default: null },
    enabledMetricKeys: { type: Array, default: () => [] },
    collectViz: { type: [Object, null], default: null }
  },
  setup(props) {
    const { t } = useI18n();
    function safeParse(text) {
      try {
        const v = JSON.parse(String(text || ""));
        return v && typeof v === "object" ? v : null;
      } catch {
        return null;
      }
    }

    function nowIso() {
      try {
        return new Date().toISOString();
      } catch {
        return String(Date.now());
      }
    }

    function makeKey() {
      return `${Date.now()}_${Math.random().toString(16).slice(2)}`;
    }

    const columns = computed(() => [
      { title: t("analysis.orid.table.id"), dataIndex: "id", key: "id", width: 90 },
      { title: t("analysis.orid.table.problem"), dataIndex: "problem", key: "problem", width: 260 },
      { title: t("analysis.orid.table.cause"), dataIndex: "cause", key: "cause", width: 240 },
      { title: t("analysis.orid.table.solution"), dataIndex: "solution", key: "solution", width: 260 },
      { title: t("analysis.orid.table.expectedEffect"), dataIndex: "expected_effect", key: "expected_effect", width: 260 },
      { title: t("analysis.orid.table.acceptanceMethod"), dataIndex: "acceptance_method", key: "acceptance_method", width: 260 },
      { title: t("analysis.orid.table.dueDate"), dataIndex: "due_date", key: "due_date", width: 120 },
      { title: t("analysis.orid.table.owner"), dataIndex: "owner_role", key: "owner_role", width: 140 },
      { title: t("analysis.orid.table.action"), key: "action", fixed: "right", width: 90 }
    ]);

    const actionCandidates = computed(() => {
      const raw = props.reportData && Array.isArray(props.reportData.actions) ? props.reportData.actions : [];
      return raw.map((a, index) => {
        const id = a && (a.id || a.no) ? String(a.id || a.no) : String(index + 1);
        return {
          key: `cand_${id}_${index}`,
          id,
          problem: a && (a.problem || a.issue || a.question) ? String(a.problem || a.issue || a.question) : t("common.none"),
          cause: a && (a.cause || a.root_cause || a.reason) ? String(a.cause || a.root_cause || a.reason) : t("common.none"),
          solution: a && (a.solution || a.title || a.action) ? String(a.solution || a.title || a.action) : t("common.none"),
          due_date: a && (a.due_date || a.due) ? String(a.due_date || a.due) : "",
          expected_effect: a && (a.expected_effect || a.expected) ? String(a.expected_effect || a.expected) : "",
          acceptance_method: a && (a.acceptance_method || a.acceptance_criteria || a.dod) ? String(a.acceptance_method || a.acceptance_criteria || a.dod) : "",
          owner_role: a && (a.owner_role || a.owner) ? String(a.owner_role || a.owner) : "",
          status: a && (a.status || a.state) ? String(a.status || a.state) : "not_started",
          severity: a && (a.severity || a.priority) ? String(a.severity || a.priority) : "medium",
          discovered_at: a && (a.discovered_at || a.discoveredAt || a.created_at || a.createdAt) ? String(a.discovered_at || a.discoveredAt || a.created_at || a.createdAt) : "",
          start_date: a && (a.start_date || a.startAt) ? String(a.start_date || a.startAt) : "",
          completed_date: a && (a.completed_date || a.completedAt) ? String(a.completed_date || a.completedAt) : ""
        };
      });
    });

    const metricsForEvidence = computed(() => {
      if (props.metricsData && typeof props.metricsData === "object") return props.metricsData;
      if (props.reportData && props.reportData.metrics && typeof props.reportData.metrics === "object") return props.reportData.metrics;
      return null;
    });

    const signalTags = computed(() => {
      const v = props.collectViz && typeof props.collectViz === "object" ? props.collectViz : null;
      const tags = [];
      const swim = v && v.swimlane && typeof v.swimlane === "object" ? v.swimlane : null;
      const burndown = v && v.burndown && typeof v.burndown === "object" ? v.burndown : null;
      const gantt = v && v.gantt && typeof v.gantt === "object" ? v.gantt : null;
      const blocked = swim && typeof swim.blocked_count === "number" ? swim.blocked_count : null;
      const th = swim && typeof swim.threshold_days === "number" ? swim.threshold_days : null;
      const verdict = burndown && burndown.verdict ? String(burndown.verdict) : "";
      const delayed = gantt && typeof gantt.delayed_count === "number" ? gantt.delayed_count : null;
      const risky = gantt && typeof gantt.risky_count === "number" ? gantt.risky_count : null;
      const verdictLabel = verdict === "ahead" || verdict === "ok" || verdict === "slow" ? t(`analysis.collect.burndown.verdict.${verdict}`) : verdict || t("common.none");
      const swimThresholdPart = th ? t("analysis.orid.signal.swimlaneThreshold", { days: th }) : "";
      tags.push({
        key: "swimlane",
        text: t("analysis.orid.signal.swimlane", { count: blocked === null ? t("common.none") : blocked, threshold: swimThresholdPart }),
        color: blocked && blocked > 0 ? "red" : "default"
      });
      tags.push({ key: "burndown", text: t("analysis.orid.signal.burndown", { verdict: verdictLabel }), color: verdict === "slow" ? "gold" : "default" });
      tags.push({
        key: "gantt",
        text: t("analysis.orid.signal.gantt", { delayed: delayed === null ? t("common.none") : delayed, risky: risky === null ? t("common.none") : risky }),
        color: (delayed && delayed > 0) || (risky && risky > 0) ? "gold" : "default"
      });
      return tags;
    });

    function pickMetricsSnapshot(metrics, key) {
      const m = metrics && typeof metrics === "object" ? metrics : {};
      const targets = m.targets && typeof m.targets === "object" ? m.targets : {};
      if (key === "lead_time_p50")
        return {
          value: m.lead_time_days && m.lead_time_days.p50 !== undefined ? t("unit.days", { n: m.lead_time_days.p50 }) : t("common.none"),
          target: t0(targets.lead_time_p50_days)
        };
      if (key === "cycle_time_p50")
        return {
          value: m.cycle_time_days && m.cycle_time_days.p50 !== undefined ? t("unit.days", { n: m.cycle_time_days.p50 }) : t("common.none"),
          target: t0(targets.cycle_time_p50_days)
        };
      if (key === "wip_avg") return { value: m.wip && m.wip.avg !== undefined ? String(m.wip.avg) : t("common.none"), target: t0(targets.wip_limit) };
      if (key === "pr_lead_time_p50")
        return {
          value: m.pr_lead_time_days && m.pr_lead_time_days.p50 !== undefined ? t("unit.days", { n: m.pr_lead_time_days.p50 }) : t("common.none"),
          target: t0(targets.pr_lead_time_p50_days)
        };
      if (key === "review_latency_p50")
        return {
          value: m.review_latency_days && m.review_latency_days.p50 !== undefined ? t("unit.days", { n: m.review_latency_days.p50 }) : t("common.none"),
          target: t0(targets.review_latency_p50_days)
        };
      if (key === "ci_success_rate")
        return {
          value: m.ci && m.ci.success_rate !== undefined ? `${Math.round(m.ci.success_rate * 1000) / 10}%` : t("common.none"),
          target: t0(targets.ci_success_rate_min)
        };
      if (key === "code_scan_pass_rate")
        return {
          value: m.ci && m.ci.code_scan_pass_rate !== undefined ? `${Math.round(m.ci.code_scan_pass_rate * 1000) / 10}%` : t("common.none"),
          target: t0(targets.code_scan_pass_rate_min)
        };
      if (key === "bug_rate")
        return {
          value: m.quality && m.quality.bug_rate !== undefined ? `${Math.round(m.quality.bug_rate * 1000) / 10}%` : t("common.none"),
          target: t0(targets.bug_rate_max)
        };
      if (key === "escaped_defects")
        return {
          value: m.quality && m.quality.escaped_defects !== undefined ? String(m.quality.escaped_defects) : t("common.none"),
          target: t0(targets.escaped_defects_max)
        };
      return { value: t("common.none"), target: null };
    }

    function t0(v) {
      return v === null || v === undefined ? null : v;
    }

    function labelOfMetricKey(key) {
      const k = String(key || "");
      const localized = t(`metric.${k}`);
      if (localized && localized !== `metric.${k}`) return localized;
      const fallback = t("analysis.metrics.metricFallback", { key: k });
      return fallback && fallback !== "analysis.metrics.metricFallback" ? fallback : `Metric (${k})`;
    }

    function interpretationOfMetric(key, valueText, targetText) {
      const k = String(key || "");
      const v = String(valueText || "");
      if (!v || v === t("common.none")) return t("analysis.orid.metricInterpret.noData");
      if (k.includes("lead_time") || k.includes("cycle_time") || k.includes("delivery_cycle_time"))
        return t("analysis.orid.metricInterpret.leadTime", { target: targetText ? String(targetText) : "" });
      if (k === "wip_avg" || k === "aging_wip") return t("analysis.orid.metricInterpret.wip");
      if (k.startsWith("pr_") || k.startsWith("review_latency")) return t("analysis.orid.metricInterpret.pr");
      if (k.startsWith("ci_") || k.includes("code_scan")) return t("analysis.orid.metricInterpret.ci");
      if (k.includes("bug") || k.includes("escaped")) return t("analysis.orid.metricInterpret.quality");
      if (k.includes("requirement_change") || k.includes("carryover") || k.includes("commitment"))
        return t("analysis.orid.metricInterpret.plan");
      return t("analysis.orid.metricInterpret.generic");
    }

    const metricInterpretColumns = computed(() => [
      { title: t("analysis.orid.metricInterpret.col.metric"), dataIndex: "metric", key: "metric", width: 200 },
      { title: t("analysis.orid.metricInterpret.col.value"), dataIndex: "value", key: "value", width: 140 },
      { title: t("analysis.orid.metricInterpret.col.target"), dataIndex: "target", key: "target", width: 170 },
      { title: t("analysis.orid.metricInterpret.col.interpretation"), dataIndex: "interpretation", key: "interpretation" }
    ]);

    const metricInterpretRows = computed(() => {
      const keys = Array.isArray(props.enabledMetricKeys) ? props.enabledMetricKeys.map((x) => String(x)) : [];
      const m = metricsForEvidence.value;
      if (!m || !keys.length) return [];
      return keys.map((k) => {
        const snap = pickMetricsSnapshot(m, k);
        const targetText = snap.target === null || snap.target === undefined ? t("common.none") : String(snap.target);
        return {
          key: `m_${k}`,
          metric: labelOfMetricKey(k),
          value: snap.value || t("common.none"),
          target: targetText,
          interpretation: interpretationOfMetric(k, snap.value, targetText === t("common.none") ? "" : targetText)
        };
      });
    });

    function relatedMetricsForAction(action) {
      const text = `${action && action.problem ? action.problem : ""} ${action && action.cause ? action.cause : ""} ${action && action.solution ? action.solution : ""}`.toLowerCase();
      const keys = new Set();
      if (text.includes("交付") || text.includes("周期") || text.includes("lead time")) {
        keys.add("lead_time_p50");
        keys.add("cycle_time_p50");
        keys.add("wip_avg");
      }
      if (text.includes("评审") || text.includes("pr") || text.includes("合并") || text.includes("review")) {
        keys.add("pr_lead_time_p50");
        keys.add("review_latency_p50");
      }
      if (text.includes("ci") || text.includes("流水线") || text.includes("构建")) {
        keys.add("ci_success_rate");
      }
      if (text.includes("扫描") || text.includes("门禁") || text.includes("code scan")) {
        keys.add("code_scan_pass_rate");
      }
      if (text.includes("缺陷") || text.includes("质量") || text.includes("返工") || text.includes("bug")) {
        keys.add("bug_rate");
        keys.add("escaped_defects");
      }
      if (keys.size === 0) keys.add("lead_time_p50");
      return Array.from(keys);
    }

    function relatedMetricsForActionWithReasons(action) {
      const text = `${action && action.problem ? action.problem : ""} ${action && action.cause ? action.cause : ""} ${action && action.solution ? action.solution : ""}`.toLowerCase();
      const out = [];
      const push = (key, reason) => {
        if (out.find((x) => x.key === key)) return;
        out.push({ key, reason });
      };
      if (text.includes("交付") || text.includes("周期") || text.includes("lead time")) {
        push("lead_time_p50", t("analysis.orid.linkReason.deliveryKeywords"));
        push("cycle_time_p50", t("analysis.orid.linkReason.deliveryKeywords"));
        push("wip_avg", t("analysis.orid.linkReason.wipAffectsCycle"));
      }
      if (text.includes("评审") || text.includes("pr") || text.includes("合并") || text.includes("review")) {
        push("pr_lead_time_p50", t("analysis.orid.linkReason.prKeywords"));
        push("review_latency_p50", t("analysis.orid.linkReason.reviewKeywords"));
      }
      if (text.includes("ci") || text.includes("流水线") || text.includes("构建")) {
        push("ci_success_rate", t("analysis.orid.linkReason.ciKeywords"));
      }
      if (text.includes("扫描") || text.includes("门禁") || text.includes("code scan")) {
        push("code_scan_pass_rate", t("analysis.orid.linkReason.scanKeywords"));
      }
      if (text.includes("缺陷") || text.includes("质量") || text.includes("返工") || text.includes("bug")) {
        push("bug_rate", t("analysis.orid.linkReason.qualityKeywords"));
        push("escaped_defects", t("analysis.orid.linkReason.escapedDefects"));
      }
      if (!out.length) push("lead_time_p50", t("analysis.orid.linkReason.defaultLeadTime"));
      return out;
    }

    const linkColumns = computed(() => [
      { title: t("analysis.orid.links.col.actionId"), dataIndex: "id", key: "id", width: 90 },
      { title: t("analysis.orid.links.col.problem"), dataIndex: "problem", key: "problem", width: 260 },
      { title: t("analysis.orid.links.col.metrics"), dataIndex: "metrics", key: "metrics" },
      { title: t("analysis.orid.links.col.reason"), dataIndex: "reason", key: "reason", width: 240 }
    ]);

    const linkRows = computed(() => {
      const actions = actionCandidates.value || [];
      const metrics = metricsForEvidence.value;
      return actions.map((a) => {
        const keys = relatedMetricsForActionWithReasons(a);
        const ms = keys.map((x) => {
          const k = x.key;
          const snap = pickMetricsSnapshot(metrics, k);
          const label = labelOfMetricKey(k);
          const targetText = snap.target === null || snap.target === undefined ? "" : t("analysis.orid.targetHint", { target: String(snap.target) });
          return { key: k, label, value: `${snap.value}${targetText}` };
        });
        const reasons = keys.map((x) => x.reason).filter(Boolean);
        return { key: a.key, id: a.id, problem: a.problem, metrics: ms, reason: reasons.join("；") };
      });
    });

    const selectedKeys = ref([]);
    const rowSelection = computed(() => ({
      selectedRowKeys: selectedKeys.value,
      onChange: (keys) => {
        selectedKeys.value = Array.isArray(keys) ? keys : [];
      }
    }));

    function addSelectedActionsToPlan() {
      const pid = String(props.selectedProjectIdModel || "").trim() || "example";
      if (!pid) return;
      const picked = new Set(selectedKeys.value || []);
      const selected = actionCandidates.value.filter((c) => picked.has(c.key));
      if (!selected.length) return;

      const items = loadPlanItems(pid);
      const seenIds = new Set(items.map((x) => String(x && x.id ? x.id : "")));
      for (const c of selected) {
        if (seenIds.has(String(c.id || ""))) continue;
        items.push({
          key: makeKey(),
          id: c.id,
          problem: c.problem,
          cause: c.cause,
          solution: c.solution,
          owner_role: c.owner_role || "",
          start_date: c.start_date || "",
          due_date: c.due_date || "",
          completed_date: c.completed_date || "",
          expected_effect: c.expected_effect || "",
          acceptance_method: c.acceptance_method || "",
          actual_effect: "",
          status: c.status || "not_started",
          severity: c.severity || "medium",
          progress: 0,
          last_update_at: nowIso()
        });
      }

      const next = { project_id: pid, updated_at: nowIso(), items };
      try {
        window.localStorage.setItem(`prjmx.actionsPlan.${pid}`, JSON.stringify(next));
      } catch {}
      planVersion.value++;

      selectedKeys.value = [];
      message.success(t("analysis.orid.msg.addSelectedSuccess"));
    }

    const detailVisible = ref(false);
    const detailRecord = ref(null);
    function openDetail(record) {
      detailRecord.value = record || null;
      detailVisible.value = true;
    }

    const planVersion = ref(0);

    function loadPlanItems(pid) {
      let existingPlan = { project_id: pid, updated_at: "", items: [] };
      try {
        const raw = window.localStorage.getItem(`prjmx.actionsPlan.${pid}`);
        const parsed = safeParse(raw);
        if (parsed && typeof parsed === "object" && Array.isArray(parsed.items)) {
          existingPlan = { project_id: pid, updated_at: parsed.updated_at || "", items: parsed.items };
        }
      } catch {}
      return Array.isArray(existingPlan.items) ? existingPlan.items.slice() : [];
    }

    function isInPlan(pid, actionId) {
      const id = String(actionId || "").trim();
      if (!id) return false;
      const items = loadPlanItems(pid);
      return items.some((x) => String(x && x.id ? x.id : "").trim() === id);
    }

    const detailAlreadyAdded = computed(() => {
      planVersion.value;
      const pid = String(props.selectedProjectIdModel || "").trim() || "example";
      const r = detailRecord.value;
      return !!(r && r.id && isInPlan(pid, r.id));
    });

    function addDetailToPlan() {
      const pid = String(props.selectedProjectIdModel || "").trim() || "example";
      const r = detailRecord.value;
      if (!r || !r.id) return;
      if (isInPlan(pid, r.id)) {
        message.info(t("analysis.addedToPlanHint"));
        planVersion.value++;
        return;
      }

      const items = loadPlanItems(pid);
      items.push({
        key: makeKey(),
        id: r.id,
        problem: r.problem,
        cause: r.cause,
        solution: r.solution,
        owner_role: r.owner_role || "",
        start_date: r.start_date || "",
        due_date: r.due_date || "",
        completed_date: r.completed_date || "",
        expected_effect: r.expected_effect || "",
        acceptance_method: r.acceptance_method || "",
        actual_effect: "",
        status: r.status || "not_started",
        severity: r.severity || "medium",
        progress: 0,
        last_update_at: nowIso()
      });
      const next = { project_id: pid, updated_at: nowIso(), items };
      try {
        window.localStorage.setItem(`prjmx.actionsPlan.${pid}`, JSON.stringify(next));
      } catch {}
      planVersion.value++;
      message.success(t("analysis.orid.msg.addDetailSuccess"));
    }

    function statusColor(status) {
      const s = String(status || "");
      if (s === "done" || s === "completed" || s === "closed") return "green";
      if (s === "in_progress" || s === "doing" || s === "ongoing") return "blue";
      if (s === "blocked") return "red";
      return "default";
    }

    function statusText(status) {
      const s = String(status || "");
      if (s === "done" || s === "completed" || s === "closed") return t("status.done");
      if (s === "in_progress" || s === "doing" || s === "ongoing") return t("status.in_progress");
      if (s === "blocked") return t("status.blocked");
      if (s === "not_started") return t("status.not_started");
      return s ? t("status.unknown") : t("common.none");
    }

    function severityColor(sev) {
      const s = String(sev || "").toLowerCase();
      if (s === "high" || s === "p0" || s === "p1" || s === "critical") return "red";
      if (s === "medium" || s === "p2") return "gold";
      if (s === "low" || s === "p3" || s === "p4") return "green";
      return "default";
    }

    function severityText(sev) {
      const s = String(sev || "").toLowerCase();
      if (s === "high" || s === "p0" || s === "p1" || s === "critical") return t("severity.high");
      if (s === "medium" || s === "p2") return t("severity.medium");
      if (s === "low" || s === "p3" || s === "p4") return t("severity.low");
      return sev ? String(sev) : t("severity.unknown");
    }

    const detailLinkColumns = computed(() => [
      { title: t("analysis.orid.detailLinks.col.metric"), dataIndex: "metric", key: "metric", width: 200 },
      { title: t("analysis.orid.detailLinks.col.value"), dataIndex: "value", key: "value", width: 240 },
      { title: t("analysis.orid.detailLinks.col.reason"), dataIndex: "reason", key: "reason" }
    ]);

    const detailLinks = computed(() => {
      const a = detailRecord.value;
      if (!a) return [];
      const metrics = metricsForEvidence.value;
      const links = relatedMetricsForActionWithReasons(a).map((x) => {
        const snap = pickMetricsSnapshot(metrics, x.key);
        const targetText = snap.target === null || snap.target === undefined ? "" : t("analysis.orid.targetHint", { target: String(snap.target) });
        return { key: x.key, metric: labelOfMetricKey(x.key), value: `${snap.value}${targetText}`, reason: x.reason };
      });
      return links;
    });

    const oridHints = computed(() => {
      const a = detailRecord.value;
      const r = props.reportData && props.reportData.orid ? props.reportData.orid : null;
      if (!a || !r) return [];
      const text = `${a.problem || ""} ${a.cause || ""} ${a.solution || ""}`.toLowerCase();
      const pool = []
        .concat(Array.isArray(r.objective) ? r.objective : [])
        .concat(Array.isArray(r.reflective) ? r.reflective : [])
        .concat(Array.isArray(r.interpretive) ? r.interpretive : []);
      return pool
        .filter((x) => String(x || "").toLowerCase().split(/\s+/).some((w) => w && text.includes(w)))
        .slice(0, 4)
        .map((x) => String(x));
    });

    return {
      t,
      columns,
      actionCandidates,
      selectedKeys,
      rowSelection,
      addSelectedActionsToPlan,
      detailVisible,
      detailRecord,
      openDetail,
      linkColumns,
      linkRows,
      addDetailToPlan,
      detailAlreadyAdded,
      detailLinks,
      detailLinkColumns,
      statusColor,
      statusText,
      severityColor,
      severityText,
      oridHints,
      signalTags,
      metricInterpretColumns,
      metricInterpretRows
    };
  }
};
</script>
