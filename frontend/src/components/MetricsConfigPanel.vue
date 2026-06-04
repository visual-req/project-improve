<template>
  <a-card title="度量展示配置" size="small">
    <a-space direction="vertical" style="width: 100%" :size="12">
      <a-alert
        type="info"
        show-icon
        message="配置说明"
        :description="hint"
      />

      <a-row :gutter="[12, 12]">
        <a-col :xs="24" :md="12">
          <a-card title="流动（Flow）" size="small">
            <a-space direction="vertical" style="width: 100%" :size="8">
              <a-checkbox v-model:checked="local.enabled.throughput" @change="emitChange">Throughput</a-checkbox>
              <a-checkbox v-model:checked="local.enabled.lead_time_p50" @change="emitChange">Lead Time p50</a-checkbox>
              <a-checkbox v-model:checked="local.enabled.cycle_time_p50" @change="emitChange">Cycle Time p50</a-checkbox>
              <a-checkbox v-model:checked="local.enabled.wip_avg" @change="emitChange">WIP 平均</a-checkbox>
            </a-space>
          </a-card>
        </a-col>
        <a-col :xs="24" :md="12">
          <a-card title="质量（Quality）" size="small">
            <a-space direction="vertical" style="width: 100%" :size="8">
              <a-checkbox v-model:checked="local.enabled.bug_rate" @change="emitChange">Bug Rate</a-checkbox>
              <a-checkbox v-model:checked="local.enabled.reopen_rate" @change="emitChange">重开率</a-checkbox>
              <a-checkbox v-model:checked="local.enabled.escaped_defects" @change="emitChange">缺陷逃逸率</a-checkbox>
            </a-space>
          </a-card>
        </a-col>
      </a-row>

      <a-row :gutter="[12, 12]">
        <a-col :xs="24" :md="12">
          <a-card title="工程效率（Engineering）" size="small">
            <a-space direction="vertical" style="width: 100%" :size="8">
              <a-checkbox v-model:checked="local.enabled.pr_lead_time_p50" @change="emitChange">PR Lead Time p50</a-checkbox>
              <a-checkbox v-model:checked="local.enabled.review_latency_p50" @change="emitChange">Review Latency p50</a-checkbox>
            </a-space>
          </a-card>
        </a-col>
        <a-col :xs="24" :md="12">
          <a-card title="持续集成（CI）" size="small">
            <a-space direction="vertical" style="width: 100%" :size="8">
              <a-checkbox v-model:checked="local.enabled.ci_integration_frequency" @change="emitChange">Integration Frequency</a-checkbox>
              <a-checkbox v-model:checked="local.enabled.ci_success_rate" @change="emitChange">CI Success Rate</a-checkbox>
              <a-checkbox v-model:checked="local.enabled.code_scan_pass_rate" @change="emitChange">Code Scan Pass Rate</a-checkbox>
            </a-space>
          </a-card>
        </a-col>
        <a-col :xs="24" :md="12">
          <a-card title="导入/导出（保存到 work/meta）" size="small">
            <a-space direction="vertical" style="width: 100%" :size="10">
              <a-space>
                <a-button @click="downloadConfig">导出配置</a-button>
                <a-upload :before-upload="handleBeforeUpload" :show-upload-list="false" accept=".json,application/json">
                  <a-button>导入配置</a-button>
                </a-upload>
              </a-space>
              <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px">
                建议保存到：<span style="font-family: ui-monospace">{{ suggestedPath }}</span>
              </div>
              <a-alert v-if="errorText" type="error" show-icon :message="errorText" />
            </a-space>
          </a-card>
        </a-col>
      </a-row>
    </a-space>
  </a-card>
</template>

<script setup>
import { computed, ref, watch } from "vue";

const props = defineProps({
  projectId: { type: String, default: "default" },
  value: { type: Object, default: null }
});

const emit = defineEmits(["change"]);

function defaultConfig() {
  return {
    version: 1,
    enabled: {
      throughput: true,
      lead_time_p50: true,
      cycle_time_p50: true,
      wip_avg: true,
      bug_rate: true,
      reopen_rate: true,
      escaped_defects: true,
      pr_lead_time_p50: true,
      review_latency_p50: true,
      ci_integration_frequency: true,
      ci_success_rate: true,
      code_scan_pass_rate: true
    }
  };
}

const local = ref(defaultConfig());
const errorText = ref("");

watch(
  () => props.value,
  (next) => {
    if (!next || typeof next !== "object") return;
    const enabled = next.enabled && typeof next.enabled === "object" ? next.enabled : {};
    local.value = { version: 1, enabled: { ...defaultConfig().enabled, ...enabled } };
  },
  { immediate: true }
);

const hint = computed(() => {
  return [
    "用于控制前端展示哪些项目扫描指标。",
    "指标分类参考 docs/assets/metrics-map.svg。",
    "该配置只影响展示，不改变 report.json 的内容。"
  ].join("\n");
});

const suggestedPath = computed(() => {
  const pid = props.projectId || "default";
  return `work/meta/${pid}/metrics-config.json`;
});

const emitChange = () => {
  emit("change", { ...local.value, enabled: { ...local.value.enabled } });
};

function downloadText(filename, text) {
  const blob = new Blob([text], { type: "application/json;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

const downloadConfig = () => {
  errorText.value = "";
  const pid = props.projectId || "default";
  const filename = `metrics-config.${pid}.json`;
  downloadText(filename, JSON.stringify(local.value, null, 2));
};

function readFileAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result || ""));
    reader.onerror = () => reject(reader.error || new Error("读取文件失败"));
    reader.readAsText(file);
  });
}

const handleBeforeUpload = async (file) => {
  errorText.value = "";
  try {
    const text = await readFileAsText(file);
    const parsed = JSON.parse(text);
    if (!parsed || typeof parsed !== "object") throw new Error("配置文件不是 JSON 对象");
    const enabled = parsed.enabled && typeof parsed.enabled === "object" ? parsed.enabled : null;
    if (!enabled) throw new Error("配置缺少 enabled 字段");
    local.value = { version: 1, enabled: { ...defaultConfig().enabled, ...enabled } };
    emitChange();
  } catch (e) {
    errorText.value = e && e.message ? e.message : String(e);
  }
  return false;
};
</script>
