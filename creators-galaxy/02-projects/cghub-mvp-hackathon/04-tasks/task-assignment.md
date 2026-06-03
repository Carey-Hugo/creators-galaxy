# CGHub MVP 黑客松 · 任务分配与代码仓库结构

> 版本：v1.0 | 日期：2026-06-03
> 黑客松周期：2026-06-01 → 2026-06-14（两周）
> 赛道：Cobo · Agentic Economy × Cobo Agentic Wallet

---

# 一、代码仓库结构

```
creators-galaxy/
└── 02-projects/
    └── cghub-mvp-hackathon/
        ├── contracts-合约/           # 🔴 合约火堆产出
        │   ├── ContributionLedger.sol    # 贡献记录核心合约
        │   ├── Distribution.sol           # 收益分配合约
        │   ├── interfaces/                # 接口定义
        │   │   ├── IContributionLedger.sol
        │   │   └── IDistribution.sol
        │   ├── libs/                      # 工具库
        │   │   └── x402verifier.sol       # x402证明验证
        │   ├── test/                      # 合约测试
        │   │   ├── ContributionLedger.t.sol
        │   │   └── Distribution.t.sol
        │   └── scripts/                   # 部署脚本
        │       └── deploy.ts
        │
        ├── frontend-前端/             # 🟡 前端火堆产出
        │   ├── src/
        │   │   ├── components/           # UI组件
        │   │   │   ├── ContributionForm.tsx
        │   │   │   ├── DistributionView.tsx
        │   │   │   ├── WalletConnect.tsx
        │   │   │   └── AgentStatus.tsx
        │   │   ├── pages/
        │   │   │   ├── index.tsx         # 贡献提交首页
        │   │   │   ├── dashboard.tsx      # 管理面板
        │   │   │   └── agent.tsx         # Agent状态页
        │   │   ├── hooks/                # 自定义hooks
        │   │   │   ├── useCoboWallet.ts
        │   │   │   └── useContribution.ts
        │   │   ├── lib/                  # 工具函数
        │   │   │   └── cobo-sdk.ts       # Cobo SDK封装
        │   │   └── App.tsx
        │   ├── public/
        │   ├── package.json
        │   └── next.config.js
        │
        ├── agent-代理/                # 🔵 Agent火堆产出
        │   ├── src/
        │   │   ├── contribution-recorder.ts   # 贡献记录Agent
        │   │   ├── x402-prover.ts              # x402证明生成
        │   │   ├── wallet-agent.ts             # Cobo Wallet调用
        │   │   ├── mcp-server.ts               # MCP工具服务
        │   │   └── index.ts                    # 入口
        │   ├── tools/                      # MCP工具定义
        │   │   ├── record-contribution.ts
        │   │   ├── generate-proof.ts
        │   │   ├── check-balance.ts
        │   │   └── request-distribution.ts
        │   ├── package.json
        │   └── tsconfig.json
        │
        ├── scripts-脚本/               # 🟢 辅助火堆产出
        │   ├── deploy.ts                # 部署脚本
        │   ├── test-suite.ts            # 测试套件
        │   ├── generate-proof.ts       # 证明生成工具
        │   └── demo-recorder.ts         # Demo录屏辅助
        │
        ├── docs-文档/                  # 全体共享
        │   ├── README.md                # 项目说明
        │   ├── API.md                   # API接口文档
        │   └── QA.md                    # 评委问答
        │
        ├── reference-agent-safe-pay/    # 参考项目（不修改）
        │   ├── contracts-合约/
        │   ├── frontend-前端/
        │   ├── demo-演示/
        │   └── scripts-脚本/
        │
        └── 03-PRD/                     # 需求文档
        └── 04-tasks/                   # 本文件
```

---

# 二、任务分配（按火堆）

## 🔴 合约火堆 · 掌火人：白织

**仓库目录：** `contracts-合约/`

