# CGHub 公众号排版规范 V4.0
# 创作与排版一体化模板
# 2026-05-20 V4.0 更新（以用户定稿版本为基准，统一结构、组件、字号）

---

## ⚠️ 核心技术原则

**微信编辑器粘贴时会发生什么：**
1. `<style>` 标签 → **完全剥离**
2. `class="xxx"` 属性 → **完全删除**
3. `var(--css-variable)` → **变成无效值**
4. `<div style="background: #xxx">` → **背景色消失**
5. `<table style="background: #xxx">` → **✅ 背景色保留**

**正确原则：**
1. **全部使用 inline style**（`style="..."`）
2. **不用 `<style>` 标签和 `class` 属性**
3. **不用 CSS 变量**
4. **彩色背景块必须用 `<table>`，不能用 `<div>`**
5. 正文段落用 `<p>`，不用 `<div>` 包裹块级内容
6. 以本规范为唯一标准，不自作主张"优化"

---

## 一、整体排版结构

```
[封面图] 1280×547 居中
↓
[开头问候] 17px rgba(0,0,0,0.9)，含"大家好，我是Hugo" + 阅读时长估算
↓
[连载标签] 灰底+蓝左边框（📖 书名 · 第XX篇连载）
↓
[声明] 14px #888 "本文为原创连载，每周一主题..."
↓
[分割线] hr 灰线
↓
[正文开场] 故事/场景切入（15px #333）
↓
[章节标题块] 深蓝背景 #0d1828 + 英文序号 + 中文标题（div结构，class方式）
↓
[正文段落] 15px #333 两端对齐
↓
[强调段] 16px #111 加粗
↓
[金句] > 引用格式，16px #444
↓
[推荐阅读] 灰底+蓝左边框（每章结尾）
↓
[分割线] hr 灰线
↓
（重复章节...）
↓
[互动区块] 渐变蓝底+蓝左边框（<section> inline style）
↓
[互动引导] 17px 正文
↓
[互动问题] 15px 正文
↓
[分割线] hr 灰线
↓
[关于本书连载] 灰底+蓝左边框
↓
[下篇预告] 15px #999 居中
↓
[互动引导] 17px "既然看到这里了..."
↓
[点赞转发] 14px 居中
↓
[署名] 14px 居中
↓
[版权] 12px #666 居中
```

**注意：** 草稿箱预览可用 `<style>` + `class`，但发布到微信编辑器前必须转换为**纯 inline style**，参考下方转换模板。

---

## 二、组件样式速查（V4.0 定稿版本）

### 2.1 封面图
```html
<img src="封面图URL" alt="文章标题" style="max-width: 100%; display: block; margin: 0 auto; border-radius: 8px;">
```

### 2.2 开头问候
```html
<div style="font-size: 17px; color: rgba(0,0,0,0.9); margin: 20px 0;">
    大家好，我是Hugo。<br>
    正文约XXXX字，X分钟阅读
</div>
```

### 2.3 连载标签（灰底+蓝左边框）
```html
<div style="margin: 14px 0; padding: 14px 18px; border-left: 4px solid rgb(87, 107, 149); background: rgb(247, 247, 247); font-size: 15px; font-style: italic;">
    📖 公众号首发，本文为书籍《书名》<br>
    （副标题）<br>
    第XX篇连载
</div>
```

### 2.4 声明
```html
<div style="font-size: 14px; color: #888; margin: 14px 0;">
    本文为原创连载，每周一主题，旨在系统探讨AI时代生产力与生产关系变革。不是投机蹭热点，而是持续结构化的深度探讨。
</div>
```

### 2.5 分割线
```html
<hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
```

### 2.6 章节标题块（深蓝背景 #0d1828）
```html
<div style="background: #0d1828; border-radius: 8px; padding: 16px 20px; margin: 30px 0 20px;">
    <div style="font-size: 10px; color: #4a9de8; letter-spacing: 3px; text-transform: uppercase; margin: 0 0 5px;">ONE</div>
    <div style="font-size: 18px; color: #dde8ff; font-weight: 700; margin: 0;">一、章节标题</div>
</div>
```
英文序号：ONE / TWO / THREE / FOUR / SUMMARY

### 2.7 正文段落
```html
<div style="font-size: 15px; color: #333; line-height: 1.8; text-align: justify; margin: 18px 0;">
    正文内容
</div>
```

### 2.8 强调段
```html
<div style="font-size: 16px; color: #111; font-weight: 700; margin: 20px 0; line-height: 1.7;">
    强调内容
</div>
```

### 2.9 金句引言（暖色调 #f9f6f0）
```html
<div style="background: #f9f6f0; border-left: 3px solid #c09060; font-size: 16px; color: #444; padding: 18px 22px; margin: 24px 0; line-height: 1.7;">
    > 金句内容
</div>
```

