<template>
  <a-card title="工作区配置（work/meta/config.yaml）" size="small">
    <a-space direction="vertical" style="width: 100%" :size="12">
      <a-space wrap>
        <a-upload :before-upload="handleBeforeUpload" :show-upload-list="false" accept=".yaml,.yml,text/yaml,text/x-yaml">
          <a-button>导入 config.yaml</a-button>
        </a-upload>
        <a-button @click="downloadConfig">导出 config.yaml</a-button>
        <a-button @click="copyCommand('/prjmx:collect')">复制 /prjmx:collect</a-button>
        <a-button @click="copyCommand('/prjmx:metrics')">复制 /prjmx:metrics</a-button>
        <a-button @click="copyCommand('/prjmx:orid')">复制 /prjmx:orid</a-button>
        <a-button type="primary" @click="copyCommand('/prjmx:report')">复制 /prjmx:report</a-button>
        <span style="color: rgba(0, 0, 0, 0.65); font-size: 12px">{{ statusText }}</span>
      </a-space>

      <a-alert
        type="info"
        show-icon
        message="提示"
        :description="hint"
      />

      <a-alert v-if="parseError" type="error" show-icon :message="parseError" />

      <a-row :gutter="[12, 12]">
        <a-col :xs="24" :md="10">
          <a-card title="项目选择" size="small">
            <a-space direction="vertical" style="width: 100%" :size="10">
              <a-select v-model:value="selectedProjectId" style="width: 100%" @change="emitProjectFromSelection">
                <a-select-option v-for="p in projects" :key="p.id" :value="p.id">
                  {{ p.id }} · {{ p.name }}
                </a-select-option>
              </a-select>
              <a-textarea v-model:value="yamlText" :rows="10" placeholder="导入或编辑 YAML，然后点击下方“解析并应用”" />
              <a-space>
                <a-button @click="parseAndApply">解析并应用</a-button>
                <a-button @click="resetToExample">加载示例</a-button>
              </a-space>
            </a-space>
          </a-card>
        </a-col>

        <a-col :xs="24" :md="14">
          <a-card title="链接与数据源" size="small">
            <div v-if="!selectedProject" style="color: rgba(0, 0, 0, 0.65)">未选择项目。</div>
            <a-descriptions v-else bordered size="small" :column="1">
              <a-descriptions-item label="项目">
                {{ selectedProject.id }} · {{ selectedProject.name }} · {{ selectedProject.slug_en }}
              </a-descriptions-item>
              <a-descriptions-item label="项目管理">
                {{ selectedProject.data_source.system }} · {{ selectedProject.data_source.base_url }}
              </a-descriptions-item>
              <a-descriptions-item label="Bug 系统">
                {{ selectedProject.bug_source.system }} · {{ selectedProject.bug_source.base_url }}
              </a-descriptions-item>
              <a-descriptions-item label="Git">
                {{ selectedProject.git_source.system }} · {{ selectedProject.git_source.base_url }} ·
                {{ selectedProject.git_source.repo.owner }}/{{ selectedProject.git_source.repo.name }}
              </a-descriptions-item>
              <a-descriptions-item label="CI">
                {{ selectedProject.ci_source.system }} · {{ selectedProject.ci_source.base_url }}
              </a-descriptions-item>
            </a-descriptions>
          </a-card>
        </a-col>
      </a-row>
    </a-space>
  </a-card>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { load as yamlLoad, dump as yamlDump } from "js-yaml";

const props = defineProps({
  projectInfo: { type: Object, default: null }
});

const emit = defineEmits(["update:project-info"]);

const yamlText = ref("");
const configObj = ref(null);
const parseError = ref("");
const statusText = ref("");

const hint = computed(() => {
  return [
    "用于查看/编辑工作区项目配置，并生成可复制的命令指令。",
    "浏览器无法直接写入 work/meta，请用“导出”保存到 work/meta/config.yaml。",
    "命令会附带 project_id，便于按项目工作目录增量输出。"
  ].join("\n");
});

