<template>
  <div v-if="!data" style="color: rgba(0, 0, 0, 0.65)">尚未导入数据。</div>
  <div v-else-if="issues.length === 0" style="color: rgba(0, 0, 0, 0.65)">未提供 issues 字段或为空。</div>
  <a-list v-else :data-source="issues" item-layout="vertical">
    <template #renderItem="{ item }">
      <a-list-item>
        <a-list-item-meta>
          <template #title>
            <a-space>
              <span>{{ item.title || "未命名问题" }}</span>
              <a-tag :color="severityColor(item.severity)">{{ severityText(item.severity) }}</a-tag>
            </a-space>
          </template>
        </a-list-item-meta>
        <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px; margin-bottom: 6px">证据</div>
        <ul style="margin: 0; padding-left: 18px">
          <li v-for="(e, idx) in (Array.isArray(item.evidence) ? item.evidence : [])" :key="idx">{{ e }}</li>
          <li v-if="!Array.isArray(item.evidence) || item.evidence.length === 0">—</li>
        </ul>
      </a-list-item>
    </template>
  </a-list>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  data: { type: Object, default: null }
});

const issues = computed(() => (props.data && Array.isArray(props.data.issues) ? props.data.issues : []));

function severityColor(sev) {
  const v = String(sev || "").toLowerCase();
  if (v === "high" || v === "p0" || v === "critical") return "red";
  if (v === "medium" || v === "p1") return "gold";
  if (v === "low" || v === "p2") return "green";
  return "default";
}

function severityText(sev) {
  const v = String(sev || "").toLowerCase();
  if (v === "high" || v === "p0" || v === "critical") return "高";
  if (v === "medium" || v === "p1") return "中";
  if (v === "low" || v === "p2") return "低";
  return "—";
}
</script>
