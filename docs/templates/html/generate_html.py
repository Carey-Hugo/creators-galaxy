"""
微信公众号文章HTML生成脚本
基于520文章样式规范，生成标准化的公众号文章HTML

支持三种主题：
  theme='520'  (默认) — 520深色标准版，对应 docs/templates/html/wechat-article-520-template.html
  theme='default'       — 经典版，对应 wechat-article-template.html
  theme='simple'        — 简洁版
"""

import re
import json
from pathlib import Path
import sys

class WeChatArticleGenerator:
    def __init__(self, theme='520'):
        self.theme = theme
        if theme == '520':
            self.template_path = Path(__file__).parent / "wechat-article-520-template.html"
        else:
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
        html = html.replace("{{连载序号}}", article_data.get("series_num", ""))
        html = html.replace("{{导言/摘要}}", article_data.get("lead", ""))
        html = html.replace("{{发布日期}}", article_data.get("pub_date", ""))
        html = html.replace("{{阅读时间}}", article_data.get("reading_time", "7"))
        html = html.replace("{{正文内容}}", article_data.get("content", ""))
        html = html.replace("{{上篇标题}}", article_data.get("prev_title", ""))
        html = html.replace("{{下篇标题}}", article_data.get("next_title", ""))
        return html

    def markdown_to_520_html(self, markdown_file, output_html_file=None):
        """
        将Markdown文件转换为520深色风格HTML
        直接读取Markdown，解析结构，输出完整HTML
        """
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取元信息
        title = re.search(r'# 【定稿】(.*)', content)
        title = title.group(1).strip() if title else ""
        series_num = re.search(r'连载序号：第(\d+)篇', content)
        series_num = series_num.group(1).zfill(2) if series_num else "00"
        pub_date = re.search(r'发布计划：公众号 (\d{4}-\d{2}-\d{2})', content)
        pub_date = pub_date.group(1) if pub_date else ""
        reading_time = re.search(r'(\d+)分钟阅读', content)
        reading_time = reading_time.group(1) if reading_time else "7"
        lead = re.search(r'^(.+)$', content.split('---')[0].split('\n\n')[1] if '---' in content else content)
        prev_topic = re.search(r'上篇：(.*)', content)
        prev_topic = prev_topic.group(1).strip() if prev_topic else ""
        next_topic = re.search(r'下篇预告：(.*)', content)
        next_topic = next_topic.group(1).strip() if next_topic else ""

        # 提取正文
        body_match = re.search(r'---(.+)$', content, re.DOTALL)
        body = body_match.group(1).strip() if body_match else ""

        # 转换正文内容
        body_html = self._convert_body_to_520_html(body)

        article_data = {
            "title": title,
            "series_num": series_num,
            "lead": self._extract_lead(body),
            "pub_date": self._format_date(pub_date),
            "reading_time": reading_time,
            "content": body_html,
            "prev_title": prev_topic,
            "next_title": next_topic,
        }

        html = self.generate_html(article_data)

        if output_html_file:
            out_path = Path(output_html_file)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"HTML已生成：{out_path}")
        return html

    def _extract_lead(self, body):
        """从正文中提取导言（第一个段落的前半部分）"""
        lines = body.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and '---' not in line:
                # 取第一段的前80字作为lead
                return line[:80] + ('...' if len(line) > 80 else '')
        return ""

    def _format_date(self, date_str):
        """将 2026-05-24 格式化为 2026年5月24日"""
        if not date_str:
            return ""
        parts = date_str.split('-')
        if len(parts) == 3:
            return f"{parts[0]}年{parts[1].lstrip('0')}月{parts[2].lstrip('0')}日"
        return date_str

    def _convert_body_to_520_html(self, body):
        """将Markdown正文转换为520深色HTML"""
        lines = body.split('\n')
        html_parts = []
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            # 跳过空行和元信息行
            if not line or line.startswith('---') or line.startswith('大家好') or \
               '公众号首发' in line or line.startswith('**声明**') or \
               '关于本书' in line or line.startswith('**互动'):
                i += 1
                continue

            # 跳过推荐阅读行（这些会作为书卡组件）
            if line.startswith('推荐阅读：') or line.startswith('【微信小店'):
                i += 1
                continue

            # 主章节标题 ## 一、xxx
            chapter_match = re.match(r'## 一、二、三、四、五、六｜一二三四五六｜章', line)
            chapter_match2 = re.match(r'##\s+([一二三四五六七八九十百\d]+)、\s*(.*)', line)
            if chapter_match2:
                chinese_num = chapter_match2.group(1)
                chapter_title = chapter_match2.group(2).strip()
                en_num = self._chapter_num_to_en(chinese_num)
                html_parts.append(f'''
    <h2>
      <span class="h2-num">{en_num}</span>
      <span class="h2-text">{chapter_title}</span>
      <span class="h2-line"></span>
    </h2>''')
                i += 1
                continue

            # 金句 > 引言块
            if line.startswith('>'):
                quote = line.lstrip('>').strip()
                # 收集多行引言
                j = i + 1
                while j < len(lines) and lines[j].strip().startswith('>'):
                    quote += '<br>' + lines[j].strip().lstrip('>').strip()
                    j += 1
                html_parts.append(f'''
    <div class="pullquote">
      <p>{quote}</p>
    </div>''')
                i = j
                continue

            # 金句标签 **金句X:**
            gold_match = re.match(r'\*\*金句[一二三四五六\d]+：\*\*', line)
            if gold_match:
                i += 1
                continue

            # 普通段落
            if line:
                # 处理加粗 **文字**
                line_html = self._format_paragraph(line)
                html_parts.append(f'    <p>{line_html}</p>')

            i += 1

        return '\n'.join(html_parts)

    def _chapter_num_to_en(self, num):
        mapping = {
            "一": "ONE", "二": "TWO", "三": "THREE", "四": "FOUR",
            "五": "FIVE", "六": "SIX", "七": "SEVEN", "八": "EIGHT",
            "九": "NINE", "十": "TEN", "1": "ONE", "2": "TWO",
            "3": "THREE", "4": "FOUR", "5": "FIVE"
        }
        return mapping.get(str(num).lstrip('零〇'), str(num))

    def _format_paragraph(self, text):
        """将Markdown段落转为HTML，处理加粗"""
        # 处理 **bold**
        parts = re.split(r'\*\*(.*?)\*\*', text)
        result = []
        for idx, part in enumerate(parts):
            if idx % 2 == 1:
                result.append(f'<strong>{part}</strong>')
            else:
                result.append(part)
        return ''.join(result)

    def format_chapter(self, chapter_num, chapter_title, content):
        """格式化章节"""
        chapter_html = f"""
        <div class="chapter-block">
            <div class="chapter-num">{chapter_num}</div>
            <div class="chapter-title">{chapter_title}</div>
        </div>
        """

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
            "land": "#ccc",
            "machine": "#aaa",
            "algorithm": "#576b95"
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
        """从Markdown文件生成HTML（默认主题）"""
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()

        article_data = {
            "title": re.search(r'# 【定稿】(.*)', content).group(1).strip() if re.search(r'# 【定稿】(.*)', content) else "",
            "word_count": re.search(r'正文约(\d+)字', content).group(1) if re.search(r'正文约(\d+)字', content) else "2000",
            "series_num": re.search(r'连载序号：第(\d+)篇', content).group(1) if re.search(r'连载序号：第(\d+)篇', content) else "0",
            "prev_topic": re.search(r'上篇：(.*)', content).group(1).strip() if re.search(r'上篇：(.*)', content) else "",
            "next_preview": re.search(r'下篇预告：(.*)', content).group(1).strip() if re.search(r'下篇预告：(.*)', content) else "",
        }

        article_data["content"] = self.extract_body_content(content)
        return self.generate_html(article_data)

    def extract_body_content(self, markdown_content):
        """从Markdown中提取正文内容并转换为HTML"""
        lines = markdown_content.split('\n')
        body_html = ""

        for line in lines:
            if line.startswith("## "):
                chapter_match = re.match(r'##\s+([一二三四五六七八九十])、\s*(.*)', line)
                if chapter_match:
                    chapter_num = self.chapter_num_to_en(chapter_match.group(1))
                    chapter_title = chapter_match.group(2)
                    body_html += self.format_chapter(chapter_num, chapter_title, "")
                else:
                    title = line.replace("## ", "")
                    body_html += f"<p><strong>{title}</strong></p>\n"

            elif line.startswith("**金句") or line.startswith(">"):
                quote_match = re.match(r'>\s*(.*)', line)
                if quote_match:
                    body_html += self.format_gold_quote(quote_match.group(1))
                else:
                    body_html += f"<p>{line}</p>\n"

            elif line.startswith("- 土地时代") or line.startswith("- 机器时代") or line.startswith("- 算法时代"):
                era_match = re.match(r'-\s+(.*):\s*(.*)', line)
                if era_match:
                    era_name = era_match.group(1)
                    era_content = era_match.group(2)
                    era_type = "land" if "土地" in era_name else "machine" if "机器" in era_name else "algorithm"
                    body_html += self.format_era_card(era_name, era_content, era_type)
                else:
                    body_html += f"<p>{line}</p>\n"

            elif line.strip() and not line.startswith("#") and not line.startswith("---"):
                body_html += f"<p>{line}</p>\n"

        return body_html

    def chapter_num_to_en(self, chinese_num):
        """将中文章节序号转换为英文"""
        mapping = {
            "一": "ONE", "二": "TWO", "三": "THREE", "四": "FOUR",
            "五": "FIVE", "六": "SIX", "七": "SEVEN", "八": "EIGHT",
            "九": "NINE", "十": "TEN"
        }
        return mapping.get(chinese_num, chinese_num)

def main():
    import sys

    if len(sys.argv) < 2:
        # 默认生成周六文章07
        md_file = Path(__file__).parent.parent.parent / "docs/04-book-plan/07-传统分配的三个致命缺陷-定稿.md"
        out_file = Path(__file__).parent / "07-传统分配的三个致命缺陷.html"
    else:
        md_file = Path(sys.argv[1])
        out_file = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).parent / "output.html"

    theme = sys.argv[3] if len(sys.argv) > 3 else '520'

    generator = WeChatArticleGenerator(theme=theme)

    if theme == '520':
        html = generator.markdown_to_520_html(md_file, out_file)
    else:
        html = generator.generate_from_markdown(md_file)
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"HTML文件已生成：{out_file}")

    return html

if __name__ == "__main__":
    main()