function normalizeConfig(obj) {
  const projects = Array.isArray(obj && obj.projects) ? obj.projects : [];
  const normalizedProjects = projects.map((p) => ({
    id: String((p && p.id) || "default"),
    name: String((p && p.name) || "—"),
    slug_en: String((p && p.slug_en) || "—"),
    data_source: {
      system: String((p && p.data_source && p.data_source.system) || "—"),
      base_url: String((p && p.data_source && p.data_source.base_url) || "—")
    },
    bug_source: {
      system: String((p && p.bug_source && p.bug_source.system) || "—"),
      base_url: String((p && p.bug_source && p.bug_source.base_url) || "—")
    },
    git_source: {
      system: String((p && p.git_source && p.git_source.system) || "—"),
      base_url: String((p && p.git_source && p.git_source.base_url) || "—"),
      repo: {
        owner: String((p && p.git_source && p.git_source.repo && p.git_source.repo.owner) || "—"),
        name: String((p && p.git_source && p.git_source.repo && p.git_source.repo.name) || "—")
      }
    },
    ci_source: {
      system: String((p && p.ci_source && p.ci_source.system) || "—"),
      base_url: String((p && p.ci_source && p.ci_source.base_url) || "—")
    }
  }));
  const active = String((obj && obj.active_project_id) || (normalizedProjects[0] && normalizedProjects[0].id) || "default");
  return { active_project_id: active, projects: normalizedProjects, raw: obj };
}

function parseYaml(text) {
  const t = String(text || "").trim();
  if (!t) throw new Error("YAML 为空");
  const obj = yamlLoad(t);
  if (!obj || typeof obj !== "object") throw new Error("YAML 解析成功，但结果不是对象");
  return obj;
}

function parseAndApply() {
  parseError.value = "";
  try {
    const obj = parseYaml(yamlText.value);
    configObj.value = normalizeConfig(obj);
    if (!selectedProjectId.value) selectedProjectId.value = configObj.value.active_project_id;
    statusText.value = "已解析";
    emitProjectFromSelection();
  } catch (e) {
    parseError.value = e && e.message ? e.message : String(e);
  }
}

function downloadText(filename, text) {
  const blob = new Blob([text], { type: "text/yaml;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

function downloadConfig() {
  parseError.value = "";
  try {
    const obj = configObj.value && configObj.value.raw ? configObj.value.raw : parseYaml(yamlText.value);
    const text = yamlDump(obj, { lineWidth: 120 });
    downloadText("config.yaml", text);
    statusText.value = "已导出";
  } catch (e) {
    parseError.value = e && e.message ? e.message : String(e);
  }
}

function readFileAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result || ""));
    reader.onerror = () => reject(reader.error || new Error("读取文件失败"));
    reader.readAsText(file);
  });
}

const handleBeforeUpload = async (file) => {
  parseError.value = "";
  try {
    const text = await readFileAsText(file);
    yamlText.value = text;
    parseAndApply();
    statusText.value = "已导入";
  } catch (e) {
    parseError.value = e && e.message ? e.message : String(e);
  }
  return false;
};

const exampleYaml = `workspace:\n  inputs_dir: "work/inputs"\n  outputs_dir: "work/outputs"\n  meta_dir: "work/meta"\n\nactive_project_id: "example"\n\nprojects:\n  - id: "example"\n    name: "example-project"\n    slug_en: "example-project"\n`;

function resetToExample() {
  yamlText.value = exampleYaml;
  parseAndApply();
}

const projects = computed(() => (configObj.value ? configObj.value.projects : []));

const selectedProjectId = ref(props.projectInfo && props.projectInfo.id ? String(props.projectInfo.id) : "");
watch(
  () => props.projectInfo,
  (next) => {
    if (!next || !next.id) return;
    if (!selectedProjectId.value) selectedProjectId.value = String(next.id);
  },
  { immediate: true }
);

const selectedProject = computed(() => projects.value.find((p) => p.id === selectedProjectId.value) || null);

function emitProjectFromSelection() {
  if (!selectedProject.value) return;
  emit("update:project-info", {
    id: selectedProject.value.id,
    name: selectedProject.value.name,
    slug_en: selectedProject.value.slug_en
  });
}

async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    statusText.value = "已复制命令";
  } catch {
    statusText.value = "复制失败";
  }
}

function copyCommand(cmd) {
  const pid = selectedProjectId.value || "example";
  copyToClipboard(`${cmd} project_id=${pid}`);
}
</script>
