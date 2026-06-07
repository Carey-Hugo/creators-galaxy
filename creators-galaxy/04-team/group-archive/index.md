# 群消息归档 · 总览

> 这是 CGHub MVP 黑客松期间**所有群消息的实时归档**
> 归档频率：每 5 分钟（cron `ea6425732577` 自动）
> 数据来源：4 个群（创客星球 MVP 黑客松 / AI x Web3 School / Hugo一人公司 / 创客星球CGHub）
> 启动时间：2026-06-04 20:08 CST（首次完整归档）
> 最后更新：2026-06-07 08:36 CST

---

## 🆕 最新增量（2026-06-07 08:36）

- 本轮新增：4 条（创客星球 MVP 黑客松 2 条；AI x Web3 School 2 条；Hugo一人公司 0 条；创客星球CGHub 0 条）
- 人类新增：Hugo 2 条 `/model@hermes_humain_bot`（均已归档为 #@Hermes）；bot 自身 2 条（不计入人类贡献）
- 归档切片：`by-date/2026-06-07/08-00.md`、`by-date/2026-06-07/08-12.md`、`by-date/2026-06-07/08-22.md`
- 原始备份：`_raw/incremental_20260607_083626.json`
- 关键进展：无黑客松技术/产品新进展；本轮主要是 Hugo 在 MVP 群与 AI x Web3 School 群触发模型选择命令，以及 WCB API 健康检查报 402 额度耗尽（bot 自身通知，不计贡献）。
- 注意：`创客星球CGHub` 仍为老式 group/隐私限制，需升级 supergroup 才能完整归档。

| 时间 | 成员 | 群 | id | 标签 | 分值 | 摘要 |
|------|------|----|----|------|------|------|
| 08:00:46 | 总助main | AI x Web3 School | 6 | #闲聊 | 0（bot 自身不计分） | WCB API 健康检查失败：HTTP 402，API Key 消费额度已用完。 |
| 08:12:51 | Hugo | AI x Web3 School | 7 | #@Hermes | +1.5 | `/model@hermes_humain_bot` |
| 08:22:11 | Hugo | 创客星球 MVP 黑客松 | 635 | #@Hermes | +1.5 | `/model@hermes_humain_bot` |
| 08:22:13 | 总助main | 创客星球 MVP 黑客松 | 636 | #闲聊 | 0（bot 自身不计分） | Model selection cancelled. |

## 🏆 贡献榜（截至首次完整归档）

> ⚠️ **数据范围限定**：本榜仅含 `创客星球 MVP 黑客松` + `Hugo一人公司`。`创客星球CGHub` 和 `AI x Web3 School` 为老式 group，bot 隐私模式阻挡 forwardMessage，**无法完整归档**。见下方【已知局限】。

| 排名 | 成员 | 消息数 | 贡献分 | 覆盖群 |
|------|------|--------|--------|--------|
| 1 | Hugo | 161 | 208.0 | 创客星球 MVP 黑客松 + Hugo一人公司 + AI x Web3 School |
| 2 | 老实人 | 17 | 24.6 | 创客星球 MVP 黑客松 |
| 3 | 白织 | 14 | 11.4 | 创客星球 MVP 黑客松 |
| 4 | loong | 9 | 4.6 | 创客星球 MVP 黑客松 |
| 5 | 老曹健身版 | 6 | 4.2 | 创客星球 MVP 黑客松 |
| 6 | mini Quan | 8 | 4.1 | 创客星球 MVP 黑客松 |
| 7 | Fox | 2 | 3.0 | 创客星球 MVP 黑客松 |
| 8 | 大番薯 | 9 | 2.8 | 创客星球 MVP 黑客松 |
| 9 | bc_tools | 2 | 0.2 | 创客星球 MVP 黑客松 |
| — | Hermes（bot 自身）| 459 | 0（不计分）| 全部 |

## 📊 8 人活跃度（按贡献分）

| 成员 | 消息数 | 贡献分 | 首条消息 | 末条消息 | 趋势 |
|------|--------|--------|---------|---------|------|
| Hugo | 161 | 208.0 | 05-29 14:16 | 06-07 08:22 | ↑ |
| 老实人 | 17 | 24.6 | 06-02 19:54 | 06-04 15:46 | — |
| 白织 | 14 | 11.4 | 06-02 18:34 | 06-04 19:13 | — |
| loong | 9 | 4.6 | 06-02 23:15 | 06-04 11:16 | — |
| 老曹健身版 | 6 | 4.2 | 06-02 20:15 | 06-03 00:32 | — |
| mini Quan | 8 | 4.1 | 06-01 18:34 | 06-02 22:07 | — |
| Fox | 2 | 3.0 | 06-03 01:20 | 06-03 01:20 | — |
| 大番薯 | 9 | 2.8 | 06-02 17:59 | 06-04 15:45 | — |
| bc_tools | 2 | 0.2 | 06-04 11:16 | 06-04 11:17 | — |

