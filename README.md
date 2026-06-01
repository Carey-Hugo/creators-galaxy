# CGHub · Creators Galaxy Hub

> AI时代个体价值操作系统 — 让每个创客的贡献都被链上记录、按代码分配。

**Hackathon：** WCB × Cobo · Agentic Economy  
**开发周期：** 2026-06-01 ~ 2026-06-14  
**Demo 核心闭环：** 贡献记录 → x402 证明 → Cobo Agentic Wallet 自动收益分配

---

## 🎯 项目一句话说明

CGHub 是创客经济的价值操作系统：AI Agent 记录贡献并生成可验证支付凭证，智能合约按预设规则自动执行收益分配，全程无需平台干预。

---

## 🔗 核心链接

| 资源 | 链接 |
|------|------|
| 官网/概览 | `/docs/06-execution-plan/CGHub-创客星球发展规划概览.md` |
| 黑客松执行方案 | `/docs/06-execution-plan/CGHub-MVP黑客松执行方案.md` |
| WCB 报名 | https://web3career.build |
| Cobo 赞助 | Cobo Agentic Wallet SDK |
| 公众号 | 胡戈AI赋能 |

---

## 🏗 项目结构

```
creators-galaxy/
├── contracts/              # 智能合约（Hardhat）
│   ├── contracts/
│   │   └── ContributionPool.sol   # 收益分配主合约
│   ├── scripts/            # 部署脚本
│   ├── test/               # 合约测试
│   └── hardhat.config.js
├── frontend/               # Next.js 前端
│   ├── app/
│   │   ├── page.tsx        # 贡献记录展示
│   │   └── wallet/         # 钱包交互页面
│   ├── components/
│   └── lib/
├── agent/                  # AI Agent（贡献记录 + x402 证明）
│   ├── record.ts           # 贡献记录逻辑
│   ├── x402.ts             # x402 协议证明生成
│   └── prompts/
├── sdk-integration/         # Sponsor SDK 对接
│   └── cobo/              # Cobo Agentic Wallet SDK
├── docs/                   # 项目文档
│   └── 06-execution-plan/
├── hackathon/
│   ├── submissions/        # WCB 任务提交物
│   └── operations-log/     # 作战日志
└── README.md
```

---

## 🔄 最小闭环流程

```
1. 创客完成贡献
      ↓
2. CGHub Agent 记录（时间、内容、价值评估）
      ↓
3. x402 协议生成贡献证明（可验证支付凭证）
      ↓
4. 智能合约按规则分配收益
      ↓
5. 创客通过 Cobo Agentic Wallet 实时到账
```

---

## 📦 技术栈

| 层级 | 技术选型 |
|------|---------|
| 合约 | Hardhat + Solidity |
| 测试网 | Polygon Amoy |
| 前端 | Next.js |
| Agent | Claude / MiniMax API |
| 钱包 | Cobo Agentic Wallet SDK |
| 证明协议 | x402 |

---

## 👥 团队

| 角色 | 负责方向 | 联系方式 |
|------|---------|---------|
| Carey Hugo | 掌火人 / 统筹 | Telegram @Carey Hugo |
| （队友待确认） | | |

---

## 📅 开发计划（两周冲刺）

```
Phase 1（D1-D3）：技术方案定稿 + Cobo SDK 对接启动
Phase 2（D4-D7）：核心合约 + Agent 记录流程打通
Phase 3（D8-D10）：前端集成 + x402 串联
Phase 4（D11-D12）：端到端调通 + Demo 录屏
Phase 5（D13-D14）：展板完善 + 评委演示
```

---

*Built with ❤️ by CGHub 初创团队 — 使命驱动，代码分配。*
