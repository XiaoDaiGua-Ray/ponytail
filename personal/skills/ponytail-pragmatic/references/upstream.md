# 来源与改造对应关系

基于 [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)，版本 5.3.2，基线提交 `09c434ab73ca43761c5d8b0c5d341926c2fba710`。

主要来源是 [skills/ponytail/SKILL.md](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail/SKILL.md)。同时参考了 [AGENTS.md](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/AGENTS.md) 的精简规则，以及 [ponytail-instructions.js](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/hooks/ponytail-instructions.js) 读取核心 skill、按模式筛选并注入上下文的实现。

| 上游规则 | 本改编 |
| --- | --- |
| Before you write：先读代码、确认调用方与影响范围 | 保留真实调用与数据流检查，补充用户范围和当前项目契约 |
| The smallest complete change：六级选择顺序 | 保留必要性 → 项目复用 → 平台能力 → 已有依赖 → 直接表达 → 最小完整实现 |
| 无需求的抽象、包装和预留功能不应新增 | 保留，明确必要复杂性可由需求或证据支撑 |
| 保留既有结构；修 bug 时检查调用者 | 保留，避免把真实不同的业务契约强行合并 |
| Never cut：校验、防数据丢失、安全、无障碍和硬件校准 | 保留，并要求满足项目规定的兼容性、性能和行为 |
| 新非平凡逻辑留一个小测试 | 改为风险与已有覆盖驱动；执行权限和项目验证要求优先 |
| 单行注释、固定 shortcut 标签 | 改为遵守当前项目的注释与已知限制记录约定 |
| 每条回复固定追加未检查项与风险 | 改为只披露与当前结论相关的验证边界及实质限制 |
| 编码人格、lite/full/ultra、整会话模式 | 改为跨任务的协作偏好；编码规则仅用于编码，当前用户要求决定深度 |
| 宿主 Hook 自动注入规则 | 使用 Codex 原生 skill 发现与调用机制，保持自动选择；本技能不附带 Hook |

本 fork 在 `personal/skills/ponytail-pragmatic/` 维护改编，保留上游 `skills/ponytail/` 及适配器用于比较和合并更新。该目录完整复制后即可独立使用；`LICENSE` 保留上游版权与 MIT 许可。

维护时先比较上游核心规则变化，只吸收与本技能目标和兼容边界一致的变更。不要自动覆盖个人改编，也不要将上游性能百分比当作本版本的测量结果。

兼容性通过读取当前任务适用的规范实现；不依赖特定框架名，不需要逐个添加 harness 适配器。该设计不代表已验证所有宿主或所有框架。
