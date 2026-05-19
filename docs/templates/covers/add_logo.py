#!/usr/bin/env python3
"""
微信公众号封面图Logo合成脚本
生成封面图后，自动叠加CGHub logo
"""

import sys
import os
import requests
from io import BytesIO
from pathlib import Path

# 检查PIL依赖
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("❌ PIL (Pillow) 库未安装")
    print("安装方法: pip3 install pillow --break-system-packages")
    print("或: sudo apt-get install python3-pil python3-pil.imagetk")
    sys.exit(1)

class CoverLogoCompositor:
    def __init__(self):
        # 配置文件路径
        self.logo_path = "/home/ubuntu/creators-galaxy/docs/00-brand/cghub-logo-official.png"
        self.covers_dir = "/home/ubuntu/creators-galaxy/docs/04-book-plan/generated-covers"
        
        # 确保目录存在
        os.makedirs(self.covers_dir, exist_ok=True)
    
    def add_logo_to_cover(self, cover_image_path, output_filename=None):
        """
        将logo添加到封面图
        
        Args:
            cover_image_path: 封面图路径或URL
            output_filename: 输出文件名（可选）
            
        Returns:
            输出文件路径或None
        """
        try:
            # 打开封面图
            if cover_image_path.startswith('http'):
                print(f"从URL下载封面图: {cover_image_path}")
                response = requests.get(cover_image_path, timeout=30)
                if response.status_code != 200:
                    print(f"下载失败: HTTP {response.status_code}")
                    return None
                cover = Image.open(BytesIO(response.content)).convert("RGBA")
            else:
                if not os.path.exists(cover_image_path):
                    print(f"文件不存在: {cover_image_path}")
                    return None
                cover = Image.open(cover_image_path).convert("RGBA")
            
            # 验证封面图尺寸
            cover_w, cover_h = cover.size
            expected_ratio = 1280/547  # 约2.34:1
            actual_ratio = cover_w/cover_h
            
            if abs(actual_ratio - expected_ratio) > 0.1:
                print(f"警告：封面图比例异常。期望约2.34:1，实际{cover_w}:{cover_h} ({actual_ratio:.2f}:1)")
                if cover_w < 1000 or cover_h < 400:
                    print("警告：封面图分辨率可能过低")
            
            # 打开logo
            if not os.path.exists(self.logo_path):
                print(f"Logo文件不存在: {self.logo_path}")
                return None
                
            logo = Image.open(self.logo_path).convert("RGBA")
            
            # 计算logo大小（封面高度的14%）
            logo_h = int(cover_h * 0.14)
            logo_w = int(logo_h * logo.size[0] / logo.size[1])
            
            # 调整logo大小
            logo_resized = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
            
            # 计算位置（右下角，距离边缘28px）
            margin = 28
            x_position = cover_w - logo_w - margin
            y_position = cover_h - logo_h - margin
            
            # 确保位置有效
            if x_position < 0:
                x_position = margin
            if y_position < 0:
                y_position = margin
            
            # 合成图片
            cover.paste(logo_resized, (int(x_position), int(y_position)), logo_resized)
            
            # 生成输出文件名
            if output_filename:
                if not output_filename.endswith('.png'):
                    output_filename += '.png'
                output_path = os.path.join(self.covers_dir, output_filename)
            else:
                # 生成默认文件名
                base_name = Path(cover_image_path).stem
                if '_base' in base_name:
                    output_name = base_name.replace('_base', '_final')
                else:
                    output_name = base_name + '_final'
                output_path = os.path.join(self.covers_dir, f"{output_name}.png")
            
            # 保存为RGB格式（去掉alpha通道）
            cover.convert("RGB").save(output_path, quality=95, optimize=True)
            
            print(f"✅ Logo合成成功：{output_path}")
            print(f"   原始尺寸: {cover_w}×{cover_h}")
            print(f"   Logo大小: {logo_w}×{logo_h}")
            print(f"   Logo位置: ({x_position}, {y_position})")
            
            return output_path
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误: {e}")
            return None
        except IOError as e:
            print(f"❌ 文件IO错误: {e}")
            return None
        except Exception as e:
            print(f"❌ 合成失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def process_multiple_covers(self, cover_paths):
        """
        批量处理多个封面图
        
        Args:
            cover_paths: 封面图路径列表
            
        Returns:
            成功处理的数量
        """
        success_count = 0
        total_count = len(cover_paths)
        
        for i, cover_path in enumerate(cover_paths, 1):
            print(f"\n[{i}/{total_count}] 处理: {cover_path}")
            result = self.add_logo_to_cover(cover_path)
            if result:
                success_count += 1
        
        print(f"\n✅ 批量处理完成: {success_count}/{total_count} 成功")
        return success_count
    
    def generate_cover_name(self, article_number, article_keywords):
        """
        生成封面图文件名
        
        Args:
            article_number: 文章序号（如"07"）
            article_keywords: 文章关键词（如"传统分配"）
            
        Returns:
            基础图和最终图的文件名
        """
        base_name = f"{article_number:02d}-{article_keywords}-cover-base.png"
        final_name = f"{article_number:02d}-{article_keywords}-cover-final.png"
        return base_name, final_name

def main():
    """命令行入口"""
    compositor = CoverLogoCompositor()
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 add_logo.py <封面图路径或URL> [输出文件名]")
        print("  python3 add_logo.py --batch <文件1> <文件2> ...")
        print("\n示例:")
        print("  python3 add_logo.py https://example.com/cover.jpg 07-传统分配-cover-final.png")
        print("  python3 add_logo.py cover_base.jpg")
        print("  python3 add_logo.py --batch cover1.jpg cover2.jpg cover3.jpg")
        return
    
    if sys.argv[1] == "--batch":
        if len(sys.argv) < 3:
            print("批量处理需要至少一个文件路径")
            return
        cover_files = sys.argv[2:]
        compositor.process_multiple_covers(cover_files)
    else:
        cover_path = sys.argv[1]
        output_name = sys.argv[2] if len(sys.argv) > 2 else None
        result = compositor.add_logo_to_cover(cover_path, output_name)
        
        if result:
            print(f"\n🎉 封面图已保存到: {result}")
            print(f"   存放目录: {compositor.covers_dir}")
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()