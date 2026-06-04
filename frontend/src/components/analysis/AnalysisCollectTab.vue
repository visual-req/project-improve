<template>
  <a-space direction="vertical" style="width: 100%" :size="10">
    <a-button type="primary" @click="requestRunSkill('collect')">{{ t("analysis.run.collect") }}</a-button>
    <a-alert v-if="collectError" type="warning" show-icon :message="collectError" />
    <a-card size="small" :title="t('analysis.files')">
      <ul style="margin: 0; padding-left: 18px">
        <li>{{ t("common.input") }}：/work/{{ selectedProjectIdModel || "&lt;project_id&gt;" }}/meta/config.yaml</li>
        <li>{{ t("common.output") }}：/work/outputs/{{ selectedProjectIdModel || "&lt;project_id&gt;" }}/project-metrics-orid/raw.json</li>
        <li>{{ t("common.output") }}：/work/outputs/{{ selectedProjectIdModel || "&lt;project_id&gt;" }}/project-metrics-orid/data_integrity.json</li>
      </ul>
    </a-card>
    <a-card size="small" :title="t('analysis.collect.previewTitle')">
      <div>raw.json：{{ collectHasRaw ? t("analysis.collect.generated") : t("analysis.collect.notFound") }}</div>
      <div>data_integrity：{{ collectIntegrity ? t("analysis.collect.generated") : t("analysis.collect.notFound") }}</div>
    </a-card>
    <a-card size="small" :title="t('analysis.collect.planTitle')">
      <a-space direction="vertical" style="width: 100%" :size="6">
        <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px">
          {{ t("analysis.collect.planSummary", { count: enabledMetricKeys.length, sources: requiredSourcesText }) }}
        </div>
        <div>
          <a-tag v-for="tag in requiredSourceTags" :key="tag" color="blue">{{ tag }}</a-tag>
        </div>
        <div v-if="enabledMetricKeys.length" style="color: rgba(0, 0, 0, 0.45); font-size: 12px">{{ metricExampleText }}</div>
      </a-space>
    </a-card>
    <a-card size="small" :title="t('analysis.collect.vizTitle')">
      <a-row :gutter="[12, 12]">
        <a-col :xs="12" :sm="12" :md="6">
          <a-card size="small">
            <template #title>{{ t("analysis.collect.viz.jiraIssues") }}</template>
            <a-statistic :value="collectViz.sources.jira_issues === null ? t('common.none') : collectViz.sources.jira_issues" />
          </a-card>
        </a-col>
        <a-col :xs="12" :sm="12" :md="6">
          <a-card size="small">
            <template #title>{{ t("analysis.collect.viz.gitCommits") }}</template>
            <a-statistic :value="collectViz.sources.git_commits === null ? t('common.none') : collectViz.sources.git_commits" />
          </a-card>
        </a-col>
        <a-col :xs="12" :sm="12" :md="6">
          <a-card size="small">
            <template #title>{{ t("analysis.collect.viz.pullRequests") }}</template>
            <a-statistic :value="collectViz.sources.git_pull_requests === null ? t('common.none') : collectViz.sources.git_pull_requests" />
          </a-card>
        </a-col>
        <a-col :xs="12" :sm="12" :md="6">
          <a-card size="small">
            <template #title>{{ t("analysis.collect.viz.ciRuns") }}</template>
            <a-statistic :value="collectViz.sources.ci_runs === null ? t('common.none') : collectViz.sources.ci_runs" />
          </a-card>
        </a-col>
      </a-row>
    </a-card>

    <a-card v-if="collectViz.issueStatus.length" size="small" :title="t('analysis.collect.dist.issueStatus')">
      <a-table :columns="simpleCountColumns" :data-source="collectViz.issueStatus" size="small" :pagination="false" />
    </a-card>
    <a-card v-if="collectViz.prStates.length" size="small" :title="t('analysis.collect.dist.prStatus')">
      <a-table :columns="simpleCountColumns" :data-source="collectViz.prStates" size="small" :pagination="false" />
    </a-card>
    <a-card v-if="collectViz.ciStates.length" size="small" :title="t('analysis.collect.dist.ciStatus')">
      <a-table :columns="simpleCountColumns" :data-source="collectViz.ciStates" size="small" :pagination="false" />
    </a-card>

    <a-card size="small" :title="t('analysis.collect.swimlane.title')">
      <a-space direction="vertical" style="width: 100%" :size="8">
        <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px">
          {{
            t("analysis.collect.swimlane.summary", {
              days: collectViz.swimlane.threshold_days || 0,
              count: collectViz.swimlane.blocked_count || 0
            })
          }}
        </div>
        <a-table :columns="swimlaneColumns" :data-source="collectViz.swimlane.columns || []" size="small" :pagination="false" />
        <a-table v-if="(collectViz.swimlane.top_blocked || []).length" :columns="blockedColumns" :data-source="collectViz.swimlane.top_blocked" size="small" :pagination="false" />
      </a-space>
    </a-card>

    <a-card size="small" :title="t('analysis.collect.burndown.title')">
      <a-space direction="vertical" style="width: 100%" :size="8">
        <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px">
          {{
            t("analysis.collect.burndown.summary", {
              start: collectViz.burndown.sprint.start_date || t("common.none"),
              end: collectViz.burndown.sprint.end_date || t("common.none"),
              total:
                collectViz.burndown.sprint.total_points === null || collectViz.burndown.sprint.total_points === undefined
                  ? t("common.none")
                  : collectViz.burndown.sprint.total_points,
              verdict: burndownVerdictText
            })
          }}
        </div>
        <a-table :columns="burndownColumns" :data-source="collectViz.burndown.series || []" size="small" :pagination="{ pageSize: 7 }" />
      </a-space>
    </a-card>

    <a-card size="small" :title="t('analysis.collect.gantt.title')">
      <a-space direction="vertical" style="width: 100%" :size="8">
        <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px">
          {{ t("analysis.collect.gantt.summary", { delayed: collectViz.gantt.delayed_count || 0, risky: collectViz.gantt.risky_count || 0 }) }}
        </div>
        <a-table :columns="ganttColumns" :data-source="collectViz.gantt.tasks || []" size="small" :pagination="false" />
      </a-space>
    </a-card>
  </a-space>
