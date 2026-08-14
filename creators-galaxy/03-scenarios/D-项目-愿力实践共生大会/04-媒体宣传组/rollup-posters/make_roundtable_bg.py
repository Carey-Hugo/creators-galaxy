#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""圆桌沙龙 LED 投屏背景图合成 — 与柔和版主画面同风格(深蓝暖金·曙光之路)"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np

W, H = 3840, 1440

# 字体
LXGW_B = '/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Bold.ttf'
LXGW_R = '/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Regular.ttf'
NOTO_B = '/home/ubuntu/.fonts/NotoSansCJKsc-Bold.otf'
NOTO_R = '/home/ubuntu/.fonts/NotoSansCJKsc-Regular.otf'

# 色板（对齐柔和版主画面）
GOLD      = (255, 223, 122)   # 亮金
GOLD_DEEP = (234, 161, 53)    # 深金
GOLD_DIM  = (217, 179, 106)   # 暗金
WHITE_W   = (245, 240, 230)   # 暖白
BLUE_SOFT = (201, 214, 240)   # 柔蓝(备用)

def font(path, size):
    return ImageFont.truetype(path, size)

def draw_center(dr, cx, y, text, fnt, fill):
    w = dr.textlength(text, font=fnt)
    dr.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w

def wrap_center(dr, cx, y, text, fnt, fill, max_w, lh):
    """支持多行: 先按\n拆, 每行内按 max_w 换行, 整体居中"""
    lines = []
    for seg in text.split('\n'):
        cur = ''
        for ch in seg:
            if dr.textlength(cur + ch, font=fnt) <= max_w:
                cur += ch
            else:
                lines.append(cur)
                cur = ch
        if cur:
            lines.append(cur)
    for i, ln in enumerate(lines):
        w = dr.textlength(ln, font=fnt)
        dr.text((cx - w / 2, y + i * lh), ln, font=fnt, fill=fill)
    return len(lines)

def main():
    base = Image.open('/tmp/roundtable_bg.png').convert('RGB')
    # 2x LANCZOS 放大到 3840x1440
    base = base.resize((W, H), Image.LANCZOS)
    # 轻微增饱和 + 对比(更接近主画面质感)
    base = ImageEnhance.Color(base).enhance(1.06)
    base = ImageEnhance.Contrast(base).enhance(1.04)
    base = base.convert('RGBA')

    # 底部与标题区轻微暗化渐变(保证文字可读,alpha 柔和)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    arr = np.zeros((H, W, 4), dtype=np.uint8)
    # 上半(标题区)很轻的暗: 从 0 -> 35
    for y in range(0, H // 2):
        a = int(35 * (1 - y / (H // 2)) * 0.6)
        arr[y, :, 3] = a
    # 下半(嘉宾区)暗: 0 -> 60
    for y in range(H // 2, H):
        a = int(60 * ((y - H // 2) / (H // 2)))
        arr[y, :, 3] = a
    overlay = Image.fromarray(arr)
    base = Image.alpha_composite(base, overlay)

    dr = ImageDraw.Draw(base)

    # ── 1. 左上角「圆桌论坛」标签 ──
    tag_x, tag_y = 130, 118
    f_tag = font(LXGW_B, 60)
    tag_w = dr.textlength('圆桌论坛', font=f_tag)
    # 左侧短竖线 + 文字 + 右侧延伸横线
    dr.line([(tag_x, tag_y - 18), (tag_x, tag_y + 78)], fill=GOLD_DEEP + (230,), width=5)
    dr.text((tag_x + 42, tag_y), '圆桌论坛', font=f_tag, fill=GOLD)
    line_x = tag_x + 42 + tag_w + 42
    dr.line([(line_x, tag_y + 30), (line_x + 260, tag_y + 30)], fill=GOLD_DEEP + (200,), width=4)

    # ── 2. 中上主标题(两行) ──
    f_title = font(LXGW_B, 128)
    f_title2 = font(LXGW_B, 112)
    cx = W // 2
    # 标题上方细金线
    dr.line([(cx - 420, 356), (cx + 420, 356)], fill=GOLD_DEEP + (190,), width=4)
    draw_center(dr, cx, 396, 'AI重构能力之后，', f_title, GOLD)
    draw_center(dr, cx, 560, '什么是真正稀缺的？', f_title2, GOLD)
    # 标题下方短金线
    dr.line([(cx - 260, 726), (cx + 260, 726)], fill=GOLD_DEEP + (190,), width=3)

    # ── 3. 嘉宾四列(名字 + 短金线 + 简介) ──
    guests = [
        ('保哥', [
            '资深资本财务顾问',
            '美股港股IPO · 跨境税务架构设计',
            '曾任多家港股主板公司财务负责人']),
        ('陆鸿', [
            '感动中国年度人物',
            '苏州市吴江区残联副主席',
            '苏州缘跃纸制品有限公司主理人']),
        ('望舒', [
            '曾任某集团公司人力资源总',
            '曾任某集团公司战略部负责人',
            '某集团一级公司一号位']),
        ('林俊廷', [
            '新媒体艺术家 · 数字活化中国古典美学',
            '策展人与艺术总监 · 四川美术学院特聘教授',
            '光影“造梦”者 · 沉浸式互动艺术体验']),
    ]
    n = len(guests)
    col_w = W // n
    name_y = 800
    f_name = font(LXGW_B, 76)
    f_bio = font(NOTO_R, 40)
    bio_lh = 60
    for i, (name, bios) in enumerate(guests):
        cxc = col_w * i + col_w // 2
        # 名字(带微弱投影增加层次)
        draw_center(dr, cxc, name_y, name, f_name, GOLD)
        # 名字下短金线
        line_w = 150
        dr.line([(cxc - line_w // 2, name_y + 108), (cxc + line_w // 2, name_y + 108)],
                fill=GOLD_DEEP + (210,), width=3)
        # 简介(最多3行,居中)
        bio_y = name_y + 150
        nlines = wrap_center(dr, cxc, bio_y, '\n'.join(bios), f_bio, WHITE_W, col_w - 150, bio_lh)
        _ = nlines

    # ── 4. 底部主旗语细线收尾 ──
    f_foot = font(LXGW_R, 42)
    dr.line([(W // 2 - 520, 1342), (W // 2 + 520, 1342)], fill=GOLD_DEEP + (160,), width=3)
    draw_center(dr, cx, 1366, '愿起东方 · 力践未来', f_foot, GOLD_DIM)

    out = '/tmp/圆桌沙龙投屏背景-3840x1440-2026-08-14.png'
    base.convert('RGB').save(out, quality=95)
    print('saved:', out)

if __name__ == '__main__':
    main()
