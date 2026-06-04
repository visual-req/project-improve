<template>
  <a-space direction="vertical" style="width: 100%" :size="12">
    <a-space wrap align="center">
      <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">{{ t("common.project") }}</span>
      <a-select v-model:value="selectedProjectIdModel" style="min-width: 320px">
        <a-select-option v-for="(p, idx) in projects" :key="String(p.id) + ':' + String(idx)" :value="String(p.id)">
          {{ projectLabel(p, idx) }}
        </a-select-option>
      </a-select>
      <a-button type="default" @click="emit('reloadProjects')">{{ t("common.reloadProjects") }}</a-button>
      <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">{{ statusText }}</span>
    </a-space>

    <a-alert v-if="errorText" type="error" show-icon :message="errorText" />

    <a-tabs v-model:activeKey="activeStep">
      <a-tab-pane key="collect" :tab="t('analysis.tabs.collect')">
        <AnalysisCollectTab
          :selectedProjectIdModel="selectedProjectIdModel"
          :requestRunSkill="requestRunSkill"
          :collectError="collectError"
          :collectHasRaw="collectHasRaw"
          :collectIntegrity="collectIntegrity"
          :enabledMetricKeys="enabledMetricKeys"
          :requiredSourcesText="requiredSourcesText"
          :requiredSourceTags="requiredSourceTags"
          :collectViz="collectViz"
          :simpleCountColumns="simpleCountColumns"
        />
      </a-tab-pane>

      <a-tab-pane key="metrics" :tab="t('analysis.tabs.metrics')">
        <AnalysisMetricsTab
          :selectedProjectIdModel="selectedProjectIdModel"
          :requestRunSkill="requestRunSkill"
          :metricsError="metricsError"
          :metricsData="metricsData"
          :enabledMetricKeys="enabledMetricKeys"
        />
      </a-tab-pane>

      <a-tab-pane key="orid" :tab="t('analysis.tabs.orid')">
        <AnalysisOridTab
          :selectedProjectIdModel="selectedProjectIdModel"
          :requestRunSkill="requestRunSkill"
          :oridError="oridError"
          :reportData="reportData"
          :metricsData="metricsData"
          :enabledMetricKeys="enabledMetricKeys"
          :collectViz="collectViz"
        />
      </a-tab-pane>
    </a-tabs>

    <AnalysisRunModal
      v-model:visible="runVisible"
      :title="runTitle"
      :tip="runTip"
      :progress="runProgress"
      :logLatestUrl="runLogLatestUrl"
      :logText="runLogText"
      @cancel="cancelRun"
    />
  </a-space>
</template>

<script>
import { computed, onMounted, ref, watch } from "vue";
import { message } from "ant-design-vue";
import { useI18n } from "../i18n.js";
import AnalysisCollectTab from "../components/analysis/AnalysisCollectTab.vue";
import AnalysisMetricsTab from "../components/analysis/AnalysisMetricsTab.vue";
import AnalysisOridTab from "../components/analysis/AnalysisOridTab.vue";
import AnalysisRunModal from "../components/analysis/AnalysisRunModal.vue";

