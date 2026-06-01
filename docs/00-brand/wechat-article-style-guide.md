# CGHub 公众号排版规范 V6.0 连载版（2026-05-31）
> ⚠️ 以微信草稿箱第10篇为基准范本，禁止自行变更样式
> ⚠️ 标准模板文件：`content/serial/10-公众号发布版-reference.html`
> ⚠️ 本版本为工作流基准，所有连载创作必须严格遵循

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

## 一、片头标准结构（必须严格按此顺序）

```
1. 封面配图（section包裹，section内img带style）
2. 声明框（table bg=#f7f7f7 border-left:4px solid #576b95，13px, #555）
3. 声明附注（table bg=#f7f7f7 border-left:4px solid #576b95，14px, #666）
4. 开场白（p 17px rgba(0,0,0,0.9)，margin:20px 0）
5. 分割线（hr gradient，margin:20px 0）
```

### 1.1 封面配图（section包裹img，img带style）

```html
<section style="text-align:center;margin:0 0 10px;">
  <img src="封面图URL" alt="文章标题" style="width:100%;border-radius:8px 8px 0 0;display:block;">
</section>
```

### 1.2 声明框（table结构，13px）

```html
<table style="background:#f7f7f7;border-left:4px solid #576b95;padding:12px 18px;border-spacing:0;margin:20px 0;width:100%;"><tbody><tr><td style="padding:12px 18px;font-size:13px;color:#555;line-height:1.7;font-family:-apple-system,'PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif;">
📖 公众号首发，本文为书籍《AI新时代——当机器人学会分配》第XX篇连载
</td></tr></tbody></table>
```

### 1.3 声明附注（table结构，14px）

```html
<table style="background:#f7f7f7;border-left:4px solid #576b95;padding:12px 18px;border-spacing:0;margin:20px 0;width:100%;"><tbody><tr><td style="padding:12px 18px;font-size:14px;color:#666;line-height:1.7;font-family:-apple-system,'PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif;">
公众号首发 · 正文约XXXX字 · X分钟阅读
</td></tr></tbody></table>
```

### 1.4 开场白

```html
<p style="margin:20px 0;font-size:17px;line-height:1.9;color:rgba(0,0,0,0.9);font-family:-apple-system,'PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif;">
大家好，我是Hugo，数字游民在路上。
</p>
```

### 1.5 分割线

```html
<hr style="border:none;height:1px;background:linear-gradient(to right,transparent,#e0e0e0,transparent);margin:20px 0;">
```

---

## 二、章节标题块（深蓝背景，table结构）

```html
<table style="background:#0d1828;border-radius:8px;padding:0;border-spacing:0;margin:28px 0 18px;width:100%;"><tbody><tr><td style="padding:14px 18px 12px;"><span style="font-size:10px;color:#4a9de8;letter-spacing:3px;display:block;margin-bottom:4px;">ONE</span><span style="font-size:17px;color:#dde8ff;font-weight:700;line-height:1.5;letter-spacing:0.3px;">一、章节标题</span></td></tr></tbody></table>
```

英文序号：ONE / TWO / THREE / FOUR / FIVE / SIX / SEVEN / SUMMARY

---

## 三、正文段落样式（3种）

### 3.1 标准正文段落

```html
<p style="margin:0 0 14px;font-size:15px;line-height:1.9;color:#333333;font-family:-apple-system,'PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif;">
正文内容
</p>
```

### 3.2 强调段落（含strong标签）

```html
<p style="margin:0 0 20px;font-size:15px;line-height:1.9;color:#333;font-family:-apple-system,'PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif;">
<strong>强调内容</strong>
</p>
```

### 3.3 独立强调句（无p包裹）

```html
<p style="margin:0 0 20px;font-size:16px;color:#111;font-weight:700;line-height:1.7;font-family:-apple-system,'PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif;">
AI正在重写组织的底层逻辑。不是慢慢变，是一夜之间。
</p>
```

---

## 四、金句引言（暖色调 blockquote，左侧金色3px边框）

```html
<blockquote style="-webkit-tap-highlight-color:rgba(0,0,0,0);margin:24px 0;padding:18px 22px;outline:0;border-left:3px solid rgb(192,144,96);color:rgb(68,68,68);font-size:16px;max-width:100%;box-sizing:border-box!important;overflow-wrap:break-word!important;font-family:'PingFang SC',system-ui,-apple-system,BlinkMacSystemFont,'Helvetica Neue','Hiragino Sans GB','Microsoft YaHei UI','Microsoft YaHei',Arial,sans-serif;background:rgb(249,246,240);line-height:1.7;">
金句内容
</blockquote>
```

⚠️ 微信编辑器会转换 `<blockquote>` 为带左边框的引用块，背景色 rgb(249,246,240) = #f9f6f0 保留
⚠️ 金句数量：按需添加（一般2~5句），选金句标准：全篇核心观点的高浓度凝练

---

## 五、文中配图规范（统一16:9比例）

### 5.1 插图包裹结构

```html
<section style="text-align:center;margin:20px 0;">
  <img src="配图URL" alt="配图描述" style="width:100%;margin:0;border-radius:6px;">
</section>
```

