<template>
  <a-space direction="vertical" style="width: 100%" :size="12">
    <a-space wrap align="center">
      <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">{{ t("common.project") }}</span>
      <a-select v-model:value="selectedProjectId" style="min-width: 320px">
        <a-select-option v-for="(p, idx) in projects" :key="String(p.id) + ':' + String(idx)" :value="String(p.id)">
          {{ projectLabel(p, idx) }}
        </a-select-option>
      </a-select>
      <a-button type="default" @click="openAddProject">{{ t("configSystem.action.addProject") }}</a-button>
      <a-button type="primary" @click="exportProjectConfigYaml">{{ t("configSystem.action.saveAndExport") }}</a-button>
      <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">{{ statusText }}</span>
    </a-space>

    <a-form layout="vertical">
      <a-divider style="margin: 8px 0">{{ t("configSystem.section.project") }}</a-divider>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.projectId')"><a-input v-model:value="projectConfig.project.id" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item :label="t('projects.field.timezone')"><a-input v-model:value="projectConfig.project.timezone" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('projects.field.name')"><a-input v-model:value="projectConfig.project.name" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item :label="t('projects.field.slug')"><a-input v-model:value="projectConfig.project.slug_en" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.iterationType')"><a-input v-model:value="projectConfig.project.iteration.type" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item :label="t('configSystem.field.iterationLengthDays')"><a-input-number v-model:value="projectConfig.project.iteration.length_days" :min="1" style="width: 100%" /></a-form-item></a-col>
      </a-row>

      <a-divider style="margin: 8px 0">{{ t("configSystem.section.dataSource") }}</a-divider>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.systemType')"><a-input v-model:value="projectConfig.data_source.system" /></a-form-item></a-col>
        <a-col :span="12"
          ><a-form-item :label="t('configSystem.field.tokenEnv')"><a-input v-model:value="projectConfig.data_source.auth.token_env" /></a-form-item></a-col
        >
      </a-row>
      <a-form-item :label="t('configSystem.field.baseUrl')"><a-input v-model:value="projectConfig.data_source.base_url" /></a-form-item>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.authType')"><a-input v-model:value="projectConfig.data_source.auth.type" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.projectKey')"><a-input v-model:value="projectConfig.data_source.query.project_key" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item :label="t('configSystem.field.boardId')"><a-input v-model:value="projectConfig.data_source.query.board_id" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12">
          <a-form-item :label="t('configSystem.field.issueTypes')">
            <a-select v-model:value="dataIssueTypesModel" mode="tags" style="width: 100%" :token-separators="[',']" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item :label="t('configSystem.field.doneStatuses')">
            <a-select v-model:value="dataDoneStatusesModel" mode="tags" style="width: 100%" :token-separators="[',']" />
          </a-form-item>
        </a-col>
      </a-row>

      <a-divider style="margin: 8px 0">{{ t("configSystem.section.bugSource") }}</a-divider>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.systemType')"><a-input v-model:value="projectConfig.bug_source.system" /></a-form-item></a-col>
        <a-col :span="12"
          ><a-form-item :label="t('configSystem.field.tokenEnv')"><a-input v-model:value="projectConfig.bug_source.auth.token_env" /></a-form-item></a-col
        >
      </a-row>
      <a-form-item :label="t('configSystem.field.baseUrl')"><a-input v-model:value="projectConfig.bug_source.base_url" /></a-form-item>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.authType')"><a-input v-model:value="projectConfig.bug_source.auth.type" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item :label="t('configSystem.field.projectKey')"><a-input v-model:value="projectConfig.bug_source.query.project_key" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12">
          <a-form-item :label="t('configSystem.field.bugIssueTypes')">
            <a-select v-model:value="bugIssueTypesModel" mode="tags" style="width: 100%" :token-separators="[',']" />
          </a-form-item>
        </a-col>
        <a-col :span="12"><a-form-item :label="t('configSystem.field.severityField')"><a-input v-model:value="projectConfig.bug_source.query.severity_field" /></a-form-item></a-col>
      </a-row>
      <a-form-item :label="t('configSystem.field.escapedDefectLabels')">
        <a-select v-model:value="bugEscapedLabelsModel" mode="tags" style="width: 100%" :token-separators="[',']" />
      </a-form-item>

      <a-divider style="margin: 8px 0">{{ t("configSystem.section.gitSource") }}</a-divider>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.systemType')"><a-input v-model:value="projectConfig.git_source.system" /></a-form-item></a-col>
        <a-col :span="12"
          ><a-form-item :label="t('configSystem.field.tokenEnv')"><a-input v-model:value="projectConfig.git_source.auth.token_env" /></a-form-item></a-col
        >
      </a-row>
      <a-form-item :label="t('configSystem.field.apiBaseUrl')"><a-input v-model:value="projectConfig.git_source.base_url" /></a-form-item>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.repoOwner')"><a-input v-model:value="projectConfig.git_source.repo.owner" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item :label="t('configSystem.field.repoName')"><a-input v-model:value="projectConfig.git_source.repo.name" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.authType')"><a-input v-model:value="projectConfig.git_source.auth.type" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item :label="t('configSystem.field.defaultBranch')"><a-input v-model:value="projectConfig.git_source.repo.default_branch" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.sinceDays')"><a-input-number v-model:value="projectConfig.git_source.query.since_days" :min="1" style="width: 100%" /></a-form-item></a-col>
        <a-col :span="12">
          <a-form-item :label="t('configSystem.field.gitInclude')">
            <a-select v-model:value="gitIncludeModel" mode="tags" style="width: 100%" :token-separators="[',']" />
          </a-form-item>
        </a-col>
      </a-row>

      <a-divider style="margin: 8px 0">{{ t("configSystem.section.ciSource") }}</a-divider>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.systemType')"><a-input v-model:value="projectConfig.ci_source.system" /></a-form-item></a-col>
        <a-col :span="12"
          ><a-form-item :label="t('configSystem.field.tokenEnv')"><a-input v-model:value="projectConfig.ci_source.auth.token_env" /></a-form-item></a-col
        >
      </a-row>
      <a-form-item :label="t('configSystem.field.apiBaseUrl')"><a-input v-model:value="projectConfig.ci_source.base_url" /></a-form-item>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.repoOwner')"><a-input v-model:value="projectConfig.ci_source.repo.owner" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item :label="t('configSystem.field.repoName')"><a-input v-model:value="projectConfig.ci_source.repo.name" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.authType')"><a-input v-model:value="projectConfig.ci_source.auth.type" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item :label="t('configSystem.field.sinceDays')"><a-input-number v-model:value="projectConfig.ci_source.query.since_days" :min="1" style="width: 100%" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"
          ><a-form-item :label="t('configSystem.field.buildWorkflow')"><a-input v-model:value="projectConfig.ci_source.pipelines.build_workflow" /></a-form-item></a-col
        >
        <a-col :span="12"
          ><a-form-item :label="t('configSystem.field.codeScanWorkflow')"><a-input v-model:value="projectConfig.ci_source.pipelines.code_scan_workflow" /></a-form-item></a-col
        >
      </a-row>

      <a-divider style="margin: 8px 0">{{ t("configSystem.section.metricsParams") }}</a-divider>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.windowDays')"><a-input-number v-model:value="projectConfig.metrics.window_days" :min="1" style="width: 100%" /></a-form-item></a-col>
        <a-col :span="12">
          <a-form-item :label="t('configSystem.field.percentiles')">
            <a-select v-model:value="metricsPercentilesModel" mode="tags" style="width: 100%" :token-separators="[',']" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item :label="t('configSystem.field.wipStatuses')">
        <a-select v-model:value="metricsWipStatusesModel" mode="tags" style="width: 100%" :token-separators="[',']" />
      </a-form-item>
      <a-divider style="margin: 8px 0">{{ t("configSystem.section.targets") }}</a-divider>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.targetLeadTimeP50')"><a-input-number v-model:value="projectConfig.metrics.targets.lead_time_p50_days" :min="0" style="width: 100%" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item :label="t('configSystem.field.targetCycleTimeP50')"><a-input-number v-model:value="projectConfig.metrics.targets.cycle_time_p50_days" :min="0" style="width: 100%" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.targetWipLimit')"><a-input-number v-model:value="projectConfig.metrics.targets.wip_limit" :min="0" style="width: 100%" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item :label="t('configSystem.field.targetEscapedDefectsMax')"><a-input-number v-model:value="projectConfig.metrics.targets.escaped_defects_max" :min="0" style="width: 100%" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.targetReopenRateMax')"><a-input-number v-model:value="projectConfig.metrics.targets.reopen_rate_max" :min="0" :max="1" :step="0.01" style="width: 100%" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item :label="t('configSystem.field.targetBugRateMax')"><a-input-number v-model:value="projectConfig.metrics.targets.bug_rate_max" :min="0" :max="1" :step="0.01" style="width: 100%" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item :label="t('configSystem.field.targetCiSuccessRateMin')"><a-input-number v-model:value="projectConfig.metrics.targets.ci_success_rate_min" :min="0" :max="1" :step="0.01" style="width: 100%" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item :label="t('configSystem.field.targetCodeScanPassRateMin')"><a-input-number v-model:value="projectConfig.metrics.targets.code_scan_pass_rate_min" :min="0" :max="1" :step="0.01" style="width: 100%" /></a-form-item></a-col>
      </a-row>

      <a-divider style="margin: 8px 0">{{ t("configSystem.section.output") }}</a-divider>
      <a-form-item :label="t('configSystem.field.reportSubdir')"><a-input v-model:value="projectConfig.output.report_subdir" /></a-form-item>
    </a-form>

    <a-drawer v-model:visible="addProjectVisible" :title="t('configSystem.drawer.addProjectTitle')" placement="right" :width="520">
      <a-form layout="vertical">
        <a-alert v-if="addProjectError" type="error" show-icon :message="addProjectError" style="margin-bottom: 10px" />
        <a-form-item :label="t('projects.field.id')">
          <a-input v-model:value="addProjectDraft.id" />
        </a-form-item>
        <a-form-item :label="t('projects.field.name')">
          <a-input v-model:value="addProjectDraft.name" />
        </a-form-item>
        <a-form-item :label="t('projects.field.slug')">
          <a-input v-model:value="addProjectDraft.slug_en" />
        </a-form-item>
        <a-form-item :label="t('projects.field.timezone')">
          <a-select v-model:value="addProjectDraft.timezone" style="width: 100%" :options="timezoneOptions" />
        </a-form-item>
        <a-space>
          <a-button type="default" @click="addProjectVisible = false">{{ t("common.cancel") }}</a-button>
          <a-button type="primary" @click="addProjectOk">{{ t("common.create") }}</a-button>
        </a-space>
      </a-form>
    </a-drawer>
  </a-space>
