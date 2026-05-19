# 创客星球CGHub公众号封面图生成规范

## 尺寸规格
- **比例：** 1280×547（约2.34:1）
- **分辨率：** 72 DPI（适合屏幕显示）
- **文件格式：** PNG（支持透明通道）

## 色彩规范
### 主色调：蓝色系（科技感+专业性）
- **深空黑：** `#0d1828` - 背景主色
- **CGHub蓝：** `#576b95` - 品牌标识色
- **电蓝：** `#4a9de8` - 强调色/标题色
- **青蓝：** `#1e88e5` - 科技主题色
- **蓝紫渐变：** `#576b95` → `#9c27b0` - 社区/共创主题

### 主题变体
1. **钱/分配/财富主题：**
   - 基础色：深空黑 `#0d1828`
   - 强调色：金色 `#ffd700`
   - 点缀：琥珀色 `#ff9800`

2. **科技/AI主题：**
   - 基础色：深空黑 `#0d1828`
   - 主色：电蓝 `#4a9de8`
   - 点缀：青蓝 `#1e88e8` + 白光 `#ffffff`

3. **社区/共创主题：**
   - 基础色：深空黑 `#0d1828`
   - 主色：蓝紫渐变 `#576b95` → `#9c27b0`
   - 点缀：暖紫 `#ba68c8`

4. **变革/突破主题：**
   - 基础色：星空渐变（深空黑 `#0d1828` → 暗蓝 `#283593`)
   - 强调色：火红 `#f44336`
   - 点缀：橙色 `#ff9800`

## 视觉元素规范
### 必须包含元素
1. **CGHub创客星球 Logo：**
   - 位置：右下角（距边缘28px）
   - 大小：高度为封面总高度的14%
   - 文件：`docs/00-brand/cghub-logo-official.png`

2. **标题文字区域：**
   - 位置：中上区域（约60%宽度）
   - 字体风格：现代无衬线，粗细适中
   - 主标题：清晰醒目，不超过12个字
   - 副标题/金句：可选，字号较小

### 视觉风格
- **深空感：** 星空、星云、星座、光晕效果
- **科技感：** 网格、粒子、光点、数据流
- **生命感：** 脉动、呼吸、流动感
- **抽象感：** 避免具体人脸/人物形象

## Prompt模板

### 通用基础模板
```
WeChat public account article cover, 1280×547 ratio (约2.34:1), landscape.
Deep space atmosphere, modern editorial style, clean and professional.
Article title area: "[文章标题]"
Subtitle area: "[副标题或金句]"
Bottom corner: CGHub brand badge area (leave space for logo).
Color palette: [主色系描述].
No faces, no people, no realistic human figures.
```

### 财富/分配主题
```
WeChat public account article cover, 1280×547 ratio (约2.34:1), landscape.
Deep space atmosphere with golden wealth elements, modern editorial style.
Article title area: "[财富相关标题]"
Subtitle area: "[副标题或金句]"
Color palette: Deep space black (#0d1828) background with golden (#ffd700) accent elements and amber (#ff9800) highlights.
Golden particle effects, wealth distribution patterns, blockchain network visualization.
Bottom corner: leave space for CGHub logo.
No faces, abstract representation only.
```

### 科技/AI主题
```
WeChat public account article cover, 1280×547 ratio (约2.34:1), landscape.
Futuristic technology atmosphere, AI network visualization, modern editorial style.
Article title area: "[科技/AI相关标题]"
Subtitle area: "[副标题或金句]"
Color palette: Deep space black (#0d1828) background with electric blue (#4a9de8) main elements, cyan-blue (#1e88e5) accents, and white (#ffffff) light glows.
Neural network patterns, data flow visualization, digital particles.
Bottom corner: leave space for CGHub logo.
No faces, abstract technology representation only.
```

