# 创客星球CGHub模板库系统安装指南

## 系统要求
- Python 3.8+
- Git
- 微信公众号AppID和AppSecret

## 安装步骤

### 1. 安装Python依赖
```bash
# 安装Pillow用于Logo合成
pip3 install pillow --break-system-packages

# 安装requests用于API调用
pip3 install requests --break-system-packages
```

### 2. 验证安装
```bash
# 验证Pillow安装
python3 -c "from PIL import Image; print('✅ Pillow安装成功')"

# 验证requests安装
python3 -c "import requests; print('✅ requests安装成功')"
```

### 3. 配置微信公众号凭证
```bash
# 确认AppID和AppSecret
echo "AppID: wx34cf0b6a53435a05"
echo "AppSecret: 6058c6ecdced8df42af3a3356eb045b7"
echo "IP白名单: 43.130.52.123"
```

### 4. 测试模板系统
```bash
cd ~/creators-galaxy
python3 docs/templates/test_template_system.py
```

## 模板使用指南

### HTML模板使用
```bash
# 生成测试HTML
cd ~/creators-galaxy/docs/templates/html
python3 generate_html.py

# 输出文件: test-output.html
```

### 封面图Logo合成
```bash
# 安装Pillow依赖
pip3 install pillow --break-system-packages

# 合成Logo到封面图
cd ~/creators-galaxy/docs/templates/covers
python3 add_logo.py 封面图.jpg

# 或指定输出文件名
python3 add_logo.py 封面图.jpg 07-传统分配-cover-final.png
```

### 公众号推送测试
```bash
# 测试API连接
cd ~/creators-galaxy/docs/templates/api-workflow
python3 wechat_publisher.py --test

# 如果显示"invalid ip"，需要添加IP白名单
# 公众号后台 → 设置与开发 → 基本配置 → IP白名单 → 添加 43.130.52.123
```

## 完整工作流示例

### 步骤1: 创建文章
```bash
# 1. 编写Markdown文章
vim docs/04-book-plan/08-文章标题-定稿.md

# 2. 生成HTML
cd ~/creators-galaxy/docs/templates/html
python3 generate_html.py

# 3. 检查HTML输出
open test-output.html
```

### 步骤2: 创建封面图
```bash
# 1. 使用AI图像生成工具生成封面图
# 2. 合成Logo
cd ~/creators-galaxy/docs/templates/covers
python3 add_logo.py generated_cover.png

# 3. 最终封面图保存到
# docs/04-book-plan/generated-covers/08-文章关键词-cover-final.png
```

### 步骤3: 推送公众号
```bash
cd ~/creators-galaxy/docs/templates/api-workflow

# 推送文章
python3 wechat_publisher.py \
  "文章标题" \
  "../html/test-output.html" \
  "../../04-book-plan/generated-covers/08-文章关键词-cover-final.png"
```

### 步骤4: Git归档
```bash
cd ~/creators-galaxy
git add -A
git commit -m "feat: 第08篇公众号定稿-[文章主题]-[关键词]"
git push origin main
```

## 故障排除

### PIL安装失败
```bash
# 如果pip安装失败，尝试以下方法
sudo apt-get update
sudo apt-get install python3-pil python3-pil.imagetk
```

### API连接失败
```bash
# 检查IP白名单
python3 wechat_publisher.py --test

# 如果返回"invalid ip"
echo "需要添加IP白名单: 43.130.52.123"
echo "操作路径: 公众号后台 → 设置与开发 → 基本配置 → IP白名单"
```

### HTML生成问题
```bash
# 检查Python版本
python3 --version

# 检查文件权限
chmod +x docs/templates/html/generate_html.py
```

## 目录结构说明

```
docs/templates/
├── html/                          # HTML模板库
│   ├── wechat-article-template.html      # 标准HTML模板
│   ├── generate_html.py                   # HTML生成脚本
│   └── README.md                          # HTML模板使用指南
│
├── covers/                         # 封面图模板
│   ├── cover-generation-spec.md           # 封面图生成规范
│   ├── add_logo.py                        # Logo合成脚本（需要Pillow）
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
    ├── wechat_publisher.py                # 完整的推送脚本（需要requests）
    ├── api-workflow-spec.md               # API工作流规范
    ├── troubleshooting-guide.md           # 故障排查指南
    ├── ip-whitelist-instructions.md      # IP白名单设置指南
    ├── html-cleanup-script.py            # HTML清理脚本
    ├── logo-sync-guidelines.md           # Logo同步指南
    └── git-commit-template.md            # Git提交模板
```

## 更新日志

### V1.0 (2026-05-19)
- 初始版本发布
- 包含完整的HTML模板、封面图模板、内容框架、API工作流
- 基于520文章样式规范
- 集成故障排查和优化方案

### 已知问题
1. Logo合成器需要Pillow库
2. 公众号推送需要IP白名单设置
3. HTML清理需要确保中文不转义

## 技术支持

### 常见问题
1. **Q: Pillow安装失败**
   A: 使用 `pip3 install pillow --break-system-packages`

2. **Q: API返回"invalid ip"**
   A: 添加IP白名单 `43.130.52.123`

3. **Q: 封面图尺寸不对**
   A: 确保为1280×547（约2.34:1）

4. **Q: HTML排版不一致**
   A: 100%复制520文章样式，不自作主张优化

### 联系信息
- 仓库: ~/creators-galaxy
- 文档: docs/templates/README.md
- 测试: docs/templates/test_template_system.py

---
*最后更新: 2026-05-19*
*版本: V1.0*