</template>

<script>
import { computed } from "vue";
import { useI18n } from "../../i18n.js";

export default {
  props: {
    selectedProjectIdModel: { type: String, default: "" },
    requestRunSkill: { type: Function, default: null },
    collectError: { type: String, default: "" },
    collectHasRaw: { type: Boolean, default: false },
    collectIntegrity: { type: [Object, null], default: null },
    enabledMetricKeys: { type: Array, default: () => [] },
    requiredSourcesText: { type: String, default: "" },
    requiredSourceTags: { type: Array, default: () => [] },
    collectViz: {
      type: Object,
      default: () => ({ sources: { jira_issues: null, git_commits: null, git_pull_requests: null, ci_runs: null }, issueStatus: [], prStates: [], ciStates: [] })
    },
    simpleCountColumns: { type: Array, default: () => [] }
  },
  setup(props) {
    const { t, locale } = useI18n();

    const metricExampleText = computed(() => {
      const list = Array.isArray(props.enabledMetricKeys) ? props.enabledMetricKeys : [];
      if (!list.length) return "";
      const joiner = String(locale.value || "").startsWith("zh") ? "，" : ", ";
      const items = list.slice(0, 12).join(joiner);
      const more = list.length > 12 ? "…" : "";
      return t("analysis.collect.planExample", { items, more });
    });

    const burndownVerdictText = computed(() => {
      const code = props.collectViz && props.collectViz.burndown ? String(props.collectViz.burndown.verdict || "") : "";
      if (code === "ahead" || code === "ok" || code === "slow") return t(`analysis.collect.burndown.verdict.${code}`);
      return code || t("common.none");
    });

    const swimlaneColumns = computed(() => [
      { title: t("analysis.collect.swimlane.col.lane"), dataIndex: "label", key: "label" },
      { title: t("analysis.collect.swimlane.col.count"), dataIndex: "count", key: "count", width: 90 }
    ]);

    const blockedColumns = computed(() => [
      { title: t("analysis.collect.blocked.col.item"), dataIndex: "key", key: "key", width: 120 },
      { title: t("analysis.collect.blocked.col.status"), dataIndex: "status", key: "status", width: 120 },
      { title: t("analysis.collect.blocked.col.agingDays"), dataIndex: "aging_days", key: "aging_days", width: 90 },
      { title: t("analysis.collect.blocked.col.summary"), dataIndex: "summary", key: "summary" }
    ]);

    const burndownColumns = computed(() => [
      { title: t("analysis.collect.burndown.col.date"), dataIndex: "date", key: "date", width: 120 },
      { title: t("analysis.collect.burndown.col.ideal"), dataIndex: "ideal_remaining_points", key: "ideal_remaining_points", width: 120 },
      { title: t("analysis.collect.burndown.col.actual"), dataIndex: "remaining_points", key: "remaining_points", width: 120 }
    ]);

    const ganttColumns = computed(() => [
      { title: t("analysis.collect.gantt.col.task"), dataIndex: "name", key: "name", width: 180 },
      { title: t("analysis.collect.gantt.col.plannedStart"), dataIndex: "planned_start", key: "planned_start", width: 110 },
      { title: t("analysis.collect.gantt.col.plannedEnd"), dataIndex: "planned_end", key: "planned_end", width: 110 },
      { title: t("analysis.collect.gantt.col.actualEnd"), dataIndex: "actual_end", key: "actual_end", width: 110 },
      { title: t("analysis.collect.gantt.col.delayDays"), dataIndex: "delay_days", key: "delay_days", width: 110 },
      {
        title: t("analysis.collect.gantt.col.risky"),
        key: "risky",
        width: 110,
        customRender: ({ record }) => (record && record.risky ? t("common.yes") : t("common.no"))
      }
    ]);

    return { t, metricExampleText, burndownVerdictText, swimlaneColumns, blockedColumns, burndownColumns, ganttColumns };
  }
};
</script>
