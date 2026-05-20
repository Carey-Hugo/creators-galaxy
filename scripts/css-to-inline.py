#!/usr/bin/env python3
"""
CSS class → inline style converter for WeChat articles.
Reads doocs-md rendered HTML, applies CSS rules as inline styles,
outputs WeChat-compatible HTML.
"""
import re
import sys

# ── CSS变量替换 ──
PRIMARY = "#0F4C81"  # 经典蓝

def resolve_css_var(css_text):
    css_text = css_text.replace("var(--md-primary-color)", PRIMARY)
    css_text = css_text.replace("var(--md-font-family)", "-apple-system, 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', sans-serif")
    css_text = re.sub(r"calc\([^)]+\)", lambda m: str(eval(m.group())), css_text)  # eval simple calcs
    return css_text

# ── base.css 规则 ──
BASE_RULES = {
    "section, container, #output": {
        "font-family": "-apple-system, 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', sans-serif",
        "font-size": "15px",
        "line-height": "1.75",
        "text-align": "left",
        "max-width": "680px",
        "margin": "0 auto",
    },
    "#output > *:first-child": {"margin-top": "0"},
    "p": {
        "font-size": "15px",
        "line-height": "1.9",
        "color": "#333",
        "margin": "0 0 16px 0",
        "font-family": "-apple-system, 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', sans-serif",
    },
    "h1": {
        "font-size": "21px",
        "font-weight": "700",
        "color": "#0F4C81",
        "padding": "8px 16px",
        "border-bottom": "2px solid #0F4C81",
        "margin": "24px 0 16px",
    },
    "h2": {
        "font-size": "18px",
        "font-weight": "700",
        "color": "#0F4C81",
        "background": "#f0f6fc",
        "padding": "10px 16px",
        "border-radius": "8px",
        "margin": "28px 0 16px",
        "border-left": "4px solid #0F4C81",
    },
    "h3": {
        "font-size": "16px",
        "font-weight": "600",
        "color": "#333",
        "border-left": "3px solid #0F4C81",
        "padding-left": "10px",
        "margin": "20px 0 10px",
    },
    "blockquote": {
        "font-style": "italic",
        "padding": "12px 16px 12px 20px",
        "border-left": "4px solid #0F4C81",
        "background": "#f9f6f0",
        "color": "#555",
        "margin": "16px 0",
        "border-radius": "0 6px 6px 0",
    },
    "blockquote p": {
        "font-size": "15px",
        "color": "#555",
        "margin": "0",
    },
    "strong": {
        "font-weight": "700",
        "color": "#111",
    },
    "em": {
        "font-style": "italic",
    },
    "hr": {
        "height": "1px",
        "border": "none",
        "margin": "24px 0",
        "background": "linear-gradient(to right, transparent, #ddd, transparent)",
    },
    "ol": {
        "padding-left": "1.5em",
        "margin": "0 0 16px 0",
    },
    "ul": {
        "padding-left": "1.5em",
        "margin": "0 0 16px 0",
    },
    "li": {
        "margin": "6px 0",
        "font-size": "15px",
        "line-height": "1.8",
        "color": "#333",
    },
    "img": {
        "border-radius": "8px",
        "max-width": "100%",
    },
    "a": {
        "color": "#576b95",
        "text-decoration": "none",
    },
    "table": {
        "border-collapse": "collapse",
        "width": "100%",
        "margin": "16px 0",
    },
    "td": {
        "padding": "8px 12px",
        "border": "1px solid #e0e0e0",
    },
    "thead td": {
        "background": "#0F4C81",
        "color": "#fff",
        "font-weight": "600",
    },
}

# ── 解析CSS文件，提取规则字典 ──
def parse_css_file(path):
    with open(path, encoding="utf-8") as f:
        css = f.read()
    css = resolve_css_var(css)
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    rules = {}
    for m in re.finditer(r'([^{}@]+?)\s*\{([^{}]*)\}', css):
        selector = m.group(1).strip()
        styles = m.group(2).strip()
        if selector and styles:
            for sel in selector.split(','):
                sel = sel.strip()
                sel = re.sub(r':[\w-]+(?::[\w-]+)*$', '', sel)  # 去掉伪类
                if sel:
                    rules[sel] = styles
    return rules

# 加载grace.css
grace_rules = parse_css_file('/home/ubuntu/doocs-md/packages/shared/src/configs/theme-css/grace.css')
base_rules = parse_css_file('/home/ubuntu/doocs-md/packages/shared/src/configs/theme-css/base.css')
all_rules = {**BASE_RULES, **base_rules, **grace_rules}