export default {
  components: { AnalysisCollectTab, AnalysisMetricsTab, AnalysisOridTab, AnalysisRunModal },
  props: {
    projects: { type: Array, default: () => [] },
    selectedProjectId: { type: String, default: "" }
  },
  emits: ["reloadProjects", "update:selectedProjectId"],
  setup(props, { emit }) {
    const { t } = useI18n();
    const projects = computed(() => (Array.isArray(props.projects) ? props.projects : []));

    const selectedProjectIdModel = computed({
      get: () => String(props.selectedProjectId || ""),
      set: (v) => emit("update:selectedProjectId", v === undefined || v === null ? "" : String(v))
    });

async function fetchJson(url) {
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) throw new Error(`${url}（${res.status}）`);
  const contentType = String(res.headers.get("content-type") || "").toLowerCase();
  try {
    const parsed = await res.json();
    if (!parsed || typeof parsed !== "object") throw new Error(`${url} 不是对象`);
    return parsed;
  } catch (e) {
    let head = "";
    try {
      const text = await res.text();
      head = String(text || "").slice(0, 160);
    } catch {}
    const hint = contentType.includes("text/html") || head.includes("<!doctype") || head.includes("<html") ? "（返回了 HTML，可能服务走了 SPA fallback / 端口不对）" : "";
    throw new Error(`${url} JSON 解析失败${hint}`);
  }
}

async function fetchJsonOptional(url) {
  const res = await fetch(url, { cache: "no-store" });
  if (res.status === 404) return null;
  if (!res.ok) throw new Error(`${url}（${res.status}）`);
  const contentType = String(res.headers.get("content-type") || "").toLowerCase();
  try {
    const parsed = await res.json();
    if (!parsed || typeof parsed !== "object") throw new Error(`${url} 不是对象`);
    return parsed;
  } catch {
    let head = "";
    try {
      const text = await res.text();
      head = String(text || "").slice(0, 160);
    } catch {}
    const hint = contentType.includes("text/html") || head.includes("<!doctype") || head.includes("<html") ? "（返回了 HTML，可能服务走了 SPA fallback / 端口不对）" : "";
    throw new Error(`${url} JSON 解析失败${hint}`);
  }
}

async function postJson(url, payload) {
  const res = await fetch(url, {
    method: "POST",
    cache: "no-store",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify(payload || {})
  });
  if (!res.ok) throw new Error(`${url}（${res.status}）`);
  try {
    return await res.json();
  } catch {
    return null;
  }
}

async function copyText(text) {
  const t = String(text || "");
  try {
    if (navigator && navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(t);
      return;
    }
  } catch {}
  const ta = document.createElement("textarea");
  ta.value = t;
  ta.setAttribute("readonly", "true");
  ta.style.position = "fixed";
  ta.style.top = "-1000px";
  document.body.appendChild(ta);
  ta.select();
  document.execCommand("copy");
  ta.remove();
}

const activeStep = ref("collect");
const statusText = ref("");
const errorText = ref("");

function projectLabel(p, idx) {
  const id = p && p.id !== undefined && p.id !== null ? String(p.id).trim() : "";
  const name = p && p.name !== undefined && p.name !== null ? String(p.name).trim() : "";
  return `${id || String(idx + 1)} · ${name || "未命名"}`;
}

const collectHasRaw = ref(false);
const collectIntegrity = ref(null);
const collectViz = ref({
  sources: { jira_issues: null, git_commits: null, git_pull_requests: null, ci_runs: null },
  issueStatus: [],
  prStates: [],
  ciStates: [],
  swimlane: { columns: [], blocked_count: 0, threshold_days: 0, top_blocked: [] },
  burndown: { sprint: { start_date: "", end_date: "", total_points: null }, series: [], verdict: "" },
  gantt: { tasks: [], delayed_count: 0, risky_count: 0 }
});
const metricsData = ref(null);
const reportData = ref(null);
const collectError = ref("");
const metricsError = ref("");
const oridError = ref("");

function cacheKey(pid, kind) {
  const p = String(pid || "").trim() || "example";
  return `prjmx.cache.analysis.${p}.${String(kind || "")}`;
}

function defaultCollectViz() {
  return {
    sources: { jira_issues: null, git_commits: null, git_pull_requests: null, ci_runs: null },
    issueStatus: [],
    prStates: [],
    ciStates: [],
    swimlane: { columns: [], blocked_count: 0, threshold_days: 0, top_blocked: [] },
    burndown: { sprint: { start_date: "", end_date: "", total_points: null }, series: [], verdict: "" },
    gantt: { tasks: [], delayed_count: 0, risky_count: 0 }
  };
}

function applyCachedOutputs(pid) {
  const p = String(pid || "").trim() || "example";
  collectError.value = "";
  metricsError.value = "";
  oridError.value = "";

  try {
    const raw = window.localStorage.getItem(cacheKey(p, "collect"));
    const parsed = raw ? JSON.parse(raw) : null;
    if (parsed && typeof parsed === "object") {
      collectHasRaw.value = parsed.collectHasRaw === true;
      collectIntegrity.value = parsed.collectIntegrity && typeof parsed.collectIntegrity === "object" ? parsed.collectIntegrity : null;
      collectViz.value = parsed.collectViz && typeof parsed.collectViz === "object" ? parsed.collectViz : defaultCollectViz();
    } else {
      collectHasRaw.value = false;
      collectIntegrity.value = null;
      collectViz.value = defaultCollectViz();
    }
  } catch {
    collectHasRaw.value = false;
    collectIntegrity.value = null;
    collectViz.value = defaultCollectViz();
  }

  try {
    const raw = window.localStorage.getItem(cacheKey(p, "metrics"));
    const parsed = raw ? JSON.parse(raw) : null;
    metricsData.value = parsed && typeof parsed === "object" ? parsed : null;
  } catch {
    metricsData.value = null;
  }

  try {
    const raw = window.localStorage.getItem(cacheKey(p, "orid"));
    const parsed = raw ? JSON.parse(raw) : null;
    reportData.value = parsed && typeof parsed === "object" ? parsed : null;
  } catch {
    reportData.value = null;
  }
}

function persistCachedOutputs(pid) {
  const p = String(pid || "").trim() || "example";
  try {
    window.localStorage.setItem(
      cacheKey(p, "collect"),
      JSON.stringify({ collectHasRaw: !!collectHasRaw.value, collectIntegrity: collectIntegrity.value, collectViz: collectViz.value })
    );
  } catch {}
  try {
    if (metricsData.value) window.localStorage.setItem(cacheKey(p, "metrics"), JSON.stringify(metricsData.value));
  } catch {}
  try {
    if (reportData.value) window.localStorage.setItem(cacheKey(p, "orid"), JSON.stringify(reportData.value));
  } catch {}
}

const simpleCountColumns = [
  { title: "分类", dataIndex: "label", key: "label" },
  { title: "数量", dataIndex: "count", key: "count", width: 90 }
];

const DEFAULT_ENABLED_KEYS = [
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
];

function loadEnabledMetricKeysFromStorage() {
  const pid = String(selectedProjectIdModel.value || "").trim() || "example";
  try {
    const raw = window.localStorage.getItem(`prjmx.metricsConfig.${pid}`);
    if (!raw) return DEFAULT_ENABLED_KEYS.slice();
    const parsed = JSON.parse(raw);
    const enabled = parsed && parsed.enabled && typeof parsed.enabled === "object" ? parsed.enabled : null;
    if (!enabled) return DEFAULT_ENABLED_KEYS.slice();
    return Object.keys(enabled).filter((k) => enabled[k] === true);
  } catch {
    return DEFAULT_ENABLED_KEYS.slice();
  }
}

function requiredSourcesFromMetrics(keys) {
  const need = { jira: false, git_commits: false, git_pull_requests: false, ci_runs: false };
  const list = Array.isArray(keys) ? keys : [];
  for (const k0 of list) {
    const k = String(k0 || "");
    if (
      k === "throughput" ||
      k === "wip_avg" ||
      k === "aging_wip" ||
      k.startsWith("lead_time") ||
      k.startsWith("cycle_time") ||
      k.startsWith("delivery_cycle_time") ||
      k === "commitment_reliability" ||
      k === "carryover_rate" ||
      k === "requirement_change_rate" ||
      k === "bug_rate" ||
      k === "reopen_rate" ||
      k.includes("defect") ||
      k.includes("defects")
    ) {
      need.jira = true;
    }
    if (k.startsWith("pr_") || k.startsWith("review_latency")) need.git_pull_requests = true;
    if (k.includes("commit")) need.git_commits = true;
    if (k.startsWith("ci_") || k === "code_scan_pass_rate" || k.includes("deployment") || k.includes("mttr") || k.includes("change_failure")) need.ci_runs = true;
  }
  if (!list.length) need.jira = true;
  return need;
}

const enabledMetricKeys = computed(() => loadEnabledMetricKeysFromStorage());
const requiredSources = computed(() => requiredSourcesFromMetrics(enabledMetricKeys.value));
const requiredSourceTags = computed(() => {
  const s = requiredSources.value || {};
  const tags = [];
  if (s.jira) tags.push("Jira 工作项");
  if (s.git_commits) tags.push("Git 提交");
  if (s.git_pull_requests) tags.push("PR/评审");
  if (s.ci_runs) tags.push("CI");
  return tags.length ? tags : ["Jira 工作项"];
});
const requiredSourcesText = computed(() => requiredSourceTags.value.join(" + "));

function countBy(items, pick) {
  const arr = Array.isArray(items) ? items : [];
  const m = new Map();
  for (const it of arr) {
    const key = String(pick(it) || "—");
    m.set(key, (m.get(key) || 0) + 1);
  }
  return Array.from(m.entries())
    .map(([label, count]) => ({ key: label, label, count }))
    .sort((a, b) => b.count - a.count);
}

function daysBetween(isoA, isoB) {
  const a = Date.parse(String(isoA || ""));
  const b = Date.parse(String(isoB || ""));
  if (!Number.isFinite(a) || !Number.isFinite(b)) return null;
  return Math.round((b - a) / (24 * 3600 * 1000));
}

function daysSince(iso) {
  const a = Date.parse(String(iso || ""));
  if (!Number.isFinite(a)) return null;
  const now = Date.now();
  return Math.round((now - a) / (24 * 3600 * 1000));
}

function computeSwimlane(issues) {
  const cols = ["To Do", "In Progress", "Review", "Done"];
  const colCounts = cols.reduce((acc, c) => ((acc[c] = 0), acc), {});
  const thresholdDays = 4;
  const blocked = [];
  for (const it of Array.isArray(issues) ? issues : []) {
    const status = String(it && it.status ? it.status : "—");
    if (colCounts[status] !== undefined) colCounts[status] += 1;
    const startedAt = it && (it.started_at || it.startedAt) ? String(it.started_at || it.startedAt) : "";
    const aging = (status === "In Progress" || status === "Review") && startedAt ? daysSince(startedAt) : null;
    if (aging !== null && Number.isFinite(aging) && aging >= thresholdDays) {
      blocked.push({
        key: String(it && it.key ? it.key : ""),
        summary: String(it && it.summary ? it.summary : ""),
        status,
        aging_days: aging
      });
    }
  }
  blocked.sort((a, b) => (b.aging_days || 0) - (a.aging_days || 0));
  const columns = cols.map((c) => ({ key: c, label: c, count: colCounts[c] || 0 }));
  return { columns, blocked_count: blocked.length, threshold_days: thresholdDays, top_blocked: blocked.slice(0, 6) };
}

function computeBurndown(planning) {
  const p = planning && typeof planning === "object" ? planning : {};
  const sprint = p.sprint && typeof p.sprint === "object" ? p.sprint : {};
  const series = (p.burndown && p.burndown.series && Array.isArray(p.burndown.series) ? p.burndown.series : []).map((x, idx) => ({
    key: String(x && x.date ? x.date : idx),
    date: String(x && x.date ? x.date : ""),
    ideal_remaining_points: x && x.ideal_remaining_points !== undefined ? Number(x.ideal_remaining_points) : null,
    remaining_points: x && x.remaining_points !== undefined ? Number(x.remaining_points) : null
  }));
  let verdict = "";
  const last = series.length ? series[series.length - 1] : null;
  if (last && Number.isFinite(last.remaining_points) && Number.isFinite(last.ideal_remaining_points)) {
    if (last.remaining_points <= last.ideal_remaining_points) verdict = "领先";
    else if (last.remaining_points <= last.ideal_remaining_points + 2) verdict = "合理";
    else verdict = "偏慢";
  }
  return {
    sprint: { start_date: String(sprint.start_date || ""), end_date: String(sprint.end_date || ""), total_points: sprint.total_points ?? null },
    series,
    verdict
  };
}

function computeGantt(planning) {
  const p = planning && typeof planning === "object" ? planning : {};
  const tasksRaw = p.gantt && p.gantt.tasks && Array.isArray(p.gantt.tasks) ? p.gantt.tasks : [];
  const nowIso = new Date().toISOString().slice(0, 10);
  const tasks = tasksRaw.map((t, idx) => {
    const plannedEnd = t && t.planned_end ? String(t.planned_end) : "";
    const actualEnd = t && t.actual_end ? String(t.actual_end) : "";
    const delay = plannedEnd && actualEnd ? Math.max(0, daysBetween(plannedEnd, actualEnd) || 0) : 0;
    const risky = plannedEnd && !actualEnd && (daysBetween(plannedEnd, nowIso) || 0) > 0;
    return {
      key: String(t && t.id ? t.id : idx),
      id: t && t.id ? String(t.id) : "",
      name: t && t.name ? String(t.name) : "",
      planned_start: t && t.planned_start ? String(t.planned_start) : "",
      planned_end: plannedEnd,
      actual_end: actualEnd,
      delay_days: delay,
      risky: risky ? "是" : "否"
    };
  });
  const delayedCount = tasks.filter((x) => (x.delay_days || 0) > 0).length;
  const riskyCount = tasks.filter((x) => x.risky === "是").length;
  return { tasks, delayed_count: delayedCount, risky_count: riskyCount };
}

async function loadCollectOutputs() {
  collectError.value = "";
  const pid = selectedProjectIdModel.value || "example";
  const rawUrl = `/work/outputs/${encodeURIComponent(pid)}/project-metrics-orid/raw.json`;
  const integrityUrl = `/work/outputs/${encodeURIComponent(pid)}/project-metrics-orid/data_integrity.json`;
  try {
    const rawRes = await fetch(rawUrl, { cache: "no-store" });
    if (!rawRes.ok) {
      persistCachedOutputs(pid);
      return;
    } else {
      const contentType = String(rawRes.headers.get("content-type") || "").toLowerCase();
      let parsed = null;
      try {
        parsed = await rawRes.json();
      } catch {
        parsed = null;
      }
      const isHtml = contentType.includes("text/html") || (parsed === null && contentType && !contentType.includes("json"));
      if (isHtml || !parsed || typeof parsed !== "object") {
        collectError.value = "raw.json 解析失败（可能服务返回了 HTML 或数据不完整）";
        persistCachedOutputs(pid);
        return;
      } else {
        collectHasRaw.value = true;
        const src = parsed.sources && typeof parsed.sources === "object" ? parsed.sources : {};
        const jira = src.jira && typeof src.jira === "object" ? src.jira : {};
        const git = src.git && typeof src.git === "object" ? src.git : {};
        const ci = src.ci && typeof src.ci === "object" ? src.ci : {};
        const issues = Array.isArray(jira.issues) ? jira.issues : [];
        const commits = Array.isArray(git.commits) ? git.commits : [];
        const prs = Array.isArray(git.pull_requests) ? git.pull_requests : [];
        const runs = Array.isArray(ci.runs) ? ci.runs : [];
        const planning = parsed.planning && typeof parsed.planning === "object" ? parsed.planning : jira.planning && typeof jira.planning === "object" ? jira.planning : {};
        collectViz.value = {
          sources: { jira_issues: issues.length, git_commits: commits.length, git_pull_requests: prs.length, ci_runs: runs.length },
          issueStatus: countBy(issues, (x) => x && x.status),
          prStates: countBy(prs, (x) => x && x.state),
          ciStates: countBy(runs, (x) => x && x.status),
          swimlane: computeSwimlane(issues),
          burndown: computeBurndown(planning),
          gantt: computeGantt(planning)
        };
      }
    }
  } catch (e) {
    collectError.value = e && e.message ? e.message : String(e);
    persistCachedOutputs(pid);
    return;
  }
  try {
    const integrity = await fetchJsonOptional(integrityUrl);
    if (!integrity) {
      persistCachedOutputs(pid);
      return;
    }
    collectIntegrity.value = integrity;
    const src = collectIntegrity.value && collectIntegrity.value.sources ? collectIntegrity.value.sources : null;
    if (src && typeof src === "object") {
      const next = { ...(collectViz.value || {}) };
      next.sources = {
        jira_issues: src.jira_issues ?? next.sources.jira_issues,
        git_commits: src.git_commits ?? next.sources.git_commits,
        git_pull_requests: src.git_pull_requests ?? src.git_prs ?? next.sources.git_pull_requests,
        ci_runs: src.ci_runs ?? next.sources.ci_runs
      };
      collectViz.value = next;
    }
  } catch (e) {
    collectError.value = e && e.message ? e.message : String(e);
  }
  persistCachedOutputs(pid);
}

async function loadMetricsOutputs() {
  metricsError.value = "";
  const pid = selectedProjectIdModel.value || "example";
  const url = `/work/outputs/${encodeURIComponent(pid)}/project-metrics-orid/metrics.json`;
  try {
    const parsed = await fetchJsonOptional(url);
    if (!parsed) {
      return;
    }
    metricsData.value = parsed && parsed.metrics ? parsed.metrics : parsed;
  } catch (e) {
    metricsError.value = e && e.message ? e.message : String(e);
  }
  persistCachedOutputs(pid);
}

async function loadOridOutputs() {
  oridError.value = "";
  const pid = selectedProjectIdModel.value || "example";
  const url = `/work/outputs/${encodeURIComponent(pid)}/project-metrics-orid/report.json`;
  try {
    const parsed = await fetchJsonOptional(url);
    if (!parsed) {
      return;
    }
    reportData.value = parsed;
  } catch (e) {
    oridError.value = e && e.message ? e.message : String(e);
  }
  persistCachedOutputs(pid);
}

async function loadCurrentOutputs() {
  if (activeStep.value === "collect") return loadCollectOutputs();
  if (activeStep.value === "metrics") return loadMetricsOutputs();
  return loadOridOutputs();
}

async function reloadAllOutputs() {
  const pid = selectedProjectIdModel.value || "example";
  applyCachedOutputs(pid);
  await Promise.allSettled([loadCollectOutputs(), loadMetricsOutputs(), loadOridOutputs()]);
}

const collectCommand = computed(() => `/prjmx:collect\nproject_id: ${selectedProjectIdModel.value || "example"}`);
const metricsCommand = computed(() => `/prjmx:metrics\nproject_id: ${selectedProjectIdModel.value || "example"}`);
const oridCommand = computed(() => `/prjmx:orid\nproject_id: ${selectedProjectIdModel.value || "example"}`);

const runVisible = ref(false);
const runTitle = ref("");
const runTip = ref("");
const runProgress = ref(0);
const runKind = ref("");
const runLogText = ref("");
const runLogLatestUrl = ref("");
let runProgressTimer = null;
let runPollTimer = null;
let runLogTimer = null;
let runStartAt = 0;
let pendingRunPreludeLogs = [];

function stopRunTimers() {
  if (runProgressTimer) {
    clearInterval(runProgressTimer);
    runProgressTimer = null;
  }
  if (runPollTimer) {
    clearInterval(runPollTimer);
    runPollTimer = null;
  }
  if (runLogTimer) {
    clearInterval(runLogTimer);
    runLogTimer = null;
  }
}

function cancelRun() {
  appendRunLog("用户取消");
  stopRunTimers();
  runVisible.value = false;
}

function ensureProjectReady() {
  const pid = String(selectedProjectIdModel.value || "").trim();
  if (!props.projects.length || !pid) {
    message.warning("请先配置并选择项目，再执行扫描。");
    return false;
  }
  return true;
}

function uiTime() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
}

