<template>
  <div v-if="!data" style="color: rgba(0, 0, 0, 0.65)">尚未导入数据。</div>
  <div v-else-if="!rootCauseMap" style="color: rgba(0, 0, 0, 0.65)">report.json 未包含 root_cause_map。</div>
  <div v-else>
    <a-space direction="vertical" style="width: 100%" :size="12">
      <a-space wrap>
        <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">现象</span>
        <a-select v-model:value="selectedId" style="min-width: 260px">
          <a-select-option v-for="p in phenomena" :key="p.id" :value="p.id">{{ p.title }}</a-select-option>
        </a-select>
      </a-space>

      <a-alert v-if="selected && selected.evidence && selected.evidence.length" type="info" show-icon>
        <template #message>证据</template>
        <template #description>
          <ul style="margin: 0; padding-left: 18px">
            <li v-for="(e, idx) in selected.evidence" :key="idx">{{ e }}</li>
          </ul>
        </template>
      </a-alert>

      <MindMap v-if="selected && selected.root" :root="selected.root" />
    </a-space>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import MindMap from "../components/MindMap.vue";

const props = defineProps({
  data: { type: Object, default: null }
});

const rootCauseMap = computed(() => (props.data && props.data.root_cause_map) || null);
const phenomena = computed(() => {
  const p = rootCauseMap.value && Array.isArray(rootCauseMap.value.phenomena) ? rootCauseMap.value.phenomena : [];
  return p
    .map((x, idx) => ({
      id: String(x && x.id ? x.id : `phen-${idx + 1}`),
      title: String((x && x.title) || "未命名现象"),
      evidence: Array.isArray(x && x.evidence) ? x.evidence : [],
      root: x && x.root ? x.root : null
    }))
    .filter((x) => x.root);
});

const selectedId = ref("");
watch(
  phenomena,
  (list) => {
    if (!list.length) {
      selectedId.value = "";
      return;
    }
    if (selectedId.value && list.some((x) => x.id === selectedId.value)) return;
    selectedId.value = list[0].id;
  },
  { immediate: true }
);

const selected = computed(() => phenomena.value.find((x) => x.id === selectedId.value) || null);
</script>
