<template>
  <a-space direction="vertical" style="width: 100%" :size="12">
    <a-button type="primary" @click="requestRunSkill('orid')">执行持续改进</a-button>
    <a-alert v-if="oridError" type="warning" show-icon :message="oridError" />
    <a-card size="small" title="输入/输出文件">
      <ul style="margin: 0; padding-left: 18px">
        <li>输入：工作区配置</li>
        <li>输入：度量结果</li>
        <li>输出：改进报告</li>
      </ul>
    </a-card>

    <a-card size="small" title="输入信号（阻塞事项 + 指标解读，用于共同形成行动项）">
      <a-space direction="vertical" style="width: 100%" :size="10">
        <div>
          <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px; margin-bottom: 6px">阻塞/节奏信号</div>
          <a-space wrap>
            <a-tag v-for="t in signalTags" :key="t.key" :color="t.color">{{ t.text }}</a-tag>
          </a-space>
        </div>

        <div>
          <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px; margin-bottom: 6px">问题发现指标解读（按已选指标）</div>
          <div v-if="metricInterpretRows.length === 0" style="color: rgba(0, 0, 0, 0.45); font-size: 12px">—</div>
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
    <div v-if="!reportData" style="color: rgba(0, 0, 0, 0.65)">尚未读取到改进报告。</div>
    <a-alert v-else type="success" show-icon message="改进报告已生成" />

    <a-card v-if="reportData" size="small" title="指标与问题的关联（把现象对齐到证据口径）">
      <div v-if="linkRows.length === 0" style="color: rgba(0, 0, 0, 0.45); font-size: 12px">—</div>
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

    <a-card v-if="reportData" size="small" title="候选行动项">
      <a-space wrap align="center" style="margin-bottom: 10px">
        <a-button type="primary" :disabled="selectedKeys.length === 0" @click="addSelectedActionsToPlan">纳入行动计划</a-button>
        <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">纳入后可在“行动项管理”中维护进度与实际效果</span>
      </a-space>
      <div v-if="actionCandidates.length === 0" style="color: rgba(0, 0, 0, 0.65)">未提供候选行动项（可能未完成分析，或数据不足）。</div>
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
            <a-button type="link" size="small" @click="openDetail(record)">详情</a-button>
          </template>
        </template>
      </a-table>
    </a-card>

    <a-drawer v-model:visible="detailVisible" title="行动项详情" width="560">
      <div v-if="!detailRecord" style="color: rgba(0, 0, 0, 0.45)">—</div>
      <a-space v-else direction="vertical" style="width: 100%" :size="12">
        <a-card size="small" title="概览">
          <a-space wrap>
            <a-tag color="blue">{{ detailRecord.id || "—" }}</a-tag>
            <a-tag :color="statusColor(detailRecord.status)">{{ statusText(detailRecord.status) }}</a-tag>
            <a-tag :color="severityColor(detailRecord.severity)">严重性：{{ severityText(detailRecord.severity) }}</a-tag>
            <a-tag color="default">负责人：{{ detailRecord.owner_role || "—" }}</a-tag>
            <a-tag v-if="detailAlreadyAdded" color="green">已加入行动计划</a-tag>
          </a-space>
          <a-descriptions size="small" :column="2" bordered style="margin-top: 10px">
            <a-descriptions-item label="发现时间">{{ detailRecord.discovered_at || "—" }}</a-descriptions-item>
            <a-descriptions-item label="开始时间">{{ detailRecord.start_date || "—" }}</a-descriptions-item>
            <a-descriptions-item label="截止时间">{{ detailRecord.due_date || "—" }}</a-descriptions-item>
            <a-descriptions-item label="完成时间">{{ detailRecord.completed_date || "—" }}</a-descriptions-item>
          </a-descriptions>
        </a-card>

        <a-card size="small" title="问题 → 原因">
          <a-space direction="vertical" style="width: 100%" :size="8">
            <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px">问题</div>
            <div style="white-space: pre-wrap">{{ detailRecord.problem || "—" }}</div>
            <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px">原因</div>
            <div style="white-space: pre-wrap">{{ detailRecord.cause || "—" }}</div>
          </a-space>
        </a-card>

        <a-card size="small" title="方案 → 预期 → 验收">
          <a-space direction="vertical" style="width: 100%" :size="8">
            <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px">解决方案</div>
            <div style="white-space: pre-wrap">{{ detailRecord.solution || "—" }}</div>
            <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px">预期效果</div>
            <div style="white-space: pre-wrap">{{ detailRecord.expected_effect || "—" }}</div>
            <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px">验收方式</div>
            <div style="white-space: pre-wrap">{{ detailRecord.acceptance_method || "—" }}</div>
          </a-space>
        </a-card>

        <a-card size="small" title="行动项如何推导出来（证据关联）">
          <div v-if="detailLinks.length === 0" style="color: rgba(0, 0, 0, 0.45); font-size: 12px">—</div>
          <a-space v-else direction="vertical" style="width: 100%" :size="8">
            <a-table :columns="detailLinkColumns" :data-source="detailLinks" size="small" :pagination="false" :scroll="{ x: 900 }" />
            <a-space wrap>
              <a-tag v-for="t in signalTags" :key="`d_${t.key}`" :color="t.color">{{ t.text }}</a-tag>
            </a-space>
            <div v-if="oridHints.length" style="color: rgba(0, 0, 0, 0.65); font-size: 12px">
              观察-感受-解读相关片段：{{ oridHints.join("；") }}
            </div>
          </a-space>
        </a-card>
      </a-space>

      <template #footer>
        <a-space direction="vertical" style="width: 100%" :size="8">
          <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px">
            候选行动项是分析生成的建议清单；加入行动计划后会进入“行动项管理”，用于分配负责人、维护进度、记录实际效果并形成闭环。候选行动项可能随新一轮分析变化，但行动计划会保留你的落地执行记录。
          </div>
          <a-space style="width: 100%" align="center" :size="10">
            <a-button type="default" @click="detailVisible = false">关闭</a-button>
            <a-button type="primary" :disabled="detailAlreadyAdded" @click="addDetailToPlan">添加到行动计划</a-button>
            <span v-if="detailAlreadyAdded" style="color: rgba(0, 0, 0, 0.45); font-size: 12px">该行动项已在行动计划中</span>
          </a-space>
        </a-space>
      </template>
    </a-drawer>
  </a-space>