### 2.10 推荐阅读（灰底+蓝左边框）
```html
<div style="margin: 14px 0; padding: 14px 18px; border-left: 4px solid rgb(87, 107, 149); background: rgb(247, 247, 247); font-size: 15px;">
    📖 推荐阅读：《书名》<br>
    推荐理由<br>
    【微信小店购买链接：待上架后插入】
</div>
```

### 2.11 互动区块（渐变蓝底）
```html
<section style="margin: 28px 0; padding: 22px 24px; background: linear-gradient(135deg, #f0f8ff, #e6f7ff); border-left: 4px solid #4a9de8; border-radius: 8px;">
    <p style="margin: 0 0 12px 0; font-size: 16px; color: #1e4d7b; font-weight: 600;">💫 标题</p>
    <p style="margin: 0 0 12px 0; font-size: 15px; color: #2c5282; line-height: 1.7;">内容</p>
    <p style="margin: 0; font-size: 15px; color: #2c5282; line-height: 1.7;">内容</p>
</section>
```

### 2.12 关于本书连载（灰底+蓝左边框）
```html
<div style="margin: 14px 0; padding: 14px 18px; border-left: 4px solid rgb(87, 107, 149); background: rgb(247, 247, 247); font-size: 15px;">
    📖 关于本书与连载：<br>
    这是《书名》第XX篇连载。<br>
    <br>
    本篇内容摘要。
</div>
```

### 2.13 固定尾部（从 V4.0 定稿提取）
```html
<!-- 互动问题 -->
<div style="font-size: 15px; color: #333; margin: 18px 0;">你有没有掉进过这三个坑？在评论区聊聊你的经历。</div>
<div style="font-size: 15px; color: #333; margin: 18px 0;">如果觉得这篇文章说到了你的痛点，<strong>转发</strong>给那个和你一样在坑里的朋友。</div>

<hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">

<!-- 下篇预告 -->
<div style="font-size: 14px; color: #999; text-align: center; margin: 20px 0 30px;">
    下篇，我们接着聊。
</div>

<!-- 互动引导 -->
<div style="font-size: 17px; margin: 25px 0;">
    既然看到这里了，欢迎评论区聊聊，若有启发请随手点赞、在看、转发三连，要第一时间收到推送，可点头像进去关注。
</div>

<!-- 点赞转发 -->
<div style="font-size: 14px; text-align: center; margin: 20px 0;">
    如果这篇文章对你有帮助，欢迎点赞、在看、转发
</div>

<!-- 署名 -->
<div style="font-size: 14px; text-align: center; margin: 15px 0;">
    「胡戈AI赋能」，专注AI编程出海、Web3、OPC
</div>

<!-- 版权 -->
<div style="font-size: 12px; text-align: center; color: #666; margin: 15px 0;">
    © 胡戈AI赋能 数字游民 新思想探路者 AI独立开发实践者
</div>
```

---

## 三、字号规范（V4.0）

| 元素 | 字号 | 颜色 | 说明 |
|------|------|------|------|
| 开头问候 | 17px | rgba(0,0,0,0.9) | "大家好，我是Hugo" + 阅读时长 |
| 连载标签 | 15px | #333 | 灰底+蓝左边框，italic |
| 声明 | 14px | #888 | 可选，放连载标签后 |
| 章节序号 | 10px | #4a9de8 | letter-spacing:3px 大写 |
| 章节标题 | 18px | #dde8ff | font-weight:700 |
| 正文段落 | 15px | #333 | 两端对齐 justify |
| 强调段 | 16px | #111 | font-weight:700 |
| 金句引言 | 16px | #444 | 暖色背景+棕色左边框 |
| 推荐阅读 | 15px | #333 | 灰底+蓝左边框 |
| 互动区块标题 | 16px | #1e4d7b | font-weight:600 |
| 互动区块正文 | 15px | #2c5282 | line-height:1.7 |
| 互动引导 | 17px | #333 | "既然看到这里了..." |
| 互动问题 | 15px | #333 | 两端对齐 |
| 下篇预告 | 14px | #999 | 居中 |
| 点赞转发 | 14px | #333 | 居中 |
| 署名 | 14px | #333 | 居中 |
| 版权 | 12px | #666 | 居中 |

---

## 四、创作规范（附加）

- 每篇提供**信息增量**，对标书籍独立章节（非重复已有内容）
- 标题不得同质化（一个主题只用一次）
- 系统性深入探讨，原创思考，无搬运洗稿
- 文章末尾声明：**"本文为原创连载，每周一主题，系统探讨AI时代变革"**
- 调性：积极框架，破局感，希望/赋能。不用"陷阱/坑/锁链/焦虑"

---

## 五、模板文件

实际创作时，直接从以下模板文件复制修改：
- `~/creators-galaxy/docs/00-brand/wechat-article-template.html`（干净空模板）

---

*本规范由 CGHub AI总助 整理*
*版本：V4.0 · 2026-05-20*
*V3.0→V4.0 变更：以用户定稿版本为基准，统一整体结构、互动区块、尾部固定格式、字号规范、创作原则*