</template>

<script>
import { computed, ref, watch } from "vue";
import { dump, load } from "js-yaml";
import { useI18n } from "../i18n.js";

export default {
  setup() {
    const { t } = useI18n();
    function safeString(v) {
      return v === undefined || v === null ? "" : String(v);
    }

    function normalizeStringArray(v) {
      return (Array.isArray(v) ? v : [])
        .map((x) => safeString(x).trim())
        .filter(Boolean);
    }

    async function fetchYamlObject(url) {
      try {
        const res = await fetch(url, { cache: "no-store" });
        if (!res.ok) return null;
        const text = await res.text();
        const obj = load(text);
        return obj && typeof obj === "object" ? obj : null;
      } catch {
        return null;
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

    function defaultProjectConfig(pid) {
      return {
        project: {
          id: pid,
          name: "",
          slug_en: "",
          timezone:
            (typeof Intl !== "undefined" &&
              Intl.DateTimeFormat &&
              Intl.DateTimeFormat().resolvedOptions &&
              Intl.DateTimeFormat().resolvedOptions().timeZone) ||
            "Asia/Shanghai",
          iteration: { type: "sprint", length_days: 14 }
        },
        data_source: {
          system: "jira",
          base_url: "",
          auth: { type: "bearer", token_env: "PM_API_TOKEN" },
          query: { project_key: "", board_id: "", issue_types: ["Story", "Bug", "Task"], done_statuses: ["Done", "Closed"] }
        },
        bug_source: {
          system: "jira",
          base_url: "",
          auth: { type: "bearer", token_env: "BUG_API_TOKEN" },
          query: { project_key: "", issue_types: ["Bug"], escaped_defect_labels: ["production", "escaped"], severity_field: "priority.name" }
        },
        git_source: {
          system: "github",
          base_url: "https://api.github.com",
          auth: { type: "token", token_env: "GIT_API_TOKEN" },
          repo: { owner: "", name: "", default_branch: "main" },
          query: { since_days: 30, include: ["commits", "pull_requests", "reviews"] }
        },
        ci_source: {
          system: "github_actions",
          base_url: "https://api.github.com",
          auth: { type: "token", token_env: "CI_API_TOKEN" },
          repo: { owner: "", name: "" },
          query: { since_days: 30 },
          pipelines: { build_workflow: "ci.yml", code_scan_workflow: "code-scan.yml" }
        },
        metrics: {
          window_days: 30,
          wip_statuses: ["In Progress", "Review", "Testing"],
          percentiles: [50, 75, 95],
          targets: {}
        },
        output: { report_subdir: "project-metrics-orid" }
      };
    }

    const statusText = ref("");
    const fallbackProjects = [{ id: "example", name: "example-project", slug_en: "example-project" }];
    const projectsConfig = ref({ projects: fallbackProjects });
    const projects = computed(() => (projectsConfig.value && Array.isArray(projectsConfig.value.projects) ? projectsConfig.value.projects : fallbackProjects));
    const selectedProjectId = ref("example");

    const addProjectVisible = ref(false);
    const addProjectError = ref("");
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
    const addProjectDraft = ref({ id: "", name: "", slug_en: "", timezone: defaultTz });

    const projectConfig = ref(defaultProjectConfig("example"));

    function projectLabel(p, idx) {
      const id = p && p.id !== undefined && p.id !== null ? String(p.id).trim() : "";
      const name = p && p.name !== undefined && p.name !== null ? String(p.name).trim() : "";
      return `${id || String(idx + 1)} · ${name || t("common.unnamed")}`;
    }

    const dataIssueTypesModel = computed({
      get: () =>
        normalizeStringArray(projectConfig.value && projectConfig.value.data_source && projectConfig.value.data_source.query && projectConfig.value.data_source.query.issue_types),
      set: (v) => {
        if (!projectConfig.value.data_source.query) projectConfig.value.data_source.query = {};
        projectConfig.value.data_source.query.issue_types = normalizeStringArray(v);
      }
    });
    const dataDoneStatusesModel = computed({
      get: () =>
        normalizeStringArray(projectConfig.value && projectConfig.value.data_source && projectConfig.value.data_source.query && projectConfig.value.data_source.query.done_statuses),
      set: (v) => {
        if (!projectConfig.value.data_source.query) projectConfig.value.data_source.query = {};
        projectConfig.value.data_source.query.done_statuses = normalizeStringArray(v);
      }
    });
    const bugIssueTypesModel = computed({
      get: () =>
        normalizeStringArray(projectConfig.value && projectConfig.value.bug_source && projectConfig.value.bug_source.query && projectConfig.value.bug_source.query.issue_types),
      set: (v) => {
        if (!projectConfig.value.bug_source.query) projectConfig.value.bug_source.query = {};
        projectConfig.value.bug_source.query.issue_types = normalizeStringArray(v);
      }
    });
    const bugEscapedLabelsModel = computed({
      get: () =>
        normalizeStringArray(
          projectConfig.value && projectConfig.value.bug_source && projectConfig.value.bug_source.query && projectConfig.value.bug_source.query.escaped_defect_labels
        ),
      set: (v) => {
        if (!projectConfig.value.bug_source.query) projectConfig.value.bug_source.query = {};
        projectConfig.value.bug_source.query.escaped_defect_labels = normalizeStringArray(v);
      }
    });
    const gitIncludeModel = computed({
      get: () => normalizeStringArray(projectConfig.value && projectConfig.value.git_source && projectConfig.value.git_source.query && projectConfig.value.git_source.query.include),
      set: (v) => {
        if (!projectConfig.value.git_source.query) projectConfig.value.git_source.query = {};
        projectConfig.value.git_source.query.include = normalizeStringArray(v);
      }
    });
    const metricsWipStatusesModel = computed({
      get: () => normalizeStringArray(projectConfig.value && projectConfig.value.metrics && projectConfig.value.metrics.wip_statuses),
      set: (v) => {
        if (!projectConfig.value.metrics) projectConfig.value.metrics = {};
        projectConfig.value.metrics.wip_statuses = normalizeStringArray(v);
      }
    });
    const metricsPercentilesModel = computed({
      get: () => normalizeStringArray(projectConfig.value && projectConfig.value.metrics && projectConfig.value.metrics.percentiles).map((x) => String(x)),
      set: (v) => {
        if (!projectConfig.value.metrics) projectConfig.value.metrics = {};
        const nums = normalizeStringArray(v)
          .map((x) => Number(x))
          .filter((n) => Number.isFinite(n));
        projectConfig.value.metrics.percentiles = nums;
      }
    });

    async function loadProjectsRegistry() {
      const obj = await fetchYamlObject("/work/meta/config.yaml");
      const next = obj && typeof obj === "object" ? obj : { projects: [] };
      if (!Array.isArray(next.projects) || next.projects.length === 0) next.projects = fallbackProjects;
      projectsConfig.value = next;
      const first = projects.value[0];
      selectedProjectId.value = (first && String(first.id)) || "example";
    }

    function buildProjectConfig() {
      const pid = selectedProjectId.value || "example";
      const base = defaultProjectConfig(pid);
      const fromRegistry = projects.value.find((p) => String(p.id) === String(pid)) || null;
      if (fromRegistry) {
        base.project.id = safeString(fromRegistry.id) || pid;
        base.project.name = safeString(fromRegistry.name);
        base.project.slug_en = safeString(fromRegistry.slug_en);
      }
      projectConfig.value = base;
    }

    function exportProjectConfigYaml() {
      const pid = selectedProjectId.value || "example";
      const text = dump(projectConfig.value || {}, { lineWidth: 120 });
      downloadText("config.yaml", text, "text/yaml");
      statusText.value = t("configSystem.status.exported", { pid });
    }

    function openAddProject() {
      addProjectError.value = "";
      addProjectDraft.value = { id: "", name: "", slug_en: "", timezone: defaultTz };
      addProjectVisible.value = true;
    }

    function addProjectOk() {
      const id = safeString(addProjectDraft.value.id).trim();
      if (!id) {
        addProjectError.value = t("configSystem.error.projectIdRequired");
        return;
      }
      const p = { id, name: safeString(addProjectDraft.value.name).trim(), slug_en: safeString(addProjectDraft.value.slug_en).trim() };
      if (!projectsConfig.value || typeof projectsConfig.value !== "object") projectsConfig.value = { projects: [] };
      if (!Array.isArray(projectsConfig.value.projects)) projectsConfig.value.projects = [];
      projectsConfig.value.projects.push(p);
      selectedProjectId.value = id;
      projectConfig.value = defaultProjectConfig(id);
      projectConfig.value.project.name = p.name;
      projectConfig.value.project.slug_en = p.slug_en;
      projectConfig.value.project.timezone = safeString(addProjectDraft.value.timezone || defaultTz) || defaultTz;
      addProjectVisible.value = false;
      statusText.value = t("configSystem.status.addedProject");
    }

    watch(selectedProjectId, () => buildProjectConfig());
    loadProjectsRegistry().then(buildProjectConfig);

    return {
      t,
      statusText,
      projects,
      selectedProjectId,
      projectLabel,
      openAddProject,
      exportProjectConfigYaml,
      projectConfig,
      addProjectVisible,
      addProjectError,
      addProjectDraft,
      timezoneOptions,
      addProjectOk,
      dataIssueTypesModel,
      dataDoneStatusesModel,
      bugIssueTypesModel,
      bugEscapedLabelsModel,
      gitIncludeModel,
      metricsWipStatusesModel,
      metricsPercentilesModel
    };
  }
};
</script>
