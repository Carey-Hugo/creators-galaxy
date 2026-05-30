# Hermes Agent 全息投影记忆系统 — 操作手册
# Hermes Agent Holographic Memory System — Operations Manual

> **适用版本：** Hermes Agent（通用）
> **创建时间：** 2026-05-26
> **适用场景：** 首次配置 / 换机重装 / 团队共建同一套记忆
> **难度：** ★★☆☆☆（约5分钟，含重启等待）

---

## 一、什么是"全息投影记忆"

Hermes Agent 的记忆系统采用**双层架构**：

```
┌─────────────────────────────────────────────────────┐
│  Layer 1：MEMORY.md（文件层）                        │
│  轻量、快速、你随时可读可改                          │
│  存放：项目上下文、用户偏好、工作状态                  │
│  路径：~/.hermes/memories/MEMORY.md                  │
└──────────────────────┬──────────────────────────────┘
                       ↓ 同步
┌─────────────────────────────────────────────────────┐
│  Layer 2：Holographic / Fact Store（向量数据库层）    │
│  持久、语义搜索、跨会话理解                           │
│  存放：事实性知识、长期记忆、概念关联                  │
│  技术：SQLite + 向量嵌入                             │
└─────────────────────────────────────────────────────┘
```

**为什么叫"全息投影"：**
同一个记忆同时存在于两个层面，互相备份、交叉验证——就像全息投影的每个碎片都包含完整图像。任意一层损坏，另一层可以重建。

---

## 二、配置前提

### 2.1 检查当前状态

```bash
# 查看 hermes CLI 路径
which hermes
# 输出类似：/home/ubuntu/.local/bin/hermes

# 查看当前记忆文件（Layer 1）
cat ~/.hermes/memories/MEMORY.md

# 查看用户配置（Layer 1）
cat ~/.hermes/memories/USER.md
```

### 2.2 前置要求

| 项目 | 要求 |
|------|------|
| 操作系统 | Linux（Ubuntu / Debian 等） |
| 用户权限 | 需要 sudo 权限（安装时需要 root） |
| 网络 | 需要访问外部向量模型 API |
| Hermer Agent 版本 | 支持 holographic 功能（v0.7+） |

---

## 三、完整配置步骤（Carey Hugo 实际配置记录）

> **配置日期：** 2026-05-25
> **配置账号：** agentuser（Hermes 专用 Linux 用户）
> **agentuser 密码：** `w2006nqszzzjf`（已记录于本手册）
> **数据库路径：** `/home/agentuser/.hermes/memory_store.db`

---

### Step 1：设置 agentuser 密码

```bash
sudo passwd agentuser
```
输入当前用户密码后，为 agentuser 设置新密码。

---

### Step 2：启动配置向导

```bash
hermes memory setup
```
输入 agentuser 密码。

**预期输出：**
```
Hermes Memory Configuration
1. MEMORY.md only
2. Holographic (recommended)
3. Custom
Select memory provider [1]:
```

---

### Step 3：选择 Holographic

输入 `2`，按回车。

**预期输出：**
```
Configuring Holographic Memory Provider
Database file [~/.hermes/memories/holographic.db]:
```

直接**按回车**（使用默认路径）。

---

### Step 4：确认 SQLite 配置

按**回车**跳过。

---

### Step 5：启用语义搜索

输入 `true`，按回车。

---

### Step 6：设置相关度阈值

输入 `0.4`，按回车。

---

### Step 7：跳过 API 配置

直接按**回车**跳过。

---

### Step 8：重启网关

```bash
hermes gateway restart
```
输入 agentuser 密码。等待 `✓ User service restarted` 出现。

---

### Step 9：验证配置成功

```bash
hermes chat
```

进入后输入：

```
fact_store(action="list")
```

**预期输出：**
```
╭─ ⚕ Hermes ─────────────────────────────╮
    Empty — no facts stored yet.
╰────────────────────────────────────────╯
```
显示 `Empty` 是正常的（尚未存入数据）。

---

## 四、批量写入数据（关键步骤）

