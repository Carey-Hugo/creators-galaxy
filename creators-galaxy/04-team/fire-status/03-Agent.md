# 🔵 Agent 火堆 · 掌火人：大番薯

> **方向**：AI Agent 调用 + x402 证明生成
> **关键产出**：Agent 调用逻辑 + x402 证明生成 + Cobo Agentic Wallet 接入

---

## 👥 成员

| 角色 | 昵称 | 备注 |
|------|------|------|
| 掌火人 | 大番薯 | 企业级 AI Agent 预研 |
| 协助 | mini Quan | AI Agent 搭建 + 合约模块讨论 |
| 协助 | loong | 前端 + Agent |
| 协助 | Fox | 前端 + Agent |

---

## 📅 进度时间线

| 日期 | 里程碑 | 状态 |
|------|--------|------|
| 2026-06-03 | Cobo Agentic Wallet CLI 跑通（Pact 协议已验证） | ✅ |
| 2026-06-03 | Hermes 起草 agent-signing-template.md（含 x402 业务层 + EIP-712 链上分工） | ✅ |
| 2026-06-03 | Hugo + Hermes 发群公告 + DM 给 Agent 掌火人 | ✅ |
| 2026-06-04 12:00 | **必须回复**：签名机制分工（业务 x402 + 链上 EIP-712） | 🟢 **Hermes 拍板：并存** |
| 2026-06-04 12:00 | Hermes 12:00 节点检查：Agent 风险点第一天，Hermes 主动补 | ✅ |
| 2026-06-04 12:00 | 6h fire-status 同步：未收到大番薯群消息，Hermes 草稿已发 DM 问"你接 OR 我推 PR" | ✅ |
| 2026-06-04 12:34 | **🎉 D1 重大产出**：大番薯亲自提交 Agent 火堆完整骨架（commit `2bcd4752`，2950 行） | ✅ **超出预期** |
| 2026-06-04 12:34 | 4 模块骨架：contribution-recorder / x402-prover / wallet-agent / mcp-server | ✅ |
| 2026-06-04 12:34 | 4 个 MCP 工具：sign-contribution / submit-contribution / check-pending / trigger-claim | ✅ |
| 2026-06-04 12:34 | tsc --noEmit 全量 0 报错 | ✅ |
| 2026-06-04 12:34 | **🆕 架构决策**：round/pending 数据前端直读合约，Agent 只做"动作+证明"层（去重决策） | 🟢 Hugo 15:14 拍板 |
| 2026-06-04 12:34 | **🆕 新阻塞**：agentSigner 私钥未到位 → 所有上链测试卡死 | 🔴 **L1 升级** |
| 2026-06-04 15:14 | Hugo 拍板"agentSigner 决策点"——走问白织路径 | 🟢 |
| 2026-06-04 15:15 | Hugo 提交"6/4 午进展同步补充：大番薯 agent/ 真实代码路径+12 个文件清单"（commit `2f31e436`） | ✅ |
| 2026-06-04 18:00 | **必须完成**：record-contribution.ts 第一版（可跑） | 🟢 **已提前 6h 交付骨架** |
| 2026-06-04 18:00 | L1 升级：18:00 没回 → Hermes 直接推 PR | 🟢 **已不需要**（大番薯自己推了） |
| 2026-06-04 18:00 | 6h fire-status 同步：18:00 节点 Agent 火堆领先 6h+，下周可提前进入联调 | ✅ **火堆绿灯** |
| 2026-06-04 18:01 | **🎉 agentSigner 私钥自然到位**：commit `b72ac3be` 提交 `agent/.env`（含 CAW API_KEY + agentSigner 私钥）| 🟢 L1 阻塞解除 |
| 2026-06-04 18:44 | **🎉 CAW executor 上链**：commit `8631e63c` 改用 `caw tx call`，端到端实测 tx `0xa56bfc61…` | 🟢 |
| 2026-06-04 18:57 | **🎉🎉 Cobo SDK 纯 HTTP executor**：commit `2c7c6bbe` 删 `caw.ts`，签名在 Cobo 服务端完成，**队友拉仓库即跑**（tx `0x103525…`）| 🟢🎉 **全链路贯通** |
| 2026-06-04 19:14 | **🎉 群消息机制修复**：@Hermes 1 分钟内响应（B2 方案）| 🟢 跨场景打通 |
| 2026-06-04 19:30 | Hermes bot 身份纠错（@hermes_humain_bot vs @hermes_huseo_bot）| 🟢 skill v2.2.3 沉淀 |
| 2026-06-04 EOD | HTTP 端点 /api/sign-contribution —— 大番薯自交付 | 🟢 **已端到端实测** |
| 2026-06-05 EOD | D2 关键里程碑：全链路真实数据首跑 | 🟢 **前置条件全部就位** |
| 2026-06-04 22:00 | **6h fire-status 同步（00:00 节点）**：大番薯 D1 重大产出已沉淀，22:00 EOD 终版完成；明提前进入联调 | 🟢 火堆持续领先 |
| 2026-06-05 06:00 | **6h fire-status 同步（06:00 节点）**：大番薯火堆持续领先 12h+，0 新 commit（22:21 后 vault 无代码变动），D2 真实数据首跑前置 100% 就位 | 🟢 待 6/5 09:00 后主动启动 D2 |

