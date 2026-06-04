<template>
  <a-card :bordered="true" style="height: 100%" :title="t('configMetrics.title')">
    <ConfigMetricsPanels />
  </a-card>
</template>

<script>
import ConfigMetricsPanels from "../components/ConfigMetricsPanels.vue";
import { useI18n } from "../i18n.js";

export default {
  components: { ConfigMetricsPanels },
  setup() {
    const { t } = useI18n();
    return { t };
  }
};
</script>
