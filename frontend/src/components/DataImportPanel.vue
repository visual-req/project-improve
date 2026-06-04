<template>
  <a-card title="数据导入" :bordered="true">
    <a-space direction="vertical" style="width: 100%" :size="12">
      <a-upload :before-upload="handleBeforeUpload" :show-upload-list="false" accept=".json,application/json">
        <a-button>选择 report.json</a-button>
      </a-upload>

      <a-space>
        <a-button type="primary" @click="renderFromText">渲染</a-button>
        <a-button @click="clearAll">清空</a-button>
        <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">{{ statusText }}</span>
      </a-space>

      <a-textarea
        v-model:value="jsonText"
        :rows="12"
        placeholder='粘贴 report.json 内容，例如：{"metrics":{...},"orid":{...},"actions":[...]}'
      />

      <a-alert v-if="errorText" type="error" show-icon :message="errorText" />

      <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px">
        推荐字段：<span style="font-family: ui-monospace">metrics</span>、
        <span style="font-family: ui-monospace">issues</span>、
        <span style="font-family: ui-monospace">orid</span>、
        <span style="font-family: ui-monospace">actions</span>
      </div>
    </a-space>
  </a-card>
</template>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["render", "clear"]);

function safeJsonParse(text) {
  const t = String(text || "").trim();
  if (!t) return { ok: false, error: "未检测到可解析的 JSON。请粘贴 report.json 内容或通过文件导入。" };
  try {
    const parsed = JSON.parse(t);
    if (!parsed || typeof parsed !== "object") return { ok: false, error: "JSON 解析成功，但内容不是对象。" };
    return { ok: true, value: parsed };
  } catch (e) {
    return { ok: false, error: e && e.message ? e.message : String(e) };
  }
}

function readFileAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result || ""));
    reader.onerror = () => reject(reader.error || new Error("读取文件失败"));
    reader.readAsText(file);
  });
}

const jsonText = ref("");
const errorText = ref("");
const statusText = ref("");

const handleBeforeUpload = async (file) => {
  errorText.value = "";
  try {
    const text = await readFileAsText(file);
    jsonText.value = text;
    statusText.value = "已导入文件";
  } catch (e) {
    errorText.value = e && e.message ? e.message : String(e);
  }
  return false;
};

const renderFromText = () => {
  errorText.value = "";
  const result = safeJsonParse(jsonText.value);
  if (!result.ok) {
    errorText.value = result.error;
    return;
  }
  emit("render", result.value);
  statusText.value = "已渲染";
};

const clearAll = () => {
  jsonText.value = "";
  errorText.value = "";
  statusText.value = "";
  emit("clear");
};
</script>