def css_to_inline_styles(css_str):
    """将CSS字符串转为HTML inline style值"""
    css_str = resolve_css_var(css_str)
    css_str = re.sub(r'/\*.*?\*/', '', css_str, flags=re.DOTALL)
    pairs = []
    for m in re.finditer(r'([\w-]+)\s*:\s*([^;]+);?', css_str):
        prop = m.group(1).strip()
        val = m.group(2).strip()
        if prop and val:
            pairs.append(f"{prop}: {val}")
    return '; '.join(pairs)

def apply_rules_to_element(tag_str, element_html):
    """将CSS规则应用到HTML元素，返回新HTML"""
    # 提取tag名和class
    tag_m = re.match(r'<(\w+)', tag_str)
    if not tag_m:
        return element_html
    tag = tag_m.group(1)
    
    # 找class属性
    class_m = re.search(r'class="([^"]+)"', tag_str)
    id_m = re.search(r'id="([^"]+)"', tag_str)
    
    applied = []
    if class_m:
        for cls in class_m.group(1).split():
            if cls in all_rules:
                applied.append(all_rules[cls])
    if id_m and f"#{id_m.group(1)}" in all_rules:
        applied.append(all_rules[f"#{id_m.group(1)}"])
    if tag in all_rules:
        applied.append(all_rules[tag])
    
    if not applied:
        return element_html
    
    # 合并规则
    combined_css = '; '.join(applied)
    inline = css_to_inline_styles(combined_css)
    
    # 替换或添加style属性
    if re.search(r'style="[^"]*"', element_html):
        new_html = re.sub(r'style="([^"]*)"', lambda m: f'style="{m.group(1)}; {inline}"', element_html)
    else:
        new_html = re.sub(r'(<(?:' + tag + r')[^>]*?)>', rf'\1 style="{inline}">', element_html, count=1)
    
    return new_html

def process_html_element(m):
    full = m.group(0)
    tag_str = m.group(1)
    content = m.group(2) if m.lastindex >= 2 else ''
    
    # 递归处理子内容
    if content:
        content = re.sub(r'<([^!][^>]*)>', lambda sm: process_html_element(sm), content)
    
    # 找对应结束标签
    tag_m = re.match(r'<(\w+)', tag_str)
    if not tag_m:
        return full
    
    tag = tag_m.group(1)
    end_tag = f'</{tag}>'
    
    # 构建完整元素
    inner = tag_str + '>' + content if content else tag_str + '>'
    element_full = inner + end_tag if not content else inner + content + end_tag
    
    # 应用CSS规则
    result = apply_rules_to_element(tag_str, element_full)
    return result

def convert(html_content):
    """处理doocs-md输出的HTML，返回纯inline style的HTML"""
    result = []
    i = 0
    while i < len(html_content):
        if html_content[i:i+4] == '<!--':
            # 跳过HTML注释
            end = html_content.find('-->', i)
            if end != -1:
                i = end + 3
                continue
        if html_content[i] == '<':
            # 找到标签
            if html_content[i:i+4] == '<sec':
                # section标签特殊处理
                end = html_content.find('</section>', i)
                if end != -1:
                    section_html = html_content[i:end+10]
                    # 去掉section标签本身，保留内容
                    inner = re.sub(r'<(/?)section[^>]*>', '', section_html)
                    result.append(inner)
                    i = end + 10
                    continue
            # 普通标签
            m = re.match(r'<([^>]+)(?<!/)>(.*?)(</[^>]+>)?', html_content[i:], re.DOTALL)
            if m:
                tag_str = m.group(1)
                content = m.group(2) if m.lastindex >= 2 else ''
                tag_m = re.match(r'<(\w+)', tag_str)
                if tag_m:
                    tag = tag_m.group(1)
                    # 自闭合标签
                    self_closing = tag in ('img', 'br', 'hr', 'input', 'meta', 'link')
                    
                    if content:
                        processed_content = convert(content)
                        # 找对应结束标签
                        end_tag = f'</{tag}>'
                        end_idx = html_content.find(end_tag, i)
                        if end_idx != -1:
                            # 构建完整标签并处理
                            element_full = html_content[i:end_idx+len(end_tag)]
                            processed = apply_rules_to_element(tag_str, element_full)
                            result.append(processed)
                            i = end_idx + len(end_tag)
                            continue
                    elif self_closing:
                        processed = apply_rules_to_element(tag_str, '<' + tag_str + '>')
                        result.append(processed)
                        i += len(tag_str) + 2
                        continue
        
        # 普通文本
        result.append(html_content[i])
        i += 1
    
    return ''.join(result)

# ── 读取并处理 ──
input_html = sys.argv[1] if len(sys.argv) > 1 else '/home/ubuntu/creators-galaxy/docs/04-book-plan/theme-previews/07-grace-经典蓝.html'

with open(input_html, encoding="utf-8") as f:
    source = f.read()

# 提取body
body_m = re.search(r'<body[^>]*>(.*?)</body>', source, re.DOTALL)
body_html = body_m.group(1).strip() if body_m else ''

