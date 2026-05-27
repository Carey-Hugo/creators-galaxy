# CGHub 公众号排版规范 V5.1 通用版
# 2026-05-27 定稿（用于：爆款文章、热点时评、招募公告等非连载文章）
# ⚠️ V5.0 为书籍连载专用版，两者结构不同，不可混用
# ⚠️ 本版本为工作流基准，所有创作必须严格遵循，禁止自行变更样式

---

## ⚠️ 核心技术原则（微信编辑器规则）

粘贴时发生什么：
1. `<style>` 标签 → **完全剥离**
2. `class="xxx"` 属性 → **完全删除**
3. `var(--css-variable)` → **失效**
4. `<div style="background:#xxx">` → **背景色消失**
5. `<table style="background:#xxx">` → **✅ 背景色保留**

**三条铁律：**
- 全部 inline style，不使用 `<style>` 标签和 `class`
- 彩色背景块必须用 `<table>`，不能用 `<div>`
- 以本规范为唯一标准，禁止自作主张"优化"

---

## 一、组件样式速查

### 1.1 封面图
```html
<img src="封面图URL" alt="文章标题" style="max-width:100%;display:block;margin:0 auto;border-radius:8px;">
```

**⚠️ Logo 合成规范（必须，不允许在 prompt 里画 logo）：**
1. AI 生成底图（prompt 只描述主体视觉，不提 logo）
2. Pillow 代码合成 `docs/00-brand/logo-v2-horizontal-clean.png` 到右下角
   - logo 高度 = 封面高度 × 11%
   - 距边缘 20px
3. 用 `uv run python3` 执行（系统 Python 无 Pillow）

logo 定稿文件（旧文件已废弃）：
- 长版(1600×700)：`docs/00-brand/logo-v2-horizontal-clean.png`
- 正版(1200×1200)：`docs/00-brand/logo-v1-square-clean.png`

### 1.2 开场白（17px，深色）
```html
<p style="font-size:17px;color:rgba(0,0,0,0.9);margin:20px 0;">大家好，我是Hugo，数字游民在路上。<br>正文约XXXX字，X分钟阅读</p>
```
⚠️ 注意：文章内容正文段落用 `rgb(51,51,51)` 而不是 `rgba(0,0,0,0.9)`，两者在正文中不要混淆。

### 1.3 声明（灰底+细边框，斜体）
```html
<table style="margin:0 0 10px;padding:0;border-collapse:collapse;display:table;width:100%;max-width:100%;box-sizing:border-box;border:1px solid rgb(221,221,221);background:rgb(255,255,255);"><tbody><tr><td style="padding:5px 10px;"><p style="margin:0;padding:0;font-size:13px;color:rgb(136,136,136);line-height:1.7;font-family:-apple-system,'PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif;"><em>本文为创客星球(CGHub)黑客松队友招募贴，期待链接同DAO有缘人。</em></p><p style="margin:0;padding:0;font-size:13px;color:rgb(136,136,136);line-height:1.7;font-family:-apple-system,'PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif;"><em>正文约1800字 · 8分钟阅读</em></p></td></tr></tbody></table>
```
⚠️ 必须用 table 结构（微信编辑器会剥离 div 的 border），斜体用 `<em>`（不是 `<span style="font-style:italic">`）

### 1.3.1 开场白
```html
<p style="margin:0 0 14px;font-size:15px;line-height:1.9;color:rgb(51,51,51);font-family:-apple-system,'PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif;">大家好，我是Hugo，数字游民在路上。</p>
<p style="margin:0 0 14px;font-size:15px;line-height:1.9;color:rgb(51,51,51);font-family:-apple-system,'PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif;">AI生产力跃迁驱动新文明正在加速到来，希望这次你不再只是旁观者...</p>
```
⚠️ 内容顶格写，不要加 text-indent 或任何缩进。

### 1.5 分割线
```html
<hr style="border:none;height:1px;background:linear-gradient(to right,transparent,#e0e0e0,transparent);margin:28px 0;">
```

### 1.6 章节标题块（深蓝背景 #0d1828，table 结构）
```html
<table style="background:#0d1828;border-radius:8px;padding:0;border-spacing:0;margin:28px 0 18px;width:100%;"><tbody><tr><td style="padding:14px 18px 12px;"><span style="font-size:10px;color:#4a9de8;letter-spacing:3px;display:block;margin-bottom:4px;">ONE</span><span style="font-size:17px;color:#dde8ff;font-weight:700;line-height:1.5;letter-spacing:0.3px;">一、章节标题</span></td></tr></tbody></table>
```
英文序号：ONE / TWO / THREE / FOUR / FIVE / SIX / SEVEN / SUMMARY

### 1.7 正文段落（必须用 `<p>`）
```html
<p style="margin:0 0 14px;font-size:15px;line-height:1.9;color:#333333;font-family:-apple-system,'PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif;">
正文内容
</p>
```
⚠️ line-height:1.9（不是1.8）；color:#333333；必须有完整 font-family

### 1.8 强调段
```html
<p style="margin:20px 0;font-size:16px;color:#111;font-weight:700;line-height:1.7;">强调内容</p>
```