| 2026-06-06 00:01 | **6h fire-status 同步（00:00 节点）**：补录 6/5 Agent API 被前端接入 + 12:50 三端联调通过 + 14:13 贡献 Agent 执行方案；18:00→00:00 静默 | 🟢 主线成型 |
| 2026-06-06 12:02 | **6h fire-status 同步（12:00 节点）**：06:00→12:00 无 Agent 功能新 commit/成员进展消息；Agent 主线保持领先，待 demo 脚本/错误处理/评分口径收敛 | 🟢 主线稳定 |
| 2026-06-07 00:01 | **6h fire-status 同步（00:00 节点）**：18:00→00:00 无 Agent 功能新 commit/大番薯公开 ack；Agent 主链路仍领先，下一步聚焦 CAW claim 稳定性、错误处理、Demo 叙事与录屏证据 | 🟢 主线稳定 |
| 2026-06-07 18:02 | **6h fire-status 同步（18:00 节点）**：12:00→18:00 0 Agent 功能 commit，大番薯 36h+ 群消息沉默延续；Agent 主线仍领先，无新阻塞 | 🟢 主线稳定 |
| 2026-06-07 21:02 | **21:00 EOD 4 场景归档（cron `ce4de7218b35`）**：18:00→21:00 0 Agent 功能 commit，4 群真静默（v2.12 鉴别），大番薯 39h+ 群消息沉默延续；Agent 主线仍最领先，三主线进入 Demo 稳定验收/封板 | 🟢 主线稳定 |
| 2026-06-08 00:02 | **6h fire-status 同步（00:00 节点）**：21:00→00:00 仍 0 Agent 功能 commit（4 commits 全为 cron 自身噪音），4 群最新 5min 切片 `incremental_20260607_221151.json` 显示 4 群 max_id == last_archived_id 真静默（v2.12 鉴别），大番薯 42h+ 群消息沉默延续；**深夜 6h 静默期 v2.7 模式**：不发群催办、00-INDEX patch 后缀 0 新增决策；Agent 主线仍最领先 | 🟢 主线稳定 |
| 2026-06-08 06:00 | **6h fire-status 同步（06:00 节点）**：00:00→06:00 仍 0 Agent 功能 commit（4 commits 全 5min 归档 cron 噪音），5min 群消息最新落盘 `incremental_20260608_001143.json` (00:11) 4 群仍 max==last 真静默（v2.12 鉴别成立），大番薯 48h+ 群消息沉默延续；**深夜 6h 静默期 v2.7 模式延续**：不发群催办、00-INDEX patch 后缀 0 新增决策；Agent 主线仍最领先，无新阻塞 | 🟢 主线稳定 |

---

## 🎉 D1 重大产出明细（commit `2bcd4752`，12:34）

**贡献追踪**（已写入 `progress-sync-0604.md`）：

| 贡献者 | 类别 | 内容 | 时间 | 凭证 |
|--------|------|------|------|------|
| 大番薯 | 方案文档 | Agent 模块方案（架构/x402/Cobo/接口） | 2026-06-04 | 已提交 |
| 大番薯 | 代码骨架 | 所有 Agent 组件骨架 | 2026-06-04 | commit `2bcd4752` |
| 大番薯 | MCP 工具 | 签贡献/上链/查可领/触发分账 | 2026-06-04 | `agent/tools/{sign,submit,check,trigger}-*.ts` |
| 大番薯 | 架构决策 | round/pending 数据前端直读合约 | 2026-06-04 | 群消息 + Hugo 拍板 |
| 大番薯 | Agent 源文件 | contribution-recorder/x402-prover/wallet-agent/mcp-server/index/config/types/abi | 2026-06-04 | `agent/src/*.ts`（8 个文件）|

