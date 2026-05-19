# 创客星球CGHub公众号连载模板库系统

## 概述

本模板库系统为CGHub公众号连载提供完整的标准化工作流，包含HTML模板、封面图模板、内容框架模板和API工作流模板，避免重复走弯路。

## 目录结构

```
docs/templates/
├── html/                          # HTML模板库
│   ├── wechat-article-template.html      # 标准HTML模板
│   ├── generate_html.py                   # HTML生成脚本
│   └── README.md                          # HTML模板使用指南
│
├── covers/                         # 封面图模板
│   ├── cover-generation-spec.md           # 封面图生成规范
│   ├── add_logo.py                        # Logo合成脚本
│   └── README.md                          # 封面图使用指南
│
├── frameworks/                     # 内容框架模板
│   ├── article-structure-template.md      # 文章结构模板
│   ├── opening-examples.md                # 开场示例库
│   ├── chapter-examples.md                # 章节示例库
│   ├── quote-library.md                   # 引用库
│   ├── era-card-templates.md              # 时代卡片模板
│   ├── gold-quote-templates.md            # 金句模板
│   └── checklist.md                       # 质量检查清单
│
└── api-workflow/                   # API工作流模板
    ├── wechat_publisher.py                # 完整的推送脚本
    ├── api-workflow-spec.md               # API工作流规范
    ├── troubleshooting-guide.md           # 故障排查指南
    ├── ip-whitelist-instructions.md      # IP白名单设置指南
    ├── html-cleanup-script.py            # HTML清理脚本
    ├── logo-sync-guidelines.md           # Logo同步指南
    └── git-commit-template.md            # Git提交模板
```

## 核心功能

### 1. HTML模板库
- **标准化排版**：基于520文章样式规范
- **自动生成**：从Markdown自动生成HTML
- **样式一致**：确保每篇连载排版统一
- **响应式设计**：适配移动端阅读

### 2. 封面图模板
- **标准尺寸**：1280×547（约2.34:1）
- **品牌规范**：CGHub蓝色系 + Logo合成
- **主题变体**：财富/科技/社区/变革主题
- **自动合成**：自动叠加Logo到右下角

### 3. 内容框架模板
- **结构标准**：2000-3000字标准结构
- **文风规范**：Carey Hugo风格指南
- **引用体系**：古代经典 + 当代思想家 + 经济学理论
- **质量检查**：完整的内容检查清单

### 4. API工作流模板
- **完整推送**：从HTML到草稿箱的完整流程
- **故障排查**：常见错误解决方案
- **自动化脚本**：一键推送 + 自动清理
- **错误预防**：中文转义、控制字符处理

## 快速开始

### 1. 生成HTML文章
```bash
cd ~/creators-galaxy
python3 docs/templates/html/generate_html.py
```

### 2. 生成封面图
```bash
# 使用AI图像生成工具生成基础图
# 然后合成Logo
python3 docs/templates/covers/add_logo.py 封面图.jpg
```

### 3. 推送公众号
```bash
python3 docs/templates/api-workflow/wechat_publisher.py \
  "文章标题" \
  "文章HTML.html" \
  "封面图.png"
```

## 工作流指南

### 周三/周六发布流程
1. **选题阶段**：参考 `frameworks/opening-examples.md`
2. **写作阶段**：参考 `frameworks/article-structure-template.md`
3. **引用阶段**：参考 `frameworks/quote-library.md`
4. **检查阶段**：使用 `frameworks/checklist.md`
5. **HTML生成**：使用 `html/generate_html.py`
6. **封面生成**：使用 `covers/add_logo.py`
7. **质量检查**：使用 `frameworks/checklist.md`
8. **API推送**：使用 `api-workflow/wechat_publisher.py`
9. **Git归档**：使用标准提交模板

### 故障排查流程
1. **文章不在草稿箱？**
   - 运行 `python3 wechat_publisher.py --test`
   - 检查 `troubleshooting-guide.md`
   - 验证IP白名单 `43.130.52.123`

2. **排版不一致？**
   - 获取520文章的完整HTML源码
   - 100%复制其样式，不自作主张优化
   - 使用 `html/generate_html.py` 重新生成

3. **封面图错误？**
   - 确认尺寸为1280×547
   - 确认已合成Logo
   - 重新生成并上传

## 关键配置

### 微信公众号凭证
```
AppID: wx34cf0b6a53435a05
AppSecret: 6058c6ecdced8df42af3a3356eb045b7
IP白名单: 43.130.52.123
```

### Logo文件路径
```
docs/00-brand/cghub-logo-official.png
```

### 封面图存放路径
```
docs/04-book-plan/generated-covers/
```

## 引用管理

### 古代经典
- **孔子、孟子、韩非子**：中国哲学
- **柏拉图、亚里士多德**：西方哲学
- **马克思、福柯、韦伯**：现代思想

### 当代思想家
- **纳瓦尔**：杠杆理论（劳动力、资本、代码）
- **赫拉利**：数据主义、未来简史
- **凯文·凯利**：科技进化
- **刘慈欣**：科幻社会学
- **马斯克**：第一性原理

### 经济学理论
- **阿克洛夫**：信息不对称理论
- **亚当斯密**：分工理论
- **李嘉图**：比较优势理论

## 质量保证

### 内容检查清单
- [ ] 字数2000-3000字（不含尾部）
- [ ] 至少三个章节（ONE/TWO/THREE）
- [ ] 每个章节有具体案例支撑
- [ ] 引用适当且合理
- [ ] 没有重复人物
- [ ] 兑现上篇预告内容

### 文风检查清单
- [ ] 短句为主（一句一行）
- [ ] 口语化表达
- [ ] 具体故事开场
- [ ] 去AI味（无机械过渡词）
- [ ] 段落间距用空行
- [ ] 传递希望感

### 技术检查清单
- [ ] HTML格式正确
- [ ] 封面图1280×547
- [ ] Logo已正确合成
- [ ] API凭证有效
- [ ] IP白名单已设置

## 版本历史

### V1.0 (2026-05-19)
- 基于520文章样式规范建立完整模板系统
- 包含HTML模板、封面图模板、内容框架、API工作流
- 集成故障排查和优化方案
- 标准化引用体系和质量检查清单

### 未来计划
- 自动化封面图生成（集成AI图像生成）
- 智能引用推荐系统
- 实时排版预览
- 多平台发布支持

## 贡献指南

1. **添加新模板**：在对应目录创建文件
2. **更新规范**：修改相关文档并更新版本号
3. **修复错误**：提交PR并说明修复内容
4. **添加功能**：确保向后兼容

## 许可证

本项目遵循MIT许可证。详见LICENSE文件。

---
*创客星球CGHub公众号连载模板库系统*
*最后更新：2026-05-19*