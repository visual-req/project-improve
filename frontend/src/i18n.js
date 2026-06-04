const Vue = (typeof window !== "undefined" && (window.__VUE__ || window.Vue)) || null;
const ref = Vue && Vue.ref ? Vue.ref : null;
const computed = Vue && Vue.computed ? Vue.computed : null;

const STORAGE_KEY = "prjmx.locale";

const DICT = {
  "zh-CN": {
    "app.title": "项目ORID持续改进",
    "nav.analysis": "项目分析",
    "nav.configSystem": "系统访问配置",
    "nav.configMetrics": "度量指标配置",
    "nav.concept": "理念",
    "nav.projectManage": "项目管理",
    "nav.actions": "行动项管理",
    "common.project": "项目",
    "common.selectProjectFirst": "请先选择项目。",
    "common.reloadProjects": "重载项目列表",
    "common.close": "关闭",
    "common.save": "保存",
    "common.detail": "详情",
    "common.edit": "编辑",
    "common.create": "新增",
    "common.delete": "删除",
    "common.cancel": "取消",
    "common.confirmDelete": "确认删除？",
    "common.language": "语言",
    "analysis.tabs.collect": "收集数据",
    "analysis.tabs.metrics": "问题发现",
    "analysis.tabs.orid": "持续改进",
    "analysis.run.collect": "执行收集数据",
    "analysis.run.metrics": "执行问题发现",
    "analysis.run.orid": "执行持续改进",
    "analysis.files": "输入/输出文件",
    "analysis.scope": "本次分析范围（按度量指标选择）",
    "analysis.noMetricsYet": "尚未读取到度量结果。",
    "analysis.noReportYet": "尚未读取到改进报告。",
    "analysis.reportReady": "改进报告已生成",
    "analysis.actionCandidates": "候选行动项",
    "analysis.addToPlan": "添加到行动计划",
    "analysis.addedToPlan": "已加入行动计划",
    "analysis.addedToPlanHint": "该行动项已在行动计划中",
    "analysis.addToPlanHelp":
      "候选行动项是分析生成的建议清单；加入行动计划后会进入“行动项管理”，用于分配负责人、维护进度、记录实际效果并形成闭环。候选行动项可能随新一轮分析变化，但行动计划会保留你的落地执行记录。",
    "plan.title": "行动计划（actions.json）",
    "plan.addCustom": "新增自定义行动项",
    "plan.empty": "暂无行动项。可新增自定义行动项。",
    "plan.saveSnapshot": "保存改进快照",
    "plan.snapshotNoReport": "未找到度量结果/改进报告，本次快照仅保存行动计划的进度概览。",
    "plan.savedSnapshot": "已保存快照",
    "plan.fillId": "请填写编号。",
    "plan.updateNotFound": "未找到要更新的行动项。",
    "plan.savedAction": "已保存行动项",
    "plan.createdAction": "已新增行动项",
    "plan.item.detail": "行动项详情",
    "plan.item.edit": "编辑行动项",
    "plan.item.create": "新增行动项",
    "plan.footerHelp": "行动计划用于管理“已确认要落地的行动项”，可以持续维护负责人、进度与实际效果；候选行动项来自分析建议，可能随新一轮分析发生变化。",
    "status.not_started": "未开始",
    "status.in_progress": "进行中",
    "status.done": "已完成",
    "status.canceled": "已取消",
    "status.blocked": "阻塞",
    "status.unknown": "未知",
    "severity.high": "高",
    "severity.medium": "中",
    "severity.low": "低",
    "severity.unknown": "未知"
  },
  "ja-JP": {
    "app.title": "プロジェクトORID継続的改善",
    "nav.analysis": "プロジェクト分析",
    "nav.configSystem": "システム接続設定",
    "nav.configMetrics": "メトリクス設定",
    "nav.concept": "コンセプト",
    "nav.projectManage": "プロジェクト管理",
    "nav.actions": "アクション管理",
    "common.project": "プロジェクト",
    "common.selectProjectFirst": "先にプロジェクトを選択してください。",
    "common.reloadProjects": "プロジェクト一覧を再読み込み",
    "common.close": "閉じる",
    "common.save": "保存",
    "common.detail": "詳細",
    "common.edit": "編集",
    "common.create": "追加",
    "common.delete": "削除",
    "common.cancel": "キャンセル",
    "common.confirmDelete": "削除してよろしいですか？",
    "common.language": "言語",
    "analysis.tabs.collect": "データ収集",
    "analysis.tabs.metrics": "課題発見",
    "analysis.tabs.orid": "継続的改善",
    "analysis.run.collect": "データ収集を実行",
    "analysis.run.metrics": "課題発見を実行",
    "analysis.run.orid": "継続的改善を実行",
    "analysis.files": "入出力ファイル",
    "analysis.scope": "今回の分析範囲（選択したメトリクス）",
    "analysis.noMetricsYet": "メトリクス結果がまだありません。",
    "analysis.noReportYet": "改善レポートがまだありません。",
    "analysis.reportReady": "改善レポートを生成しました",
    "analysis.actionCandidates": "候補アクション",
    "analysis.addToPlan": "アクション計画に追加",
    "analysis.addedToPlan": "計画に追加済み",
    "analysis.addedToPlanHint": "すでに計画に含まれています",
    "analysis.addToPlanHelp":
      "候補アクションは分析が提案した一覧です。計画に追加すると「アクション管理」で担当・進捗・実績効果を継続的に管理できます。候補は再分析で変わる可能性がありますが、計画は実行記録を保持します。",
    "plan.title": "アクション計画（actions.json）",
    "plan.addCustom": "カスタムアクションを追加",
    "plan.empty": "アクションはまだありません。カスタムアクションを追加できます。",
    "plan.saveSnapshot": "改善スナップショットを保存",
    "plan.snapshotNoReport": "メトリクス/レポートが見つからないため、今回は計画の進捗概要のみ保存します。",
    "plan.savedSnapshot": "スナップショットを保存しました",
    "plan.fillId": "番号を入力してください。",
    "plan.updateNotFound": "更新対象のアクションが見つかりません。",
    "plan.savedAction": "アクションを保存しました",
    "plan.createdAction": "アクションを追加しました",
    "plan.item.detail": "アクション詳細",
    "plan.item.edit": "アクションを編集",
    "plan.item.create": "アクションを追加",
    "plan.footerHelp": "アクション計画は実行する項目を管理します。担当・進捗・実績効果を継続的に更新できます。候補アクションは分析からの提案で、再分析で変わる可能性があります。",
    "status.not_started": "未着手",
    "status.in_progress": "進行中",
    "status.done": "完了",
    "status.canceled": "中止",
    "status.blocked": "ブロック",
    "status.unknown": "不明",
    "severity.high": "高",
    "severity.medium": "中",
    "severity.low": "低",
    "severity.unknown": "不明"
  },
  "en-US": {
    "app.title": "Project ORID Continuous Improvement",
    "nav.analysis": "Analysis",
    "nav.configSystem": "System Access",
    "nav.configMetrics": "Metrics Config",
    "nav.concept": "Concepts",
    "nav.projectManage": "Project Management",
    "nav.actions": "Action Plan",
    "common.project": "Project",
    "common.selectProjectFirst": "Please select a project first.",
    "common.reloadProjects": "Reload Projects",
    "common.close": "Close",
    "common.save": "Save",
    "common.detail": "Details",
    "common.edit": "Edit",
    "common.create": "Create",
    "common.delete": "Delete",
    "common.cancel": "Cancel",
    "common.confirmDelete": "Confirm delete?",
    "common.language": "Language",
    "analysis.tabs.collect": "Collect",
    "analysis.tabs.metrics": "Insights",
    "analysis.tabs.orid": "Improve",
    "analysis.run.collect": "Run Collection",
    "analysis.run.metrics": "Run Insights",
    "analysis.run.orid": "Run Improvement",
    "analysis.files": "Inputs/Outputs",
    "analysis.scope": "Scope (Selected Metrics)",
    "analysis.noMetricsYet": "No metrics results yet.",
    "analysis.noReportYet": "No improvement report yet.",
    "analysis.reportReady": "Improvement report is ready",
    "analysis.actionCandidates": "Candidate Actions",
    "analysis.addToPlan": "Add to Action Plan",
    "analysis.addedToPlan": "Added to Plan",
    "analysis.addedToPlanHint": "Already in action plan",
    "analysis.addToPlanHelp":
      "Candidate actions are suggestions generated by analysis. Adding to the action plan enables ongoing tracking (owner, progress, actual impact) in the Action Plan page. Candidates may change after re-analysis, but the plan preserves your execution records.",
    "plan.title": "Action Plan (actions.json)",
    "plan.addCustom": "Add Custom Action",
    "plan.empty": "No actions yet. You can add a custom action.",
    "plan.saveSnapshot": "Save Snapshot",
    "plan.snapshotNoReport": "No metrics/report found. This snapshot only saves the action plan progress summary.",
    "plan.savedSnapshot": "Snapshot saved",
    "plan.fillId": "Please fill in the ID.",
    "plan.updateNotFound": "Cannot find the action to update.",
    "plan.savedAction": "Action saved",
    "plan.createdAction": "Action created",
    "plan.item.detail": "Action Details",
    "plan.item.edit": "Edit Action",
    "plan.item.create": "Create Action",
    "plan.footerHelp":
      "The action plan manages confirmed actions to execute. Maintain owner, progress and actual impact over time. Candidate actions come from analysis and may change after re-analysis.",
    "status.not_started": "Not started",
    "status.in_progress": "In progress",
    "status.done": "Done",
    "status.canceled": "Canceled",
    "status.blocked": "Blocked",
    "status.unknown": "Unknown",
    "severity.high": "High",
    "severity.medium": "Medium",
    "severity.low": "Low",
    "severity.unknown": "Unknown"
  }
};

const locale = ref ? ref("zh-CN") : { value: "zh-CN" };

function loadLocale() {
  try {
    const v = window.localStorage.getItem(STORAGE_KEY);
    if (v && DICT[v]) locale.value = v;
  } catch {}
}

function setLocale(next) {
  const v = String(next || "").trim();
  if (!DICT[v]) return;
  locale.value = v;
  try {
    window.localStorage.setItem(STORAGE_KEY, v);
  } catch {}
}

function format(template, params) {
  if (!params || typeof params !== "object") return template;
  return String(template || "").replace(/\{(\w+)\}/g, (m, k) => {
    const v = params[k];
    return v === undefined || v === null ? m : String(v);
  });
}

function t(key, params) {
  const k = String(key || "");
  const lang = locale.value;
  const msg = (DICT[lang] && DICT[lang][k]) || (DICT["zh-CN"] && DICT["zh-CN"][k]) || k;
  return format(msg, params);
}

function useI18n() {
  const currentLocale = computed ? computed(() => locale.value) : { value: locale.value };
  return { t, locale: currentLocale, setLocale, loadLocale, supportedLocales: Object.keys(DICT) };
}

export { useI18n, setLocale, loadLocale, locale };