</template>

<script>
import { computed, ref } from "vue";
import { message } from "ant-design-vue";

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

    const columns = [
      { title: "编号", dataIndex: "id", key: "id", width: 90 },
      { title: "问题", dataIndex: "problem", key: "problem", width: 260 },
      { title: "原因", dataIndex: "cause", key: "cause", width: 240 },
      { title: "解决方案", dataIndex: "solution", key: "solution", width: 260 },
      { title: "预期效果", dataIndex: "expected_effect", key: "expected_effect", width: 260 },
      { title: "验收方式", dataIndex: "acceptance_method", key: "acceptance_method", width: 260 },
      { title: "截止", dataIndex: "due_date", key: "due_date", width: 120 },
      { title: "负责人", dataIndex: "owner_role", key: "owner_role", width: 120 },
      { title: "操作", key: "action", fixed: "right", width: 80 }
    ];

    const actionCandidates = computed(() => {
      const raw = props.reportData && Array.isArray(props.reportData.actions) ? props.reportData.actions : [];
      return raw.map((a, index) => {
        const id = a && (a.id || a.no) ? String(a.id || a.no) : String(index + 1);
        return {
          key: `cand_${id}_${index}`,
          id,
          problem: a && (a.problem || a.issue || a.question) ? String(a.problem || a.issue || a.question) : "—",
          cause: a && (a.cause || a.root_cause || a.reason) ? String(a.cause || a.root_cause || a.reason) : "—",
          solution: a && (a.solution || a.title || a.action) ? String(a.solution || a.title || a.action) : "—",
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
      tags.push({ key: "swimlane", text: `泳道阻塞：${blocked === null ? "—" : blocked}${th ? `（阈值${th}天）` : ""}`, color: blocked && blocked > 0 ? "red" : "default" });
      tags.push({ key: "burndown", text: `燃尽判断：${verdict || "—"}`, color: verdict.includes("偏慢") || verdict.includes("落后") ? "gold" : "default" });
      tags.push({ key: "gantt", text: `甘特延迟：${delayed === null ? "—" : delayed}；过期未完：${risky === null ? "—" : risky}`, color: (delayed && delayed > 0) || (risky && risky > 0) ? "gold" : "default" });
      return tags;
    });

    function pickMetricsSnapshot(metrics, key) {
      const m = metrics && typeof metrics === "object" ? metrics : {};
      const t = m.targets && typeof m.targets === "object" ? m.targets : {};
      if (key === "lead_time_p50") return { value: m.lead_time_days && m.lead_time_days.p50 !== undefined ? `${m.lead_time_days.p50} 天` : "—", target: t.lead_time_p50_days };
      if (key === "cycle_time_p50") return { value: m.cycle_time_days && m.cycle_time_days.p50 !== undefined ? `${m.cycle_time_days.p50} 天` : "—", target: t.cycle_time_p50_days };
      if (key === "wip_avg") return { value: m.wip && m.wip.avg !== undefined ? String(m.wip.avg) : "—", target: t.wip_limit };
      if (key === "pr_lead_time_p50") return { value: m.pr_lead_time_days && m.pr_lead_time_days.p50 !== undefined ? `${m.pr_lead_time_days.p50} 天` : "—", target: t.pr_lead_time_p50_days };
      if (key === "review_latency_p50") return { value: m.review_latency_days && m.review_latency_days.p50 !== undefined ? `${m.review_latency_days.p50} 天` : "—", target: t.review_latency_p50_days };
      if (key === "ci_success_rate") return { value: m.ci && m.ci.success_rate !== undefined ? `${Math.round(m.ci.success_rate * 1000) / 10}%` : "—", target: t.ci_success_rate_min };
      if (key === "code_scan_pass_rate") return { value: m.ci && m.ci.code_scan_pass_rate !== undefined ? `${Math.round(m.ci.code_scan_pass_rate * 1000) / 10}%` : "—", target: t.code_scan_pass_rate_min };
      if (key === "bug_rate") return { value: m.quality && m.quality.bug_rate !== undefined ? `${Math.round(m.quality.bug_rate * 1000) / 10}%` : "—", target: t.bug_rate_max };
      if (key === "escaped_defects") return { value: m.quality && m.quality.escaped_defects !== undefined ? String(m.quality.escaped_defects) : "—", target: t.escaped_defects_max };
      return { value: "—", target: null };
    }

    function labelOfMetricKey(key) {
      const k = String(key || "");
      const map = {
        lead_time_p50: "交付周期 p50",
        cycle_time_p50: "处理周期 p50",
        wip_avg: "平均在制",
        aging_wip: "在制老化",
        throughput: "吞吐量",
        pr_lead_time_p50: "合并请求周期 p50",
        review_latency_p50: "评审等待 p50",
        ci_success_rate: "流水线成功率",
        code_scan_pass_rate: "代码扫描通过率",
        bug_rate: "缺陷率",
        escaped_defects: "逃逸缺陷数",
        requirement_change_rate: "需求变更率",
        carryover_rate: "结转率",
        commitment_reliability: "承诺达成率"
      };
      return map[k] || `指标（${k}）`;
    }

    function interpretationOfMetric(key, valueText, targetText) {
      const k = String(key || "");
      const v = String(valueText || "");
      if (!v || v === "—") return "暂无可用数据；可能是该指标依赖字段未填写或数据源获取失败，可先检查“收集数据”的 Jira/Git/CI 结果。";
      if (k.includes("lead_time") || k.includes("cycle_time") || k.includes("delivery_cycle_time"))
        return `用于定位交付节奏是否被阻塞/排队拉长。${targetText ? `对齐目标：${targetText}。` : ""}`;
      if (k === "wip_avg" || k === "aging_wip") return "用于判断在制是否过多或在制老化，通常与泳道阻塞和周期上升强相关。";
      if (k.startsWith("pr_") || k.startsWith("review_latency")) return "用于定位评审与协作节奏是否形成排队。";
      if (k.startsWith("ci_") || k.includes("code_scan")) return "用于定位流水线门禁是否有效且是否造成返工/等待。";
      if (k.includes("bug") || k.includes("escaped")) return "用于定位质量风险是否前置以及是否存在逃逸缺陷回流。";
      if (k.includes("requirement_change") || k.includes("carryover") || k.includes("commitment"))
        return "用于判断计划稳定性与变更压力，帮助解释燃尽异常与延期原因。";
      return "用于作为现象信号，与阻塞/周期/质量指标联动形成行动项。";
    }

    const metricInterpretColumns = [
      { title: "指标", dataIndex: "metric", key: "metric", width: 180 },
      { title: "当前值", dataIndex: "value", key: "value", width: 120 },
      { title: "目标/阈值", dataIndex: "target", key: "target", width: 150 },
      { title: "解读", dataIndex: "interpretation", key: "interpretation" }
    ];

    const metricInterpretRows = computed(() => {
      const keys = Array.isArray(props.enabledMetricKeys) ? props.enabledMetricKeys.map((x) => String(x)) : [];
      const m = metricsForEvidence.value;
      if (!m || !keys.length) return [];
      return keys.map((k) => {
        const snap = pickMetricsSnapshot(m, k);
        const targetText = snap.target === null || snap.target === undefined ? "—" : String(snap.target);
        return {
          key: `m_${k}`,
          metric: labelOfMetricKey(k),
          value: snap.value || "—",
          target: targetText,
          interpretation: interpretationOfMetric(k, snap.value, targetText === "—" ? "" : targetText)
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
        push("lead_time_p50", "交付/周期相关关键词");
        push("cycle_time_p50", "交付/周期相关关键词");
        push("wip_avg", "周期通常受在制/排队影响");
      }
      if (text.includes("评审") || text.includes("pr") || text.includes("合并") || text.includes("review")) {
        push("pr_lead_time_p50", "PR/合并相关关键词");
        push("review_latency_p50", "评审等待相关关键词");
      }
      if (text.includes("ci") || text.includes("流水线") || text.includes("构建")) {
        push("ci_success_rate", "CI 相关关键词");
      }
      if (text.includes("扫描") || text.includes("门禁") || text.includes("code scan")) {
        push("code_scan_pass_rate", "扫描/门禁相关关键词");
      }
      if (text.includes("缺陷") || text.includes("质量") || text.includes("返工") || text.includes("bug")) {
        push("bug_rate", "质量/缺陷相关关键词");
        push("escaped_defects", "逃逸/线上缺陷相关");
      }
      if (!out.length) push("lead_time_p50", "默认：以交付周期作为首要现象指标");
      return out;
    }

    const linkColumns = [
      { title: "行动项", dataIndex: "id", key: "id", width: 90 },
      { title: "问题", dataIndex: "problem", key: "problem", width: 260 },
      { title: "关联指标（快照）", dataIndex: "metrics", key: "metrics" },
      { title: "关联理由", dataIndex: "reason", key: "reason", width: 220 }
    ];

    const linkRows = computed(() => {
      const actions = actionCandidates.value || [];
      const metrics = metricsForEvidence.value;
      return actions.map((a) => {
        const keys = relatedMetricsForActionWithReasons(a);
        const ms = keys.map((x) => {
          const k = x.key;
          const snap = pickMetricsSnapshot(metrics, k);
          const labelMap = {
            lead_time_p50: "交付周期p50",
            cycle_time_p50: "处理周期p50",
            wip_avg: "平均WIP",
            pr_lead_time_p50: "PR周期p50",
            review_latency_p50: "评审等待p50",
            ci_success_rate: "CI成功率",
            code_scan_pass_rate: "扫描通过率",
            bug_rate: "缺陷率",
            escaped_defects: "逃逸缺陷数"
          };
          const targetText = snap.target === null || snap.target === undefined ? "" : `（目标${typeof snap.target === "number" ? snap.target : snap.target}）`;
          return { key: k, label: labelMap[k] || k, value: `${snap.value}${targetText}` };
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
      message.success("已纳入行动计划");
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
        message.info("该行动项已在行动计划中");
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
      message.success("已加入行动计划，可在“行动项管理”中跟踪")
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
      if (s === "done" || s === "completed" || s === "closed") return "已完成";
      if (s === "in_progress" || s === "doing" || s === "ongoing") return "进行中";
      if (s === "blocked") return "阻塞";
      if (s === "not_started") return "未开始";
      return s ? "未知" : "—";
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
      if (s === "high" || s === "p0" || s === "p1" || s === "critical") return "高";
      if (s === "medium" || s === "p2") return "中";
      if (s === "low" || s === "p3" || s === "p4") return "低";
      return sev || "—";
    }

    const detailLinkColumns = [
      { title: "指标", dataIndex: "metric", key: "metric", width: 160 },
      { title: "当前值/目标", dataIndex: "value", key: "value", width: 240 },
      { title: "关联理由", dataIndex: "reason", key: "reason" }
    ];

    const detailLinks = computed(() => {
      const a = detailRecord.value;
      if (!a) return [];
      const metrics = metricsForEvidence.value;
      const labelMap = {
        lead_time_p50: "交付周期p50",
        cycle_time_p50: "处理周期p50",
        wip_avg: "平均WIP",
        pr_lead_time_p50: "PR周期p50",
        review_latency_p50: "评审等待p50",
        ci_success_rate: "CI成功率",
        code_scan_pass_rate: "扫描通过率",
        bug_rate: "缺陷率",
        escaped_defects: "逃逸缺陷数"
      };
      const links = relatedMetricsForActionWithReasons(a).map((x) => {
        const snap = pickMetricsSnapshot(metrics, x.key);
        const targetText = snap.target === null || snap.target === undefined ? "" : `（目标${typeof snap.target === "number" ? snap.target : snap.target}）`;
        return { key: x.key, metric: labelMap[x.key] || x.key, value: `${snap.value}${targetText}`, reason: x.reason };
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