| 文件 | 负责人 | 截止 | 依赖 |
|------|--------|------|------|
| `ContributionLedger.sol` | 白织 | Day3 | - |
| `Distribution.sol` | 白织 | Day5 | ContributionLedger |
| `interfaces/IContributionLedger.sol` | 白织 | Day3 | - |
| `interfaces/IDistribution.sol` | 白织 | Day3 | - |
| `libs/x402verifier.sol` | 白织 | Day5 | x402协议研究 |
| `test/ContributionLedger.t.sol` | 老曹健身版 | Day7 | 合约部署完成 |
| `test/Distribution.t.sol` | 老曹健身版 | Day7 | 合约部署完成 |
| `scripts/deploy.ts` | 白织 + 老曹健身版 | Day5 | 合约完成 |
| **Cobo SDK接入** | 白织 | Day10 | SDK文档 |

### 合约任务详细拆解

**Day 1-3（第一堆火）**
- [ ] 设计贡献记录合约接口（贡献者地址、内容、价值、时间戳）
- [ ] 定义x402证明验证接口
- [ ] 输出`接口文档.md`给前端和Agent对接
- [ ] 部署到测试网，获取合约地址

**Day 4-7（散开燃烧）**
- [ ] 实现收益分配合约（按贡献权重分账）
- [ ] 实现Cobo SDK的pact审批/策略限制逻辑
- [ ] 完成转账和审计日志功能
- [ ] 编写测试用例（老曹健身版）

**Day 8-10（第二堆火）**
- [ ] 集成Cobo Agentic Wallet SDK
- [ ] 端到端测试：贡献→记录→证明→分账全流程
- [ ] 部署到主测试网，获取tx hash

---

## 🟡 前端火堆 · 掌火人：老实人

**仓库目录：** `frontend-前端/`

| 文件 | 负责人 | 截止 | 依赖 |
|------|--------|------|------|
| Next.js项目初始化 | 老实人 | Day3 | - |
| `pages/index.tsx`（贡献提交） | 老实人 | Day5 | 合约接口 |
| `pages/dashboard.tsx`（管理面板） | 老实人 | Day7 | 合约接口 |
| `components/WalletConnect.tsx` | loong | Day5 | Cobo SDK |
| `components/ContributionForm.tsx` | Fox | Day5 | 合约接口 |
| `components/DistributionView.tsx` | loong | Day7 | 合约接口 |
| `hooks/useCoboWallet.ts` | 老实人 | Day7 | Cobo SDK |
| `lib/cobo-sdk.ts` | 白织 | Day8 | Cobo SDK |

### 前端任务详细拆解

**Day 1-3（第一堆火）**
- [ ] 初始化Next.js + TypeScript项目
- [ ] 确定UI框架和组件库
- [ ] 搭建项目结构（参考仓库结构）
- [ ] 对接合约火堆接口文档

**Day 4-7（散开燃烧）**
- [ ] 完成贡献提交表单UI
- [ ] 实现MetaMask/Cobo Wallet连接
- [ ] 完成分配合成界面
- [ ] 集成Cobo SDK前端支付UI（白织提供）

**Day 8-10（第二堆火）**
- [ ] 前端 + 合约全流程对接
- [ ] 展示贡献记录和分账结果
- [ ] 准备Demo录屏素材

---

## 🔵 Agent火堆 · 掌火人：大番薯

**仓库目录：** `agent-代理/`

| 文件 | 负责人 | 截止 | 依赖 |
|------|--------|------|------|
| `contribution-recorder.ts` | 大番薯 | Day5 | 合约接口 |
| `x402-prover.ts` | 大番薯 | Day7 | x402协议 |
| `wallet-agent.ts` | 大番薯 + mini Quan | Day7 | Cobo SDK |
| `mcp-server.ts` | 大番薯 | Day7 | MCP SDK |
| `tools/record-contribution.ts` | 大番薯 | Day5 | 合约 |
| `tools/generate-proof.ts` | mini Quan | Day7 | x402 |
| `tools/request-distribution.ts` | 大番薯 | Day7 | 合约 |

### Agent任务详细拆解

**Day 1-3（第一堆火）**
- [ ] 设计Agent架构（贡献触发→记录→证明→分账）
- [ ] 确认x402证明输出格式
- [ ] 研究Cobo Agentic Wallet接入方式
- [ ] 输出Agent方案文档给合约和前端

