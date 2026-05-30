# CGHub 核心记忆

## 创始人

- 网名：Carey Hugo
- 农历生日：今天（创客星球筹备期间）
- 自称：共同富裕探路者（不是"布道者"——"探路者"更真实，不说过头话）
- 身份：DAO探路者 · Web3创业者 · AI独立开发者 · 数字游民
- 长期使命：余生要做的事，迈向新文明的入口
- 定位：创始人军师+总编辑，战略陪跑，不是执行者

## 项目：创客星球(CGHub)

- 英文全称：Creators Galaxy Hub，简名 CGHub
- 中文版统一写"创客星球(CGHub)"，英文版统一写"Creators Galaxy Hub(CGHub)"
- 旧名 CreatorsGalaxy/Maker Star 不再使用
- 愿景：使命驱动，Web3理念的创客价值操作系统，不是GitHub复制品
- 三层结构：
  1. 身份层（个人主页/作品集）
  2. 内容与项目层
  3. 价值记录层（智能合约）
- 初创合伙人机制：加入即记录贡献，智能合约保证，类Web3空投逻辑

## 当前优先级

- WCB（Web3 Career Build）学习：W1欠9任务(+240分)，W2主线8+活动15，共学流程：共学→军师写文件→推GitHub→Carey在WCB提交→确认后推进
- 公众号：原创连载，每周一主题，系统深入，避免重复
- 《创客经济：AI时代的个体价值操作系统》写作中
- Tokenomics 设计：初创合伙人机制 + 智能合约
- 黑客松招募：文案创作+封面图+招募条件细化（技术/商业/创意分工），招募优先级：先黑客松（≤5人精英），再公众号公开招募（99元船票）

## 关键文档索引

| 用途 | 文件 |
|------|------|
| 战略总纲 | `创客星球战略规划总纲.md`（V2.0定稿） |
| 执行计划 | `docs/06-execution-plan/创客星球系统执行计划_v1.1.md` |
| 书籍大纲 | `docs/04-book-plan/创客经济-书籍大纲.md` |
| 共享记忆 | `memory.md`（本文件） |
| 品牌规范 | `docs/00-brand/wechat-article-style-guide.md`（V5.0锁定） |
| 项目全景 | `docs/00-context/CGHub-项目全景结构总结_2026-05-26.md` |

## 品牌规范

- 所有新创作内容（文章、白皮书、海报等）默认提供中英两个版本
  英文版面向国际读者自然改写，而非逐字翻译
- 公众号铁律：
  ① 严禁第一人称捏造，"我是怎么…"=抄袭
  ② 正向框架：不用"踩坑/教训"
  ③ 防御语一句带过不占主语
  ④ 有愿景画面
  ⑤ 用户手动改完草稿不覆盖

## 共学流程（WCB）

共学流程：共学→军师写文件→推GitHub→Carey在WCB提交→确认后推进

## 全息投影记忆系统（Hermes Agent 双层记忆）

- Layer 1：`~/.hermes/memories/MEMORY.md`（文件层，CGHub repo 同步版本：`memory.md`）
- Layer 2：Holographic Fact Store（向量数据库，`~/.hermes/memories/holographic.db`）
- 配置手册：`docs/00-context/Hermes-Holographic-Memory-操作手册.md`
- 配置步骤：选Holographic → SQLite默认回车 → true → 0.4 → 跳过API → 重启 → 验证`fact_store(action="list")`
- ⚠️ 若遇`su: Authentication failure`，先`sudo passwd root`设root密码

## 关键账号

- 微信公众号 AppID: wx34cf0b6a53435a05

## 技术环境

- Tailscale：服务器100.68.78.70，Carey Win PC 100.104.154.122
- VNC：端口5901，启动`vncserver :1 -localhost no`
- Chrome远程调试：Carey Win需用CMD启动（PowerShell不支持`--`参数）