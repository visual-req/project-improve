<template>
  <a-card :bordered="true" style="height: 100%" :title="t('configSystem.title')">
    <ConfigSystemPanels />
  </a-card>
</template>

<script>
import ConfigSystemPanels from "../components/ConfigSystemPanels.vue";
import { useI18n } from "../i18n.js";

export default {
  components: { ConfigSystemPanels },
  setup() {
    const { t } = useI18n();
    return { t };
  }
};
</script>
