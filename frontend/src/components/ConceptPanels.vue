<template>
  <a-collapse accordion>
    <a-collapse-panel key="overview" header="概念导航（按：问题发现 → 根因分析 → 问题解决）">
      <div style="line-height: 1.8">
        本页面展示持续改进常用概念与示意图。完整文本说明见 docs/concept/ 目录下的各个文件。
      </div>
    </a-collapse-panel>
    <a-collapse-panel key="metrics" header="指标体系（按阶段 × 类型）">
      <div style="line-height: 1.8; margin-bottom: 10px">
        指标以阶段与类型组织，是为了把度量映射到工作流位置，便于从“现象 → 证据 → 原因 → 行动”形成闭环。
      </div>
      <img
        src="/docs/assets/metrics-map.svg"
        style="width: 100%; max-width: 960px; border: 1px solid #f0f0f0; border-radius: 8px"
      />
    </a-collapse-panel>
    <a-collapse-panel key="orid" header="ORID 方法（把数据转成行动）">
      <img
        src="/docs/assets/orid-process.svg"
        style="width: 100%; max-width: 960px; border: 1px solid #f0f0f0; border-radius: 8px; margin-bottom: 10px"
      />
      <div style="line-height: 1.8">O：可复核事实；R：摩擦与感受；I：原因假设与验证；D：行动项与验收。</div>
    </a-collapse-panel>
    <a-collapse-panel key="scrum" header="Scrum 框架（回顾会的位置 + 尽早改进）">
      <img src="/docs/assets/scrum-framework.svg" style="width: 100%; max-width: 960px; border: 1px solid #f0f0f0; border-radius: 8px; margin-bottom: 10px" />
      <div style="line-height: 1.8">
        回顾会在迭代末尾，但改进不必等回顾会：站会清障、看板/WIP、PR/CI 门禁都可以让问题更早被发现与解决。
      </div>
    </a-collapse-panel>
    <a-collapse-panel key="pdca" header="PDCA（持续改进闭环）">
      <img
        src="/docs/assets/pdca.svg"
        style="width: 100%; max-width: 960px; border: 1px solid #f0f0f0; border-radius: 8px; margin-bottom: 10px"
      />
      <div style="line-height: 1.8">
        P：定义问题与目标；D：实施最小变更；C：用数据验证效果；A：固化或修正假设，进入下一轮。
      </div>
    </a-collapse-panel>
    <a-collapse-panel key="cicd" header="持续集成/持续交付（CI/CD）与门禁">
      <img src="/docs/assets/ci-cd-pipeline.svg" style="width: 100%; max-width: 960px; border: 1px solid #f0f0f0; border-radius: 8px; margin-bottom: 10px" />
      <div style="line-height: 1.8">
        CI/CD 的价值是把质量检查与交付流程自动化：问题在合并前暴露、发布可回滚、反馈更快，从而支撑质量左移与持续改进。
      </div>
    </a-collapse-panel>
    <a-collapse-panel key="shiftleft" header="质量左移（Shift Left Quality）">
      <img src="/docs/assets/shift-left-quality.svg" style="width: 100%; max-width: 960px; border: 1px solid #f0f0f0; border-radius: 8px; margin-bottom: 10px" />
      <div style="line-height: 1.8">把质量门禁前移到需求/设计/编码/评审/CI，减少重开与缺陷逃逸。</div>
    </a-collapse-panel>
    <a-collapse-panel key="ai" header="AI 赋能（按阶段切入点映射）">
      <img src="/docs/assets/ai-enabled-points.svg" style="width: 100%; max-width: 960px; border: 1px solid #f0f0f0; border-radius: 8px; margin-bottom: 10px" />
      <div style="line-height: 1.8">
        AI 更适合做结构化、风险提示、归因聚类与草稿生成；最终结论仍需团队基于证据确认并落到可验收行动项。
      </div>
    </a-collapse-panel>
    <a-collapse-panel key="talent" header="人才模型：T / π / # 型">
      <img src="/docs/assets/talent-models.svg" style="width: 100%; max-width: 960px; border: 1px solid #f0f0f0; border-radius: 8px; margin-bottom: 10px" />
      <div style="line-height: 1.8">持续改进需要深度能力与横向协作的组合，π/# 型更擅长牵头机制建设与提升基线。</div>
    </a-collapse-panel>
    <a-collapse-panel key="baseline" header="提升基线（逐层把正确做法固化为默认）">
      <img src="/docs/assets/raise-baseline-code.svg" style="width: 100%; max-width: 960px; border: 1px solid #f0f0f0; border-radius: 8px; margin-bottom: 10px" />
      <div style="line-height: 1.8">从坏味道→测试→结构→范式逐层提升，把改进从“本次做到”变成“以后默认”。</div>
    </a-collapse-panel>
    <a-collapse-panel key="why" header="5 Why（原因树/思维导图 + 权重）">
      <img
        src="/docs/assets/5whys.svg"
        style="width: 100%; max-width: 960px; border: 1px solid #f0f0f0; border-radius: 8px; margin-bottom: 10px"
      />
      <img
        src="/docs/assets/5why-example.svg"
        style="width: 100%; max-width: 960px; border: 1px solid #f0f0f0; border-radius: 8px; margin-bottom: 10px"
      />
      <div style="line-height: 1.8">
        5 Why 更适合作为“下钻框架”。真实问题往往是多路径并行原因，建议用原因树展开分支，再收敛到可验证杠杆点。
      </div>
    </a-collapse-panel>
    <a-collapse-panel key="actions" header="行动项（字段化 + 排期 + 验收）">
      <div style="line-height: 1.8">
        行动项需要明确：问题、原因、方案、发现/截止/完成日期、预期效果、验收方法、负责人角色，确保可追踪、可复盘、可度量。
      </div>
    </a-collapse-panel>
  </a-collapse>
</template>
