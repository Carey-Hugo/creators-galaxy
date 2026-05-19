#!/usr/bin/env python3
"""
微信公众号文章HTML生成脚本
基于520文章样式规范，生成标准化的公众号文章HTML
"""

import re
import json
from pathlib import Path
import sys

class WeChatArticleGenerator:
    def __init__(self):
        self.template_path = Path(__file__).parent / "wechat-article-template.html"
        self.styles = {
            "paragraph": {
                "font-size": "15px",
                "color": "#333",
                "line-height": "1.9",
                "text-align": "justify",
                "margin-bottom": "14px"
            },
            "chapter_block": {
                "background": "#0d1828",
                "border-radius": "8px",
                "padding": "16px 20px",
                "margin": "20px 0 18px"
            },
            "chapter_num": {
                "font-size": "10px",
                "color": "#576b95",
                "letter-spacing": "3px",
                "text-transform": "uppercase",
                "margin-bottom": "6px"
            },
            "chapter_title": {
                "font-size": "18px",
                "color": "#ffffff",
                "font-weight": "700",
                "line-height": "1.4"
            },
            "series_tag": {
                "margin": "14px 0",
                "padding": "14px 18px",
                "border-left": "4px solid rgb(87, 107, 149)",
                "background": "rgb(247, 247, 247)",
                "font-size": "15px",
                "font-style": "italic"
            },
            "gold_quote": {
                "background": "#f9f6f0",
                "border-left": "3px solid #c09060",
                "font-size": "16px",
                "color": "#444",
                "padding": "18px 22px",
                "margin": "20px 0"
            }
        }
    
    def generate_html(self, article_data):
        """根据文章数据生成HTML"""
        with open(self.template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # 替换模板变量
        html = template.replace("{{文章标题}}", article_data.get("title", ""))
        html = html.replace("{{字数}}", article_data.get("word_count", "2000"))
        html = html.replace("{{阅读时间}}", article_data.get("reading_time", "7"))
        html = html.replace("{{连载序号}}", article_data.get("series_num", "0"))
        html = html.replace("{{正文内容}}", article_data.get("content", ""))
        html = html.replace("{{推荐书籍}}", article_data.get("recommend_book", ""))
        html = html.replace("{{推荐理由}}", article_data.get("recommend_reason", ""))
        html = html.replace("{{购买链接}}", article_data.get("buy_link", "待上架后插入"))
        html = html.replace("{{结尾问句}}", article_data.get("closing_question", ""))
        html = html.replace("{{下篇预告}}", article_data.get("next_preview", ""))
        html = html.replace("{{上篇主题}}", article_data.get("prev_topic", ""))
        html = html.replace("{{本篇主题}}", article_data.get("current_topic", ""))
        
        return html
    
    def format_chapter(self, chapter_num, chapter_title, content):
        """格式化章节"""
        chapter_html = f"""
        <div class="chapter-block">
            <div class="chapter-num">{chapter_num}</div>
            <div class="chapter-title">{chapter_title}</div>
        </div>
        """
        
        # 添加内容段落
        if isinstance(content, list):
            paragraphs = "\n".join([f"<p>{para}</p>" for para in content])
        else:
            paragraphs = f"<p>{content}</p>"
        
        return chapter_html + paragraphs
    
    def format_gold_quote(self, quote_text):
        """格式化金句引言"""
        return f"""
        <div class="gold-quote">
            <p>{quote_text}</p>
        </div>
        """
    
    def format_era_card(self, era_name, era_content, era_type="normal"):
        """格式化时代卡片"""
        color_map = {
            "land": "#ccc",      # 土地时代
            "machine": "#aaa",    # 机器时代
            "algorithm": "#576b95"  # 算法时代（CGHub蓝）
        }
        
        border_color = color_map.get(era_type, "#576b95")
        background = "#f0f5ff" if era_type == "algorithm" else "#f7f8fa"
        
        return f"""
        <div class="era-card" style="background:{background};border-left:3px solid {border_color};">
            <p><strong>{era_name}</strong></p>
            <p>{era_content}</p>
        </div>
        """
    
    def generate_from_markdown(self, markdown_file):
        """从Markdown文件生成HTML"""
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取基本信息
        article_data = {
            "title": re.search(r'# 【定稿】(.*)', content).group(1).strip() if re.search(r'# 【定稿】(.*)', content) else "",
            "word_count": re.search(r'正文约(\d+)字', content).group(1) if re.search(r'正文约(\d+)字', content) else "2000",
            "series_num": re.search(r'连载序号：第(\d+)篇', content).group(1) if re.search(r'连载序号：第(\d+)篇', content) else "0",
            "prev_topic": re.search(r'上篇：(.*)', content).group(1).strip() if re.search(r'上篇：(.*)', content) else "",
            "next_preview": re.search(r'下篇预告：(.*)', content).group(1).strip() if re.search(r'下篇预告：(.*)', content) else "",
        }
        
        # 提取正文内容
        article_data["content"] = self.extract_body_content(content)
        
        return self.generate_html(article_data)
    
    def extract_body_content(self, markdown_content):
        """从Markdown中提取正文内容并转换为HTML"""
        lines = markdown_content.split('\n')
        body_html = ""
        
        for line in lines:
            # 处理章节标题
            if line.startswith("## "):
                chapter_match = re.match(r'##\s+([一二三四五六七八九十])、\s*(.*)', line)
                if chapter_match:
                    chapter_num = self.chapter_num_to_en(chapter_match.group(1))
                    chapter_title = chapter_match.group(2)
                    body_html += self.format_chapter(chapter_num, chapter_title, "")
                else:
                    # 处理其他标题格式
                    title = line.replace("## ", "")
                    body_html += f"<p><strong>{title}</strong></p>\n"
            
            # 处理金句引言
            elif line.startswith("**金句") or line.startswith(">"):
                quote_match = re.match(r'>\s*(.*)', line)
                if quote_match:
                    body_html += self.format_gold_quote(quote_match.group(1))
                else:
                    body_html += f"<p>{line}</p>\n"
            
            # 处理时代卡片
            elif line.startswith("- 土地时代") or line.startswith("- 机器时代") or line.startswith("- 算法时代"):
                era_match = re.match(r'-\s+(.*):\s*(.*)', line)
                if era_match:
                    era_name = era_match.group(1)
                    era_content = era_match.group(2)
                    era_type = "land" if "土地" in era_name else "machine" if "机器" in era_name else "algorithm"
                    body_html += self.format_era_card(era_name, era_content, era_type)
                else:
                    body_html += f"<p>{line}</p>\n"
            
            # 处理普通段落
            elif line.strip() and not line.startswith("#") and not line.startswith("---"):
                body_html += f"<p>{line}</p>\n"
        
        return body_html
    
    def chapter_num_to_en(self, chinese_num):
        """将中文章节序号转换为英文"""
        mapping = {
            "一": "ONE",
            "二": "TWO", 
            "三": "THREE",
            "四": "FOUR",
            "五": "FIVE",
            "六": "SIX",
            "七": "SEVEN",
            "八": "EIGHT",
            "九": "NINE",
            "十": "TEN"
        }
        return mapping.get(chinese_num, chinese_num)

def main():
    generator = WeChatArticleGenerator()
    
    # 测试数据
    test_data = {
        "title": "不透明、中心化、可篡改：AI时代如何破局？",
        "word_count": "2500",
        "reading_time": "7",
        "series_num": "07",
        "content": """
            <p>上周，一个做外卖的朋友跟我说，他跑了三年，收入从八千降到五千。</p>
            <p>我问平台，为什么？</p>
            <p>平台说：“算法动态调整。”</p>
            <p>我问他：你知道算法里有多少个变量吗？</p>
            <p>他摇头。</p>
            <p>我说：这不是你的错，这是第一个坑——<strong>不透明</strong>。</p>
            <p>但好消息是，这个坑，现在有办法填了。</p>
        """,
        "recommend_book": "《信息不对称与市场失灵》",
        "recommend_reason": "这本书详细阐述了信息垄断如何扭曲市场，值得深思。",
        "closing_question": "创客星球CGHub新LOGO已定稿，欢迎鉴赏点评",
        "next_preview": "区块链如何用代码重构分配规则",
        "prev_topic": "AI时代三种杠杆，普通人如何拿到",
        "current_topic": "传统分配的三个致命缺陷"
    }
    
    html = generator.generate_html(test_data)
    
    # 保存HTML文件
    output_path = Path(__file__).parent / "test-output.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML文件已生成：{output_path}")
    return html

if __name__ == "__main__":
    main()