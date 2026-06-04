<template>
  <a-space direction="vertical" style="width: 100%" :size="12">
    <a-space wrap align="center">
      <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">{{ t("common.project") }}</span>
      <a-select v-model:value="selectedProjectIdModel" style="min-width: 320px">
        <a-select-option v-for="(p, idx) in projectsSafe" :key="String(p.id) + ':' + String(idx)" :value="String(p.id)">
          {{ projectLabel(p, idx) }}
        </a-select-option>
      </a-select>
      <a-button type="default" @click="openCreateAction">{{ t("plan.addCustom") }}</a-button>
    </a-space>

    <a-space wrap align="center">
      <a-button type="default" :loading="savingSnapshot" @click="saveSnapshot">{{ t("plan.saveSnapshot") }}</a-button>
      <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">{{ planSummaryText }}</span>
    </a-space>

    <a-alert v-if="errorText" type="error" show-icon :message="errorText" />

    <a-card size="small" :title="t('plan.title')">
      <div v-if="planItems.length === 0" style="color: rgba(0, 0, 0, 0.65)">{{ t("plan.empty") }}</div>
      <a-table v-else :columns="planColumns" :data-source="planItems" size="small" :pagination="{ pageSize: 8 }" :scroll="{ x: 1600 }">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'status'">
            <a-tag :color="statusColor(record.status)">{{ statusText(record.status) }}</a-tag>
          </template>
          <template v-else-if="column.key === 'progress'">
            <a-progress :percent="numOr0(record.progress)" size="small" />
          </template>
          <template v-else-if="column.key === 'op'">
            <a-space>
              <a-button size="small" type="link" @click="openDetailAction(record)">{{ t("common.detail") }}</a-button>
              <a-button size="small" type="link" @click="openEditAction(record)">{{ t("common.edit") }}</a-button>
              <a-popconfirm :title="t('common.confirmDelete')" :ok-text="t('common.delete')" :cancel-text="t('common.cancel')" @confirm="removePlanItem(record.key)">
                <a-button size="small" type="link" danger>{{ t("common.delete") }}</a-button>
              </a-popconfirm>
            </a-space>
          </template>
        </template>
      </a-table>
    </a-card>

    <a-drawer v-model:visible="actionDrawerVisible" :title="actionDrawerTitle" placement="right" :width="560">
      <a-space direction="vertical" style="width: 100%" :size="12">
        <a-card size="small" :title="t('plan.section.overview')">
          <a-space wrap>
            <a-tag color="blue">{{ actionDraft.id || "—" }}</a-tag>
            <a-tag :color="statusColor(actionDraft.status)">{{ statusText(actionDraft.status) }}</a-tag>
            <a-tag :color="severityColor(actionDraft.severity)">{{ t("plan.tag.severity") }}{{ severityText(actionDraft.severity) }}</a-tag>
            <a-tag color="default">{{ t("plan.tag.owner") }}{{ actionDraft.owner_role || "—" }}</a-tag>
          </a-space>
          <a-descriptions size="small" :column="2" bordered style="margin-top: 10px">
            <a-descriptions-item :label="t('plan.field.progress')">{{ numOr0(actionDraft.progress) }}%</a-descriptions-item>
            <a-descriptions-item :label="t('plan.field.lastUpdate')">{{ actionDraft.last_update_at || "—" }}</a-descriptions-item>
            <a-descriptions-item :label="t('plan.field.startDate')">{{ actionDraft.start_date || "—" }}</a-descriptions-item>
            <a-descriptions-item :label="t('plan.field.dueDate')">{{ actionDraft.due_date || "—" }}</a-descriptions-item>
            <a-descriptions-item :label="t('plan.field.completedDate')">{{ actionDraft.completed_date || "—" }}</a-descriptions-item>
            <a-descriptions-item label="—">—</a-descriptions-item>
          </a-descriptions>
        </a-card>

        <a-card size="small" :title="t('plan.section.problemCause')" v-if="actionDrawerReadOnly">
          <a-space direction="vertical" style="width: 100%" :size="8">
            <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px">{{ t("plan.field.problem") }}</div>
            <div style="white-space: pre-wrap">{{ actionDraft.problem || "—" }}</div>
            <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px">{{ t("plan.field.cause") }}</div>
            <div style="white-space: pre-wrap">{{ actionDraft.cause || "—" }}</div>
          </a-space>
        </a-card>

        <a-card size="small" :title="t('plan.section.solutionExpectedAcceptance')" v-if="actionDrawerReadOnly">
          <a-space direction="vertical" style="width: 100%" :size="8">
            <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px">{{ t("plan.field.solution") }}</div>
            <div style="white-space: pre-wrap">{{ actionDraft.solution || "—" }}</div>
            <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px">{{ t("plan.field.expectedEffect") }}</div>
            <div style="white-space: pre-wrap">{{ actionDraft.expected_effect || "—" }}</div>
            <div style="color: rgba(0, 0, 0, 0.45); font-size: 12px">{{ t("plan.field.acceptanceMethod") }}</div>
            <div style="white-space: pre-wrap">{{ actionDraft.acceptance_method || "—" }}</div>
          </a-space>
        </a-card>

        <a-card size="small" :title="t('plan.section.actualEffect')" v-if="actionDrawerReadOnly">
          <div style="white-space: pre-wrap">{{ actionDraft.actual_effect || "—" }}</div>
        </a-card>

        <a-form v-if="!actionDrawerReadOnly" layout="vertical">
          <a-card size="small" :title="t('plan.section.basicInfo')">
            <a-row :gutter="[12, 12]">
              <a-col :span="12">
                <a-form-item :label="t('plan.field.id')">
                  <a-input v-model:value="actionDraft.id" />
                </a-form-item>
              </a-col>
              <a-col :span="12">
                <a-form-item :label="t('plan.field.owner')">
                  <a-input v-model:value="actionDraft.owner_role" />
                </a-form-item>
              </a-col>
              <a-col :span="12">
                <a-form-item :label="t('plan.field.status')">
                  <a-select v-model:value="actionDraft.status">
                    <a-select-option value="not_started">{{ t("status.not_started") }}</a-select-option>
                    <a-select-option value="in_progress">{{ t("status.in_progress") }}</a-select-option>
                    <a-select-option value="done">{{ t("status.done") }}</a-select-option>
                    <a-select-option value="canceled">{{ t("status.canceled") }}</a-select-option>
                    <a-select-option value="blocked">{{ t("status.blocked") }}</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col :span="12">
                <a-form-item :label="t('plan.field.severity')">
                  <a-select v-model:value="actionDraft.severity">
                    <a-select-option value="high">{{ t("severity.high") }}</a-select-option>
                    <a-select-option value="medium">{{ t("severity.medium") }}</a-select-option>
                    <a-select-option value="low">{{ t("severity.low") }}</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col :span="12">
                <a-form-item :label="t('plan.field.progressRange')">
                  <a-input-number v-model:value="actionDraft.progress" :min="0" :max="100" style="width: 100%" />
                </a-form-item>
              </a-col>
              <a-col :span="12">
                <a-form-item :label="t('plan.field.startDateWithFormat')">
                  <a-input v-model:value="actionDraft.start_date" :placeholder="t('plan.placeholder.date')"/>
                </a-form-item>
              </a-col>
              <a-col :span="12">
                <a-form-item :label="t('plan.field.dueDateWithFormat')">
                  <a-input v-model:value="actionDraft.due_date" :placeholder="t('plan.placeholder.date')"/>
                </a-form-item>
              </a-col>
              <a-col :span="12">
                <a-form-item :label="t('plan.field.completedDateWithFormat')">
                  <a-input v-model:value="actionDraft.completed_date" :placeholder="t('plan.placeholder.date')"/>
                </a-form-item>
              </a-col>
            </a-row>
          </a-card>

          <a-card size="small" :title="t('plan.section.problemSolution')">
            <a-form-item :label="t('plan.field.problem')">
              <a-textarea v-model:value="actionDraft.problem" :rows="3" />
            </a-form-item>
            <a-form-item :label="t('plan.field.cause')">
              <a-textarea v-model:value="actionDraft.cause" :rows="3" />
            </a-form-item>
            <a-form-item :label="t('plan.field.solution')">
              <a-textarea v-model:value="actionDraft.solution" :rows="3" />
            </a-form-item>
          </a-card>

          <a-card size="small" :title="t('plan.section.acceptanceEffect')">
            <a-form-item :label="t('plan.field.expectedEffect')">
              <a-textarea v-model:value="actionDraft.expected_effect" :rows="2" />
            </a-form-item>
            <a-form-item :label="t('plan.field.acceptanceMethod')">
              <a-textarea v-model:value="actionDraft.acceptance_method" :rows="2" />
            </a-form-item>
            <a-form-item :label="t('plan.field.actualEffectAfter')">
              <a-textarea v-model:value="actionDraft.actual_effect" :rows="2" />
            </a-form-item>
          </a-card>
        </a-form>
      </a-space>

      <template #footer>
        <a-space direction="vertical" style="width: 100%" :size="8">
          <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px">
            {{ t("plan.footerHelp") }}
          </div>
          <a-space style="width: 100%" align="center" :size="10">
            <a-button type="default" @click="actionDrawerVisible = false">{{ t("common.close") }}</a-button>
            <a-button v-if="!actionDrawerReadOnly" type="primary" @click="saveActionDraft">{{ t("common.save") }}</a-button>
          </a-space>
        </a-space>
      </template>
    </a-drawer>
  </a-space>