### 社区/共创主题
```
WeChat public account article cover, 1280×547 ratio (约2.34:1), landscape.
Community network atmosphere, modern editorial style with collaborative feel.
Article title area: "[社区/共创相关标题]"
Subtitle area: "[副标题或金句]"
Color palette: Deep space black (#0d1828) background with blue-purple gradient (#576b95 → #9c27b0) main elements and warm purple (#ba68c8) accents.
Network nodes visualization, interconnected community patterns, collaborative energy flows.
Bottom corner: leave space for CGHub logo.
No faces, abstract community representation only.
```

## Logo合成脚本

### Python合成脚本
```python
#!/usr/bin/env python3
"""
微信公众号封面图Logo合成脚本
生成封面图后，自动叠加CGHub logo
"""

import sys
import requests
from PIL import Image
from io import BytesIO

def add_logo_to_cover(cover_image_path, logo_path, output_path):
    """
    将logo添加到封面图
    
    Args:
        cover_image_path: 封面图路径
        logo_path: logo路径
        output_path: 输出路径
    """
    try:
        # 打开封面图
        if cover_image_path.startswith('http'):
            response = requests.get(cover_image_path)
            cover = Image.open(BytesIO(response.content)).convert("RGBA")
        else:
            cover = Image.open(cover_image_path).convert("RGBA")
        
        # 打开logo
        logo = Image.open(logo_path).convert("RGBA")
        
        # 计算logo大小（封面高度的14%）
        cover_w, cover_h = cover.size
        logo_h = int(cover_h * 0.14)
        logo_w = int(logo_h * logo.size[0] / logo.size[1])
        
        # 调整logo大小
        logo_resized = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        
        # 计算位置（右下角，距离边缘28px）
        margin = 28
        x_position = cover_w - logo_w - margin
        y_position = cover_h - logo_h - margin
        
        # 合成图片
        cover.paste(logo_resized, (x_position, y_position), logo_resized)
        
        # 保存为RGB格式（去掉alpha通道）
        cover.convert("RGB").save(output_path, quality=95)
        
        print(f"Logo合成成功：{output_path}")
        return True
        
    except Exception as e:
        print(f"Logo合成失败：{e}")
        return False

def main():
    # 示例使用
    cover_image = input("请输入封面图路径或URL：")
    logo_path = "/home/ubuntu/creators-galaxy/docs/00-brand/cghub-logo-official.png"
    output_path = "cover_with_logo_final.png"
    
    success = add_logo_to_cover(cover_image, logo_path, output_path)
    
    if success:
        print(f"最终封面图已保存到：{output_path}")
        return output_path
    else:
        print("封面图生成失败")
        return None

if __name__ == "__main__":
    main()
```

### 使用指南
1. **生成基础封面图：**
   - 使用AI图像生成工具，输入对应的Prompt模板
   - 保存生成的图片到本地

2. **合成Logo：**
   ```bash
   python3 add_logo.py
   ```
   或直接调用函数：
   ```python
   from cover_generator import add_logo_to_cover
   
   result = add_logo_to_cover(
       "generated_cover.png",
       "/home/ubuntu/creators-galaxy/docs/00-brand/cghub-logo-official.png",
       "final_cover_with_logo.png"
   )
   ```

3. **命名规范：**
   - 基础图：`0X-文章关键词-cover-base.png`
   - 合成图：`0X-文章关键词-cover-final.png`
   - 示例：`07-传统分配-cover-final.png`

## 质量检查清单
- [ ] 尺寸为1280×547像素
- [ ] 清晰度足够（无模糊）
- [ ] 标题文字可读性强
- [ ] 色彩符合主题要求
- [ ] Logo已正确合成
- [ ] 无具体人脸/人物形象
- [ ] 文件名符合命名规范
- [ ] 文件大小适中（200KB-1MB）

## 目录结构
```
docs/04-book-plan/generated-covers/
├── 07-传统分配-cover-base.png    # AI生成的基础图
├── 07-传统分配-cover-final.png   # 合成Logo的最终图
├── add_logo.py                    # Logo合成脚本
└── README.md                      # 本规范文件
```

---
*最后更新：2026-05-19*
*版本：V1.0*