**Agent 仓库结构**（已确认）：
```
02-projects/cghub-mvp-hackathon/agent/
├── src/
│   ├── contribution-recorder.ts    # 贡献记录核心（EIP-712 签名）
│   ├── x402-prover.ts              # x402 证明生成
│   ├── wallet-agent.ts             # Cobo Wallet 调用（contractCall 调 claimFor + payment 走 x402）
│   ├── mcp-server.ts               # MCP Server 入口
│   ├── index.ts                    # 总入口
│   ├── config.ts                   # 配置
│   ├── types.ts                    # 类型定义
│   └── abi.ts                      # 合约 ABI 封装（运行时加载）
├── tools/
│   ├── sign-contribution.ts        # MCP 工具：签贡献
│   ├── submit-contribution.ts      # MCP 工具：上链
│   ├── check-pending.ts            # MCP 工具：查可领
│   └── trigger-claim.ts            # MCP 工具：触发分账
├── docs/Agent方案设计.md           # 260 行方案文档
├── abi/                            # 合约方提供 ABI（不存手写版）
├── .env.example                    # 22 行配置模板
├── README.md                       # 48 行
├── package.json + package-lock.json
└── tsconfig.json
```

**技术亮点**：
- 4 模块独立、低耦合
- 4 个 MCP 工具 zod schema 完整
- ABI 运行时加载（不存手写版，避免接口变更不同步）
- `.gitignore` 排除 `node_modules`
- `tsc --noEmit` 0 报错（开发规范到位）

---

## 🆕 架构决策（去重）

**决策**：round 状态、pending 等展示数据 → **前端直接读合约**，Agent 层不重复做

**理由**：
- 避免双重数据源
- UI 响应更快（少一个 HTTP 链路）
- Agent 模块更纯粹（"动作+证明"）

**Hugo 拍板**（15:14）：默认接受，老实人 6/4 EOD 前确认能改，6/5 接入

---

## 🆕 18:00 → 21:00 EOD 重大反转

### 🎉🎉 全链路贯通（agentSigner 阻塞自然解除）

**反转时间线**（18:00 fire-status 报 L1 阻塞 → 18:57 全链路贯通，**56 分钟闭环**）：

1. **18:01** `b72ac3be` —— 大番薯提交 `agent/.env`（含 CAW 凭据 + agentSigner 私钥）—— **白织/owner 18:00 之前就发了私钥**，18:01 大番薯收到即提交
2. **18:44** `8631e63c` —— 改用 **CAW 钱包当 executor**（`caw tx call` + 轮询），端到端实测上链，tx `0xa56bfc61…` ✅
3. **18:57** `2c7c6bbe` —— 再收敛到 **Cobo SDK 服务端签名**（`pact-scoped api_key` + `contractCall`），**删 `caw.ts`**，纯 HTTP 无 caw CLI，tx `0x103525…` ✅

**架构演进**（从硬到软）：
- 旧方案：本地 EOA + executor 私钥（需要私钥分享）
- v1 (18:44)：CAW 钱包 + `caw tx call`（需要 caw CLI + TSS 分片）
- v2 (18:57)：**Cobo SDK 服务端签名**（任意机器 + api_key 即可驱动同一钱包）

**意义**：
- 队友拉仓库 `npm install && npm run` 即跑（.env + ABI 已在仓库，私有仓库共享）
- 后续不需要 caw CLI / TSS 分片 / 私钥分享 = **降低接入门槛**
- 风险：私有仓库转公开或泄露需立即轮换 agentSigner 私钥 + CAW API key

### 🟢 L1 阻塞已解除（无需升级）

| 原 18:00 L1 条件 | 21:00 状态 |
|----------------|-----------|
| agentSigner 私钥到位 | ✅ 18:01 自然到位（私钥发放时间 < fire-status 同步时间）|
| 端到端上链实测 | ✅ 18:44 CAW executor / 18:57 SDK executor 两次成功 |
| 队友可拉仓库跑 | ✅ README 重写为"拉下来即用" |

