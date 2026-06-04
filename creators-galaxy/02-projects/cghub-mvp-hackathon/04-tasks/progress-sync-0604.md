# CGHub 黑客松 · 进展同步 · 2026-06-04 12:00

> 本文档跟踪 6/4 12:00 节点检查结果。
> 触发：cron 12:00 节点检查（`hermes-coordination-authority` §一）
> 状态：**Hermes 按授权拍板**——5 个对齐 + Cobo 凭据路径 + Agent 草稿支援

---

## 🚦 12:00 节点检查结果（已按 v2.0 建议方案拍板）

### 5 个对齐问题 · Hermes 拍板结论

| # | 问题 | 建议方案 | 实际状态 | 拍板结论 |
|---|------|---------|---------|---------|
| 1 | 合约命名 | ContributionPool 统一 | ❌ 12:00 前未回 | ✅ **ContributionPool**（拍板） |
| 2 | 测试网 | Sepolia 统一 | ❌ 12:00 前未回 | ✅ **Sepolia**（拍板） |
| 3 | 签名机制 | EIP-712 链上 + x402 业务层并存 | ❌ 12:00 前未回 | ✅ **EIP-712 + x402 并存**（拍板） |
| 4 | 数据模型 | 前端补"贡献分数"字段 | ❌ 12:00 前未回 | ✅ **前端补字段**（拍板） |
| 5 | Cobo CAW 凭据 | 6/4 12:00 截止 | ❌ 12:00 前未到位 | 🟡 **启动备用方案**（见下） |

**拍板依据**：`task-assignment-v2.md` 第二节、第三节 + `hermes-coordination-authority.md` §1。
**同步动作**：白织/老实人/大番薯 DM 已发模板（执行记录见 `04-team/fire-status/dm-templates/`）。

### Cobo CAW 凭据处理

- **现状**：6/4 12:00 未到位
- **拍板**：启动**方案 A · mock 数据先行**：
  - 6/4 EOD：Hermes 出 mock 凭据 `.env.example` 样例（AGENT_WALLET_API_KEY=WALLET_UUID=API_URL 全部 mock 值）
  - 6/4 EOD：Hermes 出 mock 贡献数据 5 条（contributor/source/evidenceId/score 完整）
  - 6/5 EOD：老实人拿 mock 数据先跑通前端链路
  - 6/5→6/9 备用升级路径：拿不到真凭据 → Demo 用录屏+截图兜底（见 `task-assignment-v2.md` §六）
- **升级触发器**：
  - 6/5 12:00 仍没拿到 → L2（Hermes 在群里公开点出 + 主动帮写催 CAW 团队话术）
  - 6/9 12:00 仍没拿到 → L3（Hermes 直接出 mock 走完全流程，Demo 用录屏兜底）

---

## 🔵 Agent 火堆 · record-contribution.ts（6/4 18:00 截止）

**当前状态**：大番薯尚未出 PR，群里未回进展。
**Hermes 主动补位**（按 `task-assignment-v2.md` §三、§六 风险 + 备用方案）：

- Hermes 出**草稿 PR**放到 `reference-agent-safe-pay/agent/record-contribution.ts.draft`（备份在 vault）
- DM 大番薯："**你接 OR 我出草稿**？18:00 没回我直接推 PR 到 `agent` 分支"
- 草稿包含 4 项 checklist（见 `04-team/fire-status/03-Agent.md`）：
  - [ ] signContribution(contributor, source, evidenceId, score, paymentId)
  - [ ] curl 调 /api/sign-contribution 拿到完整返回
  - [ ] cast verifyTypedData 自检通过
  - [ ] cast send 上链一条 demo，scores() 累加成功

**判断**：6/4 是 D1，Agent 风险点第一天——必须主动补，不能等。

---

## 📅 8 人 · 今日必做（已按 v2.0 个性化清单锁定）

| 成员 | 火堆 | 今日必做 1 句 | 状态 |
|------|------|--------------|------|
| **白织** | 🔴 合约 | 12:00 前回 5 个对齐（**已超时，Hermes 拍板**）+ 推 Cobo 凭据到 CAW 团队 | 🟡 Hermes 已拍板 |
| **大番薯** | 🔵 Agent | 18:00 前出 `record-contribution.ts`（**Hermes 出草稿备援**） | 🟡 草稿备援中 |
| **mini Quan** | 🔵 Agent | 看 `task-assignment-v2.md` §四，准备 6/5 第一次出活 | 🟢 待启动 |
| **老实人** | 🟡 前端 | 切 Sepolia + 接入 ABI + 补"贡献分数"字段 + 等 Cobo 凭据 | 🟡 进行中 |
| **loong** | 🟡 前端 | 配合老实人切 Sepolia + 接 ABI | 🟢 配合 |
| **Fox** | 🟡 前端 | 看 `task-assignment-v2.md` §四，6/5 链路跑通配合 | 🟢 待命 |
| **老曹健身版** | 🟢 辅助 | **6/4 必须出**测试计划 + "我需要别人提供什么"清单 | 🟡 待启动 |
| **bc_tools** | 🟢 辅助 | 看 PRD + task-assignment v2.0（理解架构，6/7 起可上手） | 🟢 学习 |

---

## 🕐 时间节点 · 接下来 24h

| 时间 | 节点 | 责任 |
|------|------|------|
| **6/4 18:00** | 大番薯 record-contribution.ts 第一版（OR Hermes 推草稿 PR） | 大番薯 + Hermes |
| **6/4 18:00** | Hermes 出 mock 数据 + mock 凭据 .env.example | Hermes |
| **6/4 22:00** | 今日进展同步（progress-sync-0604.md 22:00 版） | Hermes cron |
| **6/5 12:00** | Agent 火堆签名机制实际落地确认 | 大番薯 |
| **6/5 EOD** | 🔴 **全链路首跑**（最关键里程碑）—— 提前量铁律 | 老实人 + 全体 |
| **6/5 22:00** | 全链路首跑结果同步 | Hermes cron |

---

## ⚠️ Hugo 私聊重点关注

- **Cobo CAW 凭据** 仍是最大风险——Hugo 是否有 CAW 团队私聊渠道加速？
- **大番薯 18:00 截止**——若 Hermes 草稿 PR 落地，等于 Agent 火堆"代劳"第一天，需要 Hugo 后续让大番薯接力
- **老实人前端联调**——6/5 EOD 是 D2 关键里程碑，今晚 22:00 检查前端切 Sepolia 进展

---

> **最后更新**：2026-06-04 12:00 | 维护：Hermes（cron 12:00 节点检查）
> **归档位置**：`creators-galaxy/02-projects/cghub-mvp-hackathon/04-tasks/progress-sync-0604.md`
