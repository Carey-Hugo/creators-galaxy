#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""圆桌沙龙 LED 投屏背景图 v2 — AI艺术字标题(画进底图) + PIL叠加嘉宾信息"""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np

W, H = 3840, 1440

LXGW_B = '/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Bold.ttf'
LXGW_R = '/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Regular.ttf'
NOTO_R = '/home/ubuntu/.fonts/NotoSansCJKsc-Regular.otf'

GOLD      = (255, 223, 122)
GOLD_DEEP = (234, 161, 53)
GOLD_DIM  = (217, 179, 106)
WHITE_W   = (245, 240, 230)

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap_center(dr, cx, y, text, fnt, fill, max_w, lh):
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
    base = Image.open('/tmp/roundtable_bg2_ai.png').convert('RGB')
    base = base.resize((W, H), Image.LANCZOS)
    base = ImageEnhance.Color(base).enhance(1.06)
    base = ImageEnhance.Contrast(base).enhance(1.04)
    base = base.convert('RGBA')

    # 嘉宾区(文字带)轻微暗化, 保证可读
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    arr = np.zeros((H, W, 4), dtype=np.uint8)
    # y 780-1120 嘉宾文字区: 暗化 0->55->0
    for y in range(780, 1120):
        if y < 900:
            a = int(55 * (y - 780) / 120)
        elif y < 1020:
            a = 55
        else:
            a = int(55 * (1 - (y - 1020) / 100))
        arr[y, :, 3] = a
    base = Image.alpha_composite(base, Image.fromarray(arr))
    dr = ImageDraw.Draw(base)

    # 嘉宾四列
    guests = [
        ('保哥', ['资深资本财务顾问', '美股港股IPO · 跨境税务架构设计', '曾任多家港股主板公司财务负责人']),
        ('陆鸿', ['感动中国年度人物', '苏州市吴江区残联副主席', '苏州缘跃纸制品有限公司主理人']),
        ('望舒', ['曾任某集团公司人力资源总', '曾任某集团公司战略部负责人', '某集团一级公司一号位']),
        ('林俊廷', ['新媒体艺术家 · 数字活化中国古典美学', '策展人与艺术总监 · 四川美术学院特聘教授', '光影“造梦”者 · 沉浸式互动艺术体验']),
    ]
    n = len(guests)
    col_w = W // n
    name_y = 806
    f_name = font(LXGW_B, 72)
    f_bio = font(NOTO_R, 38)
    bio_lh = 56

    for i, (name, bios) in enumerate(guests):
        cxc = col_w * i + col_w // 2
        # 名字(双层: 深色阴影 + 亮金)
        for dx, dy, col in [(-2, 2, (0, 0, 0, 160)), (0, 0, GOLD + (255,))]:
            w = dr.textlength(name, font=f_name)
            dr.text((cxc - w / 2 + dx, name_y + dy), name, font=f_name, fill=col)
        # 短金线
        lw = 150
        dr.line([(cxc - lw // 2, name_y + 100), (cxc + lw // 2, name_y + 100)],
                fill=GOLD_DEEP + (215,), width=3)
        # 简介(暖白, 最多3行)
        wrap_center(dr, cxc, name_y + 142, '\n'.join(bios), f_bio, WHITE_W, col_w - 150, bio_lh)

    out = '/tmp/圆桌沙龙投屏背景-AI艺术字-3840x1440-2026-08-14.png'
    base.convert('RGB').save(out, quality=95)
    print('saved:', out)

if __name__ == '__main__':
    main()
