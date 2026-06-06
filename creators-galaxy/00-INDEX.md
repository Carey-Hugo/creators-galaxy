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

## 📌 近期关键决策（时间倒序，最多保留 10 条；超过滚动压缩）

> 关键战略/架构决策在这里登记，方便随时回看。

- **2026-06-04 22:00** · **🆕 22:00 EOD 进展同步**：6/4 终版 `progress-sync-0604.md`（EOD 终版）已写+提交+双推。8 人状态 + 6/5 12:00 截止项按人分解。3 L1 催办延续到明早 12:00
- **2026-06-04 20:00** · **🆕 5min 群消息归档 cron `ea6425732577` 启动**：取代 2h 兜底 cron（`d49eecfc9ca3` 已废）。586 条历史 + 增量，首跑 60-80s/cron 周期
- **2026-06-04 18:00** · **🎉🎉 全链路贯通三连击（agentSigner 自然解除）**：大番薯 18:01 `.env`(`b72ac3be`) → 18:44 CAW executor(`8631e63c`) → 18:57 Cobo SDK 纯 HTTP executor(`2c7c6bbe`)，**D2 前置全部就位**，56 分钟闭环 —— **6/5 12:50 三端联调通过**（白织 `20b64e25`：合约+前端+Agent 联调通；14:13 Hugo 补 507 行贡献 Agent 执行方案）
- **2026-06-04 19:30** · **🆕 bot 身份纠错**（v2.2.3）：@hermes_humain_bot（总助main/主目录）才是真我，@hermes_huseo_bot 是 huseo profile 沿用配置；修正 chat_id 映射 3/4 是错的（Hugo一人公司 ↔ AI x Web3 School 对调）
- **2026-06-04 19:14** · **🎉 群消息机制修复**（v2.2.3 终版）：关隐私模式 + 重启 gateway = 1 分钟内响应。**明日必修 2 件事**：① 3 老式 group 升 supergroup；② AI x Web3 School 升 bot admin
- **2026-06-04 18:00** · **🆕 大番薯 D1 重大产出 + 架构决策**（合并）：Agent 骨架 2950 行（`2bcd4752`） + "round/pending 前端直读合约"（去重，Hugo 15:14 拍板）
- **2026-06-04 12:00** · **🔴 3 火堆 6h 沉默**（白织/老实人/老曹健身版）→ 全部由 Hermes 拍板执行；老曹健身版 12h 沉默已 2 倍升级，6/5 12:00 仍未出 → Hermes 起草测试计划模板—— **6/5 00:00 L1 延续，老曹健身版 24h 沉默 L2 升级挂起到 6/5 12:00** —— **6/5 06:00 L1 延续，老曹健身版 30h 沉默 L2 升级挂起继续，6/5 12:00 cron 自动执行兜底** —— **6/6 12:00 L2 延续：仅辅助火堆仍红灯，三端联调已通但测试计划/QA 缺口未补；本 job 禁止 send_message，先落盘待白天兜底**
- **2026-06-04** · 4 场景共享记忆架构搭建完成（`03-scenarios/` + `04-team/` + 6 个 cron 协作） + 4 堆火堆 Day 1 状态已对齐
- **2026-06-04** · Hugo 授权机制固化：12:00/18:00/22:00 三时间点 + 12:00 未回 Hermes 拍板 + 进度落后本火堆优先
- **2026-06-03** · Day 3 关键发现 5 个接口不一致问题（命名/Sepolia/签名/数据模型/Cobo 凭据） + Hermes 起草 3 份补位文档（frontend-quickstart / agent-signing-template / task-assignment v1.1） + Day 17 Cobo CAW CLI 跑通

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

| **最后更新**：2026-06-06 12:02（6h fire-status 同步 by cron `9c117e476344`；决策 10 条不变；06:00→12:00 无项目新进展，辅助 L2 延续）|
> **同步状态**：Gitee ✅ GitHub ✅
