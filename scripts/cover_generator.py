#!/usr/bin/env python3
"""
封面图生成与优化工具
功能：
1. 自动生成1280×547（2.34:1）封面图
2. 标题与封面图同步更新机制
3. 蓝色系科技感模板库
4. CGHub logo自动合成
5. 批量生成封面图功能
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from templates import get_template, TEMPLATE_CONFIGS
from logo_handler import add_cghub_logo

class CoverGenerator:
    """封面图生成器"""
    
    def __init__(self, template_name="tech_blue"):
        """
        初始化封面图生成器
        
        Args:
            template_name: 模板名称，默认为"tech_blue"
        """
        self.template_name = template_name
        self.width = 1280
        self.height = 547
        self.output_dir = Path("output/covers")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 字体路径设置
        self.font_dir = Path("fonts")
        if not self.font_dir.exists():
            self.font_dir.mkdir(parents=True, exist_ok=True)
        
    def generate(self, title, subtitle=None, author=None, date=None, output_path=None):
        """
        生成封面图
        
        Args:
            title: 主标题
            subtitle: 副标题（可选）
            author: 作者/来源（可选）
            date: 日期（可选）
            output_path: 输出路径（可选，默认为自动生成）
            
        Returns:
            生成的封面图文件路径
        """
        # 获取模板配置
        template_config = get_template(self.template_name)
        
        # 创建基础图像
        image = Image.new('RGB', (self.width, self.height), template_config['background_color'])
        
        # 添加背景元素（如果模板有）
        if template_config.get('background_image'):
            bg_image = Image.open(template_config['background_image'])
            bg_image = bg_image.resize((self.width, self.height))
            image = bg_image
        
        # 添加装饰元素
        draw = ImageDraw.Draw(image)
        
        # 添加科技感元素（节点、网格等）
        self.add_tech_elements(draw, template_config)
        
        # 添加标题
        self.add_title(draw, title, template_config)
        
        # 添加副标题（如果有）
        if subtitle:
            self.add_subtitle(draw, subtitle, template_config)
        
        # 添加作者和日期信息
        if author or date:
            self.add_metadata(draw, author, date, template_config)
        
        # 添加CGHub logo
        image = add_cghub_logo(image, template_config)
        
        # 保存图像
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cover_{timestamp}_{title.replace(' ', '_')}.png"
            output_path = self.output_dir / filename
        
        image.save(output_path, quality=95)
        
        print(f"封面图已生成: {output_path}")
        return str(output_path)
    
    def add_tech_elements(self, draw, template_config):
        """添加科技感元素"""
        # 添加网格线
        grid_color = template_config['grid_color']
        grid_spacing = 50
        
        for x in range(0, self.width, grid_spacing):
            draw.line([(x, 0), (x, self.height)], fill=grid_color, width=1)
        
        for y in range(0, self.height, grid_spacing):
            draw.line([(0, y), (self.width, y)], fill=grid_color, width=1)
        
        # 添加三个警示节点（科技感元素）
        node_colors = template_config['node_colors']
        node_positions = [
            (self.width // 4, self.height // 3),
            (self.width // 2, self.height // 2),
            (self.width * 3 // 4, self.height * 2 // 3)
        ]
        
        for i, pos in enumerate(node_positions):
            # 节点外圈
            radius = 40
            draw.ellipse(
                [pos[0] - radius, pos[1] - radius, pos[0] + radius, pos[1] + radius],
                fill=node_colors[i % len(node_colors)],
                outline=template_config['node_outline_color'],
                width=3
            )
            
            # 节点内圈
            inner_radius = 20
            draw.ellipse(
                [pos[0] - inner_radius, pos[1] - inner_radius, 
                 pos[0] + inner_radius, pos[1] + inner_radius],
                fill=template_config['node_center_color'],
                outline=template_config['node_outline_color'],
                width=2
            )
            
            # 添加连接线
            if i < len(node_positions) - 1:
                next_pos = node_positions[i + 1]
                draw.line([pos, next_pos], fill=template_config['connection_color'], width=2)
    
    def add_title(self, draw, title, template_config):
        """添加主标题"""
        try:
            # 尝试加载字体
            font_path = template_config.get('font_path', 'fonts/default.ttf')
            if Path(font_path).exists():
                font = ImageFont.truetype(font_path, template_config['title_font_size'])
            else:
                # 使用默认字体
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # 计算标题位置
        title_color = template_config['title_color']
        title_position = template_config['title_position']
        
        # 如果标题太长，适当缩短
        if len(title) > 30:
            title = title[:27] + "..."
        
        # 绘制标题
        draw.text(
            title_position,
            title,
            fill=title_color,
            font=font,
            stroke_width=2,
            stroke_fill=template_config['title_outline_color']
        )
    
    def add_subtitle(self, draw, subtitle, template_config):
        """添加副标题"""
        try:
            font_path = template_config.get('font_path', 'fonts/default.ttf')
            if Path(font_path).exists():
                font = ImageFont.truetype(font_path, template_config['subtitle_font_size'])
            else:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        subtitle_color = template_config['subtitle_color']
        subtitle_position = template_config['subtitle_position']
        
        draw.text(
            subtitle_position,
            subtitle,
            fill=subtitle_color,
            font=font
        )
    
    def add_metadata(self, draw, author, date, template_config):
        """添加作者和日期信息"""
        try:
            font_path = template_config.get('font_path', 'fonts/default.ttf')
            if Path(font_path).exists():
                font = ImageFont.truetype(font_path, template_config['metadata_font_size'])
            else:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        metadata_color = template_config['metadata_color']
        metadata_position = template_config['metadata_position']
        
        text = ""
        if author:
            text += f"作者: {author}"
        if date:
            if text:
                text += " | "
            text += f"发布日期: {date}"
        
        if text:
            draw.text(
                metadata_position,
                text,
                fill=metadata_color,
                font=font
            )


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='封面图生成工具')
    parser.add_argument('-t', '--title', required=True, help='封面图标题')
    parser.add_argument('-s', '--subtitle', help='副标题')
    parser.add_argument('-a', '--author', help='作者/来源')
    parser.add_argument('-d', '--date', help='日期')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-tm', '--template', default='tech_blue', 
                       help='模板名称 (tech_blue, tech_blue_dark, tech_blue_light)')
    parser.add_argument('-b', '--batch', action='store_true', 
                       help='批量生成模式，从文件读取多个标题')
    parser.add_argument('-f', '--file', help='批量生成使用的文件路径')
    
    args = parser.parse_args()
    
    generator = CoverGenerator(args.template)
    
    if args.batch:
        if not args.file:
            print("批量生成需要指定文件路径 (-f)")
            return
        
        from batch_generator import batch_generate
        batch_generate(args.file, args.template)
    else:
        output_path = generator.generate(
            title=args.title,
            subtitle=args.subtitle,
            author=args.author,
            date=args.date,
            output_path=args.output
        )
        
        print(f"\n封面图生成成功!")
        print(f"文件: {output_path}")
        print(f"尺寸: 1280×547 (2.34:1)")
        print(f"模板: {args.template}")
        

if __name__ == "__main__":
    main()