</template>

<script>
import { computed, ref, watch } from "vue";
import { message } from "ant-design-vue";
import { useI18n } from "../i18n.js";

export default {
  props: {
    projects: { type: Array, default: () => [] },
    selectedProjectId: { type: String, default: "" }
  },
  emits: ["update:selectedProjectId"],
  setup(props, { emit }) {
    const { t } = useI18n();
    const projectsSafe = computed(() => (Array.isArray(props.projects) ? props.projects : []));
    const selectedProjectIdModel = computed({
      get: () => String(props.selectedProjectId || ""),
      set: (v) => emit("update:selectedProjectId", v === undefined || v === null ? "" : String(v))
    });

    function projectLabel(p, idx) {
      const id = p && p.id !== undefined && p.id !== null ? String(p.id).trim() : "";
      const name = p && p.name !== undefined && p.name !== null ? String(p.name).trim() : "";
      return `${id || String(idx + 1)} · ${name || t("common.unnamed")}`;
    }

    function numOr0(v) {
      const n = typeof v === "number" ? v : Number(v);
      return Number.isFinite(n) ? n : 0;
    }

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

    const errorText = ref("");
    const savingSnapshot = ref(false);

    function ensureProjectReady() {
      const pid = String(selectedProjectIdModel.value || "").trim();
      if (!pid) {
        message.warning(t("common.selectProjectFirst"));
        return null;
      }
      return pid;
    }

    async function fetchJson(url) {
      const res = await fetch(url, { cache: "no-store" });
      if (!res.ok) throw new Error(t("analysis.error.http", { url, status: res.status }));
      const parsed = await res.json();
      if (!parsed || typeof parsed !== "object") throw new Error(t("analysis.error.notObject", { url }));
      return parsed;
    }

    async function fetchJsonOptional(url) {
      const res = await fetch(url, { cache: "no-store" });
      if (res.status === 404) return null;
      if (!res.ok) throw new Error(t("analysis.error.http", { url, status: res.status }));
      const parsed = await res.json();
      return parsed && typeof parsed === "object" ? parsed : null;
    }


    const plan = ref({ project_id: "", updated_at: "", items: [] });

    function loadPlan() {
      const pid = String(selectedProjectIdModel.value || "").trim();
      if (!pid) {
        plan.value = { project_id: "", updated_at: "", items: [] };
        return;
      }
      try {
        const raw = window.localStorage.getItem(`prjmx.actionsPlan.${pid}`);
        const parsed = safeParse(raw);
        if (parsed && typeof parsed === "object" && Array.isArray(parsed.items)) {
          plan.value = { project_id: pid, updated_at: parsed.updated_at || "", items: parsed.items };
          return;
        }
      } catch {}
      plan.value = { project_id: pid, updated_at: "", items: [] };
    }

    function persistPlan() {
      const pid = String(selectedProjectIdModel.value || "").trim();
      if (!pid) return;
      const next = { ...(plan.value || {}), project_id: pid, updated_at: nowIso() };
      plan.value = next;
      try {
        window.localStorage.setItem(`prjmx.actionsPlan.${pid}`, JSON.stringify(next));
      } catch {}
    }

    watch(selectedProjectIdModel, () => loadPlan(), { immediate: true });

    const planItems = computed(() =>
      (plan.value && Array.isArray(plan.value.items) ? plan.value.items : []).map((x, idx) => ({
        key: x && x.key ? String(x.key) : `plan_${idx}`,
        ...x
      }))
    );

function updatePlanItem(key, patch) {
  const k = String(key || "");
  const existing = planItems.value.slice();
  const idx = existing.findIndex((x) => String(x.key) === k);
  if (idx < 0) return;
  existing.splice(idx, 1, { ...(existing[idx] || {}), ...(patch || {}), last_update_at: nowIso() });
  plan.value = { ...(plan.value || {}), items: existing };
  persistPlan();
}

function removePlanItem(key) {
  const k = String(key || "");
  const existing = planItems.value.slice().filter((x) => String(x.key) !== k);
  plan.value = { ...(plan.value || {}), items: existing };
  persistPlan();
}

function statusText(status) {
  const s = String(status || "");
  if (s === "done") return t("status.done");
  if (s === "in_progress") return t("status.in_progress");
  if (s === "blocked") return t("status.blocked");
  if (s === "canceled") return t("status.canceled");
  if (s === "not_started") return t("status.not_started");
  return t("status.unknown");
}

function statusColor(status) {
  const s = String(status || "");
  if (s === "done") return "green";
  if (s === "in_progress") return "blue";
  if (s === "blocked") return "red";
  if (s === "canceled") return "default";
  return "default";
}

function severityText(severity) {
  const s = String(severity || "").toLowerCase();
  if (s === "high" || s === "p0" || s === "p1" || s === "critical") return t("severity.high");
  if (s === "medium" || s === "p2") return t("severity.medium");
  if (s === "low" || s === "p3" || s === "p4") return t("severity.low");
  return t("severity.unknown");
}

function severityColor(severity) {
  const s = String(severity || "").toLowerCase();
  if (s === "high" || s === "p0" || s === "p1" || s === "critical") return "red";
  if (s === "medium" || s === "p2") return "gold";
  if (s === "low" || s === "p3" || s === "p4") return "green";
  return "default";
}

const planColumns = computed(() => [
  { title: t("plan.col.id"), dataIndex: "id", key: "id", width: 100 },
  { title: t("plan.col.problem"), dataIndex: "problem", key: "problem", width: 320 },
  { title: t("plan.col.owner"), dataIndex: "owner_role", key: "owner_role", width: 140 },
  { title: t("plan.col.due"), dataIndex: "due_date", key: "due_date", width: 120 },
  { title: t("plan.col.status"), dataIndex: "status", key: "status", width: 110 },
  { title: t("plan.col.progress"), dataIndex: "progress", key: "progress", width: 140 },
  { title: t("plan.col.op"), key: "op", width: 220 }
]);

const actionDrawerVisible = ref(false);
const actionDrawerMode = ref("detail");
const actionDraft = ref({
  key: "",
  id: "",
  problem: "",
  cause: "",
  solution: "",
  owner_role: "",
  start_date: "",
  due_date: "",
  completed_date: "",
  expected_effect: "",
  acceptance_method: "",
  actual_effect: "",
  status: "not_started",
  severity: "medium",
  progress: 0,
  last_update_at: ""
});

const actionDrawerReadOnly = computed(() => String(actionDrawerMode.value) === "detail");
const actionDrawerTitle = computed(() =>
  actionDrawerReadOnly.value ? t("plan.item.detail") : String(actionDrawerMode.value) === "create" ? t("plan.item.create") : t("plan.item.edit")
);

function normalizeDraft(d) {
  const src = d && typeof d === "object" ? d : {};
  return {
    key: src.key ? String(src.key) : makeKey(),
    id: src.id ? String(src.id) : "",
    problem: src.problem ? String(src.problem) : "",
    cause: src.cause ? String(src.cause) : "",
    solution: src.solution ? String(src.solution) : "",
    owner_role: src.owner_role ? String(src.owner_role) : "",
    start_date: src.start_date ? String(src.start_date) : "",
    due_date: src.due_date ? String(src.due_date) : "",
    completed_date: src.completed_date ? String(src.completed_date) : "",
    expected_effect: src.expected_effect ? String(src.expected_effect) : "",
    acceptance_method: src.acceptance_method ? String(src.acceptance_method) : "",
    actual_effect: src.actual_effect ? String(src.actual_effect) : "",
    status: src.status ? String(src.status) : "not_started",
    severity: src.severity ? String(src.severity) : "medium",
    progress: numOr0(src.progress),
    last_update_at: src.last_update_at ? String(src.last_update_at) : ""
  };
}

function openCreateAction() {
  const pid = ensureProjectReady();
  if (!pid) return;
  const nextId = `A-${(planItems.value || []).length + 1}`;
  actionDrawerMode.value = "create";
  actionDraft.value = normalizeDraft({ id: nextId, status: "not_started", severity: "medium", progress: 0, last_update_at: nowIso() });
  actionDrawerVisible.value = true;
}

function openEditAction(record) {
  actionDrawerMode.value = "edit";
  actionDraft.value = normalizeDraft(record);
  actionDrawerVisible.value = true;
}

function openDetailAction(record) {
  actionDrawerMode.value = "detail";
  actionDraft.value = normalizeDraft(record);
  actionDrawerVisible.value = true;
}

function saveActionDraft() {
  const pid = ensureProjectReady();
  if (!pid) return;
  const mode = String(actionDrawerMode.value);
  const draft = normalizeDraft(actionDraft.value);
  if (!draft.id.trim()) {
    message.warning(t("plan.fillId"));
    return;
  }
  const existing = planItems.value.slice();
  if (mode === "create") {
    existing.unshift({ ...draft, last_update_at: nowIso() });
    plan.value = { ...(plan.value || {}), items: existing };
    persistPlan();
    actionDrawerVisible.value = false;
    message.success(t("plan.createdAction"));
    return;
  }
  const idx = existing.findIndex((x) => String(x.key) === String(draft.key));
  if (idx < 0) {
    message.warning(t("plan.updateNotFound"));
    return;
  }
  existing.splice(idx, 1, { ...(existing[idx] || {}), ...draft, last_update_at: nowIso() });
  plan.value = { ...(plan.value || {}), items: existing };
  persistPlan();
  actionDrawerVisible.value = false;
  message.success(t("plan.savedAction"));
}

const planSummaryText = computed(() => {
  const items = planItems.value || [];
  const total = items.length;
  const done = items.filter((x) => x.status === "done").length;
  const inProgress = items.filter((x) => x.status === "in_progress").length;
  return t("plan.summary", { done, total, inProgress });
});

const improvements = ref([]);

function loadHistory() {
  const pid = String(selectedProjectIdModel.value || "").trim();
  if (!pid) {
    improvements.value = [];
    return;
  }
  try {
    const raw = window.localStorage.getItem(`prjmx.improvements.${pid}`);
    const parsed = safeParse(raw);
    improvements.value = Array.isArray(parsed) ? parsed : [];
  } catch {
    improvements.value = [];
  }
}

function persistHistory() {
  const pid = String(selectedProjectIdModel.value || "").trim();
  if (!pid) return;
  try {
    window.localStorage.setItem(`prjmx.improvements.${pid}`, JSON.stringify(improvements.value || []));
  } catch {}
}

watch(selectedProjectIdModel, () => loadHistory(), { immediate: true });

function extractKeyMetrics(reportOrMetrics) {
  if (!reportOrMetrics || typeof reportOrMetrics !== "object") {
    return { throughput: null, lead_time_p50_days: null, cycle_time_p50_days: null, bug_rate: null, reopen_rate: null, escaped_defects: null };
  }
  const m = reportOrMetrics && reportOrMetrics.metrics ? reportOrMetrics.metrics : reportOrMetrics;
  const throughput = m && m.throughput && m.throughput.count !== undefined ? m.throughput.count : m && m.throughput !== undefined ? m.throughput : null;
  const leadP50 =
    m && m.lead_time_days && m.lead_time_days.p50 !== undefined ? m.lead_time_days.p50 : m && m.lead_time_p50_days !== undefined ? m.lead_time_p50_days : null;
  const cycleP50 =
    m && m.cycle_time_days && m.cycle_time_days.p50 !== undefined ? m.cycle_time_days.p50 : m && m.cycle_time_p50_days !== undefined ? m.cycle_time_p50_days : null;
  const quality = m && m.quality ? m.quality : {};
  const bugRate = quality && quality.bug_rate !== undefined ? quality.bug_rate : m && m.bug_rate !== undefined ? m.bug_rate : null;
  const reopenRate = quality && quality.reopen_rate !== undefined ? quality.reopen_rate : m && m.reopen_rate !== undefined ? m.reopen_rate : null;
  const escaped = quality && quality.escaped_defects !== undefined ? quality.escaped_defects : m && m.escaped_defects !== undefined ? m.escaped_defects : null;
  return {
    throughput: throughput === null || throughput === undefined ? null : throughput,
    lead_time_p50_days: leadP50 === null || leadP50 === undefined ? null : leadP50,
    cycle_time_p50_days: cycleP50 === null || cycleP50 === undefined ? null : cycleP50,
    bug_rate: bugRate === null || bugRate === undefined ? null : bugRate,
    reopen_rate: reopenRate === null || reopenRate === undefined ? null : reopenRate,
    escaped_defects: escaped === null || escaped === undefined ? null : escaped
  };
}

async function saveSnapshot() {
  const pid = ensureProjectReady();
  if (!pid) return;
  errorText.value = "";
  savingSnapshot.value = true;
  try {
    const reportUrl = `/work/outputs/${encodeURIComponent(pid)}/project-metrics-orid/report.json`;
    const metricsUrl = `/work/outputs/${encodeURIComponent(pid)}/project-metrics-orid/metrics.json`;
    let base = await fetchJsonOptional(reportUrl);
    if (!base) base = await fetchJsonOptional(metricsUrl);
    if (!base) message.info(t("plan.snapshotNoReport"));
    const metrics = extractKeyMetrics(base);
    const items = planItems.value || [];
    const snapshot = {
      at: nowIso(),
      window: base && base.metrics && base.metrics.window ? String(base.metrics.window) : "",
      metrics,
      plan_summary: {
        total: items.length,
        done: items.filter((x) => x.status === "done").length,
        in_progress: items.filter((x) => x.status === "in_progress").length
      }
    };
    improvements.value = (improvements.value || []).concat([snapshot]);
    persistHistory();
    message.success(t("plan.savedSnapshot"));
  } catch (e) {
    errorText.value = e && e.message ? e.message : String(e);
  } finally {
    savingSnapshot.value = false;
  }
}

    return {
      t,
      projectsSafe,
      selectedProjectIdModel,
      projectLabel,
      numOr0,
      errorText,
      savingSnapshot,
      plan,
      planItems,
      updatePlanItem,
      removePlanItem,
      planColumns,
      planSummaryText,
      saveSnapshot,
      improvements,
      statusText,
      statusColor,
      severityText,
      severityColor,
      openCreateAction,
      openEditAction,
      openDetailAction,
      actionDrawerVisible,
      actionDrawerTitle,
      actionDrawerReadOnly,
      actionDraft,
      saveActionDraft
    };
  }
};
</script>
