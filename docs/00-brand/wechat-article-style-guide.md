# CGHub 公众号排版规范 V5.0 连载版
# 2026-05-29 更新（用于：书籍《AI新时代——当机器人学会分配》连载专用）
# ⚠️ V5.1 为通用版（爆款/招募/时评），两者结构不同，不可混用
# ⚠️ 标准模板文件：`content/serial/09-Harness-AI失控边界.html`（连载参考范本）
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

### 1.2 封面配图（article内嵌配图，section包裹，居中）
```html
<section style="text-align:center;margin:0 0 10px;">
  <img src="封面图URL" alt="文章标题" style="max-width:100%;display:block;margin:0 auto;border-radius:8px;">
</section>
```

### 1.2.1 片头标准顺序（必须严格按此顺序）
```
1. 封面配图（section包裹）
2. 声明框（灰底+蓝左边框div）
3. 声明附注（font-size:14px;color:#888）
4. 开场白（17px，深色，rgba(0,0,0,0.9)）
5. 分割线hr
```

### 1.3 开场白（17px，深色）
```html
<p style="font-size:17px;color:rgba(0,0,0,0.9);margin:20px 0;">
大家好，我是Hugo，数字游民在路上。<br>
正文约XXXX字，X分钟阅读
</p>
```
⚠️ 注意：文章内容正文段落用 `rgb(51,51,51)` / `#333333` 而不是 `rgba(0,0,0,0.9)`，两者不要混淆。

### 1.4 声明（灰底+蓝左边框div，斜体）
```html
<div style="margin:14px 0;padding:14px 18px;border-left:4px solid rgb(87,107,149);background:rgb(247,247,247);font-size:15px;font-style:italic;">
📖 公众号首发，本文为书籍《AI新时代——当机器人学会分配》第XX篇连载
</div>
```
⚠️ 斜体用 `<em>` 在声明附注中，正文声明框用 `font-style:italic` 在 div 上；不要用 `<span>` 斜体

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

### 1.9 金句引言（暖色调 div #f9f6f0，左侧金色3px边框）
```html
<div style="background:#f9f6f0;border-left:3px solid #c09060;padding:18px 22px;margin:24px 0;font-size:16px;color:#444;line-height:1.7;">
"金句内容"
</div>
```
⚠️ 金句用 `<div>` 而非 `<blockquote>`（微信编辑器会剥离 blockquote 的背景色）；div 内直接写文字，不需要再包 `<p>`
⚠️ **金句数量：按需添加，一般2~5句**。每篇根据内容质量判断是否值得做金句，不要机械套用固定数量。选金句标准：该句是全篇核心观点的高浓度凝练，或引用有力值得特别突出。

### 1.10 推荐阅读（灰底+蓝左边框）
```html
<div style="margin:14px 0;padding:14px 18px;border-left:4px solid rgb(87,107,149);background:rgb(247,247,247);font-size:15px;">
📖 推荐阅读：《书名》<br>
推荐理由
</div>
```

### 1.11 互动区块（渐变蓝底，末尾元素）
```html
<section style="margin:28px 0;padding:22px 24px;background:linear-gradient(135deg,#f0f8ff,#e6f7ff);border-left:4px solid #4a9de8;border-radius:8px;">
<p style="margin:0 0 12px;font-size:16px;color:#1e4d7b;font-weight:600;">💫 互动话题</p>
<p style="margin:0 0 12px;font-size:15px;color:#2c5282;line-height:1.7;">互动内容</p>
<p style="margin:0;font-size:15px;color:#2c5282;line-height:1.7;">互动引导</p>
</section>
```
⚠️ **互动话题是文章最后一个内容模块**，在「关于本书与连载」之后

### 1.12 结尾模块标准顺序（连载版）
```
1. 关于本书与连载（灰底+蓝左边框div）← 连载版才有
2. 下篇预告（14px灰色居中）← 连载版才有
3. 分割线hr
4. 互动话题区块（section渐变蓝底）
5. 互动引导（17px正文）
6. 公众号名片
7. 署名（12px灰色居中）
```

### 1.13 结尾模块标准顺序（通用版）
```
1. 分割线hr
2. 互动话题区块（section渐变蓝底）
3. 互动引导（17px正文）
4. 公众号名片
5. 署名（12px灰色居中）
```

### 1.14 互动引导（17px 正文）
```html
<p style="font-size:17px;color:#333;margin:25px 0;line-height:1.7;">既然看到这里了，欢迎评论区聊聊，若有启发请随手点赞、在看、转发三连。</p>
```

### 1.15 关于本书连载（灰底+蓝左边框）
```html
<div style="margin:14px 0;padding:14px 18px;border-left:4px solid rgb(87,107,149);background:rgb(247,247,247);font-size:15px;">
📖 关于本书与连载：<br>
这是《AI新时代——当机器人学会分配》第XX篇连载。<br><br>
上篇聊了XXX，这篇聊了XXX。<br>
下篇，我们聊XXX。
</div>
```

### 1.16 下篇预告
```html
<p style="font-size:14px;color:#999;text-align:center;margin:20px 0 30px;">下篇，我们接着聊。</p>
```

### 1.18 角色表格（深蓝表头，数据结构）
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