<template>
  <a-card :bordered="true" style="height: 100%" title="度量指标配置（work/<project_id>/meta/metrics.json）">
    <ConfigMetricsPanels />
  </a-card>
</template>

<script>
import ConfigMetricsPanels from "../components/ConfigMetricsPanels.vue";

export default {
  components: { ConfigMetricsPanels }
};
</script>
