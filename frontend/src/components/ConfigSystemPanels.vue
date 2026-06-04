<template>
  <a-space direction="vertical" style="width: 100%" :size="12">
    <a-space wrap align="center">
      <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">项目</span>
      <a-select v-model:value="selectedProjectId" style="min-width: 320px">
        <a-select-option v-for="(p, idx) in projects" :key="String(p.id) + ':' + String(idx)" :value="String(p.id)">
          {{ String(p.id) }} · {{ String(p.name || "") }}
        </a-select-option>
      </a-select>
      <a-button type="default" @click="openAddProject">添加项目</a-button>
      <a-button type="primary" @click="exportProjectConfigYaml">保存并导出</a-button>
      <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">{{ statusText }}</span>
    </a-space>

    <a-form layout="vertical">
      <a-divider style="margin: 8px 0">项目</a-divider>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="项目ID"><a-input v-model:value="projectConfig.project.id" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item label="时区"><a-input v-model:value="projectConfig.project.timezone" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="项目名称"><a-input v-model:value="projectConfig.project.name" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item label="英文名（slug_en）"><a-input v-model:value="projectConfig.project.slug_en" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="迭代类型"><a-input v-model:value="projectConfig.project.iteration.type" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item label="迭代周期（天）"><a-input-number v-model:value="projectConfig.project.iteration.length_days" :min="1" style="width: 100%" /></a-form-item></a-col>
      </a-row>

      <a-divider style="margin: 8px 0">项目管理系统（data_source）</a-divider>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="系统类型"><a-input v-model:value="projectConfig.data_source.system" /></a-form-item></a-col>
        <a-col :span="12"
          ><a-form-item label="鉴权Token环境变量（token_env）"><a-input v-model:value="projectConfig.data_source.auth.token_env" /></a-form-item></a-col
        >
      </a-row>
      <a-form-item label="服务地址（base_url）"><a-input v-model:value="projectConfig.data_source.base_url" /></a-form-item>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="鉴权方式（auth.type）"><a-input v-model:value="projectConfig.data_source.auth.type" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="项目Key（project_key）"><a-input v-model:value="projectConfig.data_source.query.project_key" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item label="看板ID（board_id）"><a-input v-model:value="projectConfig.data_source.query.board_id" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12">
          <a-form-item label="需求类型（issue_types）">
            <a-select v-model:value="dataIssueTypesModel" mode="tags" style="width: 100%" :token-separators="[',']" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="完成状态集合（done_statuses）">
            <a-select v-model:value="dataDoneStatusesModel" mode="tags" style="width: 100%" :token-separators="[',']" />
          </a-form-item>
        </a-col>
      </a-row>

      <a-divider style="margin: 8px 0">缺陷系统（bug_source）</a-divider>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="系统类型"><a-input v-model:value="projectConfig.bug_source.system" /></a-form-item></a-col>
        <a-col :span="12"
          ><a-form-item label="鉴权Token环境变量（token_env）"><a-input v-model:value="projectConfig.bug_source.auth.token_env" /></a-form-item></a-col
        >
      </a-row>
      <a-form-item label="服务地址（base_url）"><a-input v-model:value="projectConfig.bug_source.base_url" /></a-form-item>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="鉴权方式（auth.type）"><a-input v-model:value="projectConfig.bug_source.auth.type" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item label="项目Key（project_key）"><a-input v-model:value="projectConfig.bug_source.query.project_key" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12">
          <a-form-item label="缺陷类型（issue_types）">
            <a-select v-model:value="bugIssueTypesModel" mode="tags" style="width: 100%" :token-separators="[',']" />
          </a-form-item>
        </a-col>
        <a-col :span="12"><a-form-item label="严重级别字段（severity_field）"><a-input v-model:value="projectConfig.bug_source.query.severity_field" /></a-form-item></a-col>
      </a-row>
      <a-form-item label="线上逃逸标签（escaped_defect_labels）">
        <a-select v-model:value="bugEscapedLabelsModel" mode="tags" style="width: 100%" :token-separators="[',']" />
      </a-form-item>

      <a-divider style="margin: 8px 0">代码仓库（git_source）</a-divider>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="系统类型"><a-input v-model:value="projectConfig.git_source.system" /></a-form-item></a-col>
        <a-col :span="12"
          ><a-form-item label="鉴权Token环境变量（token_env）"><a-input v-model:value="projectConfig.git_source.auth.token_env" /></a-form-item></a-col
        >
      </a-row>
      <a-form-item label="API地址（base_url）"><a-input v-model:value="projectConfig.git_source.base_url" /></a-form-item>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="仓库Owner（repo.owner）"><a-input v-model:value="projectConfig.git_source.repo.owner" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item label="仓库名称（repo.name）"><a-input v-model:value="projectConfig.git_source.repo.name" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="鉴权方式（auth.type）"><a-input v-model:value="projectConfig.git_source.auth.type" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item label="默认分支（repo.default_branch）"><a-input v-model:value="projectConfig.git_source.repo.default_branch" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="拉取时间窗（天）（query.since_days）"><a-input-number v-model:value="projectConfig.git_source.query.since_days" :min="1" style="width: 100%" /></a-form-item></a-col>
        <a-col :span="12">
          <a-form-item label="拉取范围（query.include）">
            <a-select v-model:value="gitIncludeModel" mode="tags" style="width: 100%" :token-separators="[',']" />
          </a-form-item>
        </a-col>
      </a-row>

      <a-divider style="margin: 8px 0">持续集成（ci_source）</a-divider>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="系统类型"><a-input v-model:value="projectConfig.ci_source.system" /></a-form-item></a-col>
        <a-col :span="12"
          ><a-form-item label="鉴权Token环境变量（token_env）"><a-input v-model:value="projectConfig.ci_source.auth.token_env" /></a-form-item></a-col
        >
      </a-row>
      <a-form-item label="API地址（base_url）"><a-input v-model:value="projectConfig.ci_source.base_url" /></a-form-item>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="仓库Owner（repo.owner）"><a-input v-model:value="projectConfig.ci_source.repo.owner" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item label="仓库名称（repo.name）"><a-input v-model:value="projectConfig.ci_source.repo.name" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="鉴权方式（auth.type）"><a-input v-model:value="projectConfig.ci_source.auth.type" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item label="拉取时间窗（天）（query.since_days）"><a-input-number v-model:value="projectConfig.ci_source.query.since_days" :min="1" style="width: 100%" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"
          ><a-form-item label="构建流水线（build_workflow）"><a-input v-model:value="projectConfig.ci_source.pipelines.build_workflow" /></a-form-item></a-col
        >
        <a-col :span="12"
          ><a-form-item label="扫描流水线（code_scan_workflow）"><a-input v-model:value="projectConfig.ci_source.pipelines.code_scan_workflow" /></a-form-item></a-col
        >
      </a-row>

      <a-divider style="margin: 8px 0">度量计算参数（metrics）</a-divider>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="统计窗口（天）（window_days）"><a-input-number v-model:value="projectConfig.metrics.window_days" :min="1" style="width: 100%" /></a-form-item></a-col>
        <a-col :span="12">
          <a-form-item label="分位数（percentiles）">
            <a-select v-model:value="metricsPercentilesModel" mode="tags" style="width: 100%" :token-separators="[',']" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item label="在制状态集合（wip_statuses）">
        <a-select v-model:value="metricsWipStatusesModel" mode="tags" style="width: 100%" :token-separators="[',']" />
      </a-form-item>
      <a-divider style="margin: 8px 0">目标阈值（metrics.targets）</a-divider>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="交付周期p50目标（天）（lead_time_p50_days）"><a-input-number v-model:value="projectConfig.metrics.targets.lead_time_p50_days" :min="0" style="width: 100%" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item label="处理周期p50目标（天）（cycle_time_p50_days）"><a-input-number v-model:value="projectConfig.metrics.targets.cycle_time_p50_days" :min="0" style="width: 100%" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="WIP上限（wip_limit）"><a-input-number v-model:value="projectConfig.metrics.targets.wip_limit" :min="0" style="width: 100%" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item label="逃逸缺陷数量上限（escaped_defects_max）"><a-input-number v-model:value="projectConfig.metrics.targets.escaped_defects_max" :min="0" style="width: 100%" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="重开率上限（reopen_rate_max）"><a-input-number v-model:value="projectConfig.metrics.targets.reopen_rate_max" :min="0" :max="1" :step="0.01" style="width: 100%" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item label="缺陷率上限（bug_rate_max）"><a-input-number v-model:value="projectConfig.metrics.targets.bug_rate_max" :min="0" :max="1" :step="0.01" style="width: 100%" /></a-form-item></a-col>
      </a-row>
      <a-row :gutter="[12, 12]">
        <a-col :span="12"><a-form-item label="CI成功率下限（ci_success_rate_min）"><a-input-number v-model:value="projectConfig.metrics.targets.ci_success_rate_min" :min="0" :max="1" :step="0.01" style="width: 100%" /></a-form-item></a-col>
        <a-col :span="12"><a-form-item label="扫描通过率下限（code_scan_pass_rate_min）"><a-input-number v-model:value="projectConfig.metrics.targets.code_scan_pass_rate_min" :min="0" :max="1" :step="0.01" style="width: 100%" /></a-form-item></a-col>
      </a-row>

      <a-divider style="margin: 8px 0">输出（output）</a-divider>
      <a-form-item label="报告输出目录名（report_subdir）"><a-input v-model:value="projectConfig.output.report_subdir" /></a-form-item>
    </a-form>

    <a-drawer v-model:visible="addProjectVisible" title="添加项目" placement="right" :width="520">
      <a-form layout="vertical">
        <a-alert v-if="addProjectError" type="error" show-icon :message="addProjectError" style="margin-bottom: 10px" />
        <a-form-item label="项目 ID">
          <a-input v-model:value="addProjectDraft.id" />
        </a-form-item>
        <a-form-item label="项目名称">
          <a-input v-model:value="addProjectDraft.name" />
        </a-form-item>
        <a-form-item label="英文名（slug_en）">
          <a-input v-model:value="addProjectDraft.slug_en" />
        </a-form-item>
        <a-form-item label="时区">
          <a-select v-model:value="addProjectDraft.timezone" style="width: 100%" :options="timezoneOptions" />
        </a-form-item>
        <a-space>
          <a-button type="default" @click="addProjectVisible = false">取消</a-button>
          <a-button type="primary" @click="addProjectOk">添加</a-button>
        </a-space>
      </a-form>
    </a-drawer>
  </a-space>
</template>

<script>
import { computed, ref, watch } from "vue";
import { dump, load } from "js-yaml";

export default {
  setup() {
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
      statusText.value = `已导出 config.yaml（放到 work/${pid}/meta/config.yaml）`;
    }

    function openAddProject() {
      addProjectError.value = "";
      addProjectDraft.value = { id: "", name: "", slug_en: "", timezone: defaultTz };
      addProjectVisible.value = true;
    }

    function addProjectOk() {
      const id = safeString(addProjectDraft.value.id).trim();
      if (!id) {
        addProjectError.value = "项目 id 不能为空";
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
      statusText.value = "已添加项目（列表仅在本次会话内，持久化请手工维护 work/meta/config.yaml）";
    }

    watch(selectedProjectId, () => buildProjectConfig());
    loadProjectsRegistry().then(buildProjectConfig);

    return {
      statusText,
      projects,
      selectedProjectId,
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
