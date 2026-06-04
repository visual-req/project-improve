<template>
  <div v-if="!data" style="color: rgba(0, 0, 0, 0.65)">尚未导入数据。</div>
  <a-collapse v-else accordion>
    <a-collapse-panel key="o" header="Objective（客观事实）">
      <ul style="margin: 0; padding-left: 18px">
        <li v-for="(x, idx) in o" :key="idx">{{ x }}</li>
        <li v-if="o.length === 0">—</li>
      </ul>
    </a-collapse-panel>
    <a-collapse-panel key="r" header="Reflective（主观感受）">
      <ul style="margin: 0; padding-left: 18px">
        <li v-for="(x, idx) in r" :key="idx">{{ x }}</li>
        <li v-if="r.length === 0">—</li>
      </ul>
    </a-collapse-panel>
    <a-collapse-panel key="i" header="Interpretive（意义解释/假设）">
      <ul style="margin: 0; padding-left: 18px">
        <li v-for="(x, idx) in i" :key="idx">{{ x }}</li>
        <li v-if="i.length === 0">—</li>
      </ul>
    </a-collapse-panel>
    <a-collapse-panel key="d" header="Decisional（决策/行动方向）">
      <ul style="margin: 0; padding-left: 18px">
        <li v-for="(x, idx) in d" :key="idx">{{ x }}</li>
        <li v-if="d.length === 0">—</li>
      </ul>
    </a-collapse-panel>
  </a-collapse>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  data: { type: Object, default: null }
});

const orid = computed(() => (props.data && props.data.orid) || {});
const toArr = (v) => (Array.isArray(v) ? v : v ? [v] : []);

const o = computed(() => toArr(orid.value.objective));
const r = computed(() => toArr(orid.value.reflective));
const i = computed(() => toArr(orid.value.interpretive));
const d = computed(() => toArr(orid.value.decisional));
</script>
