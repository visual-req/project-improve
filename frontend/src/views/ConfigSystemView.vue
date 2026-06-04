<template>
  <a-card :bordered="true" style="height: 100%" title="系统访问配置（work/<project_id>/meta/config.yaml）">
    <ConfigSystemPanels />
  </a-card>
</template>

<script>
import ConfigSystemPanels from "../components/ConfigSystemPanels.vue";

export default {
  components: { ConfigSystemPanels }
};
</script>
