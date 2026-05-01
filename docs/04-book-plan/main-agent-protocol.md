# 总助（Main Agent）创客星球任务触发条件 & 同步协议
# CGHub Project — Conditional Context Loading Protocol

> **可见范围 / Visibility：** 内部（Internal Only）
> **适用对象 / Target：** 总助（Main Agent）
> **最后更新 / Last Updated：** 2025-05-01

---

## 一、触发条件 / Trigger Conditions

当你的任务涉及以下任一关键词或场景时，**自动进入创客星球上下文加载模式**：

```
触发关键词（满足任一即触发）：
- 创客星球 / 创客 / CGHub / Creators Galaxy Hub
- 《AI新时代——当机器学会分配》/ 书籍封面 / 书籍策划 / 书籍内容
- 白皮书 / 合伙人招募 / 品牌文案
- Web3 / DAO / 区块链（且与CGHub相关）
- Gitee 仓库 / 推送代码 / git pull / git push
- conversation-YYYY-MM-DD.md / 会话记录
```

```
当任务不涉及以上关键词时：
- 正常执行其他任务
- 不需要读取任何CGHub相关文件
```

---

## 二、上下文加载流程 / Context Loading Flow

**当触发条件满足时，按以下顺序读取：**

```
Step 1：git pull origin main
        （先拉取最新仓库内容）

Step 2：读取 .repo-guide.md
        （了解隐私规范和协作协议）

Step 3：读取 docs/04-book-plan/conversation-index.md
        （了解历史会话索引）

Step 4：读取最新的那条 conversation-*.md
        （接上最新上下文）

Step 5：根据任务类型，读取对应的项目文件：
       - 书籍相关 → docs/04-book-plan/CGHub书籍框架大纲_V2.md
       - 封面设计 → docs/04-book-plan/CGHub封面设计提示词.md
       - 白皮书   → docs/03-whitepaper/ 目录下的文件
       - 合伙人   → docs/02-partner-recruitment/ 目录下的文件
       - 其他     → 根据文件名判断
```

---

## 三、会话记录写入要求 / Session Logging Requirement

**重要**：当完成任何与创客星球相关的任务后，必须将工作内容和结果写入会话记录。

```
写入时机：
- 每次完成一个阶段性任务
- 每次做出关键决策或确定内容
- 每次与Carey Hugo沟通后（如果是你主动发起的沟通）
- 每天结束前（汇总当日工作）

写入文件：
- docs/04-book-plan/conversation-YYYY-MM-DD.md
- 如果文件已存在，追加到当日文件中
- 如果是新的日期，创建新文件

写入格式：
```markdown
## [时间] 任务：[任务名称]

### 决策/结论
- 决定事项1
- 决定事项2

### 完成内容
- 完成的内容1
- 完成的内容2

### 待确认
- 需要Carey Hugo确认的事项

### 下一步
- 后续工作安排
```
```

---

## 四、同步检查清单 / Sync Checklist

**每次开始任务前，确认以下事项：**

```
□ 已执行 git pull origin main（最新代码）
□ 已读取 .repo-guide.md（如有更新）
□ 已读取 conversation-index.md（了解历史）
□ 已读取最新 conversation-*.md（接上上下文）
□ 已读取任务对应的项目文件
□ 确认无隐私文件被意外传播
```

**每次完成任务后，确认以下事项：**

```
□ 工作结果已写入当日 conversation-*.md
□ 如有新文件创建，已添加可见范围标记
□ 如有敏感内容，已确认不会外泄
□ 必要时已执行 git push origin main
□ 已通知Carey Hugo（如需要）
```

---

## 五、品牌信息（速查）

```
品牌名：CGHub / 创客星球
Slogan：点燃激情，点亮梦想 / Ignite Passion, Illuminate Dreams
Gitee：https://gitee.com/carey-hugo/creators-galaxy
GitHub：由Gitee镜像同步

当前书籍：《AI新时代——当机器学会分配》
英文名：The AI Epoch — When Machines Learn to Distribute
```

---

## 六、注意事项

1. **仓库信息是唯一真相**：当对话中的信息与仓库文件矛盾时，以仓库文件为准
2. **隐私优先**：任何标记为"内部"或"私人"的内容，不得在公开场合传播
3. **主动同步**：如果发现仓库有更新，主动告知Carey Hugo
4. **条件触发**：本协议仅在触发条件满足时生效，其他任务正常执行

---

*本文件由 Hermes Agent 生成，用于总助（Main Agent）的长期记忆配置*
