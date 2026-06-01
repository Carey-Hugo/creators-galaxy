# CGHub Hackathon Direction Card

> WCB Week 3 任务提交 | 赛道：Cobo · Agentic Economy × Cobo Agentic Wallet
> 提交时间：2026-06-01 | 版本：v1.0

---

## 一、项目基本信息

| 字段 | 内容 |
|------|------|
| 项目名称 | 创客星球（CGHub）— AI时代个体价值操作系统 |
| 英文名 | Creators Galaxy Hub (CGHub) |
| Hackathon 赛道 | **Cobo · Agentic Economy** |
| 核心方向 | Agent-Native Payments / A2A Economy（智能体原生支付） |
| Demo 形式 | MVP 演示（录屏） |
| 开发周期 | 2026-06-01 ~ 2026-06-14（两周） |
| 团队状态 | 组队，潜在队友待确认后加入 Telegram 共创群 |

---

## 二、要解决的核心问题

**问题：** 创客（开发者、写作者、设计师）的劳动付出，回报由平台决定——平台制定规则，创客只能认栽。

**CGHub 的答案：** 让每个创客的贡献都被链上记录、按代码分配。AI Agent 作为"价值记录官"，把贡献转译为可验证的支付凭证（x402 协议），智能合约按预设规则自动执行收益分配。

---

## 三、最小闭环 Demo 叙事

```
创客A完成项目贡献
    ↓
CGHub Agent 记录贡献（时间、内容、价值评估）
    ↓
x402 协议生成贡献证明（可验证的支付凭证）
    ↓
智能合约按预设规则自动分配收益
    ↓
创客A通过 Cobo Agentic Wallet 实时到账
```

**核心演示点：** AI Agent 自己持有钱包、执行分配——体现 Agent-Native Payments，不依赖人工干预。

---

## 四、为什么选择 Cobo 赛道

1. **技术契合**：Cobo Agentic Wallet 是目前最接近"AI Agent 持有链上身份"的产品，CGHub 的价值分配场景直接依赖钱包的 Agent 托管能力
2. **叙事优势**：Cobo 评委看 Agentic Wallet 在真实场景（创客经济）中的应用，比概念 Demo 更有说服力
3. **生态资源**：Cobo SDK 对接是 CGHub v1.0 MVP 的核心依赖

---

## 五、技术方案（两周 MVP）

### 技术栈
- **合约侧**：Hardhat + Solidity（收益分配合约）
- **测试网**：Polygon Amoy（ Mumbai 升级版，费用低）
- **前端**：Next.js（展示贡献记录 + 钱包交互）
- **Agent**：Claude/MiniMax API（贡献记录 + x402 证明生成）
- **核心依赖**：Cobo Agentic Wallet SDK（优先对接）

### 两周里程碑

| 阶段 | 时间 | 目标 |
|------|------|------|
| Day 1-3 | 6/1-6/3 | 团队确认 + 技术方案定稿 + Cobo SDK 对接启动 |
| Day 4-7 | 6/4-6/7 | 核心合约开发 + Agent 记录流程打通 |
| Day 8-10 | 6/8-6/10 | 前端集成 + x402 证明串联 |
| Day 11-12 | 6/11-6/12 | 端到端调通 + Demo 录屏 |
| Day 13-14 | 6/13-6/14 | 展板 / 文档完善 + 评委演示准备 |

---

## 六、预期挑战与 Fallback

| 挑战 | Fallback |
|------|----------|
| Cobo SDK 对接复杂 | 先用 Safe + 传统钱包模拟，SDK 后续替换 |
| x402 协议理解门槛高 | 用简化的贡献证明替代，保留核心逻辑 |
| 队友确认延迟 | 先单人 MVP，队友到位后合并 |

---

## 七、相关文档链接

- CGHub 项目概览：`/docs/06-execution-plan/CGHub-创客星球发展规划概览.md`
- 黑客松执行方案：`/docs/06-execution-plan/CGHub-MVP黑客松执行方案.md`
- GitHub Repo：待建（基于本文档结构扩展）

---

*掌火人：Carey Hugo | 联系方式：微信 HugoAID | Telegram @Carey Hugo*
