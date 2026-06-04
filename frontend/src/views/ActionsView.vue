<template>
  <div v-if="!data" style="color: rgba(0, 0, 0, 0.65)">尚未导入数据。</div>
  <div v-else-if="rows.length === 0" style="color: rgba(0, 0, 0, 0.65)">未提供 actions 字段或为空。</div>
  <div v-else>
    <div style="color: rgba(0, 0, 0, 0.65); font-size: 12px; margin-bottom: 10px">
      用于展示决策/整改计划（JSON 存储 → 前端表格呈现）。
    </div>
    <a-table :columns="columns" :data-source="rows" :pagination="{ pageSize: 8 }" :scroll="{ x: scrollX }" />
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  data: { type: Object, default: null }
});

const rows = computed(() => {
  const actions = props.data && Array.isArray(props.data.actions) ? props.data.actions : [];
  return actions.map((a, index) => ({
    key: String(index),
    id: a.id || a.no || String(index + 1),
    problem: a.problem || a.issue || a.question || "—",
    cause: a.cause || a.root_cause || a.reason || "—",
    solution: a.solution || a.title || a.action || "—",
    discovered_date: a.discovered_date || a.found_date || a.discoveredAt || null,
    due_date: a.due_date || a.due || null,
    completed_date: a.completed_date || a.done_date || a.completedAt || null,
    expected_effect: a.expected_effect || a.expected || "—",
    acceptance_method: a.acceptance_method || a.acceptance_criteria || a.dod || "—",
    owner_role: a.owner_role || a.owner || "—"
  }));
});

const columns = [
  { title: "编号", dataIndex: "id", key: "id", width: 80 },
  { title: "问题", dataIndex: "problem", key: "problem", width: 220 },
  { title: "原因", dataIndex: "cause", key: "cause", width: 220 },
  { title: "解决方案", dataIndex: "solution", key: "solution", width: 260 },
  { title: "发现日期", dataIndex: "discovered_date", key: "discovered_date", width: 120 },
  {
    title: "截止",
    dataIndex: "due_date",
    key: "due_date",
    width: 120,
    sorter: (a, b) => {
      const da = a.due_date ? new Date(a.due_date).getTime() : Number.POSITIVE_INFINITY;
      const db = b.due_date ? new Date(b.due_date).getTime() : Number.POSITIVE_INFINITY;
      return da - db;
    }
  },
  { title: "完成日期", dataIndex: "completed_date", key: "completed_date", width: 120 },
  { title: "预期效果", dataIndex: "expected_effect", key: "expected_effect", width: 240 },
  { title: "验收方法", dataIndex: "acceptance_method", key: "acceptance_method", width: 220 },
  { title: "负责人", dataIndex: "owner_role", key: "owner_role", width: 120 }
];

const scrollX = 1600;
</script>
