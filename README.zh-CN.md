# AgentMind

用于沉淀一套面向工作与学习场景的 Agent 思维模式、执行流程与可复用技能。

[English README](./README.md)

## 项目简介

AgentMind 是一个用于持续构建个人助手体系的仓库，核心目标是把稳定、可复用的 Agent / Skill 工作方式沉淀下来，既服务于自己的学习与工作，也方便后续分享给他人使用。

这个仓库当前主要关注以下方向：

- 学习与研究
- 规划与评审
- 执行过程约束
- 可复用 Agent 能力沉淀

## 当前已添加技能

### `prohibition`

当前仓库中的第一个公开技能是 [`prohibition`](./skills/prohibition/SKILL.md)。

`prohibition` 背后的核心判断是：Agent 的稳定性，并不主要来自一段试图把“该做什么”一次性说全的大而全 SOP，而是来自一套分层的负向约束系统。

1. 常驻系统提示只保留高频、通用、可复用的边界规则。
2. 与当前会话相关的约束按需注入，而不是默认全部展开。
3. Skill 不应预先塞满上下文，而应先做低成本发现，命中后再展开正文。
4. 工具提示、权限规则、分类器、沙箱、运行期切换等机制，会在执行阶段再次兜底，把“禁令”从文案变成机制。

它针对的是已知失误模式，采用的是“先发现，再展开”的渐进式披露思路：把详细约束延迟到真正需要的时候，同时让不同层次各自提供独立兜底。

`prohibition` 现在被定位为一层内部 anti-regression 约束。它的目标是减少错误确定性、误报完成、范围漂移以及 safety theater 这类坏结果，而不是默认把开放探索压缩成保守答案，或把边界话术暴露给用户。

### `exp`

当前仓库中的第二个公开技能是 [`exp`](./skills/exp/SKILL.md)。

`exp` 是一个被动触发、面向失败后的经验库。它不试图提前阻止模型犯错，而是在具体失败已经发生之后，帮助模型检索过往的已解决路径和可复用的 dead-end 经验，减少在同类问题上的重复试错成本。

它把运行时规则和经验内容分开：

- [`skills/exp/SKILL.md`](./skills/exp/SKILL.md)：触发条件、失败分簇、检索预算、`pending` 规则、晋升规则
- [`skills/exp/scripts/`](./skills/exp/scripts/)：`.explib` 的脚本执行层，目前覆盖初始化、校验与只读查询
- [`.explib/EXP.md`](./.explib/EXP.md)：封闭分类法、导航入口、手动扩展说明
- [`.explib/domains/`](./.explib/domains/)：resolved 和 dead-end 共用的 domain 级 TOC

## 仓库结构

- [`skills/prohibition/`](./skills/prohibition/)：`prohibition` 技能及其配套参考模块
- [`skills/exp/`](./skills/exp/)：`exp` 技能运行规则与检索行为定义
- [`skills/exp/scripts/`](./skills/exp/scripts/)：`.explib` 初始化、校验与查询脚本
- [`.explib/`](./.explib/)：经验库路由文档、顶层 TOC 与 domain 导航
- [`README.md`](./README.md)：英文版项目简介