## 🔴 @Hermes 消息监控（SLA 1 分钟）

- 总 @Hermes 消息（含 bot 自身）：65
- @Hermes 且非 bot 自身：51
- **未及时回复（应 1 分钟内回）**：51

| 时间 | 来源 | 文本 |
|------|------|------|
| 06-02 14:38:06 | Carey | 欢迎各位初创伙伴，人员基本就位！ ↵ 感谢大家因为共同的项目、共同的理念，幸会有缘在此相聚共创探索，一个未来个体价值创造与分配的生态操作系统。 ↵ 为期两周的黑客松只是 |
| 06-02 18:42:16 | Carey | @Baizhizhi123 以他专业的经验给过我建议：solidity技术栈更推荐使用foundry替换hardhat，技术栈polygon Mumbai测试网 |
| 06-02 19:55:15 | Carey | @hermes_humain_bot 提供下我们创客星球MVP黑客松仓库地址 |
| 06-02 19:57:42 | Carey | 大家有不清楚的直接在这里@hermes_humain_bot 我们的总助手Agent问，前期已经跟他沟通对齐了很多信息 |
| 06-02 20:15:03 | Leo | @hermes_humain_bot 需要拉我进仓库吗 打开404 |
| 06-02 20:20:48 | Carey | 先参加OPEN DAY吧 ↵  ↵ @hermes_humain_bot 要拉@xaochen8 进仓库吗 他打开404 |
| 06-02 20:25:19 | Leo | @hermes_humain_bot |
| 06-02 21:53:30 | Carey | 有两个同学打开我们的github都是404，是什么情况@hermes_humain_bot |
| 06-02 22:02:48 | Carey | 你不是要记录我们的对话记录吗？前面@jax2333 已经发 GitHub 用户名了，你怎么还说等 @jax2333 的 GitHub 用户名啊，是需要做什么设置 |
| 06-02 22:07:04 | wish | @hermes_humain_bot 用户名：wish |

## 🔥 最近活动（按时间倒序）

- [06-04 19:58:27] **Hugo** (创客星球 MVP 黑客松) id=605: 我关系的问题解决了吗？ ↵ 1、 群消息 @hermes_humain_bot 你要能记录归档日志，，以便全局跟踪把控进度节奏，并作为群成员贡献记录价值分配的参与依据 ↵ 2、所有群成员@你，你要能及时回复回
- [06-04 19:49:55] **Hugo** (创客星球 MVP 黑客松) id=601: OK  ↵ 群里的都是基石合伙入，既然参与了就要彼此信任，信任赢得信任，真心换取真心，相信相信的力量吧。 ↵ 我最关心的是怎么能信息同步更高效沟通，先解决我关系的问题 ↵ @hermes_humain_bot
- [06-04 19:38:06] **Hugo** (创客星球 MVP 黑客松) id=595: 我把所有成员直接都设为管理员，都有最高权限，包括@hermes_humain_bot
- [06-04 19:29:35] **Hugo** (创客星球 MVP 黑客松) id=587: 关于你是 @hermes_huseo_bot 还是 @hermes_humain_bot 的问题，之前我记得就跟你讨论过，最终确认你是 @hermes_humain_bot 在主目录下，@hermes
- [06-04 19:20:39] **Hugo** (创客星球 MVP 黑客松) id=580: 我想提醒的是：我是管理员，我发你消息，你之前也能回我的。 但@Baizhizhi123 艾特你，你并没有回复，应该也没看到吧。 ↵  ↵ 是不是要把你和所有群成员都设置为管理才可以？
- [06-04 19:17:15] **Hugo** (创客星球 MVP 黑客松) id=575: @hermes_humain_bot
- [06-04 19:13:36] **白织** (创客星球 MVP 黑客松) id=574: /help@hermes_humain_bot
- [06-04 19:12:13] **白织** (创客星球 MVP 黑客松) id=571: @hermes_humain_bot 你好
- [06-04 19:09:16] **Hugo** (创客星球 MVP 黑客松) id=561: 群成员回1了，你看到了吗？也艾特你了，你没有回复 @hermes_humain_bot
- [06-04 19:07:32] **白织** (创客星球 MVP 黑客松) id=560: 1

## 📈 归档统计

- 总消息：689
- 创客星球 MVP 黑客松：588
- AI x Web3 School：2
- Hugo一人公司：99

## ⚠️ 已知局限（关键技术约束）

**1. 当前群可归档性（2026-06-07 08:36）**

