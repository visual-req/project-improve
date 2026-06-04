<template>
  <a-modal v-model:visible="visibleProxy" :closable="false" :maskClosable="false" :footer="null" width="520">
    <a-space direction="vertical" style="width: 100%" :size="12">
      <div style="font-weight: 600">{{ title }}</div>
      <a-progress :percent="progress" :status="progress >= 100 ? 'success' : 'active'" />
      <div style="color: rgba(0, 0, 0, 0.65)">{{ tip }}</div>
      <div v-if="logLatestUrl" style="color: rgba(0, 0, 0, 0.65); font-size: 12px">日志文件：{{ logLatestUrl }}</div>
      <div
        style="
          border: 1px solid #f0f0f0;
          background: #fafafa;
          border-radius: 8px;
          padding: 10px;
          max-height: 220px;
          overflow: auto;
          font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;
          font-size: 12px;
          white-space: pre-wrap;
        "
      >
        {{ logText || "（暂无日志）" }}
      </div>
      <a-space>
        <a-button type="default" @click="cancel">取消</a-button>
      </a-space>
    </a-space>
  </a-modal>
</template>

<script>
import { computed } from "vue";

export default {
  props: {
    visible: { type: Boolean, default: false },
    title: { type: String, default: "" },
    tip: { type: String, default: "" },
    progress: { type: Number, default: 0 },
    logLatestUrl: { type: String, default: "" },
    logText: { type: String, default: "" }
  },
  emits: ["update:visible", "cancel"],
  setup(props, { emit }) {
    const visibleProxy = computed({
      get: () => !!props.visible,
      set: (v) => emit("update:visible", !!v)
    });
    function cancel() {
      emit("cancel");
    }
    return { visibleProxy, cancel };
  }
};
</script>