function appendRunLog(message) {
  const msg = String(message || "").trim();
  if (!msg) return;
  const line = `[${uiTime()}] ${msg}`;
  runLogText.value = runLogText.value ? `${runLogText.value}\n${line}` : line;
  const pid = String(selectedProjectIdModel.value || "example").trim() || "example";
  const kind = String(runKind.value || "").trim();
  if (!kind) return;
  postJson("/api/logs/append", { project_id: pid, kind, message: msg }).catch(() => {});
}

async function initRunLog(kind) {
  const pid = String(selectedProjectIdModel.value || "example").trim() || "example";
  runKind.value = String(kind || "").trim();
  runLogText.value = "";
  runLogLatestUrl.value = "";
  try {
    const res = await postJson("/api/logs/init", { project_id: pid, kind: runKind.value });
    runLogLatestUrl.value = res && res.latest_url ? String(res.latest_url) : "";
  } catch {
    runLogLatestUrl.value = "";
  }
}

async function refreshRunLogFromFile() {
  const url = String(runLogLatestUrl.value || "").trim();
  if (!url) return;
  try {
    const res = await fetch(`${url}?t=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) return;
    const text = await res.text();
    if (text && text.length >= runLogText.value.length) runLogText.value = text.trimEnd();
  } catch {}
}

async function startRun(kind) {
  stopRunTimers();
  runStartAt = Date.now();
  await initRunLog(kind);
  runTitle.value = kind === "collect" ? "正在执行：收集数据" : kind === "metrics" ? "正在执行：问题发现" : "正在执行：持续改进";
  runTip.value = "等待 Skill 执行完成…";
  runProgress.value = 5;
  runVisible.value = true;
  const preludes = Array.isArray(pendingRunPreludeLogs) ? pendingRunPreludeLogs.slice() : [];
  pendingRunPreludeLogs = [];
  for (const p of preludes) appendRunLog(p);
  appendRunLog("开始执行");

  runProgressTimer = setInterval(() => {
    if (runProgress.value >= 95) return;
    runProgress.value = Math.min(95, runProgress.value + 1);
  }, 350);

  const poll = async () => {
    const pid = String(selectedProjectIdModel.value || "example").trim() || "example";
    const elapsed = Date.now() - runStartAt;
    if (elapsed > 180000) {
      runTip.value = "等待超时。请检查 Skill 是否正在运行，或稍后重试。";
      appendRunLog("等待超时（180s）");
      runProgress.value = Math.min(100, Math.max(runProgress.value, 98));
      stopRunTimers();
      return;
    }
    const prevCollectRaw = collectHasRaw.value;
    const prevCollectIntegrity = !!collectIntegrity.value;
    const prevMetricsOk = !!metricsData.value;
    const prevOridOk = !!reportData.value;
    const prevCollectError = String(collectError.value || "");
    const prevMetricsError = String(metricsError.value || "");
    const prevOridError = String(oridError.value || "");
    if (pid !== "example") {
      await loadCurrentOutputs();
    }
    if (kind === "collect") {
      if (!prevCollectRaw && collectHasRaw.value) appendRunLog("检测到 raw.json 已生成");
      if (!prevCollectIntegrity && collectIntegrity.value) appendRunLog("检测到 data_integrity.json 已生成");
      if (!prevCollectError && collectError.value) appendRunLog(`收集错误：${collectError.value}`);
    }
    if (kind === "metrics") {
      if (!prevMetricsOk && metricsData.value) appendRunLog("检测到 metrics.json 已生成");
      if (!prevMetricsError && metricsError.value) appendRunLog(`问题发现错误：${metricsError.value}`);
    }
    if (kind === "orid") {
      if (!prevOridOk && reportData.value) appendRunLog("检测到 report.json 已生成");
      if (!prevOridError && oridError.value) appendRunLog(`持续改进错误：${oridError.value}`);
    }
    if (kind === "collect" && collectHasRaw.value && collectIntegrity.value) {
      runProgress.value = 100;
      runTip.value = "已完成，正在刷新数据…";
      appendRunLog("执行完成");
      stopRunTimers();
      setTimeout(() => (runVisible.value = false), 400);
      return;
    }
    if (kind === "metrics" && metricsData.value) {
      runProgress.value = 100;
      runTip.value = "已完成，正在刷新数据…";
      appendRunLog("执行完成");
      stopRunTimers();
      setTimeout(() => (runVisible.value = false), 400);
      return;
    }
    if (kind === "orid" && reportData.value) {
      runProgress.value = 100;
      runTip.value = "已完成，正在刷新数据…";
      appendRunLog("执行完成");
      stopRunTimers();
      setTimeout(() => (runVisible.value = false), 400);
    }
  };

  runLogTimer = setInterval(refreshRunLogFromFile, 900);
  runPollTimer = setInterval(poll, 1500);
  await poll();
}

async function runMock(kind) {
  const pid = String(selectedProjectIdModel.value || "example").trim() || "example";
  const q = `?project=${encodeURIComponent(pid)}`;
  async function writeOutput(filename, payload) {
    try {
      await fetch("/api/outputs/write", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project_id: pid, filename, payload })
      });
    } catch {}
  }
  function localMock() {
    const issues = [];
    const sprint_start = "2026-05-01";
    const sprint_end = "2026-05-10";
    const sprint_total_points = 30;
    for (let i = 1; i <= 12; i++) {
      const status = i % 5 === 0 ? "Done" : i % 4 === 0 ? "Review" : i % 3 === 0 ? "In Progress" : "To Do";
      const created_at = "2026-05-01";
      const started_at = status === "In Progress" || status === "Review" || status === "Done" ? "2026-05-03" : "";
      const done_at = status === "Done" ? "2026-05-08" : "";
      const history = [{ status: "To Do", at: created_at }];
      if (started_at) history.push({ status: "In Progress", at: started_at });
      if (status === "Review") history.push({ status: "Review", at: "2026-05-06" });
      if (done_at) history.push({ status: "Done", at: done_at });
      issues.push({
        key: `${pid.toUpperCase()}-${100 + i}`,
        type: i % 4 === 0 ? "Bug" : "Story",
        summary: `示例需求/缺陷 ${i}`,
        status,
        assignee: i % 2 === 0 ? "dev-a" : "dev-b",
        story_points: i % 4 === 0 ? 3 : 1,
        labels: ["mock", pid],
        created_at: "2026-05-01",
        updated_at: "2026-05-10",
        started_at,
        done_at,
        due_date: "2026-05-10",
        status_history: history
      });
    }
    const commits = [];
    for (let i = 1; i <= 14; i++) {
      commits.push({
        sha: `deadbeef${String(i).padStart(2, "0")}`,
        author: i % 2 === 0 ? "dev-b" : "dev-a",
        date: `2026-05-${String(i).padStart(2, "0")}T10:00:00Z`,
        message: `mock commit ${i}: refactor/test/feature`,
        files_changed: (i % 5) + 1
      });
    }
    const pull_requests = [];
    for (let i = 1; i <= 8; i++) {
      pull_requests.push({
        id: i,
        title: `PR ${i}: 示例改动`,
        author: i % 2 === 0 ? "dev-b" : "dev-a",
        state: i % 3 === 0 ? "open" : "merged",
        created_at: `2026-05-${String(i).padStart(2, "0")}T09:00:00Z`,
        merged_at: i % 3 === 0 ? null : `2026-05-${String(i).padStart(2, "0")}T18:00:00Z`,
        additions: 50 + i * 3,
        deletions: 20 + i,
        reviews: i % 2 === 0 ? [] : [{ reviewer: "dev-c", state: "approved" }]
      });
    }
    const runs = [];
    for (let i = 1; i <= 10; i++) {
      runs.push({
        id: i,
        pipeline: "ci",
        status: i % 6 === 0 ? "failed" : "success",
        duration_seconds: 300 + i * 18,
        created_at: `2026-05-${String(i).padStart(2, "0")}T12:00:00Z`
      });
    }
    const burndown = [];
    for (let d = 0; d < 10; d++) {
      const date = `2026-05-${String(1 + d).padStart(2, "0")}`;
      const ideal = Math.max(0, sprint_total_points - Math.round((sprint_total_points / 9) * d));
      const drift = d >= 5 ? 2 : 0;
      const actual = Math.max(0, ideal + drift);
      burndown.push({ date, ideal_remaining_points: ideal, remaining_points: actual });
    }
    const gantt = {
      tasks: [
        { id: "T-1", name: "需求澄清与拆分", planned_start: "2026-05-01", planned_end: "2026-05-02", actual_end: "2026-05-02" },
        { id: "T-2", name: "实现与自测", planned_start: "2026-05-03", planned_end: "2026-05-06", actual_end: "2026-05-07" },
        { id: "T-3", name: "联调与回归", planned_start: "2026-05-06", planned_end: "2026-05-09", actual_end: "" }
      ]
    };
    const planning = { sprint: { start_date: sprint_start, end_date: sprint_end, total_points: sprint_total_points }, burndown: { series: burndown }, gantt };
    return {
      jira: { project: pid, issues, planning },
      commits: { project: pid, commits },
      prs: { project: pid, pull_requests },
      ci: { project: pid, runs }
    };
  }

  appendRunLog("拉取 mock 数据：Jira issues / Git commits / PR / CI runs");
  let jira = null;
  let commits = null;
  let prs = null;
  let ci = null;
  const need = requiredSourcesFromMetrics(loadEnabledMetricKeysFromStorage());
  try {
    const reqs = [];
    const planned = [];
    if (kind !== "collect" || need.jira) {
      reqs.push(fetchJson(`/mock/jira/issues${q}`));
      planned.push("jira");
    }
    if (kind !== "collect" || need.git_commits) {
      reqs.push(fetchJson(`/mock/git/commits${q}`));
      planned.push("commits");
    }
    if (kind !== "collect" || need.git_pull_requests) {
      reqs.push(fetchJson(`/mock/git/pull_requests${q}`));
      planned.push("prs");
    }
    if (kind !== "collect" || need.ci_runs) {
      reqs.push(fetchJson(`/mock/ci/runs${q}`));
      planned.push("ci");
    }
    const results = await Promise.all(reqs);
    const map = { jira: null, commits: null, prs: null, ci: null };
    planned.forEach((k, idx) => (map[k] = results[idx]));
    jira = map.jira;
    commits = map.commits;
    prs = map.prs;
    ci = map.ci;
  } catch {
    appendRunLog("mock endpoint 不可用，切换为前端内置 mock 数据");
    const local = localMock();
    jira = kind !== "collect" || need.jira ? local.jira : { project: pid, issues: [] };
    commits = kind !== "collect" || need.git_commits ? local.commits : { project: pid, commits: [] };
    prs = kind !== "collect" || need.git_pull_requests ? local.prs : { project: pid, pull_requests: [] };
    ci = kind !== "collect" || need.ci_runs ? local.ci : { project: pid, runs: [] };
  }

  const issues = jira && Array.isArray(jira.issues) ? jira.issues : [];
  const planning = jira && jira.planning && typeof jira.planning === "object" ? jira.planning : {};
  const doneIssues = issues.filter((x) => String(x && x.status) === "Done");
  const inProgressIssues = issues.filter((x) => String(x && x.status) === "In Progress");
  const bugDone = doneIssues.filter((x) => String(x && x.type) === "Bug").length;
  const totalDone = doneIssues.length || 1;

  const ciRuns = ci && Array.isArray(ci.runs) ? ci.runs : [];
  const ciOk = ciRuns.filter((x) => String(x && x.status) === "success").length;
  const ciRate = ciRuns.length ? ciOk / ciRuns.length : 1;

  const prList = prs && Array.isArray(prs.pull_requests) ? prs.pull_requests : [];
  const merged = prList.filter((x) => String(x && x.state) === "merged").length;
  appendRunLog(`mock 数据统计：issues=${issues.length} done=${doneIssues.length} wip=${inProgressIssues.length} mergedPR=${merged} ciRuns=${ciRuns.length}`);

  if (kind === "collect") {
    appendRunLog("生成 raw.json 与 data_integrity.json（mock）");
    collectHasRaw.value = true;
    collectIntegrity.value = {
      ok: true,
      mode: "mock",
      sources: { jira_issues: issues.length, git_commits: (commits && commits.commits ? commits.commits.length : 0), git_prs: prList.length, ci_runs: ciRuns.length }
    };
    collectViz.value = {
      sources: { jira_issues: issues.length, git_commits: (commits && commits.commits ? commits.commits.length : 0), git_pull_requests: prList.length, ci_runs: ciRuns.length },
      issueStatus: countBy(issues, (x) => x && x.status),
      prStates: countBy(prList, (x) => x && x.state),
      ciStates: countBy(ciRuns, (x) => x && x.status),
      swimlane: computeSwimlane(issues),
      burndown: computeBurndown(planning),
      gantt: computeGantt(planning)
    };
    await writeOutput("raw.json", {
      mode: "mock",
      project: pid,
      sources: { jira: { issues }, git: { commits: commits && commits.commits ? commits.commits : [], pull_requests: prList }, ci: { runs: ciRuns } },
      planning
    });
    await writeOutput("data_integrity.json", { ok: true, mode: "mock", project: pid, sources: collectIntegrity.value.sources });
    persistCachedOutputs(pid);
    return;
  }

  if (kind === "metrics") {
    appendRunLog("计算 metrics.json（mock）");
    metricsData.value = {
      window: "mock:30d",
      throughput: { count: doneIssues.length },
      wip: { avg: inProgressIssues.length, aging_count: Math.max(0, inProgressIssues.length - 2) },
      lead_time_days: { p50: 5, p75: 7, p95: 12 },
      cycle_time_days: { p50: 2, p75: 3, p95: 6 },
      pr_lead_time_days: { p50: 1.2, p75: 2.1, p95: 4.8 },
      review_latency_days: { p50: 0.4, p75: 0.9, p95: 1.8 },
      plan: { commitment_reliability: 0.78, scope_change: { added: 2, removed: 1 } },
      quality: { bug_rate: bugDone / totalDone, reopen_rate: 0.06, escaped_defects: 1, escaped_defect_rate: 1 / totalDone },
      ci: { integration_frequency: { count: ciRuns.length }, success_rate: ciRate, code_scan_pass_rate: 0.93 },
      targets: {
        lead_time_p50_days: 7,
        cycle_time_p50_days: 3,
        wip_limit: 10,
        bug_rate_max: 0.1,
        reopen_rate_max: 0.1,
        escaped_defects_max: 2,
        ci_success_rate_min: 0.9,
        code_scan_pass_rate_min: 0.95
      },
      mock_details: { done_items: doneIssues.length, wip_items: inProgressIssues.length, merged_prs: merged }
    };
    await writeOutput("metrics.json", { mode: "mock", project: pid, metrics: metricsData.value });
    persistCachedOutputs(pid);
    return;
  }

  if (!metricsData.value) await runMock("metrics");

  appendRunLog("生成 report.json（mock ORID + actions）");
  reportData.value = {
    mode: "mock",
    project: pid,
    metrics: metricsData.value,
    orid: {
      objective: [
        `完成 ${doneIssues.length} 个条目（Done），在制 ${inProgressIssues.length} 个（In Progress）`,
        `流水线成功率 ${(ciRate * 100).toFixed(0)}%，合并请求 ${merged} 个`
      ],
      reflective: ["迭代中后期出现提交/合并集中，评审与集成可能存在排队", "质量门禁未达标导致返工风险上升"],
      interpretive: ["任务拆分偏大导致合并慢", "评审等待与 CI 波动导致反馈不连续", "质量门禁阈值未固化导致缺陷回流"],
      decisional: ["把行动项纳入计划并设定验收/负责人，下一窗口验证 lead time 与门禁趋势"]
    },
    actions: [
      {
        id: "A-1",
        problem: "交付节奏不稳定，出现集中合并",
        cause: "任务拆分偏大 + 评审等待",
        solution: "把需求拆到 1 天内可合并粒度；设置每日评审窗口；限制在制数量",
        due_date: "",
        expected_effect: "降低 PR 周期 p50，减少末期堆积",
        acceptance_method: "下个窗口合并请求周期下降，评审等待下降",
        owner_role: "研发负责人"
      },
      {
        id: "A-2",
        problem: "代码扫描通过率偏低",
        cause: "门禁未前置 + 修复缺少明确责任链",
        solution: "合并请求阶段强制扫描门禁；为阻断级问题建立修复时限；引入智能辅助定位与修复草稿",
        due_date: "",
        expected_effect: "提升 code_scan_pass_rate，减少返工",
        acceptance_method: "下个窗口代码扫描通过率达到目标且无新增阻断级问题",
        owner_role: "质量/研发"
      }
    ]
  };
  await writeOutput("report.json", reportData.value);
  persistCachedOutputs(pid);
}

async function requestRunSkill(kind) {
  if (!ensureProjectReady()) return;
  const pid = selectedProjectIdModel.value || "example";
  if (String(pid) === "example") {
    statusText.value = "使用 mock 数据快速生成（example 项目）";
    pendingRunPreludeLogs = ["使用 mock 数据快速生成（example 项目）"];
    startRun(kind);
    try {
      await runMock(kind);
    } catch (e) {
      appendRunLog(`执行失败：${e && e.message ? e.message : String(e)}`);
      errorText.value = e && e.message ? e.message : String(e);
    }
    return;
  }
  const cmd = kind === "collect" ? collectCommand.value : kind === "metrics" ? metricsCommand.value : oridCommand.value;
  const payload = { type: "prjmx.runSkill", kind, project_id: pid, command: cmd };
  try {
    if (window && window.parent && window.parent !== window) window.parent.postMessage(payload, "*");
  } catch {}
  try {
    window.postMessage(payload, "*");
  } catch {}
  await copyText(cmd);
  statusText.value = "已发起执行请求";
  pendingRunPreludeLogs = ["已发送执行请求（postMessage），并已复制命令到剪贴板"];
  startRun(kind);
}

    watch(activeStep, () => loadCurrentOutputs());
    watch(
      () => props.selectedProjectId,
      () => reloadAllOutputs(),
      { immediate: true }
    );
    onMounted(() => reloadAllOutputs());

    return {
      t,
      emit,
      props,
      projects,
      selectedProjectIdModel,
      projectLabel,
      activeStep,
      statusText,
      errorText,
      collectHasRaw,
      collectIntegrity,
      collectViz,
      enabledMetricKeys,
      requiredSourcesText,
      requiredSourceTags,
      simpleCountColumns,
      metricsData,
      reportData,
      collectError,
      metricsError,
      oridError,
      requestRunSkill,
      runVisible,
      runTitle,
      runTip,
      runProgress,
      runLogText,
      runLogLatestUrl,
      cancelRun
    };
  }
};
</script>
