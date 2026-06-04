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
| 2026-06-04 12:00 | **必须回复**：签名机制分工（业务 x402 + 链上 EIP-712） | 🟡 待回 |
| 2026-06-04 18:00 | **必须产出**：record-contribution.ts 第一版（可跑） | 🟡 待办 |
| 2026-06-04 EOD | HTTP 端点 /api/sign-contribution | 🟡 待办 |

---

## 🔗 关键信息（来自 6/3 晚 Hugo 整理）

- **签名机制分工**（Hermes 建议）：
  - 业务层做 x402（agentSigner 私钥放 .env 的 AGENT_PRIVATE_KEY）
  - 链上验签用 EIP-712
  - 暴露 HTTP 端点 `/api/sign-contribution` 给前端
  - canonical payload 用 JSON.stringify 字典序序列化
- **4 个 MCP 工具**（Agent 火堆交付物）：
  - record-contribution
  - generate-proof
  - check-balance
  - request-distribution
- **6/4 18:00 截止标准**（第一版 record-contribution）：
  - [ ] signContribution(contributor, source, evidenceId, score, paymentId) 返回 { proof, signature, agentSigner }
  - [ ] curl 调 /api/sign-contribution 拿到完整返回
  - [ ] 用 cast verifyTypedData 自检签名通过
  - [ ] 跑通 cast send 上链一条 demo 贡献，scores() 累加成功

---

## 📄 关联文档

- 学习笔记：`../../hackathon/cobo-agentic-wallet-tutorial-notes.md`
- 实战日志：`../../02-projects/cghub-mvp-hackathon/03-caw-example/`
- 签名模板（Hermes 起草）：`../../02-projects/cghub-mvp-hackathon/docs-文档/agent-signing-template.md`

---

## 🚦 当前卡点

- ❗ Agent 火堆**还没正式启动**（待接口契约拍板）
- ❗ 12:00 前未回签名机制分工 → Hermes 用模板 C DM 催办
- ❗ 18:00 前 record-contribution.ts 第一版未出 → 6/5 联调会延后

---

> **最后更新**：2026-06-04 10:00
