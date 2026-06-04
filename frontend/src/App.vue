<template>
  <a-layout style="min-height: 100vh">
    <a-layout-header style="background: #ffffff; border-bottom: 1px solid #f0f0f0">
      <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px">
        <div style="display: flex; align-items: center; gap: 10px">
          <img src="/frontend/favicon.svg" alt="icon" style="width: 22px; height: 22px" />
          <div style="font-size: 16px; font-weight: 600">项目ORID持续改进</div>
        </div>
        <a-menu mode="horizontal" :selectedKeys="[activePage]" style="border-bottom: 0; line-height: 62px">
          <a-menu-item key="analysis" @click="go('analysis')">项目分析</a-menu-item>
          <a-menu-item key="configSystem" @click="go('configSystem')">系统访问配置</a-menu-item>
          <a-menu-item key="configMetrics" @click="go('configMetrics')">度量指标配置</a-menu-item>
          <a-menu-item key="concept" @click="go('concept')">理念</a-menu-item>
          <a-menu-item key="projectManage" @click="go('projectManage')">项目管理</a-menu-item>
          <a-menu-item key="actions" @click="go('actions')">行动项管理</a-menu-item>
        </a-menu>
      </div>
    </a-layout-header>

    <a-layout-content style="padding: 16px">
      <AnalysisView v-if="activePage === 'analysis'" :projects="projects" v-model:selectedProjectId="selectedProjectId" @reloadProjects="loadWorkspaceConfig" />
      <ConfigSystemView v-else-if="activePage === 'configSystem'" />
      <ConfigMetricsView v-else-if="activePage === 'configMetrics'" />
      <ProjectManageView
        v-else-if="activePage === 'projectManage'"
        :projects="projects"
        v-model:selectedProjectId="selectedProjectId"
        :workspaceConfig="workspaceConfig"
        @reloadWorkspaceConfig="loadWorkspaceConfig"
        @saveWorkspaceProjects="saveWorkspaceProjects"
      />
      <ActionPlanView v-else-if="activePage === 'actions'" :projects="projects" v-model:selectedProjectId="selectedProjectId" />
      <ConceptView v-else />
    </a-layout-content>
  </a-layout>
</template>

<script>
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { load } from "js-yaml";
import { getInitialRoute, listenRouteChange, navigateTo } from "./routes.js";
import AnalysisView from "./views/AnalysisView.vue";
import ConceptView from "./views/ConceptView.vue";
import ConfigSystemView from "./views/ConfigSystemView.vue";
import ConfigMetricsView from "./views/ConfigMetricsView.vue";
import ProjectManageView from "./views/ProjectManageView.vue";
import ActionPlanView from "./views/ActionPlanView.vue";

export default {
  components: { AnalysisView, ConceptView, ConfigSystemView, ConfigMetricsView, ProjectManageView, ActionPlanView },
  setup() {
    const activePage = ref("analysis");

    const workspaceConfig = ref(null);
    const projects = computed(() => (workspaceConfig.value && Array.isArray(workspaceConfig.value.projects) ? workspaceConfig.value.projects : []));
    const selectedProjectId = ref("");

    async function loadWorkspaceConfig() {
      try {
        const res = await fetch("/work/meta/config.yaml", { cache: "no-store" });
        if (!res.ok) {
          workspaceConfig.value = { projects: [] };
          selectedProjectId.value = "example";
          return;
        }
        const text = await res.text();
        const obj = load(text);
        workspaceConfig.value = obj && typeof obj === "object" ? obj : { projects: [] };
        const first = projects.value[0];
        if (!selectedProjectId.value) selectedProjectId.value = (first && String(first.id)) || "example";
      } catch {
        workspaceConfig.value = { projects: [] };
        selectedProjectId.value = "example";
      }
    }

    let stopListen = null;
    onMounted(() => {
      loadWorkspaceConfig();
      const r = getInitialRoute();
      activePage.value = String(r.page || "analysis");
      stopListen = listenRouteChange((next) => {
        activePage.value = String((next && next.page) || "analysis");
      });
    });

    onBeforeUnmount(() => {
      if (stopListen) stopListen();
    });

    watch(projects, (list) => {
      if (!selectedProjectId.value) {
        const first = list && list[0];
        selectedProjectId.value = (first && String(first.id)) || "example";
      }
    });

    watch(
      selectedProjectId,
      (v) => {
        try {
          window.localStorage.setItem("prjmx.selectedProjectId", String(v || ""));
        } catch {}
      },
      { immediate: true }
    );

    onMounted(() => {
      try {
        const v = window.localStorage.getItem("prjmx.selectedProjectId");
        if (v && !selectedProjectId.value) selectedProjectId.value = String(v) === "default" ? "example" : String(v);
      } catch {}
    });

    function go(page) {
      activePage.value = String(page || "analysis");
      navigateTo(activePage.value);
    }

    function saveWorkspaceProjects(nextProjects) {
      if (!workspaceConfig.value || typeof workspaceConfig.value !== "object") workspaceConfig.value = {};
      workspaceConfig.value.projects = Array.isArray(nextProjects) ? nextProjects : [];
    }

    return {
      activePage,
      workspaceConfig,
      projects,
      selectedProjectId,
      loadWorkspaceConfig,
      saveWorkspaceProjects,
      go
    };
  }
};
</script>
