<template>
  <a-space direction="vertical" style="width: 100%" :size="10">
    <a-button type="primary" @click="requestRunSkill('collect')">{{ t("analysis.run.collect") }}</a-button>
    <a-alert v-if="collectError" type="warning" show-icon :message="collectError" />
    <a-card size="small" :title="t('analysis.files')">
      <ul style="margin: 0; padding-left: 18px">
        <li>输入：/work/{{ selectedProjectIdModel || "&lt;project_id&gt;" }}/meta/config.yaml</li>
        <li>输出：/work/outputs/{{ selectedProjectIdModel || "&lt;project_id&gt;" }}/project-metrics-orid/raw.json</li>
        <li>输出：/work/outputs/{{ selectedProjectIdModel || "&lt;project_id&gt;" }}/project-metrics-orid/data_integrity.json</li>
      </ul>
    </a-card>
    <a-card size="small" title="结果（预览）">
      <div>raw.json：{{ collectHasRaw ? "已生成" : "未找到" }}</div>
      <div>data_integrity：{{ collectIntegrity ? "已生成" : "未找到" }}</div>
    </a-card>
    <a-card size="small" title="采集计划（按度量指标）">
      <a-space direction="vertical" style="width: 100%" :size="6">
        <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px">
          已启用指标：{{ enabledMetricKeys.length }} 个；需要采集：{{ requiredSourcesText }}
        </div>
        <div>
          <a-tag v-for="t in requiredSourceTags" :key="t" color="blue">{{ t }}</a-tag>
        </div>
        <div v-if="enabledMetricKeys.length" style="color: rgba(0, 0, 0, 0.45); font-size: 12px">
          示例（前 12 个）：{{ enabledMetricKeys.slice(0, 12).join("，") }}{{ enabledMetricKeys.length > 12 ? "…" : "" }}
        </div>
      </a-space>
    </a-card>
    <a-card size="small" title="采集结果（可视化）">
      <a-row :gutter="[12, 12]">
        <a-col :xs="12" :sm="12" :md="6">
          <a-card size="small">
            <template #title>Jira 工作项</template>
            <a-statistic :value="collectViz.sources.jira_issues === null ? '—' : collectViz.sources.jira_issues" />
          </a-card>
        </a-col>
        <a-col :xs="12" :sm="12" :md="6">
          <a-card size="small">
            <template #title>Git 提交</template>
            <a-statistic :value="collectViz.sources.git_commits === null ? '—' : collectViz.sources.git_commits" />
          </a-card>
        </a-col>
        <a-col :xs="12" :sm="12" :md="6">
          <a-card size="small">
            <template #title>Pull Requests</template>
            <a-statistic :value="collectViz.sources.git_pull_requests === null ? '—' : collectViz.sources.git_pull_requests" />
          </a-card>
        </a-col>
        <a-col :xs="12" :sm="12" :md="6">
          <a-card size="small">
            <template #title>CI 运行</template>
            <a-statistic :value="collectViz.sources.ci_runs === null ? '—' : collectViz.sources.ci_runs" />
          </a-card>
        </a-col>
      </a-row>
    </a-card>

    <a-card v-if="collectViz.issueStatus.length" size="small" title="Jira 状态分布">
      <a-table :columns="simpleCountColumns" :data-source="collectViz.issueStatus" size="small" :pagination="false" />
    </a-card>
    <a-card v-if="collectViz.prStates.length" size="small" title="PR 状态分布">
      <a-table :columns="simpleCountColumns" :data-source="collectViz.prStates" size="small" :pagination="false" />
    </a-card>
    <a-card v-if="collectViz.ciStates.length" size="small" title="CI 状态分布">
      <a-table :columns="simpleCountColumns" :data-source="collectViz.ciStates" size="small" :pagination="false" />
    </a-card>

    <a-card size="small" title="泳道阻塞（Swimlane Blocking）">
      <a-space direction="vertical" style="width: 100%" :size="8">
        <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px">
          阈值：在制/评审停留 ≥ {{ collectViz.swimlane.threshold_days || 0 }} 天；阻塞条目：{{ collectViz.swimlane.blocked_count || 0 }}
        </div>
        <a-table :columns="swimlaneColumns" :data-source="collectViz.swimlane.columns || []" size="small" :pagination="false" />
        <a-table v-if="(collectViz.swimlane.top_blocked || []).length" :columns="blockedColumns" :data-source="collectViz.swimlane.top_blocked" size="small" :pagination="false" />
      </a-space>
    </a-card>

    <a-card size="small" title="燃尽图合理性（Burndown）">
      <a-space direction="vertical" style="width: 100%" :size="8">
        <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px">
          Sprint：{{ collectViz.burndown.sprint.start_date || "—" }} ~ {{ collectViz.burndown.sprint.end_date || "—" }}；总点数：{{
            collectViz.burndown.sprint.total_points === null || collectViz.burndown.sprint.total_points === undefined ? "—" : collectViz.burndown.sprint.total_points
          }}；判断：{{ collectViz.burndown.verdict || "—" }}
        </div>
        <a-table :columns="burndownColumns" :data-source="collectViz.burndown.series || []" size="small" :pagination="{ pageSize: 7 }" />
      </a-space>
    </a-card>

    <a-card size="small" title="甘特图延迟（Gantt Delay）">
      <a-space direction="vertical" style="width: 100%" :size="8">
        <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px">
          已延迟：{{ collectViz.gantt.delayed_count || 0 }}；计划已过期未完成：{{ collectViz.gantt.risky_count || 0 }}
        </div>
        <a-table :columns="ganttColumns" :data-source="collectViz.gantt.tasks || []" size="small" :pagination="false" />
      </a-space>
    </a-card>
  </a-space>
</template>

<script>
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
  setup() {
    const { t } = useI18n();
    return { t };
  },
  data() {
    return {
      swimlaneColumns: [
        { title: "泳道", dataIndex: "label", key: "label" },
        { title: "数量", dataIndex: "count", key: "count", width: 90 }
      ],
      blockedColumns: [
        { title: "条目", dataIndex: "key", key: "key", width: 120 },
        { title: "状态", dataIndex: "status", key: "status", width: 120 },
        { title: "停留(天)", dataIndex: "aging_days", key: "aging_days", width: 90 },
        { title: "摘要", dataIndex: "summary", key: "summary" }
      ],
      burndownColumns: [
        { title: "日期", dataIndex: "date", key: "date", width: 120 },
        { title: "理想剩余", dataIndex: "ideal_remaining_points", key: "ideal_remaining_points", width: 100 },
        { title: "实际剩余", dataIndex: "remaining_points", key: "remaining_points", width: 100 }
      ],
      ganttColumns: [
        { title: "任务", dataIndex: "name", key: "name", width: 180 },
        { title: "计划开始", dataIndex: "planned_start", key: "planned_start", width: 110 },
        { title: "计划结束", dataIndex: "planned_end", key: "planned_end", width: 110 },
        { title: "实际结束", dataIndex: "actual_end", key: "actual_end", width: 110 },
        { title: "延迟(天)", dataIndex: "delay_days", key: "delay_days", width: 90 },
        { title: "过期未完", dataIndex: "risky", key: "risky", width: 90 }
      ]
    };
  }
};
</script>
