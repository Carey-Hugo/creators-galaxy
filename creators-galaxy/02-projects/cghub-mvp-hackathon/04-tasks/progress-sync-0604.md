# CGHub 黑客松 · 进展同步 · 2026-06-04 午

> 本文档跟踪 4 个火堆的实时进展、贡献者记录、待解决问题
> **贡献追踪表是奖金分配和星钻发放的核心凭证，所有贡献必须即时记录**

---

## ✅ 今日进展

### 🔵 Agent 火堆 · 大番薯（D1 重大产出）

**贡献者**：大番薯
**贡献内容**（已交付）：
- ✅ **Agent 模块方案文档**（架构 + x402 + Cobo 接入 + 对接接口）
- ✅ **所有组件骨架代码已提交**

**MCP 工具能力包**（已具备，前端可对接）：
- 签贡献（EIP-712 签名）
- 上链（recordContributionBySig）
- 查可领（pending 查询）
- 触发分账（distribution 触发）

**架构决策**：
- 大番薯明确：**round 状态、pending 等展示数据**前端**直接读合约**，**不在 Agent 层重复做**
- 这是个**重要的去重决策**——避免双重数据源，Agent 只做"动作+证明"层

**待对齐**：
1. **agentSigner 私钥** —— 大番薯需要拿到
2. （其他细节未说）

**贡献追踪条目**：

| 贡献者 | 类别 | 内容 | 时间 | 凭证 |
|--------|------|------|------|------|
| 大番薯 | 方案文档 | Agent 模块方案（架构/x402/Cobo/接口）| 2026-06-04 | 已提交（未列路径）|
| 大番薯 | 代码骨架 | 所有 Agent 组件骨架 | 2026-06-04 | commit `2bcd4752` |
| 大番薯 | MCP 工具 | 签贡献/上链/查可领/触发分账 | 2026-06-04 | `agent/tools/{sign-contribution,submit-contribution,check-pending,trigger-claim}.ts` |
| 大番薯 | 架构决策 | round/pending 数据前端直读合约 | 2026-06-04 | 群消息 |
| 大番薯 | Agent 源文件 | contribution-recorder/x402-prover/wallet-agent/mcp-server/index/config/types/abi | 2026-06-04 | `agent/src/*.ts`（8 个文件）|

**Agent 仓库结构**（已确认）：

```
02-projects/cghub-mvp-hackathon/agent/
├── src/
│   ├── contribution-recorder.ts    # 贡献记录核心
│   ├── x402-prover.ts              # x402 证明生成
│   ├── wallet-agent.ts             # Cobo Wallet 调用
│   ├── mcp-server.ts               # MCP Server 入口
│   ├── index.ts                    # 总入口
│   ├── config.ts                   # 配置
│   ├── types.ts                    # 类型定义
│   └── abi.ts                      # 合约 ABI 封装
└── tools/
    ├── sign-contribution.ts        # MCP 工具：签贡献
    ├── submit-contribution.ts      # MCP 工具：上链
    ├── check-pending.ts            # MCP 工具：查可领
    └── trigger-claim.ts            # MCP 工具：触发分账
```

---

### 🔴 合约火堆 · 白织
- 状态：昨天 6/3 晚已完成 Sepolia 部署（ContributionPool 0x876A0741223EddaE081Ef22beA513E92335B1Bd5）
- 今日进展：待群里回复（5 个对齐问题 12:00 截止）
- 贡献追踪条目：6/3 部署 + 文档（已记）

### 🟡 前端火堆 · 老实人
- 状态：MVP 已合入 main（贡献提交 + 钱包连接）
- 今日进展：待群里回复（切 Sepolia + 接 ABI）
- ⚠️ **大番薯新信息影响**：原本"前端要展示 round 状态/pending"是 Agent 做的，现在改前端**直读合约**。这意味着老实人需要多做：
  - 用 viem/wagmi 直接读 `getRoundState` / `getPending`
  - 不再等 Agent 接口
- 贡献追踪条目：6/3 MVP（已记）

### 🟢 辅助火堆 · 老曹健身版
- 状态：昨日说"做测试打辅助"
- 今日进展：待出测试计划 + 需求清单
- 贡献追踪条目：暂无

---

## 🚨 紧急事项（v2.1 提前量铁律触发）

### 🔴 紧急 1：agentSigner 私钥（影响所有上链测试）

