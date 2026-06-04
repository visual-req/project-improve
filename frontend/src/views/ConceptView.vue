<template>
  <a-card :bordered="true" style="height: 100%" :title="t('concept.title')">
    <a-row :gutter="[12, 12]">
      <a-col :xs="24" :md="7" :lg="6">
        <a-menu mode="inline" :selectedKeys="[activeKey]" @click="onMenuClick">
          <a-menu-item v-for="it in menuItems" :key="it.key">{{ it.label }}</a-menu-item>
        </a-menu>
      </a-col>
      <a-col :xs="24" :md="17" :lg="18">
        <a-card size="small" :title="activeItem.label">
          <div v-for="(p, idx) in activeItem.paragraphs" :key="String(activeItem.key) + ':p:' + String(idx)" style="line-height: 1.8; margin-bottom: 10px">
            {{ p }}
          </div>
          <div v-for="(it, idx) in activeItem.imgs" :key="String(activeItem.key) + ':img:' + String(idx)" style="margin-top: 10px">
            <div v-if="it.caption" style="color: rgba(0, 0, 0, 0.65); font-size: 12px; margin-bottom: 6px">{{ it.caption }}</div>
            <img :src="it.src" style="width: 100%; max-width: 980px; border: 1px solid #f0f0f0; border-radius: 8px" />
          </div>
        </a-card>
      </a-col>
    </a-row>
  </a-card>
</template>

<script>
import { computed, ref } from "vue";
import { useI18n } from "../i18n.js";

