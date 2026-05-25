# CGHub 公众号排版规范 V5.0
# 2026-05-25 定稿锁定版（以用户定时发表文章为唯一标准）
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

### 1.2 开头问候
```html
<p style="font-size:17px;color:rgba(0,0,0,0.9);margin:20px 0;">大家好，我是Hugo。<br>正文约XXXX字，X分钟阅读</p>
```

### 1.3 连载标签（灰底+蓝左边框）
```html
<div style="margin:14px 0;padding:14px 18px;border-left:4px solid rgb(87,107,149);background:rgb(247,247,247);font-size:15px;font-style:italic;">
📖 公众号首发，本文为书籍《AI新时代——当机器人学会分配》第XX篇连载
</div>
```

### 1.4 声明
```html
<div style="font-size:14px;color:#888;margin:14px 0;">
本文为原创连载，每周一主题，系统探讨AI时代变革。
</div>
```

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

### 1.15 署名
```html
<p style="font-size:14px;text-align:center;margin:15px 0;">「胡戈AI赋能」，专注AI编程出海、Web3、OPC</p>
```

### 1.16 版权
```html
<p style="font-size:12px;text-align:center;color:#666;margin:15px 0;">© 胡戈AI赋能 数字游民 新思想探路者 AI独立开发实践者</p>
```

---

## 二、字号规范

| 元素 | 字号 | 颜色 |
|------|------|------|
| 开头问候 | 17px | rgba(0,0,0,0.9) |
| 连载标签 | 15px | #333（italic） |
| 声明 | 14px | #888 |
| 章节序号 | 10px | #4a9de8 |
| 章节标题 | 17px | #dde8ff（font-weight:700） |
| 正文段落 | 15px | #333333 |
| 强调段 | 16px | #111 |
| 金句 | 16px | #444 |
| 互动区块标题 | 16px | #1e4d7b |
| 互动区块正文 | 15px | #2c5282 |
| 互动引导 | 17px | #333 |
| 关于本书 | 15px | #333 |
| 下篇预告 | 14px | #999 |
| 署名 | 14px | #333 |
| 版权 | 12px | #666 |

---

## 三、创作规范

- 每篇提供信息增量，对标书籍独立章节
- 标题不得同质化
- 系统性深入探讨，原创思考
- 调性：积极、破局、希望感。不用"陷阱/坑/锁链/焦虑"
- 引用经典：古代（孔孟老易）+ 当代（纳瓦尔/哈耶克/卢梭）
- 结尾引导关注，回复词："AI创客"

---

*版本：V5.0 · 2026-05-25 · 以定时发表文章为唯一标准锁定*