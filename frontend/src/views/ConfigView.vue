<template>
  <a-space direction="vertical" style="width: 100%" :size="16">
    <WorkspaceConfigPanel :project-info="localProject" @update:project-info="handleProjectFromYaml" />

    <a-card title="项目工作区" size="small">
      <a-form layout="vertical">
        <a-row :gutter="[12, 12]">
          <a-col :xs="24" :md="8">
            <a-form-item label="项目 ID">
              <a-input v-model:value="localProject.id" placeholder="例如：proj-123" @change="emitProjectInfo" />
            </a-form-item>
          </a-col>
          <a-col :xs="24" :md="8">
            <a-form-item label="项目名称">
              <a-input v-model:value="localProject.name" placeholder="例如：订单平台" @change="emitProjectInfo" />
            </a-form-item>
          </a-col>
          <a-col :xs="24" :md="8">
            <a-form-item label="英文名/Slug">
              <a-input v-model:value="localProject.slug_en" placeholder="例如：order-platform" @change="emitProjectInfo" />
            </a-form-item>
          </a-col>
        </a-row>
      </a-form>
      <a-alert
        style="margin-top: 8px"
        type="info"
        show-icon
        message="建议的工作区目录结构"
        :description="workspaceHint"
      />
    </a-card>

    <MetricsConfigPanel :project-id="localProject.id" :value="localMetricsConfig" @change="handleConfigChange" />
  </a-space>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import MetricsConfigPanel from "../components/MetricsConfigPanel.vue";
import WorkspaceConfigPanel from "../components/WorkspaceConfigPanel.vue";

const props = defineProps({
  projectInfo: { type: Object, default: null },
  metricsConfig: { type: Object, default: null }
});

const emit = defineEmits(["update:project-info", "update:metrics-config"]);

const localProject = ref({
  id: props.projectInfo && props.projectInfo.id ? String(props.projectInfo.id) : "default",
  name: props.projectInfo && props.projectInfo.name ? String(props.projectInfo.name) : "—",
  slug_en: props.projectInfo && props.projectInfo.slug_en ? String(props.projectInfo.slug_en) : "—"
});

const localMetricsConfig = ref(props.metricsConfig || { version: 1, enabled: {} });

watch(
  () => props.projectInfo,
  (next) => {
    if (!next) return;
    localProject.value = {
      id: String(next.id || "default"),
      name: String(next.name || "—"),
      slug_en: String(next.slug_en || "—")
    };
  }
);

watch(
  () => props.metricsConfig,
  (next) => {
    if (!next) return;
    localMetricsConfig.value = next;
  }
);

const workspaceHint = computed(() => {
  const pid = localProject.value.id || "default";
  return [
    `输入：work/inputs/${pid}/`,
    `输出：work/outputs/${pid}/project-metrics-orid/`,
    `配置：work/meta/config.yaml`,
    `配置（本页导出）：work/meta/${pid}/metrics-config.json`
  ].join("\n");
});

const emitProjectInfo = () => {
  emit("update:project-info", { ...localProject.value });
};

const handleProjectFromYaml = (next) => {
  localProject.value = {
    id: String(next.id || "default"),
    name: String(next.name || "—"),
    slug_en: String(next.slug_en || "—")
  };
  emitProjectInfo();
};

const handleConfigChange = (next) => {
  emit("update:metrics-config", next);
};
</script>