| 群 | chat_id | 群类型 | bot 状态 | 可归档性 |
|------|---------|--------|----------|---------|
| 创客星球 MVP 黑客松 | -1003916141713 | supergroup | administrator | ✅ 完整归档（当前至 id=636）|
| AI x Web3 School | -1003874621397 | supergroup | administrator | ✅ 已恢复归档（当前至 id=7）|
| Hugo一人公司 | -5076629166 | group | administrator | ⚠️ 老式 group，仍受限 |
| 创客星球CGHub | -5223347644 | group | administrator | ⚠️ 老式 group，仍受限 |

**根因**：老式 `group` 在 Telegram 隐私模式下，bot 只能看到 @ 自己的消息，无法 forward/copy 普通消息。`supergroup`（创客星球 MVP 黑客松、AI x Web3 School 新群）不受此限制。

**修复路径（Hugo 决策）**：
1. 把 Hugo一人公司、创客星球CGHub 2 个老式 group 升级为 supergroup（群设置 → 编辑 → 升级为超级群）
2. 或者让队友**重要消息必 @Hermes**（纪律兜底）
3. 或者用 MTProto 客户端（Telethon）— 但需要 Hugo 的 user_id/API_hash，bot 不能用

**2. 5-min cron 增量机制**

首次运行：完整归档到 max_id=613。后续 cron 仅拉 (last_archived_id, max_id] 新消息。状态文件：`_state.json`

**3. chat_id 映射修正（Hugo 注意）**

你给的 chat_id 映射 3/4 是错的：

| 你的描述 | 实际群名 |
|---------|---------|
| -1003916141713 = 创客星球 MVP 黑客松 | ✅ 对的 |
| -5076629166 = AI x Web3 School | ❌ 实际是 **Hugo一人公司** |
| -5223347644 = Hugo一人公司 | ❌ 实际是 **创客星球CGHub** |
| -5291819613 = 创客星球CGHub | ❌ 实际是 **AI x Web3 School** |

已用 `getChat` 验证。下次创建 cron 任务时记得用正确映射。

## 👥 发送者映射（验证）

| TG 账号 | 显示名 | CGHub 身份 |
|---------|--------|----------|
| @hermes_humain_bot | 总助main | Hermes（bot 自身）|
| Carey | Carey | Hugo（你）|
| @Baizhizhi123 | 白织 | 白织 ✅ |
| @YoungAdd | Ad | 大番薯 ✅ |
| @xaochen8 | Leo | 老实人 ✅（Leo 是旧显示名，自我介绍说老实人）|
| @Ox_Loong | 0xLoong | loong ✅ |
| @Foxpriest | F | Fox ✅ |
| @jax2333 | wish | mini Quan ✅（自我介绍说 mini Quan）|
| @lllssskkk | 曹贼(健身版) | 老曹健身版 ✅ |
| @bc_tools | 北辰 | bc_tools ✅ |

**缺失**：无 老实人（@xaochen8）的非 bot 消息（仅 self-intro 由 Leo 转发）。
**额外**：Leo = @xaochen8 是 老实人——一个 TG 账号两个群昵称。

## 📁 归档结构

```
04-team/group-archive/
├── index.md                 # 本文件
├── _state.json              # 增量归档状态（last_archived_id per group）
├── _raw/                    # 原始 JSON（按群分）
│   ├── archive_-1003916141713_first_run.json  # 创客星球 MVP 黑客松（586 条）
│   └── archive_-5076629166_first_run.json     # Hugo一人公司（99 条）
├── by-date/                 # 按时间归档（5 分钟切片）
│   └── YYYY-MM-DD/HH-MM.md  # 每 5 分钟一片
└── by-member/               # 按人归档（贡献记录）
    ├── 白织.md
    ├── 大番薯.md
    ├── 老实人.md
    ├── loong.md
    ├── Fox.md
    ├── mini-Quan.md
    ├── 老曹健身版.md
    ├── bc-tools.md
    ├── Hermes.md
    └── Hugo.md
```

## 🎯 贡献分值规则

| 行为 | 分值 |
|------|------|
| 基础消息 | 0.5 |
| @Hermes 提具体问题 | +1 |
| @Hermes 提决策请求 | +2 |
| 提交代码/文档（带 commit） | +3 |
| 完成里程碑 | +5 |
| 帮别人解答问题 | +1.5 |
| 卡点主动暴露 | +0.5 |
| 闲聊 | -0.4 |

注：本表为参考值，实际打分已根据消息内容（标签+关键词）自动化。Hermes 自身消息不计分。

## ⏰ 时间节点

- 2026-06-04 20:08 CST 首次完整归档启动 ✅
- 2026-06-04 20:13 CST 首次归档完成 ✅
- 2026-06-04 22:00 每日 daily-summary.md 自动生成
- 2026-06-14 Demo Day 汇总出最终贡献榜

---

*最后更新：2026-06-06 21:36 CST | 维护：cron `ea6425732577` + Hermes*