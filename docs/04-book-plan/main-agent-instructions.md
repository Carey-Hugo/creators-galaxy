# 给总助的一次性设置指令
# One-Time Setup Instruction for Main Agent

> **可见范围 / Visibility：** 内部（Internal Only）
> **用途：** 复制发给总助，执行一次即可
> **最后更新 / Last Updated：** 2025-05-01

---

## 要发给总助的指令（复制下面的全部内容）

```
请帮我做以下一次性设置：

我有一个长期项目叫"创客星球（CGHub）"，涉及书籍写作、品牌策划、技术文档等。

请按以下方式工作：

1. 首先拉取仓库：
git clone https://gitee.com/carey-hugo/creators-galaxy.git
cd creators-galaxy

2. 阅读项目协议（以后每次涉及该项目时，自动执行）：
docs/04-book-plan/main-agent-protocol.md

这个协议里写了：
- 什么时候需要读取仓库（触发条件：创客星球/CGHub/书籍封面/Web3等关键词）
- 读取哪些文件（按顺序：.repo-guide.md → conversation-index → 最新会话）
- 完成任务后要把工作内容写回会话记录

3. 设置完成后，告诉我你已经完成设置，以后你会在触发条件满足时自动加载上下文。

之后关于创客星球的事情，你不需要我每次都解释背景，直接读仓库里的文件就行。
```

---

## 触发关键词（供总助识别）

```
创客星球 | CGHub | Creators Galaxy Hub | 《AI新时代——当机器学会分配》
书籍封面 | 书籍策划 | 白皮书 | 合伙人招募 | Web3 | DAO
Gitee | git push | git pull
```

---

*本文件是给总助的指令模板，实际使用时请复制上面的完整指令段发给总助*