export default {
  setup() {
    const { t, locale } = useI18n();

    const docsDir = computed(() => {
      const v = String(locale.value || "");
      if (v === "en-US" || v === "ja-JP" || v === "zh-CN") return v;
      return "zh-CN";
    });

    function asset(name) {
      return `/docs/${docsDir.value}/assets/${name}`;
    }

    const CONTENT = {
      "zh-CN": [
        {
          key: "overview",
          label: "概览",
          paragraphs: [
            "理念页用于把“问题发现 → 根因分析 → 问题解决”的方法论与示意图集中展示，帮助团队在同一套语言与证据口径下协作。",
            "左侧选择主题，右侧会展示该主题的关键要点、如何落地、以及与 ORID/行动项的关系。",
            "完整文档在 docs/zh-CN/concept/ 目录；这里展示的是用于日常讨论与对齐的“可视化摘要”。"
          ],
          imgs: []
        },
        {
          key: "metrics",
          label: "指标体系",
          paragraphs: [
            "指标不是为了“评价个人”，而是为了把问题尽早显性化：哪里在等待、哪里在返工、哪里在堆积、哪里在门禁失败。",
            "按“阶段 × 类型”组织指标，可以让团队把信号映射到工作流位置（需求/计划、开发/评审、测试/交付、线上/运行），从而更快定位阻碍点。",
            "使用方式：先看趋势与断点，再到看板/PR/CI 等系统中回溯证据，最后再进入 ORID 推导行动项。"
          ],
          imgs: [{ src: asset("metrics-map.svg"), caption: "指标地图：阶段 × 类型" }]
        },
        {
          key: "orid",
          label: "ORID",
          paragraphs: [
            "ORID 用于把“数据与事实”变成“可验收的行动项”。核心是把事实（O）与感受（R）分离，避免把情绪当结论。",
            "O：可复核事实（来自看板/代码/CI/缺陷等）；R：团队摩擦（等待、返工、插入）；I：原因假设与验证；D：决策方向与行动排期/验收。",
            "落地建议：每条行动项都写清负责人、开始时间、验收方法与预期/实际效果，形成可复盘闭环。"
          ],
          imgs: [{ src: asset("orid-process.svg"), caption: "ORID：从事实到行动" }]
        },
        {
          key: "scrum",
          label: "Scrum",
          paragraphs: [
            "Scrum 的关键不是“开会”，而是用固定节奏让风险早暴露：计划对齐范围、站会清障、评审拿反馈、回顾做改进。",
            "重要原则：改进不必等回顾会。看板/WIP、PR/CI 门禁、透明性信号，都应该让问题在更早环节就被发现并处理。"
          ],
          imgs: [{ src: asset("scrum-framework.svg"), caption: "Scrum 框架：工件沿横轴推进，活动发生在交付之后并回流" }]
        },
        {
          key: "pdca",
          label: "PDCA",
          paragraphs: [
            "PDCA 是持续改进的最小闭环：P 定义问题与目标，D 实施最小变更，C 用数据验证效果，A 固化有效做法或修正假设。",
            "用法建议：每次只做 1–2 个最小可行变更，并设定对比窗口（前/后两个时间窗），避免“同时改太多导致无法归因”。"
          ],
          imgs: [{ src: asset("pdca.svg"), caption: "PDCA：计划-执行-检查-处理" }]
        },
        {
          key: "transparency",
          label: "透明性",
          paragraphs: [
            "透明性的目标不是监控个体，而是让团队共享同一张事实底座：风险早暴露、阻碍可定位、行动可验证。",
            "燃尽图用于发现“偏离点”：线条平坦通常意味着等待/验收卡点，突然上升意味着范围变更或返工显性化，末期陡降意味着在制堆积与批量验收。",
            "提交频率用于发现“节奏断点”：长时间低谷常见于澄清/依赖/环境卡住；爆发式提交往往意味着批量合并与质量风险。",
            "质量门禁（覆盖率/Sonar/CI）用于发现“内建质量是否有效”：覆盖率长期不动通常指向可测性/架构耦合问题；门禁频繁失败指向构建稳定性与依赖治理问题。",
            "看板泳道图用于发现“堆积与等待”：某泳道长期堆积就是瓶颈；泳道间等待时间长说明交接/验收标准不清或容量不足；WIP 长期超限会导致整体 Lead Time 上升。",
            "甘特图用于暴露“依赖链与关键路径”：关键路径延期会直接影响交付日期；大量任务依赖单点外部交付时，应前置对齐并拆分依赖。"
          ],
          imgs: [
            { src: asset("transparency-burndown.svg"), caption: "燃尽图：用偏离定位阻碍点" },
            { src: asset("transparency-git-frequency.svg"), caption: "提交节奏：用断点定位阻碍点" },
            { src: asset("transparency-quality-gates.svg"), caption: "质量门禁：覆盖率 / 扫描 / CI 信号" },
            { src: asset("transparency-kanban-swimlane.svg"), caption: "看板泳道：堆积与等待（瓶颈定位）" },
            { src: asset("transparency-gantt.svg"), caption: "甘特图：依赖与关键路径（风险暴露）" }
          ]
        },
        {
          key: "efficiency",
          label: "效率跃迁例子",
          paragraphs: [
            "通过透明性信号，团队可以尽早发现一种常见风险：有人长期闷头开发、交付量显著偏低、反馈稀疏，持续停留在低效区。",
            "这类现象首先要排除系统性原因（外部依赖/权限/环境/评审排队/模块复杂度差异），然后再用“拆小任务 + 频繁集成 + 求助机制 + 门禁固化”的方式帮助跃迁。",
            "目标不是让个人更卷，而是让系统更顺畅：减少等待与返工，让正确做法成为默认。"
          ],
          imgs: [{ src: asset("transparency-efficiency-shift.svg"), caption: "从低效区跃迁到高效区：路径与动作" }]
        },
        {
          key: "cicd",
          label: "CI/CD",
          paragraphs: [
            "CI/CD 的价值是把质量检查与交付流程自动化：问题在合并前暴露、发布可回滚、反馈更快，从而支撑质量左移与持续改进。",
            "关键是把门禁绑定到 PR/流水线：静态检查、测试、扫描、构建稳定性、发布策略与观测信号一起形成反馈回路。"
          ],
          imgs: [{ src: asset("ci-cd-pipeline.svg"), caption: "CI/CD：流水线分区、门禁与反馈回路" }]
        },
        {
          key: "shiftleft",
          label: "质量左移",
          paragraphs: [
            "质量左移是把返工最贵的阶段往前移：从上线前集中补救，变成在需求/设计/编码/评审/CI 阶段就及时发现问题。",
            "落地手段包括：可视化评审、PR 门禁、设计走查、测试策略前置、以及对“可测性/可维护性”的结构化要求。"
          ],
          imgs: [{ src: asset("shift-left-quality.svg"), caption: "Shift Left：把质量门禁前移" }]
        },
        {
          key: "ai",
          label: "AI 赋能",
          paragraphs: [
            "AI 更适合做结构化、风险提示、归因聚类与草稿生成；它可以显著缩短“理解-定位-表达”的时间，但不能替代证据与共识。",
            "使用原则：让 AI 做‘候选’，让团队做‘确认与验收’，并把结果落到可追踪行动项（负责人/开始/验收/效果）。"
          ],
          imgs: [{ src: asset("ai-enabled-points.svg"), caption: "AI 切入点：阶段 × 能力映射" }]
        },
        {
          key: "talent",
          label: "人才模型",
          paragraphs: [
            "持续改进需要深度能力与横向协作的组合：T 型强调一专多能，π/# 型更擅长跨域整合与机制建设。",
            "在团队实践中，π/# 型更容易牵头把改进固化为基线（流程/门禁/工具/模板），让能力建设不依赖个人英雄主义。"
          ],
          imgs: [{ src: asset("talent-models.svg"), caption: "T / π / # 型人才模型示意" }]
        },
        {
          key: "baseline",
          label: "提升基线",
          paragraphs: [
            "提升基线的目标是把‘本次做到’固化成‘以后默认’：从坏味道治理，到自动化测试，再到结构与架构，再到范式与复用。",
            "基线一旦固化，就能显著减少反复踩坑与隐性返工，并为更高层的效率跃迁提供地基。"
          ],
          imgs: [{ src: asset("raise-baseline-code.svg"), caption: "从代码角度逐层提升基线（阶梯式上升）" }]
        }
      ],
      "en-US": [
        {
          key: "overview",
          label: "Overview",
          paragraphs: [
            "This page summarizes the improvement methodology with short explanations and diagrams so the team can align on shared language and evidence.",
            "Pick a topic on the left. The right side shows key ideas, how to apply them, and how they relate to ORID and actions.",
            "Full docs are under docs/en-US/ (and detailed concept pages are currently maintained in Chinese under docs/zh-CN/concept/)."
          ],
          imgs: []
        },
        {
          key: "metrics",
          label: "Metrics System",
          paragraphs: [
            "Metrics are not for evaluating individuals. They surface system problems early: waiting, rework, piling up, and gate failures.",
            "Organizing metrics by Stage × Type helps map signals back to workflow locations (Plan, Dev/Review, Test/Delivery, Production/Run).",
            "Suggested flow: look for trends/breakpoints → trace evidence in boards/PR/CI → use ORID to derive actionable items."
          ],
          imgs: [{ src: asset("metrics-map.svg"), caption: "Metrics map: Stage × Type" }]
        },
        {
          key: "orid",
          label: "ORID",
          paragraphs: [
            "ORID turns facts into actions with clear acceptance. The key is separating Objective facts (O) from Reflective feelings (R).",
            "O: verifiable facts (board/code/CI/defects). R: friction (waiting, rework, interrupts). I: hypotheses & validation. D: decisions and action plans.",
            "Tip: every action should have an owner, start date, acceptance method, and expected/actual impact for a closed loop."
          ],
          imgs: [{ src: asset("orid-process.svg"), caption: "ORID: from facts to actions" }]
        },
        { key: "scrum", label: "Scrum", paragraphs: ["Scrum is not about meetings. It is a cadence to expose risks early and improve continuously.", "Use visual signals (WIP, PR/CI gates, transparency indicators) to discover and fix issues earlier."], imgs: [{ src: asset("scrum-framework.svg"), caption: "Scrum framework (diagram)" }] },
        { key: "pdca", label: "PDCA", paragraphs: ["PDCA is the smallest continuous-improvement loop: Plan → Do → Check → Act.", "Make 1–2 small changes at a time and compare before/after windows to avoid confusing causality."], imgs: [{ src: asset("pdca.svg"), caption: "PDCA loop (diagram)" }] },
        { key: "transparency", label: "Transparency", paragraphs: ["Transparency is not surveillance. It creates a shared fact base: risks surface early, blockers are locatable, and actions are verifiable."], imgs: [{ src: asset("transparency-burndown.svg"), caption: "Burndown (diagram)" }, { src: asset("transparency-git-frequency.svg"), caption: "Commit rhythm (diagram)" }, { src: asset("transparency-quality-gates.svg"), caption: "Quality gates (diagram)" }, { src: asset("transparency-kanban-swimlane.svg"), caption: "Swimlane (diagram)" }, { src: asset("transparency-gantt.svg"), caption: "Gantt delay (diagram)" }] },
        { key: "efficiency", label: "Efficiency Shift Example", paragraphs: ["Signals can highlight a common risk: low throughput + sparse feedback. First rule out systemic causes, then improve via smaller batches, frequent integration, help-seeking mechanisms, and gates."], imgs: [{ src: asset("transparency-efficiency-shift.svg"), caption: "Efficiency shift (diagram)" }] },
        { key: "cicd", label: "CI/CD", paragraphs: ["CI/CD automates checks and delivery: issues surface before merge, releases are safer, and feedback is faster.", "Bind gates to PR/pipelines: lint/tests/scans/build stability/release strategy/observability form the feedback loop."], imgs: [{ src: asset("ci-cd-pipeline.svg"), caption: "CI/CD pipeline (diagram)" }] },
        { key: "shiftleft", label: "Shift Left Quality", paragraphs: ["Shift-left moves expensive rework earlier: discover problems in requirements/design/coding/review/CI instead of late-stage firefighting."], imgs: [{ src: asset("shift-left-quality.svg"), caption: "Shift left (diagram)" }] },
        { key: "ai", label: "AI Enabled", paragraphs: ["AI is best for structure, risk hints, clustering, and drafting. It speeds up understanding and articulation, but cannot replace evidence and consensus."], imgs: [{ src: asset("ai-enabled-points.svg"), caption: "AI entry points (diagram)" }] },
        { key: "talent", label: "Talent Models", paragraphs: ["Continuous improvement needs deep expertise plus cross-functional collaboration (T / π / # shapes)."], imgs: [{ src: asset("talent-models.svg"), caption: "Talent models (diagram)" }] },
        { key: "baseline", label: "Raise the Baseline", paragraphs: ["Raise the baseline by turning one-off wins into defaults: from smell fixes, to tests, to architecture, to reusable patterns."], imgs: [{ src: asset("raise-baseline-code.svg"), caption: "Baseline ladder (diagram)" }] }
      ],
      "ja-JP": [
        { key: "overview", label: "概要", paragraphs: ["このページは、継続的改善の考え方を短い説明と図でまとめ、チームが同じ言葉と証拠で合意できるようにします。", "左でテーマを選ぶと、右に要点・適用方法・ORID/アクションとの関係を表示します。", "詳細ドキュメントは docs/ja-JP/ にあり、コンセプトの詳細本文は現在 docs/zh-CN/concept/（中国語）でメンテナンスしています。"], imgs: [] },
        { key: "metrics", label: "メトリクス体系", paragraphs: ["メトリクスは個人評価のためではなく、待ち・手戻り・滞留・門禁失敗などのシステム課題を早期に可視化するためのものです。", "段階×タイプで整理すると、シグナルをワークフロー上の位置に対応づけやすくなります。", "おすすめ：トレンド/断点 → 看板/PR/CI で証拠 → ORID でアクションへ。"], imgs: [{ src: asset("metrics-map.svg"), caption: "メトリクスマップ（図）" }] },
        { key: "orid", label: "ORID", paragraphs: ["ORID は事実をアクションに落とし込むための枠組みです。O（事実）と R（感情）を分離します。", "O: 検証可能な事実。R: 摩擦。I: 仮説と検証。D: 決定と計画。", "各アクションには担当・開始日・受け入れ方法・期待/実績効果を記載し、閉ループにします。"], imgs: [{ src: asset("orid-process.svg"), caption: "ORID（図）" }] },
        { key: "scrum", label: "Scrum", paragraphs: ["Scrum は会議のためではなく、固定のリズムでリスクを早く露出させ、改善するための仕組みです。", "WIP、PR/CI の門禁、透明性のシグナルで、より早い段階で発見・解決します。"], imgs: [{ src: asset("scrum-framework.svg"), caption: "Scrum（図）" }] },
        { key: "pdca", label: "PDCA", paragraphs: ["PDCA は最小の改善ループ：Plan → Do → Check → Act。", "一度に 1–2 個の小さな変更に絞り、前後の比較期間を設けます。"], imgs: [{ src: asset("pdca.svg"), caption: "PDCA（図）" }] },
        { key: "transparency", label: "透明性", paragraphs: ["透明性は監視ではなく、共通の事実基盤を作り、阻害要因の特定と検証可能なアクションを支えます。"], imgs: [{ src: asset("transparency-burndown.svg"), caption: "バーンダウン（図）" }, { src: asset("transparency-git-frequency.svg"), caption: "コミットリズム（図）" }, { src: asset("transparency-quality-gates.svg"), caption: "品質門禁（図）" }, { src: asset("transparency-kanban-swimlane.svg"), caption: "スイムレーン（図）" }, { src: asset("transparency-gantt.svg"), caption: "ガント遅延（図）" }] },
        { key: "efficiency", label: "効率のジャンプ例", paragraphs: ["低スループット＋フィードバックの希薄さはよくあるリスクです。まずシステム要因を除外し、次に小さなバッチ・頻繁な統合・助け合い・門禁で改善します。"], imgs: [{ src: asset("transparency-efficiency-shift.svg"), caption: "効率のジャンプ（図）" }] },
        { key: "cicd", label: "CI/CD", paragraphs: ["CI/CD は品質チェックとデリバリーを自動化し、マージ前に問題を露出させ、速いフィードバックを実現します。"], imgs: [{ src: asset("ci-cd-pipeline.svg"), caption: "CI/CD（図）" }] },
        { key: "shiftleft", label: "品質左シフト", paragraphs: ["手戻りが高コストになる前に、要求/設計/実装/レビュー/CI の段階で問題を発見します。"], imgs: [{ src: asset("shift-left-quality.svg"), caption: "左シフト（図）" }] },
        { key: "ai", label: "AI 活用", paragraphs: ["AI は構造化、リスク提示、クラスタリング、ドラフト生成に向きます。証拠と合意の代替にはなりません。"], imgs: [{ src: asset("ai-enabled-points.svg"), caption: "AI の切り口（図）" }] },
        { key: "talent", label: "人材モデル", paragraphs: ["継続的改善には深さと横断協力（T / π / #）が必要です。"], imgs: [{ src: asset("talent-models.svg"), caption: "人材モデル（図）" }] },
        { key: "baseline", label: "基線の引き上げ", paragraphs: ["一度の成功をデフォルトにします。臭いの解消→テスト→アーキテクチャ→再利用可能なパターンへ。"], imgs: [{ src: asset("raise-baseline-code.svg"), caption: "基線（図）" }] }
      ]
    };

    const menuItems = computed(() => CONTENT[docsDir.value] || CONTENT["zh-CN"]);

    const activeKey = ref("overview");

    const byKey = computed(() => {
      const m = {};
      (menuItems.value || []).forEach((x) => (m[String(x.key)] = x));
      return m;
    });

    const activeItem = computed(() => byKey.value[String(activeKey.value)] || (menuItems.value && menuItems.value[0]) || { key: "", label: "", paragraphs: [], imgs: [] });

    function onMenuClick(e) {
      activeKey.value = e && e.key ? String(e.key) : "overview";
    }

    return { t, menuItems, activeKey, activeItem, onMenuClick };
  }
};
</script>
