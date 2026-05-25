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

## 三、完整配置步骤

> ⚠️ **如果遇到 `su: Authentication failure`**
>
> 说明 Ubuntu 云服务器默认没有 root 密码。解决方法：
> ```bash
> sudo passwd root
> ```
> 先输入当前用户密码（SSH 登录密码），再设置新的 root 密码。
> 设好后重新执行 `hermes memory setup`。

---

### Step 1：启动配置向导

```bash
hermes memory setup
```

**预期输出：**
```
Hermes Memory Configuration
1. MEMORY.md only
2. Holographic (recommended)
3. Custom
Select memory provider [1]:
```

---

### Step 2：选择 Holographic

输入 `2`，按回车。

**预期输出：**
```
Configuring Holographic Memory Provider
Database file [~/.hermes/memories/holographic.db]:
```

直接**按回车**（使用默认路径）。

---

### Step 3：确认 SQLite 配置

> 这步用户描述是"直接回车"，说明默认 SQLite 配置已足够。

按**回车**跳过。

---

### Step 4：启用语义搜索

> 用户描述："选 true"

输入 `true`，按回车。

---

### Step 5：设置相关度阈值

> 用户描述："填 0.4"

输入 `0.4`，按回车。

**说明：** 0.4 是语义相似度阈值，数值越高越严格（越要求匹配精确）。0.4 是平衡值。

---

### Step 6：跳过 API 配置

> 用户描述："下一个不用填，直接回车"

这是 API 配置（如 OpenAI 等），直接按**回车**跳过（使用默认/内置）。

---

### Step 7：重启网关

```bash
hermes gateway restart
```

**等待约 10-30 秒**，等待网关完全重启。

---

### Step 8：验证配置成功

重启后，在任意对话中输入：

```
check this "fact_store(action=\"list\")"
```

**预期输出：**
显示 holographic fact store 中的记录列表（可能是空的，也可能有之前的记忆片段）。

如果看到类似这样的输出，说明配置成功：
```
✅ Holographic provider active
✅ Database: ~/.hermes/memories/holographic.db
```

---

## 四、日常使用

### 4.1 Layer 1（MEMORY.md）— 手动维护

**什么时候更新：**
- 用户告诉你新的偏好或信息
- 项目有新的进展或方向变化
- 每次重要对话结束后

**更新方法（两种）：**

**方法A：让 Agent 帮你更新**
在对话中直接说"记住 XXX"，Agent 会自动更新 MEMORY.md。

**方法B：手动编辑文件**
```bash
nano ~/.hermes/memories/MEMORY.md
```

**格式规范：**
```
主题1：内容描述
§
主题2：内容描述
§
```

用 `§` 分隔不同记忆条目。

---

### 4.2 Layer 2（Holographic）— 自动积累

- Agent 在对话中会自动将重要事实写入 fact store
- 语义搜索无需手动干预
- Agent 通过 `fact_store` 工具读写长期记忆

**常用操作：**

| 操作 | 命令 |
|------|------|
| 列出所有记忆 | `check this "fact_store(action=\"list\")"` |
| 搜索记忆 | `search memory for "关键词"` |
| 写入新记忆 | `remember that "内容"` |
| 删除记忆 | `forget "内容"` |

---

### 4.3 记忆同步检查（每次开始工作前）

```
我开始今天的工作了，请确认你的记忆是最新的。
```

Agent 会自动检查两层记忆是否一致，有冲突会提示你。

---

## 五、避坑指南

### 坑1：root 密码未设置
**问题：** 执行 `hermes memory setup` 时提示 `su: Authentication failure`  
**解决：** `sudo passwd root` → 设置 root 密码

### 坑2：网关未重启就测试
**问题：** 配置完成但验证命令不生效  
**解决：** 必须先 `hermes gateway restart`，等待 10-30 秒后再测试

### 坑3：API 超额导致 Holographic 不可用
**问题：** fact store 查询返回空或报错  
**解决：** 检查 API 配额，或在配置 Step 6 时跳过自定义 API（使用内置）

### 坑4：MEMORY.md 过长被截断
**问题：** 记忆文件超过 2200 字符限制  
**解决：** 定期整理，用 `§` 分隔，删除过时内容

### 坑5：两层记忆不一致
**问题：** Layer 1 和 Layer 2 信息矛盾  
**解决：** 以 Layer 1（MEMORY.md）为准，手动同步到 Layer 2

---

## 六、团队共享方案

如果多个 Agent 或多台设备需要共享同一套记忆：

### 方案A：共享 MEMORY.md（推荐）

把 `~/.hermes/memories/MEMORY.md` 替换为软链接：

```bash
# 将共享记忆文件链接到 CGHub repo
ln -s ~/creators-galaxy/memory.md ~/.hermes/memories/MEMORY.md
```

**优势：** Git 版本管理，任何变更自动 push/pull  
**劣势：** Holographic 层（fact store）不共享

### 方案B：两层都共享（高级）

```bash
# 在 CGHub repo 建立共享记忆目录
mkdir -p ~/creators-galaxy/shared-memory

# 链接 Layer 1
ln -s ~/creators-galaxy/shared-memory/MEMORY.md ~/.hermes/memories/MEMORY.md

# 链接 Layer 2（Holographic SQLite）
ln -s ~/creators-galaxy/shared-memory/holographic.db ~/.hermes/memories/holographic.db
```

**优势：** 两层完全同步  
**劣势：** 多设备同时写入可能导致 SQLite 锁

---

## 七、配置状态记录

| 项目 | 状态 | 值 |
|------|------|-----|
| Provider | 待配置 | Holographic |
| Database path | 待配置 | `~/.hermes/memories/holographic.db` |
| Semantic search | 待配置 | `true` |
| Relevance threshold | 待配置 | `0.4` |
| API config | 待配置 | 默认/跳过 |
| 配置日期 | 待记录 | YYYY-MM-DD |
| 配置执行人 | 待记录 | 你的名字 |

**配置完成后请更新上表。**

---

## 八、快速重置（重装时）

如果需要重装或迁移：

```bash
# 1. 备份旧记忆
cp ~/.hermes/memories/MEMORY.md ~/backup-memory.md
cp ~/.hermes/memories/USER.md ~/backup-user.md

# 2. 删除旧配置
rm ~/.hermes/memories/holographic.db

# 3. 重新配置（见第三节）
hermes memory setup

# 4. 恢复 Layer 1
cp ~/backup-memory.md ~/.hermes/memories/MEMORY.md
cp ~/backup-user.md ~/.hermes/memories/USER.md

# 5. 重启网关
hermes gateway restart
```

---

*操作手册版本：V1.0*  
*创建：Hermes Agent，2026-05-26*  
*审核：待 Carey Hugo 确认后正式使用*