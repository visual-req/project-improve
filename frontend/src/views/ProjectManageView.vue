<template>
  <a-space direction="vertical" style="width: 100%" :size="12">
    <a-space wrap align="center">
      <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">{{ t("common.project") }}</span>
      <a-select v-model:value="selectedProjectIdModel" style="min-width: 320px">
        <a-select-option v-for="(p, idx) in projectsSafe" :key="String(p.id) + ':' + String(idx)" :value="String(p.id)">
          {{ projectLabel(p, idx) }}
        </a-select-option>
      </a-select>
      <a-button type="primary" @click="openAddProject">{{ t("projects.add") }}</a-button>
      <a-button type="default" @click="reloadWorkspaceConfig">{{ t("projects.reloadFromFile") }}</a-button>
      <a-button type="default" @click="goActions">{{ t("projects.goActions") }}</a-button>
    </a-space>

    <a-card size="small" :title="t('projects.listTitle')">
      <a-table :columns="projectColumns" :data-source="projectRows" size="small" :pagination="{ pageSize: 8 }" :scroll="{ x: 900 }">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'op'">
            <a-space>
              <a-button size="small" type="link" @click="openProjectDetail(record)">{{ t("common.detail") }}</a-button>
              <a-button size="small" type="link" @click="openEditProject(record)">{{ t("common.edit") }}</a-button>
              <a-popconfirm :title="t('common.confirmDelete')" :ok-text="t('common.delete')" :cancel-text="t('common.cancel')" @confirm="deleteProject(record)">
                <a-button size="small" type="link" danger>{{ t("common.delete") }}</a-button>
              </a-popconfirm>
            </a-space>
          </template>
        </template>
      </a-table>
    </a-card>

    <a-card size="small" :title="t('projects.historyTitle')">
      <div v-if="!selectedProjectIdModel" style="color: rgba(0, 0, 0, 0.65)">{{ t("common.selectProjectFirst") }}</div>
      <div v-else-if="improvements.length === 0" style="color: rgba(0, 0, 0, 0.65)">
        {{ t("projects.noHistory") }}
      </div>
      <a-space v-else direction="vertical" style="width: 100%" :size="10">
        <a-alert type="info" show-icon :message="improveSummaryText" />
        <a-table :columns="historyColumns" :data-source="historyRows" size="small" :pagination="{ pageSize: 6 }" :scroll="{ x: 900 }" />
      </a-space>
    </a-card>
  </a-space>

  <a-drawer v-model:visible="projectFormVisible" :title="projectFormMode === 'edit' ? t('projects.editTitle') : t('projects.addTitle')" placement="right" :width="520">
    <a-form layout="vertical">
      <a-alert v-if="projectFormError" type="error" show-icon :message="projectFormError" style="margin-bottom: 10px" />
      <a-form-item :label="t('projects.field.id')">
        <a-input v-model:value="projectFormDraft.id" />
      </a-form-item>
      <a-form-item :label="t('projects.field.name')">
        <a-input v-model:value="projectFormDraft.name" />
      </a-form-item>
      <a-form-item :label="t('projects.field.slug')">
        <a-input v-model:value="projectFormDraft.slug_en" />
      </a-form-item>
      <a-form-item :label="t('projects.field.timezone')">
        <a-select v-model:value="projectFormDraft.timezone" style="width: 100%" :options="timezoneOptions" />
      </a-form-item>
      <a-space>
        <a-button type="default" @click="projectFormVisible = false">{{ t("common.cancel") }}</a-button>
        <a-button type="primary" @click="saveProject">{{ t("common.save") }}</a-button>
      </a-space>
    </a-form>
  </a-drawer>

  <a-modal v-model:visible="projectDetailVisible" :title="t('projects.detailTitle')" :footer="null" width="720">
    <pre style="margin: 0; white-space: pre-wrap">{{ JSON.stringify(projectDetail, null, 2) }}</pre>
  </a-modal>
</template>

<script>
import { computed, ref, watch } from "vue";
import { navigateTo } from "../routes.js";
import { useI18n } from "../i18n.js";