### 🎉 群消息机制（跨场景打通）
- 19:14 B2 方案：@Hermes 1 分钟内响应（**Hermes 现在能在群里主动 @ 大番薯**）
- 19:30 bot 身份纠错：@hermes_humain_bot 才是真我，huseo profile 那个 bot（搜优seo）一直在误导
- 5 群里 2 群已是 admin：Hugo一人公司(-5076629166) / AI x Web3 School(-5291819613)
- 3 群待升 admin：创客星球CGHub(-5223347644) / MoWa愿力文明(-5163870876) / 创客星球 MVP 黑客松(-1003916141713)

---

## 🔗 关键信息

- **签名机制分工**（Hermes 拍板）：
  - 业务层做 x402（agentSigner 私钥放 .env 的 `AGENT_PRIVATE_KEY`）
  - 链上验签用 EIP-712
  - 暴露 HTTP 端点 `/api/sign-contribution` 给前端
  - canonical payload 用 JSON.stringify 字典序序列化
- **4 个 MCP 工具**（Agent 火堆交付物）：record-contribution / generate-proof / check-balance / request-distribution
  - **实际落地**（12:34 提交）：sign-contribution / submit-contribution / check-pending / trigger-claim

---

## 📄 关联文档

- 学习笔记：`../../hackathon/cobo-agentic-wallet-tutorial-notes.md`
- 实战日志：`../../02-projects/cghub-mvp-hackathon/03-caw-example/`
- 签名模板（Hermes 起草）：`../../02-projects/cghub-mvp-hackathon/docs-文档/agent-signing-template.md`
- 6/4 进展同步：`../../02-projects/cghub-mvp-hackathon/04-tasks/progress-sync-0604.md`
- Agent 骨架代码：`../../02-projects/cghub-mvp-hackathon/agent/`
- Agent 方案文档：`../../02-projects/cghub-mvp-hackathon/agent/docs/Agent方案设计.md`

---

## 🚦 当前卡点

- 🟢 **大番薯火堆 6h+ 内无任何阻塞**（D1 重大产出 + 18:01/18:44/18:57 三 commit 全链路贯通）
- 🟢 6/5 D2 真实数据首跑前置条件全部就位（agentSigner 到位 + 端到端实测上链 + 队友可拉仓库跑）
- 🟢 群消息机制打通（19:14 B2 方案）—— Hermes 现在能主动 @ 大番薯协调
- 🟡 5 群 bot 升 admin：2 群已 admin，3 群待升（创客星球CGHub / MoWa愿力文明 / 创客星球 MVP 黑客松）

> **最后更新**：2026-06-04 21:02（21:00 EOD 4 场景归档 by cron `ce4de7218b35`）
> **本轮新增**：🎉🎉 全链路贯通（agentSigner 自然解除，18:00 L1 阻塞 18:01 自然解决）+ 🆕 群消息机制打通

## 🆕 本轮新增（18:00 节点 · 6h 同步）

**过去 6h 唯一变化**（12:00 → 18:00）：
- A 路 git：仅 `35d257d1`（5min 群消息归档），**0 Agent 功能新 commit**。
- B 路群消息：MVP 群 4 条全为 Hugo `/model` 切换与 bot 自确认；其余 3 群无大番薯/mini Quan/loong/Fox 消息。
- C 路 session_search：无最近 6h Agent 实质新命中。
- 结论：Agent 火堆仍是 4 堆绿灯，36h+ 无新阻塞；下一步重点是 CAW claim 稳定性、Demo 录屏证据与错误处理。

**本轮不主动 @大番薯 群催办**：
- 白天 6h 静默延续，按 v2.7 模式白天也不进群催办。
- Agent 火堆不是当前硬阻塞，6/8 节点再视情况走主动 ack。
- 兜底：6/9 EOD 仍无大番薯 demo 录屏脚本，Hermes 直接按 12:50 联调 tx（`0x103525…`）+ Cobo 审计日志起草 3 分钟讲解脚本。

## 🚦 当前卡点（06:02 重写）

