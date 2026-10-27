# M7C 直接频点诊断阶段长任务计划 — 2026-10-27

状态：IMPLEMENTATION_QUALIFICATION_IN_PROGRESS；原科学状态保持 HOLD_M7C_GUARD。

## 用户授权与阶段范围

用户确认上一轮单假设方案，并明确授权：

> 请你自己规划一个长任务，你可以自行决定是否需要build或者solve，我给你权限。直到这个阶段的任务做完。

本授权适用于 M7C 弱响应直接频点诊断这一阶段的准备、必要执行、只读资格判定和完整 closeout。它不是整个项目后续架构/几何优化的无限授权。

代理当前决定：不需要重建几何。使用已通过 BUILD/人工 review 的相同 M7C 源，准备最多一次新 SOLVE 事务；仅改变已预登记的直接频点计算/结果语义。BUILD 不设为 live，不改变 moat、回流结构、材料、端口或线性求解精度。此处预算是新阶段预算，旧 recovery 的一次消费和所有失败证据保持不动。

准备期间 live booleans 均保持 false。只有入口资格 PASS、source commit/入口/依赖哈希冻结后，才根据本条用户明确授权建立本阶段唯一 live SOLVE grant。记录“准备授权”与“具体一次性 live grant”之间的区别，不从历史 grant 推断权限。

## 工作顺序与完成条件

1. **实现资格**：核对 CST 2022 安装版帮助中的直接采样 API；证明它区别于宽带曲线重新采样；完成控制 Python/CST Python 兼容、help、静态调用预算、native parser 和诊断判别逻辑的回归。无 production solver。
2. **冻结并执行**：沿用 `M7C_WEAK_RESPONSE_DIRECT_SAMPLE_FREEZE_V01.md` 的 15 个频点、一个主假设、原始数值门槛与新诊断分辨标准。冻结明确 config/入口/依赖，建立 fresh matching SOLVE grant、runner-task-v0.2 packet，native contract-check/validate/dry-run 全部 PASS 后最多一次 run_solver。实际命令、source/contract/packet SHA 和执行边界全部记录。
3. **判定与关闭**：只读导出 96×15 直接频点响应及原生求解/残差/收敛证据，判为 H_NUM_SUPPORTED / FEATURE_REPRODUCED / INCONCLUSIVE_HOLD；如遇执行失败则保留具体 HOLD。锁定完整项目身份、关闭 grant、同步 handoff/contract/报告并提交证据。

阶段完成不要求得到某个有利结果；可审计的 INCONCLUSIVE/HOLD 是有效终态。若 solver 已完成而提取代码失败，仅允许零求解的只读提取修复，不能重跑已完成 solver。

## 执行边界

- 主机 NW；用户此前明确允许 Codex 直接 SSH，不强制 DC。沿用 SimulationOps 0.2.26，runner/native locks 不绕过。
- 原 BUILD、旧 solved file 和 D: 各基线保持只读；新输出使用新的项目私有 C: NTFS 目录。
- 输出 32 GiB、TEMP 8 GiB，同卷合计 40 GiB；在 presolve 前和唯一 solver 调用前检查。
- 正式预算：最多一次 SOLVE，零自动重试；BUILD 预算当前为零。执行入口未获资格前不得消耗新 SOLVE。
- 不清理、不迁移旧项目；不改变架构、几何、材料、原 M7C Sdc/Sdd/Guard 阈值，不做全带优化、LNA 或 CST251 任务。
- 开始稳定求解后被动等待现有连接完成，不持续轮询原生日志/进程；仅完成或明确异常时读一次任务节点状态。
- 不能证明实际直接频点计算、数值/互易精度不足、缺少必需数据或 source 漂移时保留 HOLD，不能临时追加频点或改阈值救结果。

当前正式权限仍以 stage_contract.json 为准；此计划是新用户授权的范围记录，不是已资格化入口或正式 packet。


## 2026-10-27 stage closeout

Stage completed: H_NUM_SUPPORTED_M7C_DIRECT_SAMPLE, with original science HOLD retained. Exactly one solve; zero geometry builds, retries or recovery solves. See M7C_DIRECT_SAMPLE_DIAGNOSTIC_RESULT_20261027.md.