⚠️ 配图比例：统一16:9（width:100%，高度auto）
⚠️ 配图右下角统一合成CGHub logo（logo高度=图片高度×12%，距边缘20px）
⚠️ 配图存储路径：`docs/04-book-plan/generated-covers/{篇号}-{图描述}.png`

### 5.2 封面配图特殊处理

```html
<section style="text-align:center;margin:0 0 10px;">
  <img src="封面图URL" alt="文章标题" style="width:100%;border-radius:8px 8px 0 0;display:block;">
</section>
```

⚠️ 封面图有特殊的圆角样式（顶部圆角8px），其他配图统一6px圆角

---

## 六、章节结尾分割线

```html
<hr style="border:none;height:1px;background:linear-gradient(to right,transparent,#e0e0e0,transparent);margin:20px 0;">
```

---

## 七、结尾模块标准顺序（连载版）

```
1. 关于本书与连载（table bg=#f7f7f7 border-left:4px solid #576b95）
2. 下篇预告（p 14px #999 text-align:center）
3. 分割线（hr gradient margin:20px 0）
4. 互动话题区块（table渐变蓝底+蓝左边框）
5. 互动引导（p 17px #333 margin:25px 0）
6. 公众号名片（p 14px 居中）
7. 署名（p 12px 居中 #ccc）
```

### 7.1 关于本书与连载

```html
<table style="background:#f7f7f7;border-left:4px solid #576b95;padding:12px 18px;border-spacing:0;margin:20px 0;width:100%;"><tbody><tr><td style="padding:12px 18px;font-size:14px;color:#666;line-height:1.7;font-family:-apple-system,'PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif;">
<p style="margin:0 0 12px;font-size:16px;color:#1e4d7b;font-weight:600;">💫 关于本书与连载</p>
上篇聊了XXX，这篇聊了XXX。<br><br>
如果觉得这篇文章对你有启发，请随手点赞、在看、转发三连。
</td></tr></tbody></table>
```

### 7.2 下篇预告

```html
<p style="font-size:14px;color:#999;text-align:center;margin:20px 0 30px;">
下篇，我们接着聊。
</p>
```

### 7.3 互动话题区块

```html
<section style="margin:28px 0;padding:22px 24px;background:linear-gradient(135deg,#f0f8ff,#e6f7ff);border-left:4px solid #4a9de8;border-radius:8px;">
<p style="margin:0 0 12px;font-size:16px;color:#1e4d7b;font-weight:600;">💫 互动话题</p>
<p style="margin:0 0 12px;font-size:15px;color:#2c5282;line-height:1.7;">互动内容</p>
<p style="margin:0;font-size:15px;color:#2c5282;line-height:1.7;">互动引导</p>
</section>
```

### 7.4 互动引导

```html
<p style="font-size:17px;color:#333;margin:25px 0;line-height:1.7;">
既然看到这里了，欢迎评论区聊聊，若有启发请随手点赞、在看、转发三连。
</p>
```

### 7.5 公众号名片

```html
<p style="font-size:14px;color:#666;text-align:center;margin:15px 0;">
如果这篇文章对你有帮助，欢迎<strong style="color:rgb(6,102,217);">点赞、在看、转发</strong>
</p>
<p style="font-size:14px;color:#666;text-align:center;margin:15px 0;">
「<strong style="color:rgb(6,102,217);">胡戈AI赋能</strong>」，专注AI编程出海、Web3、OPC
</p>
```

### 7.6 署名

```html
<p style="font-size:12px;text-align:center;color:#ccc;margin:15px 0;">
© 胡戈AI赋能 数字游民 新思想探路者 AI独立开发实践者
</p>
```

---

## 八、正文字号规范（V6.0）

| 元素 | 字号 | 颜色 |
|------|------|------|
| 开场白 | 17px | rgba(0,0,0,0.9) |
| 声明框（标签） | 13px | #555 |
| 声明附注 | 14px | #666 |
| 章节序号 | 10px | #4a9de8（letter-spacing:3px） |
| 章节标题 | 17px | #dde8ff（font-weight:700） |
| 标准正文 | 15px | #333333（line-height:1.9） |
| 强调段落 | 16px | #111（font-weight:700） |
| 金句引言 | 16px | rgb(68,68,68) |
| 互动话题标题 | 16px | #1e4d7b（font-weight:600） |
| 互动正文 | 15px | #2c5282（line-height:1.7） |
| 名片 | 14px | #666 |
| 署名 | 12px | #ccc |

---

## 九、创作规范（2026-05-31 更新）

- 每篇提供信息增量，对标书籍独立章节
- 标题不得同质化
- 系统性深入探讨，原创思考
- 调性：积极、破局、希望感。不用"陷阱/坑/锁链/焦虑"
- 引用经典：古代（孔孟老易）+ 当代（纳瓦尔/哈耶克/卢梭）
- 结尾引导关注，回复词："AI创客"
- **内容顶格写，禁止缩进**
- **金句用 blockquote**（微信渲染后保留背景色）
- **彩色背景块用 table**（不能用 div）
- **配图统一16:9比例**

---

*版本：V6.0 · 2026-05-31 · 连载版（以第10篇草稿箱为基准范本）*