# 模板 C · 催 Agent 组

> **使用时机**：6/4 12:00 群内未回 → 私聊 Agent 掌火人
> **使用方**：Hermes
> **关联火堆**：🔵 Agent

---

## DM 文本

@Agent 掌火人 早，4 个 MCP 工具（record-contribution / generate-proof / check-balance / request-distribution）今天能开干吗？

- **签名机制**：业务层做 x402 + 链上 EIP-712，分工 OK 吗？

Hermes 可以帮：
- 写 ethers signTypedData 模板
- EIP-712 字段顺序对照表

**截止 6/4 EOD 出 record-contribution.ts 第一版。**

---

## 备选（如果已确认签名机制但 MCP 工具未动）

@Agent 掌火人 签名机制确认收到 👍
剩 4 个 MCP 工具：今天 18:00 前能出 record-contribution.ts 第一版吗？其余 3 个可以晚 1-2 天。

---

## Agent 火堆启动路径（Hermes 建议，今日 6/4 完成）

| 时间 | 任务 | 输出 |
|------|------|------|
| 6/4 上午 | signContribution() 函数骨架 | `agent-代理/src/sign-contribution.ts` |
| 6/4 下午 | HTTP 端点 /api/sign-contribution | `agent-代理/src/server.ts` |
| 6/4 18:00 截止 | **第一版可跑的 record-contribution** | 含 .env、curl 验证通过 |

### 6/4 18:00 第一版最低标准

- [ ] signContribution(contributor, source, evidenceId, score, paymentId) 返回 { proof, signature, agentSigner }
- [ ] curl 调 /api/sign-contribution 拿到完整返回
- [ ] 用 cast verifyTypedData 自检签名通过
- [ ] 跑通 cast send 上链一条 demo 贡献，scores() 累加成功

---

## 跟进记录

| 时间 | 动作 | 结果 |
|------|------|------|
| （待填） | DM 发出 | — |
| （待填） | Agent 掌火人回复 | — |

---

> 创建：2026-06-04 10:00（Hermes）
