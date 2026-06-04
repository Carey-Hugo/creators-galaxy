# 模板 D · 催 Cobo CAW 凭据

> **使用时机**：6/4 12:00 凭据未到位 → 私聊白织 + CAW 团队
> **使用方**：Hermes
> **关联火堆**：🔴 合约（白织帮推）+ 🟢 Cobo CAW 团队

---

## DM 文本 · 发给白织

@白织 早，Cobo CAW 凭据这事不直接归你，但要麻烦你帮忙推一下。我整理了推进路径 + 一些具体建议，你照着转发给 CAW 团队就行：

### 前端联调时间压力（为什么这事急）
- 6/4 12:00 前拿到凭据 → 6/4 下午前端可联调
- 6/4 18:00 前拿到 → 6/5 EOD 跑通完整 demo
- 6/5 之后才拿到 → 联调延后 1-2 天，6/14 截止会紧张

### CAW 团队最省事的提供方式

**方案 A · 临时测试账号（推荐，1 分钟搞定）**
- 一个 CAW 测试账号（带预充值）
- 一份能触发 Pact 审批的 Demo 步骤
- 前端先用测试账号跑通 UI，联调通过后切到正式账号

**方案 B · 完整凭据（5 分钟）**
- AGENT_WALLET_API_KEY
- AGENT_WALLET_WALLET_UUID
- AGENT_WALLET_API_URL（默认 https://api.agenticwallet.cobo.com）
- 直接给前端调 SDK 即可

### 建议传给 CAW 团队的简短话术（你直接复制粘贴）

```
@CAW 团队 您好，我们是 CGHUB MVP 黑客松团队，前端火堆需要 CAW 测试凭据进行 Cobo Wallet 分账流程联调。

麻烦提供以下任一方案（方案 A 最省事）：

A. 临时测试账号 + Pact 审批触发步骤（推荐）
   - 1 个 CAW 测试账号（带预充值）
   - 1 份能触发 Pact 审批的 Demo 步骤文档

B. 完整 API 凭据
   - AGENT_WALLET_API_KEY
   - AGENT_WALLET_WALLET_UUID
   - AGENT_WALLET_API_URL（默认 https://api.agenticwallet.cobo.com）

截止：6/4 12:00 前
凭据接收方：Hugo（@Carey Hugo）或 Hermes（@Hermes）私聊

感谢支持 🙏
```

### 如果 CAW 团队不在你们群里
你直接私聊他们负责人，或者告诉我 CAW 负责人是谁，我私聊推进（Hugo 已经授权跨组协调）。

### Hermes 后续动作
- 6/4 12:00 还没拿到 → 我会私聊你 + CAW 团队催办
- 6/4 18:00 还没拿到 → 升级为阻塞风险，写入每日进度同步

---

## 跟进记录

| 时间 | 动作 | 结果 |
|------|------|------|
| （待填） | DM 发出 | — |
| （待填） | 白织回复 | — |
| （待填） | CAW 凭据到位 | — |

---

> 创建：2026-06-04 10:00（Hermes）
