# CGHub 公众号排版规范 V2.0
# 增强版：纯 inline style + 丰富视觉组件
# 2026-05-20 V2.0 更新

---

## 核心原则

1. **全部使用 inline style**，不用 class/外部CSS（微信编辑器不支持）
2. **保留丰富的视觉组件**：深色标题块、金句引言、灰底推荐区等
3. 以本规范为唯一标准，不自作主张"优化"

---

## 一、整体排版结构

```
[封面图] 1280×547 居中
↓
[开头问候] 17px rgba(0,0,0,0.9)
↓
[连载标签] 灰底+蓝左边框 blockquote 风格
↓
[声明] 14px #888（可选）
↓
[分割线] 渐变灰线
↓
[正文开场] 故事/场景切入
↓
[章节标题块] 深蓝背景 #0d1828 + 英文序号 + 中文标题
↓
[正文段落] 15px #333 + [强调段] 16px #111 加粗
↓
[金句引言] 暖色背景 #f9f6f0 + 棕色左边框 #c09060
↓
[推荐阅读] 灰底+蓝左边框
↓
[分割线]
↓
（重复章节...）
↓
[互动环节]
↓
[关于本书连载] 灰底+蓝左边框
↓
[互动引导] 17px
↓
[点赞转发] 14px 居中
↓
[署名] 14px 居中
↓
[版权] 12px 居中
```

---

## 二、组件样式速查

### 2.1 正文段落
```html
<p style="margin: 0 0 16px; font-size: 15px; line-height: 1.9; color: #333; text-align: justify; font-family: -apple-system, 'PingFang SC', system-ui, BlinkMacSystemFont, 'Helvetica Neue', 'Microsoft YaHei', sans-serif;">
```

### 2.2 章节标题块（深蓝背景）
```html
<div style="background: #0d1828; border-radius: 8px; padding: 16px 20px; margin: 30px 0 20px;">
    <p style="margin: 0 0 6px; font-size: 10px; color: #4a9de8; letter-spacing: 3px; text-transform: uppercase;">ONE</p>
    <p style="margin: 0; font-size: 18px; color: #dde8ff; font-weight: 700; line-height: 1.4;">章节标题</p>
</div>
```
英文序号：ONE / TWO / THREE / FOUR / SUMMARY

### 2.3 强调段
```html
<p style="margin: 20px 0; font-size: 16px; color: #111; font-weight: 700; line-height: 1.7; font-family: ...;">
```

### 2.4 金句引言（暖色调）
```html
<div style="background: #f9f6f0; border-left: 3px solid #c09060; padding: 18px 22px; margin: 24px 0; font-size: 16px; color: #444; line-height: 1.7; font-family: ...;">
```

### 2.5 连载标签 / 推荐阅读 / 关于本书（统一风格）
```html
<div style="margin: 14px 0; padding: 14px 18px; border-left: 4px solid #576b95; background: #f7f7f7; font-size: 15px; font-family: ...; color: #555;">
```
连载标签加 `font-style: italic;`

### 2.6 分割线
```html
<hr style="border: none; height: 1px; background: linear-gradient(to right, transparent, #ddd, transparent); margin: 28px 0;">
```

### 2.7 行内加粗
```html
<strong style="color: #111; font-weight: 700;">加粗文字</strong>
```

---

## 三、字号规范

| 元素 | 字号 | 颜色 | 说明 |
|------|------|------|------|
| 开头问候 | 17px | rgba(0,0,0,0.9) | "大家好，我是Hugo。" |
| 正文段落 | 15px | #333 | 两端对齐 justify |
| 章节序号 | 10px | #4a9de8 | letter-spacing:3px 大写 |
| 章节标题 | 18px | #dde8ff | font-weight:700 |
| 强调段 | 16px | #111 | font-weight:700 |
| 金句引言 | 16px | #444 | 暖色背景+棕色左边框 |
| blockquote内文 | 15px | #555 | 灰底+蓝左边框 |
| 声明 | 14px | #888 | 可选 |
| 互动引导 | 17px | #333 | "既然看到这里了..." |
| 点赞转发 | 14px | #333 | 居中 |
| 署名 | 14px | #666 | 居中 |
| 版权 | 12px | #999 | 居中 |

---

## 四、固定尾部内容

```
[互动引导] 17px
既然看到这里了，欢迎评论区聊聊，若有启发请随手点赞、在看、转发三连，
要第一时间收到推送，可点头像进去右上角设为星标⭐️～感谢鼓励支持，下次见。

[点赞行] 14px 居中
如果这篇文章对你有帮助，欢迎点赞、在看、转发

[署名] 14px 居中
「胡戈AI赋能」，专注AI编程出海、Web3、OPC

[版权] 12px 居中
© 胡戈AI赋能 数字游民 新思想探路者 AI独立开发实践者
```

---

## 五、封面图规范（不变）

- 比例：1280×547（约2.34:1）
- 主色调：蓝色系 + 深空黑
- 必须包含 CGHub 创客星球 logo
- Logo 必须用代码合成（Pillow），不靠 prompt 描述

---

*本规范由 CGHub AI总助 整理*
*版本：V2.0 · 2026-05-20*
*V1.0→V2.0 变更：统一为纯 inline style，同时保留深色标题块、金句引言等丰富组件*