### 1.9 金句引言（暖色调 #f9f6f0）
```html
<div style="background:#f9f6f0;border-left:3px solid #c09060;padding:18px 22px;margin:24px 0;font-size:16px;color:#444;line-height:1.7;">
"金句内容"
</div>
```

### 1.10 推荐阅读（灰底+蓝左边框）
```html
<div style="margin:14px 0;padding:14px 18px;border-left:4px solid rgb(87,107,149);background:rgb(247,247,247);font-size:15px;">
📖 推荐阅读：《书名》<br>
推荐理由
</div>
```

### 1.11 互动区块（渐变蓝底）
```html
<section style="margin:28px 0;padding:22px 24px;background:linear-gradient(135deg,#f0f8ff,#e6f7ff);border-left:4px solid #4a9de8;border-radius:8px;">
<p style="margin:0 0 12px;font-size:16px;color:#1e4d7b;font-weight:600;">💫 互动话题</p>
<p style="margin:0 0 12px;font-size:15px;color:#2c5282;line-height:1.7;">互动内容</p>
<p style="margin:0;font-size:15px;color:#2c5282;line-height:1.7;">互动引导</p>
</section>
```

### 1.12 互动引导（17px 正文）
```html
<p style="font-size:17px;color:#333;margin:25px 0;line-height:1.7;">既然看到这里了，欢迎评论区聊聊，若有启发请随手点赞、在看、转发三连。</p>
```

### 1.13 关于本书连载（灰底+蓝左边框）
```html
<div style="margin:14px 0;padding:14px 18px;border-left:4px solid rgb(87,107,149);background:rgb(247,247,247);font-size:15px;">
📖 关于本书与连载：<br>
这是《AI新时代——当机器人学会分配》第XX篇连载。<br><br>
上篇聊了XXX，这篇聊了XXX。<br>
下篇，我们聊XXX。
</div>
```

### 1.14 下篇预告
```html
<p style="font-size:14px;color:#999;text-align:center;margin:20px 0 30px;">下篇，我们接着聊。</p>
```

### 1.16 角色表格（深蓝表头，数据结构）
```html
<table style="border-collapse:collapse;margin:12px 0;font-size:14px;font-family:-apple-system,'PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif;width:100%;"><thead><tr style="background:#0d1828;color:#dde8ff;"><th style="padding:10px 12px;text-align:left;font-weight:600;border-bottom:1px solid #e0e0e0;color:rgb(2,30,170);">角色</th><th style="padding:10px 12px;text-align:left;font-weight:600;border-bottom:1px solid #e0e0e0;color:rgb(2,30,170);">职责</th><th style="padding:10px 12px;text-align:left;font-weight:600;border-bottom:1px solid #e0e0e0;color:rgb(2,30,170);">技能要求</th></tr></thead><tbody><tr><td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;color:#333333;">Solidity 开发者</td><td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;color:#333333;">合约：贡献记录 + 收益分配 + 多签</td><td style="padding:10px 12px;border-bottom:1px solid #e0e0e0;color:#333333;">Solidity / 智能钱包 / ERC-4337</td></tr></tbody></table>
```
⚠️ 表头背景 `#0d1828`，表头文字颜色 `rgb(2,30,170)`（深蓝，非电蓝）

### 1.17 小标题（emoji + 加粗）
```html
<p style="margin:0 0 14px;font-size:15px;line-height:1.9;color:#333333;"><strong>🎯 核心角色（参与执行，成为初创合伙人）</strong></p>
```

### 1.18 署名（居中，14px）
```html
<p style="font-size:14px;text-align:center;color:#666;margin:15px 0;">© 胡戈AI赋能 数字游民 新思想探路者 AI独立开发实践者</p>
```

---

## 三、正文内容顶格原则

⚠️ **所有正文内容必须顶格写，禁止加任何缩进（text-indent、padding-left 等）**

---

## 四、字号规范（V5.1 更新）

| 元素 | 字号 | 颜色 |
|------|------|------|
| 开场白（17px） | 17px | rgba(0,0,0,0.9) |
| 声明（灰底框） | 13px | rgb(136,136,136) |
| 章节序号 | 10px | #4a9de8 |
| 章节标题 | 17px | #dde8ff（font-weight:700） |
| 正文段落 | 15px | #333333 或 rgb(51,51,51) |
| 强调段 | 16px | #111（font-weight:700） |
| 引用（金句框） | 16px | rgb(68,68,68) |
| 小标题 | 15px | #333（加粗） |
| 表格内容 | 14px | #333333 |
| 署名 | 14px | #666（居中） |
| 版权 | 14px | #666（居中） |

---

## 五、创作规范（2026-05-27 更新）

- 每篇提供信息增量，对标书籍独立章节
- 标题不得同质化
- 系统性深入探讨，原创思考
- 调性：积极、破局、希望感。不用"陷阱/坑/锁链/焦虑"
- 引用经典：古代（孔孟老易）+ 当代（纳瓦尔/哈耶克/卢梭）
- 结尾引导关注，回复词："AI创客"
- **内容顶格写，禁止缩进**

---

*版本：V5.1 · 2026-05-27 · 通用版（爆款/招募/时评）*
*V5.0（书籍连载专用）结构：连载标签+声明+章节ONE-TWO+金句+推荐阅读+关于本书连载 ——见 V5.0 历史版本或 conversation-2026-05-25.md*