# 去掉外层<section class="container...">
body_html = re.sub(r'<section\s+class="[^"]*">', '', body_html)
body_html = re.sub(r'</section>', '', body_html)

# 去掉所有 class= 和 id= 属性（用于显示，实际会删掉）
# 先处理每个标签的style
def process_element(m):
    full = m.group(0)
    open_tag = m.group(1)
    inner = m.group(2) if m.lastindex >= 2 else ''
    close_tag = m.group(3) if m.lastindex >= 3 else ''
    
    tag_m = re.match(r'(\w+)', open_tag)
    if not tag_m:
        return full
    tag = tag_m.group(1)
    
    # 自闭合
    self_closing = tag in ('img', 'br', 'hr', 'input', 'meta', 'link')
    if self_closing:
        processed = apply_styles_to_open_tag(open_tag, '<' + open_tag + '>')
        return '<' + processed + '>'
    
    # 处理内容（递归）
    processed_inner = re.sub(r'<([^!][^>]*)>(.*?)</[^>]+>',
                              lambda sm: process_element(sm), inner, flags=re.DOTALL)
    
    end_tag = f'</{tag}>'
    full_element = f'<{open_tag}>{processed_inner}{end_tag}'
    processed = apply_styles_to_open_tag(open_tag, full_element)
    return processed

def apply_styles_to_open_tag(tag_str, element_html):
    """将CSS规则应用到开标签"""
    tag_m = re.match(r'(\w+)', tag_str)
    if not tag_m:
        return element_html
    tag = tag_m.group(1)
    
    class_m = re.search(r'class="([^"]+)"', tag_str)
    id_m = re.search(r'id="([^"]+)"', tag_str)
    
    applied_css = []
    if class_m:
        for cls in class_m.group(1).split():
            if cls in all_rules:
                applied_css.append(all_rules[cls])
    if id_m:
        id_key = f"#{id_m.group(1)}"
        if id_key in all_rules:
            applied_css.append(all_rules[id_key])
    if tag in all_rules:
        applied_css.append(all_rules[tag])
    
    if not applied_css:
        return element_html
    
    combined = '; '.join(applied_css)
    inline = css_to_inline_styles(combined)
    
    # 在开标签中添加/更新style
    if 'style="' in element_html:
        new = re.sub(r'style="([^"]*)"', f'style="\\1; {inline}"', element_html)
    else:
        new = re.sub(r'<((\w+)([^>]*?)?)(>)', f'<\\1 style="{inline}">', element_html, count=1)
    return new

# 逐标签处理
def process_html(html):
    """处理HTML字符串，为每个带class/id的标签应用inline样式"""
    # 去掉<!--注释-->
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    # 去掉<style>块
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    
    # 找到所有标签
    result = []
    pos = 0
    while pos < len(html):
        if html[pos] == '<':
            # 判断是否是注释
            if html[pos:pos+4] == '<!--':
                end = html.find('-->', pos)
                if end != -1:
                    pos = end + 3
                    continue
            # 找标签
            tag_end = html.find('>', pos)
            if tag_end == -1:
                result.append(html[pos])
                pos += 1
                continue
            open_tag = html[pos+1:tag_end]
            self_close = open_tag.endswith('/')
            if self_close:
                open_tag = open_tag[:-1].strip()
            
            # 跳过结束标签
            if open_tag.startswith('/'):
                result.append(html[pos:tag_end+1])
                pos = tag_end + 1
                continue
            # 自闭合标签
            if open_tag.startswith('!') or any(open_tag.startswith(x) for x in ['meta','link','br','hr','img','input']):
                processed = apply_styles_to_open_tag(open_tag, '<' + open_tag + '>')
                result.append('<' + processed + '>')
                pos = tag_end + 1
                continue
            
            tag_m = re.match(r'(\w+)', open_tag)
            tag = tag_m.group(1) if tag_m else open_tag
            
            # 找结束标签
            end_tag = f'</{tag}>'
            content_start = tag_end + 1
            content_end = html.find(end_tag, content_start)
            
            if content_end == -1:
                processed = apply_styles_to_open_tag(open_tag, '<' + open_tag + '>')
                result.append('<' + processed + '>')
                pos = tag_end + 1
                continue
            
            # 提取内容并递归处理
            raw_content = html[content_start:content_end]
            processed_content = process_html(raw_content)
            full_element = f'<{open_tag}>{processed_content}{end_tag}'
            processed = apply_styles_to_open_tag(open_tag, full_element)
            result.append(processed)
            pos = content_end + len(end_tag)
        else:
            result.append(html[pos])
            pos += 1
    
    return ''.join(result)

converted = process_html(body_html)

# 输出
output_path = '/home/ubuntu/creators-galaxy/docs/04-book-plan/07-公众号文章-inline排版.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(converted)
print(f"✅ 生成: {output_path} ({len(converted)} chars)")