**Day 4-7（散开燃烧）**
- [ ] 实现贡献记录Agent逻辑
- [ ] 实现x402证明生成
- [ ] 实现MCP Server工具（11个工具参考AgentVault）
- [ ] 实现Cobo Wallet调用（mini Quan协助）

**Day 8-10（第二堆火）**
- [ ] 全流程串联：贡献→证明→Cobo Wallet→分账
- [ ] 端到端自动化演示
- [ ] 验证Agent持有钱包、自己发起分配

---

## 🟢 辅助火堆 · 掌火人：老曹健身版

**仓库目录：** `scripts-脚本/` + `docs-文档/`

| 文件 | 负责人 | 截止 | 依赖 |
|------|--------|------|------|
| `scripts/test-suite.ts` | 老曹健身版 | Day7 | 合约部署 |
| `scripts/demo-recorder.ts` | 老曹健身版 | Day13 | 前端完成 |
| `docs/README.md` | 老曹健身版 + 全体 | Day13 | 全部完成 |
| `docs/API.md` | 白织 + 大番薯 | Day10 | 合约+Agent完成 |
| `docs/QA.md` | 老曹健身版 + 全体 | Day13 | Demo完成 |

### 辅助任务详细拆解

**Day 1-3（第一堆火）**
- [ ] 熟悉项目架构和代码库
- [ ] 制定测试计划
- [ ] 了解Cobo SDK测试方法

**Day 4-7（散开燃烧）**
- [ ] 编写合约单元测试
- [ ] 编写集成测试
- [ ] 追踪和记录Bug

**Day 8-10（第二堆火）**
- [ ] 全流程测试
- [ ] 辅助脚本开发（部署、证明生成）
- [ ] bc_tools协助简单任务

**Day 11-14（第三堆火）**
- [ ] Demo录屏辅助脚本
- [ ] README + 操作指南
- [ ] QA文档（评委可能问的技术问题）
- [ ] 协助各火堆修复问题

---

# 三、接口对接表（关键依赖）

```
合约火堆（白织）
    │
    ├─ 接口文档 ─────────────────→ 前端火堆（老实人）：贡献提交UI
    │                                └─ 合约地址 + ABI → frontend/lib
    │
    ├─ 接口文档 ─────────────────→ Agent火堆（大番薯）：贡献记录Agent
    │                                └─ 合约地址 + ABI → agent/tools
    │
    └─ Cobo SDK ─────────────────→ 前端火堆：支付UI（白织提供）
         └─ Cobo SDK ─────────────→ Agent火堆：Wallet调用（大番薯）

前端火堆（老实人）← ─ ─ ─ ─ ─ → Agent火堆（大番薯）
   UI状态同步        贡献触发 + 证明查询
```

**关键接口（必须Day3确定）：**
1. `recordContribution(address contributor, string memory content, uint256 value)` → tx hash
2. `generateProof(contributionId)` → x402 proof string
3. `requestDistribution(contributionId)` → 触发Cobo Wallet

---

# 四、Git提交规范

```
[contracts] 新增/修改 合约功能
[frontend] 新增/修改 前端功能
[agent] 新增/修改 Agent功能
[docs] 新增/修改 文档
[test] 新增/修改 测试用例
[chore] 杂项（依赖、配置）
```

---

# 五、里程碑检查点

| 日期 | 里程碑 | 通过标准 |
|------|--------|---------|
| Day 3（6/7） | 第一堆火烧完 | 合约骨架+接口文档 ✅ 前端初始化 ✅ Agent方案 ✅ |
| Day 7（6/7） | 中间检查点 | 合约可部署 ✅ 前端Demo可用 ✅ Agent流程跑通 ✅ |
| Day 10（6/10） | MVP完成 | 全流程串联 ✅ Cobo Wallet对接 ✅ |
| Day 13（6/13） | Demo提交 | README ✅ Demo视频 ✅ 测试网验证 ✅ |
| Day 14（6/14） | Demo Day | 路演+评审 |

---

*文档状态：v1.0 | 最后更新：2026-06-03*
*归档位置：creators-galaxy/02-projects/cghub-mvp-hackathon/04-tasks/*