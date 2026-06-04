# 🌍 CGHub 全局总览（共享核心层）

> **这是 Hugo（创始人/总编辑）和 Hermes（总助）的全局记忆入口。**
> 每次对话开始，Hermes 第一件事就是读这个文件，做到心中有全局。
> 任何场景下的关键信息都会同步到这里，确保 4 个沟通渠道（学习群/黑客松群/CGHub群/私聊）共享同一份记忆。

---

## 🎯 Hugo 当前核心目标（2026 长期）

- **CGHub 创客星球**：和合共生、天下大同，迈向新文明的入口
- **AI × Web3 School**：30 天学习计划 + WCB 黑客松参赛
- **本次双轨**：W3 课程推进 + MVP 黑客松执行（6/1-14）

---

## 📡 4 个沟通场景（共享同一份 vault）

| 场景 | TG 群 | 归档目录 | 主要内容 |
|------|------|---------|---------|
| **A. 学习** | AI x Web3 School | `03-scenarios/A-学习-AI×Web3-School/` | W1-W4 学习任务、概念笔记、Proof-of-Work |
| **B. 项目** | 创客星球 MVP 黑客松 | `03-scenarios/B-项目-黑客松-MVP/` | 4 堆篝火进展、Proposal、代码产出 |
| **C. 品牌** | 创客星球CGHub | `03-scenarios/C-品牌-CGHub/` | 书籍连载、整体规划、品牌资产 |
| **D. 私聊** | Carey Hugo (DM) | `03-scenarios/D-私聊-总助沟通/` | 战略对齐、跨场景协调、决策记录 |

**👉 跨场景引用规范**：使用 `[[../B-项目-.../xxx]]` wikilink 互相指向

---

## 🧑‍🤝‍🧑 团队（8 位初创基石合伙人 + Hugo + Hermes）

**合伙人档案**：`04-team/profiles/`
**火堆状态**：`04-team/fire-status/`

### 4 堆篝火分工

| 火堆 | 掌火人 | 协助 | 归档位置 |
|------|-------|------|---------|
| 🔴 合约 | 白织 | 大番薯、mini Quan | `04-team/fire-status/01-合约.md` |
| 🟡 前端 | 老实人 | loong、Fox、白织 | `04-team/fire-status/02-前端.md` |
| 🔵 Agent | 大番薯 | mini Quan、loong、Fox | `04-team/fire-status/03-Agent.md` |
| 🟢 辅助 | 老曹健身版 | bc_tools | `04-team/fire-status/04-辅助.md` |

---

## 📚 关键资源

- **AI×Web3 School 仓库**：`/home/ubuntu/ai-web3-school-cghub/`（独立仓库，WCB 任务提交）
- **CGHub 创客星球仓库**：`/home/ubuntu/creators-galaxy/`（Gitee + GitHub 双同步）= **本 vault**
- **Obsidian**：Hugo Windows 桌面编辑入口
- **Codex**：Hugo Windows 桌面执行入口

---

## 🔄 信息流（写入规范）

### 触发归档的场景

| 触发 | 归档到 |
|------|-------|
| 学习群有任务/概念讨论 | `03-scenarios/A-学习/...` |
| 黑客松群有进展/代码提交 | `03-scenarios/B-项目/...` + `04-team/fire-status/` |
| CGHub 群有品牌/规划内容 | `03-scenarios/C-品牌/...` |
| 私聊有战略决策/跨场景协调 | `03-scenarios/D-私聊/...` |
| 任何信息涉及 ≥2 个场景 | 写到对应场景 + 在本文件"近期关键决策"区登记一条 |

### 写入原则

- **重要信息 24h 内必须落盘**，不能只在脑子里
- **Hugo 偏好简洁直接**，少铺垫，重点判断 + 可执行建议
- **跨场景引用必须用 wikilink**，方便 Hugo 在 Obsidian 里跳转

---

## 📌 近期关键决策（时间倒序，最多保留 10 条）

> 关键战略/架构决策在这里登记，方便随时回看。

- **2026-06-04** · 4 场景共享记忆架构搭建完成（`03-scenarios/` + `04-team/` + cron 归档）
- **2026-06-04** · 4 堆火堆状态已对齐（5 个接口不一致问题已识别），12:00 待 4 掌火人拍板
- **2026-06-04** · Hugo 授权：12:00 未回 → Hermes 主动 DM；进度落后 → 本火堆优先，跨火堆必要时调度
- **2026-06-03** · Day 3 关键发现：5 个接口不一致问题（命名/Sepolia/签名/数据模型/Cobo 凭据），6/4 12:00 前必须拉齐，否则 6/12 联调会崩
- **2026-06-03** · Hermes 起草 3 份补位文档（frontend-quickstart / agent-signing-template / task-assignment v1.1）
- **2026-06-03** · Day 17 学习 Cobo Agentic Wallet，跑通 CLI + Pact 协议
- **2026-06-01** · Day 15 黑客松正式启动，Day 3 团队分工确定

---

## 🚦 当前状态（2026-06-04 Day 18）

### 学习线
- W1 ✅ W2 ✅ 完成
- W3 进行中任务 **29 个**（4 张截图覆盖，已去重入档 `w3-tasks-2026-06-04.md`）
- W3 关键任务：赞助方问题(+5) / 完整Week 4 Ready Pack(+40) / 技术验证计划(+30) / 项目流程图(+30) / 深度研究包(+30) / Sponsor SDK API Plan(+30) / Z.AI赛道对齐(+30)
- 6/3 Day 17 学习 Cobo Agentic Wallet 已跑通 CLI + Pact

### 项目线（Day 4/14）
- ✅ 4 堆火堆 Day 3 进展已对齐：前端 MVP 完工、合约已部署 Sepolia、Agent 待启动、辅助待启动
- 🚨 5 个接口不一致问题待 6/4 12:00 拉齐（命名/Sepolia/签名/数据模型/Cobo凭据）
- 🔑 合约地址：0x876A0741223EDdaE081Ef22beA513E92335B1Bd5 (Sepolia)
- 关键节点：Day 7 中间检查点（6/7）、Day 10 MVP 核心（6/10）、Day 14 Demo（6/14）

### Hermes 已起草 3 份补位文档
- `frontend-quickstart.md` (Sepolia + ABI + 4 useHook)
- `agent-signing-template.md` (EIP-712 + x402 分工)
- `task-assignment.md v1.1` (4 项变更说明)

### 今日时间表
- 12:00 检查 4 个对齐问题，未回用模板 A/B/C/D DM 催办
- 18:00 收齐决策 + Cobo 凭据
- 22:00 第一份每日进度同步（Hermes 主动起草）

---

> **最后更新**：2026-06-04 09:50（由 Hermes 自动维护）
> **同步状态**：Gitee ✅ GitHub ✅