> **问题：** 一条条在 hermes chat 里输入太麻烦。
> **解法：** 用脚本直接写数据库，配合 agentuser 密码批量写入。

### 4.1 批量写入脚本

```bash
#!/bin/bash
# 写入事实到 fact_store
sudo -u agentuser -S bash -c '
PASSWORD="w2006nqszzzjf"
echo $PASSWORD | sqlite3 /home/agentuser/.hermes/memory_store.db "
INSERT OR REPLACE INTO facts (fact, category, source, created_at, updated_at)
VALUES (\"你的事实内容\", \"category_name\", \"manual\", datetime(\"now\"), datetime(\"now\"));
"
' <<< "ubuntu用户的sudo密码"
```

### 4.2 实际使用的批量写入方法

在配置当晚（2026-05-25），军师通过读取 `~/.hermes/memories/MEMORY.md` 内容，组织成「记得：」格式，然后在 hermes chat 里一次性粘贴，批量写入 fact_store。

**最终状态：fact_store 存储了约 20 条事实，分类包括：**
- user_pref（用户偏好）
- general（一般信息）
- concept（概念）
- project（项目）
- brand（品牌）
- config（配置）
- learning（学习进度）
- role（角色定位）
- preference（偏好）

### 4.3 验证写入成功

```
fact_store(action="list")
```

会显示所有已存入的事实。

---

## 五、日常使用命令

### 5.1 基本操作（hermes chat 内）

| 操作 | 命令格式 | 示例 |
|------|---------|------|
| 存入事实 | `记得：内容` | `记得：我是Carey Hugo，喜欢简洁回复` |
| 更新事实 | `更新：旧内容 → 新内容` | `更新：W1欠9任务 → W1已完成5个` |
| 删除事实 | `删掉：内容` | `删掉：我喜欢喝咖啡` |
| 查看列表 | `fact_store(action="list")` | 直接输入 |

### 5.2 固定不变的信息（一次性存入）

```
记得：我是Carey Hugo，创客星球(CGHub)创始人
记得：偏好简洁回复，讨厌废话，不要问我"懂了吗"
记得：CGHub三层结构：身份层+内容与项目层+价值记录层
记得：正在写《创客经济：AI时代的个体价值操作系统》
记得：WCB学习流程：共学→文件→推GitHub→WCB提交→确认后推进
```

### 5.3 变化信息（随时更新）

```
更新：WCB进度是W1欠9任务 → 更新：WCB进度是W1完成5个，还剩4个
更新：公众号#08已发布 → 更新：公众号#09已发布
```

---

## 六、agentuser 密码与数据库访问

### 6.1 为什么需要 agentuser 密码

Hermes 运行在 `agentuser` 这个专用 Linux 账户下。所有涉及记忆文件的操作（setup、gateway restart、memory write）都需要切换到该用户。

**agentuser 密码：** `w2006nqszzzjf`

### 6.2 直接访问数据库

如果需要在服务器上直接操作数据库（不通过 hermes chat）：

```bash
# 读取所有事实
sudo -u agentuser sqlite3 /home/agentuser/.hermes/memory_store.db "SELECT id, fact, category FROM facts;"

# 手动写入
echo "PASSWORD" | sudo -u agentuser -S sqlite3 /home/agentuser/.hermes/memory_store.db \
  "INSERT INTO facts(fact,category,source) VALUES('内容','category','manual');"
```

### 6.3 重要提醒

> ⚠️ **agentuser 密码已记录在此手册中。**
> 如果密码变更，需要同步更新本手册第六节。
> 如需重置 fact_store，删除数据库文件后重新配置：
> ```bash
> sudo rm /home/agentuser/.hermes/memory_store.db
> hermes memory setup  # 重新选择 Holographic
> hermes gateway restart
> ```

---

*操作手册版本：V1.1*
*创建：Hermes Agent，2026-05-26*
*更新：V1.1 — 2026-05-26：增加真实配置记录、批量写入方法、agentuser 密码*
*审核：Carey Hugo 已确认，可正式使用*