# ORID 分析（根因分析与改进闭环）

命令指令：`/prjmx:orid`

目标：把指标与样本事实转化为可验证的根因假设，并输出可执行决策与行动方向（供下一步排期与落盘）。

## 输入

- `metrics`（当前值、趋势、阈值判定）
- `data_integrity`（缺失字段与可靠性提示）
- `raw`（需要时引用具体样本：aging wip、重开条目、review 延迟条目、escaped 缺陷等）

## 子步骤（展开版）

按顺序执行：

1. `01-objective.md`：提炼客观事实（必须可引用、可复核）
2. `02-reflective.md`：将事实转译为团队摩擦点（不归因个人）
3. `03-interpretive.md`：提出原因假设（证据 + 反证 + 数据缺口）
4. `04-root-cause-mindmap.md`：用思维导图方式扩展原因树，输出带权重的根因图 JSON
5. `05-decisional.md`：形成决策方向与约束（量化目标、优先级）

## 输出（给下一步消费）

生成 `orid` 对象：

- `orid.objective`：数组（5–10 条事实）
- `orid.reflective`：数组（5–10 条感受/摩擦点）
- `orid.interpretive`：数组（3–5 个原因假设；每条包含证据与反证摘要）
- `orid.decisional`：数组（决策方向与行动原则）

可选补充：

- `issues`：从红/黄指标与异常样本提炼的问题清单（下一步会用于行动排期）