export default {
  props: {
    projects: { type: Array, default: () => [] },
    selectedProjectId: { type: String, default: "" },
    workspaceConfig: { type: Object, default: null }
  },
  emits: ["reloadWorkspaceConfig", "saveWorkspaceProjects", "update:selectedProjectId"],
  setup(props, { emit }) {
    const { t } = useI18n();
    const defaultTz =
      (typeof Intl !== "undefined" &&
        Intl.DateTimeFormat &&
        Intl.DateTimeFormat().resolvedOptions &&
        Intl.DateTimeFormat().resolvedOptions().timeZone) ||
      "Asia/Shanghai";
    const timezoneOptions = [
      "Asia/Shanghai",
      "Asia/Singapore",
      "Asia/Tokyo",
      "Asia/Dubai",
      "Europe/London",
      "Europe/Paris",
      "Europe/Berlin",
      "America/New_York",
      "America/Los_Angeles",
      "America/Chicago",
      "Australia/Sydney"
    ].map((tz) => ({ label: tz, value: tz }));

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

    const projectRows = computed(() =>
      projectsSafe.value.map((p, idx) => ({
        key: String((p && p.id) || idx),
        idx,
        id: p && p.id !== undefined && p.id !== null ? String(p.id) : "",
        name: p && p.name !== undefined && p.name !== null ? String(p.name) : "",
        slug_en: p && p.slug_en !== undefined && p.slug_en !== null ? String(p.slug_en) : "",
        timezone: p && p.timezone !== undefined && p.timezone !== null ? String(p.timezone) : "",
        no: p && p.no !== undefined && p.no !== null ? String(p.no) : ""
      }))
    );

    const projectColumns = computed(() => [
      { title: t("projects.col.id"), dataIndex: "id", key: "id", width: 200 },
      { title: t("projects.col.name"), dataIndex: "name", key: "name", width: 200 },
      { title: t("projects.col.slug"), dataIndex: "slug_en", key: "slug_en", width: 200 },
      { title: t("projects.col.timezone"), dataIndex: "timezone", key: "timezone", width: 180 },
      { title: t("projects.col.op"), key: "op", width: 220 }
    ]);

    const projectFormVisible = ref(false);
    const projectFormMode = ref("add");
    const projectFormError = ref("");
    const projectFormDraft = ref({ id: "", name: "", slug_en: "", timezone: defaultTz });
    const projectEditingId = ref("");

    const projectDetailVisible = ref(false);
    const projectDetail = ref(null);

    function openAddProject() {
      projectFormError.value = "";
      projectFormMode.value = "add";
      projectEditingId.value = "";
      projectFormDraft.value = { id: "", name: "", slug_en: "", timezone: defaultTz };
      projectFormVisible.value = true;
    }

    function openEditProject(rec) {
      const r = rec || {};
      projectFormError.value = "";
      projectFormMode.value = "edit";
      projectEditingId.value = String(r.id || "");
      projectFormDraft.value = { id: String(r.id || ""), name: String(r.name || ""), slug_en: String(r.slug_en || ""), timezone: String(r.timezone || defaultTz) };
      projectFormVisible.value = true;
    }

    function openProjectDetail(rec) {
      projectDetail.value = rec || null;
      projectDetailVisible.value = true;
    }

    function saveProject() {
      const id = String(projectFormDraft.value.id || "").trim();
      const name = String(projectFormDraft.value.name || "").trim();
      const slug = String(projectFormDraft.value.slug_en || "").trim();
      const timezone = String(projectFormDraft.value.timezone || "").trim() || defaultTz;
      if (!id) {
        projectFormError.value = t("projects.error.idRequired");
        return;
      }

      const list = projectsSafe.value.slice();
      const existsIdx = list.findIndex((x) => String(x && x.id) === id);

      if (projectFormMode.value === "add") {
        if (existsIdx >= 0) {
          projectFormError.value = t("projects.error.idExists");
          return;
        }
        list.push({ id, name, slug_en: slug, timezone });
        selectedProjectIdModel.value = id;
      } else {
        const editingId = String(projectEditingId.value || "");
        const idx = list.findIndex((x) => String(x && x.id) === editingId);
        if (idx < 0) {
          projectFormError.value = t("projects.error.notFound");
          return;
        }
        if (id !== editingId && existsIdx >= 0) {
          projectFormError.value = t("projects.error.idExists");
          return;
        }
        list.splice(idx, 1, { ...(list[idx] || {}), id, name, slug_en: slug, timezone });
        if (selectedProjectIdModel.value === editingId) selectedProjectIdModel.value = id;
      }

      emit("saveWorkspaceProjects", list);
      projectFormVisible.value = false;
    }

    function deleteProject(rec) {
      const r = rec || {};
      const list = projectsSafe.value.slice();
      const idx = typeof r.idx === "number" ? r.idx : list.findIndex((x) => String(x && x.id) === String(r.id));
      if (idx < 0) return;
      const removedId = String(list[idx] && list[idx].id);
      list.splice(idx, 1);
      emit("saveWorkspaceProjects", list);
      if (selectedProjectIdModel.value === removedId) selectedProjectIdModel.value = String((list[0] && list[0].id) || "example");
    }

    function goActions() {
      navigateTo("actions");
    }

    function reloadWorkspaceConfig() {
      emit("reloadWorkspaceConfig");
    }

function safeParse(jsonText) {
  try {
    const v = JSON.parse(String(jsonText || ""));
    return v && typeof v === "object" ? v : null;
  } catch {
    return null;
  }
}

    const improvements = ref([]);

function loadImprovements() {
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

    watch(selectedProjectIdModel, () => loadImprovements(), { immediate: true });

function pickMetric(metrics, path, fallback) {
  const keys = String(path || "")
    .split(".")
    .map((s) => s.trim())
    .filter(Boolean);
  let cur = metrics;
  for (const k of keys) {
    if (!cur || typeof cur !== "object") return fallback;
    cur = cur[k];
  }
  return cur === undefined ? fallback : cur;
}

function formatDelta(cur, base) {
  const c = typeof cur === "number" ? cur : Number(cur);
  const b = typeof base === "number" ? base : Number(base);
  if (!Number.isFinite(c) || !Number.isFinite(b)) return "—";
  const d = Math.round((c - b) * 1000) / 1000;
  const sign = d > 0 ? "+" : d < 0 ? "" : "";
  return `${sign}${d}`;
}

const improveSummaryText = computed(() => {
  if (!improvements.value.length) return t("common.none");
  const first = improvements.value[0] || {};
  const last = improvements.value[improvements.value.length - 1] || {};
  const fm = first.metrics || {};
  const lm = last.metrics || {};
  const leadBase = pickMetric(fm, "lead_time_p50_days", null);
  const leadCur = pickMetric(lm, "lead_time_p50_days", null);
  const bugBase = pickMetric(fm, "bug_rate", null);
  const bugCur = pickMetric(lm, "bug_rate", null);
  const reopenBase = pickMetric(fm, "reopen_rate", null);
  const reopenCur = pickMetric(lm, "reopen_rate", null);
  const escapedBase = pickMetric(fm, "escaped_defects", null);
  const escapedCur = pickMetric(lm, "escaped_defects", null);
  const throughputBase = pickMetric(fm, "throughput", null);
  const throughputCur = pickMetric(lm, "throughput", null);
  return t("projects.improveSummary", {
    lead: formatDelta(leadCur, leadBase),
    bug: formatDelta(bugCur, bugBase),
    reopen: formatDelta(reopenCur, reopenBase),
    escaped: formatDelta(escapedCur, escapedBase),
    throughput: formatDelta(throughputCur, throughputBase)
  });
});

    const historyRows = computed(() =>
  (improvements.value || [])
    .slice()
    .reverse()
    .map((x, idx) => ({
      key: String(idx),
      at: x && x.at ? String(x.at) : "—",
      window: x && x.window ? String(x.window) : "—",
      plan_total: x && x.plan_summary && x.plan_summary.total !== undefined ? String(x.plan_summary.total) : "—",
      plan_done: x && x.plan_summary && x.plan_summary.done !== undefined ? String(x.plan_summary.done) : "—",
      lead_time_p50_days: x && x.metrics ? pickMetric(x.metrics, "lead_time_p50_days", "—") : "—",
      bug_rate: x && x.metrics ? pickMetric(x.metrics, "bug_rate", "—") : "—",
      reopen_rate: x && x.metrics ? pickMetric(x.metrics, "reopen_rate", "—") : "—",
      escaped_defects: x && x.metrics ? pickMetric(x.metrics, "escaped_defects", "—") : "—",
      throughput: x && x.metrics ? pickMetric(x.metrics, "throughput", "—") : "—"
    }))
    );

    const historyColumns = computed(() => [
      { title: t("projects.history.col.at"), dataIndex: "at", key: "at", width: 200 },
      { title: t("projects.history.col.window"), dataIndex: "window", key: "window", width: 140 },
      { title: t("projects.history.col.plan"), key: "plan", width: 170, customRender: ({ record }) => `${record.plan_done}/${record.plan_total}` },
      { title: t("projects.history.col.lead"), dataIndex: "lead_time_p50_days", key: "lead_time_p50_days", width: 130 },
      { title: t("projects.history.col.bug"), dataIndex: "bug_rate", key: "bug_rate", width: 110 },
      { title: t("projects.history.col.reopen"), dataIndex: "reopen_rate", key: "reopen_rate", width: 110 },
      { title: t("projects.history.col.escaped"), dataIndex: "escaped_defects", key: "escaped_defects", width: 130 },
      { title: t("projects.history.col.throughput"), dataIndex: "throughput", key: "throughput", width: 110 }
    ]);

    return {
      t,
      projectsSafe,
      selectedProjectIdModel,
      projectLabel,
      reloadWorkspaceConfig,
      openAddProject,
      goActions,
      projectColumns,
      projectRows,
      openProjectDetail,
      openEditProject,
      deleteProject,
      projectFormVisible,
      projectFormMode,
      projectFormError,
      projectFormDraft,
      timezoneOptions,
      saveProject,
      projectDetailVisible,
      projectDetail,
      improvements,
      improveSummaryText,
      historyRows,
      historyColumns
    };
  }
};
</script>
