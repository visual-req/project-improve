<template>
  <div v-if="!rootNode" style="color: rgba(0, 0, 0, 0.65)">未提供根因图数据。</div>
  <div v-else style="width: 100%; overflow: auto">
    <svg :width="svgWidth" :height="svgHeight" :viewBox="`0 0 ${layout.width} ${layout.height}`" role="img">
      <g>
        <path
          v-for="e in layout.edges"
          :key="e.id"
          :d="e.d"
          :stroke="edgeColor"
          :stroke-width="e.strokeWidth"
          fill="none"
          stroke-linecap="round"
        />
      </g>
      <g>
        <g v-for="n in layout.nodes" :key="n.id">
          <rect
            :x="n.x"
            :y="n.y"
            :width="n.w"
            :height="n.h"
            rx="10"
            :fill="n.fill"
            stroke="#d9d9d9"
          />
          <text
            :x="n.x + 12"
            :y="n.y + 22"
            font-size="12"
            font-family="system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial"
            fill="#262626"
          >
            {{ n.title }}
          </text>
          <text
            :x="n.x + 12"
            :y="n.y + 40"
            font-size="11"
            font-family="system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial"
            fill="#595959"
          >
            {{ n.subTitle }}
          </text>
        </g>
      </g>
    </svg>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  root: { type: Object, default: null }
});

const edgeColor = "#8c8c8c";

function safeNumber(value) {
  const n = typeof value === "number" ? value : Number(value);
  return Number.isFinite(n) ? n : null;
}

function normalizeNode(node) {
  const children = Array.isArray(node && node.children) ? node.children : [];
  const normalizedChildren = children.map(normalizeNode);
  if (normalizedChildren.length === 0) {
    const w = safeNumber(node && node.weight);
    return {
      id: String((node && node.id) || cryptoRandomId()),
      title: String((node && node.title) || "—"),
      confidence: String((node && node.confidence) || ""),
      evidence: Array.isArray(node && node.evidence) ? node.evidence : [],
      weight: w === null ? 0 : w,
      children: []
    };
  }
  const weight = normalizedChildren.reduce((sum, c) => sum + (safeNumber(c.weight) || 0), 0);
  return {
    id: String((node && node.id) || cryptoRandomId()),
    title: String((node && node.title) || "—"),
    confidence: String((node && node.confidence) || ""),
    evidence: Array.isArray(node && node.evidence) ? node.evidence : [],
    weight,
    children: normalizedChildren
  };
}

function cryptoRandomId() {
  try {
    return crypto.randomUUID();
  } catch {
    return String(Math.random()).slice(2);
  }
}

function buildLayout(root) {
  const paddingX = 16;
  const paddingY = 16;
  const xGap = 220;
  const leafGap = 62;
  const boxW = 200;
  const boxH = 54;

  const leaves = [];
  function collectLeaves(n) {
    if (!n.children || n.children.length === 0) {
      leaves.push(n);
      return;
    }
    n.children.forEach(collectLeaves);
  }
  collectLeaves(root);

  const leafY = new Map();
  leaves.forEach((n, idx) => {
    leafY.set(n.id, paddingY + idx * leafGap);
  });

  const nodes = [];
  const edges = [];

  function clamp01(v) {
    if (v < 0) return 0;
    if (v > 1) return 1;
    return v;
  }

  function colorFromWeight(w) {
    const t = clamp01(w);
    const a = 0.08 + t * 0.18;
    return `rgba(24, 144, 255, ${a.toFixed(3)})`;
  }

  function subTitle(n) {
    const weight = safeNumber(n.weight);
    const pct = weight === null ? "—" : `${Math.round(weight * 100)}%`;
    const conf = n.confidence ? ` / ${n.confidence}` : "";
    return `权重 ${pct}${conf}`;
  }

  function assign(n, depth) {
    const x = paddingX + depth * xGap;
    let y;
    if (!n.children || n.children.length === 0) {
      y = leafY.get(n.id) ?? paddingY;
    } else {
      const ys = n.children.map((c) => assign(c, depth + 1));
      y = ys.reduce((a, b) => a + b, 0) / ys.length;
    }

    nodes.push({
      id: n.id,
      title: n.title,
      subTitle: subTitle(n),
      x,
      y,
      w: boxW,
      h: boxH,
      fill: colorFromWeight(n.weight)
    });

    if (n.children && n.children.length) {
      n.children.forEach((c) => {
        const childX = paddingX + (depth + 1) * xGap;
        const childY = getNodeY(c.id);
        const sx = x + boxW;
        const sy = y + boxH / 2;
        const tx = childX;
        const ty = childY + boxH / 2;
        const mx = (sx + tx) / 2;
        edges.push({
          id: `${n.id}->${c.id}`,
          d: `M ${sx} ${sy} C ${mx} ${sy}, ${mx} ${ty}, ${tx} ${ty}`,
          strokeWidth: 1 + clamp01(safeNumber(c.weight) || 0) * 5
        });
      });
    }

    return y;
  }

  const yById = new Map();
  function getNodeY(id) {
    if (yById.has(id)) return yById.get(id);
    return paddingY;
  }

  function preAssignY(n, depth) {
    if (!n.children || n.children.length === 0) {
      yById.set(n.id, leafY.get(n.id) ?? paddingY);
      return yById.get(n.id);
    }
    const ys = n.children.map((c) => preAssignY(c, depth + 1));
    const y = ys.reduce((a, b) => a + b, 0) / ys.length;
    yById.set(n.id, y);
    return y;
  }
  preAssignY(root, 0);

  assign(root, 0);

  const maxDepth = Math.max(...nodes.map((n) => (n.x - paddingX) / xGap));
  const width = paddingX * 2 + (maxDepth + 1) * xGap + boxW - xGap;
  const height = paddingY * 2 + Math.max(boxH, leaves.length * leafGap);

  return { nodes, edges, width, height };
}

const rootNode = computed(() => (props.root ? normalizeNode(props.root) : null));
const layout = computed(() => (rootNode.value ? buildLayout(rootNode.value) : { nodes: [], edges: [], width: 1, height: 1 }));

const svgWidth = "100%";
const svgHeight = computed(() => Math.min(680, Math.max(260, layout.value.height)));
</script>