**问题**：大番薯要 agentSigner 私钥才能跑 record-contribution
**根因**：合约用 EIP-712 验签，agentSigner 是签名方；私钥不发给 Agent，所有上链动作都跑不通
**现状**：
- 私钥应在白织手里（他部署的合约，agentSigner 应该是他设置的）
- 还没给到大番薯

**Hermes 行动路径**（3 选 1，按最优）：
1. **问白织要**（最直接）—— Herme s 12:00 之前 DM 问白织
2. **问 Hugo 决策** —— agentSigner 是谁设的？是单一私钥还是多签？
3. **临时方案** —— 大番薯自己生成一个测试私钥，配置到合约 owner 那边的 agentSigner 槽位（需要 owner 权限调 setAgentSigner）

**风险**：
- L3 落后（按 v2.1 提前量铁律，agentSigner 不到位 = D2 6/5 EOD "全链路首跑"完不成）
- 必须今天 18:00 之前解决

**Hugo 决策点**：
- agentSigner 私钥是白织自己生成（测试网自己掌握）还是用 Cobo 提供的 Agent 钱包？
- Cobo Agentic Wallet 本来就要做"Agent 持钱包"，这正好契合

### 🟡 紧急 2：前端"直读合约"架构变更

**变更**：原本前端通过 Agent 查 round 状态/pending，**现在改前端直读合约**

**影响**：
- 老实人/loong 工作量略增（要写合约读函数 + wagmi hook）
- Agent 模块更纯粹（只做"动作+证明"，不做"查询"）
- **优势**：去重，避免双数据源；UI 响应更快

**需要确认**：
- ✅ 大番薯已决策，Hermes/Hugo 默认接受
- 待办：老实人 6/4 EOD 前确认能改、6/5 接入读合约

---

## 📋 6/4 剩余关键节点

| 时间 | 节点 | 责任 | 状态 |
|------|------|------|------|
| **12:00** | 5 个对齐问题截止 | 4 个火堆 | 🟡 群里等回复 |
| **12:00** | Cobo CAW 凭据 | 白织 | 🟡 群里等回复 |
| **14:00** | agentSigner 私钥到位 | 白织/Hermes | 🔴 紧急 |
| **18:00** | Agent 第一版 record-contribution | 大番薯 | 🟢 提前交付（骨架已提交）|
| **22:00** | 每日进展同步（cron 自动）| Hermes | ⏰ |

---

## 📊 8 人·今日进展（截至 6/4 中午）

| 成员 | 火堆 | 今日动作 | 状态 | 卡点 |
|------|------|---------|------|------|
| Hugo | 统筹 | 战略决策 | 🟢 在线 | — |
| Hermes | 协调 | v2.0/v2.1 任务分解 + Git 同步 | ✅ 已完成 | — |
| 白织 | 合约 | 待回 5 个对齐 + Cobo 凭据 + agentSigner | 🟡 12:00 截止 | agentSigner 是大番薯新提的，需马上答 |
| 大番薯 | Agent | **方案文档 + 骨架代码 + MCP 4 工具** | ✅ **D1 重大产出** | agentSigner 私钥未到位 |
| 老实人 | 前端 | 待切 Sepolia + 接 ABI + 改"直读合约" | 🟡 进行中 | 大番薯新决策要追加工作量 |
| loong | 前端 | 配合老实人 | 🟡 待动 | — |
| Fox | 机动 | 待命 | 🟢 | — |
| mini Quan | Agent 后端 | 待起 agent-backend 骨架 | 🟡 6/5 出活 | — |
| 老曹健身版 | 辅助 | 待出测试计划 + 需求清单 | 🟡 | — |
| bc_tools | 学习 | 看架构 | 🟢 | — |

---

## 🎯 Hermes 接下来动作

1. **立刻**（< 30 min）：
   - DM 白织要 agentSigner 私钥（紧急）
   - 群里公告"大番薯 D1 重大产出已记录"
   - 同步给 Hugo 私聊："agentSigner 决策点需要你拍板"

2. **12:00 节点**（cron 自动触发）：
   - 检查 5 个对齐 + Cobo 凭据
   - 检查 agentSigner 是否到位

3. **今晚 22:00**（cron 自动触发）：
   - 写完整 progress-sync-0604.md（含所有 8 人进展）
   - Git 提交推送

---

*最后更新：2026-06-04 12:15 | 维护：Hermes（军师）*
*归档位置：creators-galaxy/02-projects/cghub-mvp-hackathon/04-tasks/progress-sync-0604.md*