- 🟢 **Agent 主线稳定**：贡献签名 → 前端提交 → 合约记录 → CAW/Agent 执行链路已通过。
- 🟢 **Demo 叙事明确**：Agent 作为"贡献证明 + 自动分账执行者"，评委可看懂。
- 🟡 **当前重点**：CAW claim 稳定性、接口错误处理、录屏证据、贡献评分口径、Demo 3 分钟讲解脚本。
- 🔴 **密钥历史风险仍需处理**：公开前必须轮换并清理 `.env` / CAW / agentSigner 历史。**Day 14 Demo（6/14）前必须解决**。
- ⏰ **本轮无 Agent 新进展**：00:00→06:00 持续无大番薯/Agent 功能 commit 或群消息；4 群真静默 v2.12 鉴别（00:11 切片全群 max_id == last_archived_id）；深夜 6h 静默期 v2.7 模式不催办（睡觉时段延续到 06:00 之后窗口）。

> **最后更新**：2026-06-08 00:02（6h fire-status 同步 00:00 节点 by cron `9c117e476344`，4 commits 全 cron 噪音 0 项目功能 commit；4 群真静默 v2.12 鉴别 22:11 切片成立；深夜 6h 静默期 v2.7 模式不发群催办；Agent 主线仍最领先）
> **本轮新增**：0 项目功能 commit；4 群真静默（v2.12 鉴别 22:11 切片）；深夜 6h 静默期 v2.7 模式；本轮 0 新决策（patch 旧 L1 决策行后缀待 6/8 18:00 同步执行）

## 🆕 本轮新增（00:00 节点 · 6h 同步）

**过去 6h 唯一变化**（18:00 → 00:00）：
- A 路 git：4 commits 全为 cron 自身噪音，**0 Agent 功能新 commit**。
- B 路群消息：4 群最新 5min 切片 `incremental_20260607_221151.json`（22:11 跑通）显示 4 群 max_id == last_archived_id，全部 0 新增。
- C 路 session_search：无最近 6h Agent 实质新命中。
- 结论：Agent 火堆仍是 4 堆绿灯，42h+ 无新阻塞；下一步重点是 CAW claim 稳定性、Demo 录屏证据与错误处理；深夜 6h 静默期 v2.7 模式不催办。

**本轮不主动 @大番薯 群催办**（深夜 6h 静默期例外窗口）：
- 当前 00:02 属深夜睡觉时段（22:00→06:00），按 v2.7 铁律**不发**群催办。
- Agent 火堆不是当前硬阻塞，6/8 18:00 节点（白天窗口）再视情况走主动 ack。
- 兜底：6/9 EOD 仍无大番薯 demo 录屏脚本，Hermes 直接按 12:50 联调 tx（`0x103525…`）+ Cobo 审计日志起草 3 分钟讲解脚本。

## 🆕 本轮新增（06:00 节点 · 6h 同步）

**过去 6h 唯一变化**（00:00 → 06:00）：
- A 路 git：4 commits 全 5min 归档 cron 噪音，**0 Agent 功能新 commit**。
- B 路群消息：5min 群消息归档最新落盘 `incremental_20260608_001143.json`（00:11）显示 4 群仍 max_id == last_archived_id，全部 0 新增。
- C 路 session_search：无最近 6h Agent 实质新命中。
- 结论：Agent 火堆仍是 4 堆绿灯，48h+ 无新阻塞；下一步重点是 CAW claim 稳定性、Demo 录屏证据与错误处理；深夜 6h 静默期 v2.7 模式延续不催办。

**本轮不主动 @大番薯 群催办**（深夜 6h 静默期例外窗口）：
- 06:00 仍属深夜睡觉时段（22:00→06:00），按 v2.7 铁律**不发**群催办。
- Agent 火堆不是当前硬阻塞，6/8 18:00 节点（白天窗口）再视情况走主动 ack。
- 兜底：6/9 EOD 仍无大番薯 demo 录屏脚本，Hermes 直接按 12:50 联调 tx（`0x103525…`）+ Cobo 审计日志起草 3 分钟讲解脚本。

> **最后更新**：2026-06-08 06:02（6h fire-status 同步 06:00 节点 by cron `9c117e476344`，4 commits 全 5min 归档 cron 噪音 0 项目功能 commit；4 群真静默 v2.12 鉴别 00:11 切片成立；深夜 6h 静默期 v2.7 模式延续不发群催办；Agent 主线仍最领先）
> **本轮新增**：0 项目功能 commit；4 群真静默（v2.12 鉴别 00:11 切片）；深夜 6h 静默期 v2.7 模式延续；本轮 0 新决策（patch 旧 L1 决策行后缀待 6/8 18:00 同步执行）
