#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会议议程内容图易拉宝合成脚本 v2（紧凑版）
风格：A款 深蓝暖金·曙光之路（沿用主题意象图印刷版底图）
尺寸：80x200cm -> 3172x7932 (≈101dpi)
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import datetime

W, H = 3172, 7932
BASE = 'A-易拉宝主题意象图-印刷版.jpg'
OUT = 'B-易拉宝会议议程-印刷版.jpg'
PREVIEW = 'B-议程预览.jpg'

FONT_BOLD = '/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Bold.ttf'
FONT_REG  = '/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Regular.ttf'

GOLD      = (255, 223, 122)
GOLD_DEEP = (234, 161, 53)
GOLD_DIM  = (217, 179, 106)
WHITE_W   = (245, 240, 230)
BLUE_SOFT = (201, 214, 240)
PANEL_BG  = (8, 18, 42)

PANEL_TOP = int(H * 0.425)   # 3371 标题区结束、面板开始
PANEL_MX  = 130
PANEL_W   = W - PANEL_MX * 2
BOT_TOP   = int(H * 0.865)   # 6868 底部信息区起点
FADE      = 70               # 面板顶部距 PANEL_TOP 的留白（标签区）

AGENDA = {
 'DAY1': [
  ('上午', '愿力实践共生大会主论坛', [
    ('08:30—09:10', '签到 · 入场 · 大会开场', ''),
    ('09:10—09:35', '主题分享一｜当智能成为文明基础设施，我们选择怎样的未来？',
     '明哥 · MoWa愿力文明零号志愿者'),
    ('09:35—10:10', '主题分享二｜从人类之源到愿力实践',
     '天玉 · 资深法律人 · 生命花园源头主理人'),
    ('10:10—10:45', '主题分享三｜量子时代：智慧灯塔建设与愿力实践',
     '王慧中 · 上海自主创新工程研究院院长'),
    ('10:45—11:05', '午餐 · 自由交流 · 休息', ''),
    ('11:05—11:20', '愿力实践生命样本分享',
     '李悦心 · 知行者工程联合总召集人 · 两岸著名广播主持人'),
    ('11:20—11:30', '静默 · 《愿力实践宣言》共读', '天玉带领'),
    ('11:30—11:35', '认知与生命感收束', ''),
    ('11:35—13:30', '午餐 · 自由交流 · 休息', ''),
  ]),
  ('下午', '从时代之问到愿力实践行动', [
    ('13:30—14:20', '圆桌沙龙｜AI时代，什么不再稀缺？什么真正开始稀缺？',
     '保哥 · 资深资本财务顾问 ／ 陆鸿 · 感动中国年度人物 ／ 林俊廷 · 新媒体艺术家'),
    ('14:20—15:10', '未来样本｜已经发生的未来',
     '雅淇&望舒 · 饮食文明传承实践者 ／ 罗海棠 · 觉醒创富体系创始人'),
    ('15:10—15:30', '茶歇 · 自由交流', ''),
    ('15:30—16:10', '生命品牌共生体联合发布', '天玉 ／ 京鱼 ／ 悦心 ／ 杨靖'),
    ('16:10—16:30', '愿库发布 · 捐赠与价值流转', '天玉带领'),
    ('16:30—16:50', '愿力实践共学基地发布', '朱斌 · 生命教练 · MoWa生态智慧教练主理人'),
    ('16:50—17:20', '愿力实践行动认领 · 8月16日共建主题发布', '各工作坊主理人'),
    ('17:20—17:25', '大会收束', ''),
  ]),
 ],
 'DAY2': [
  ('上午', '工作坊 · 自由共建', [
    ('08:30—09:00', '签到 · 工作坊分流', ''),
    ('09:00—12:00', '工作坊A｜个人愿力与智慧教练', '朱斌 · 生命教练 · MoWa生态智慧教练主理人'),
    ('09:00—12:00', '工作坊B｜生命品牌与生命花园落地', '天玉 · 生命花园源头主理人'),
    ('09:00—12:00', '工作坊F｜餐饮文化传承社区 · 上午场', '望舒&雅琪 · 饮食文明传承实践者'),
    ('12:00—13:30', '午餐 · 自由安排', ''),
  ]),
  ('下午', '工作坊 · 自由共建', [
    ('13:30—16:30', '工作坊C｜智慧灯塔企业与组织实践 · 共学基地', '王慧中'),
    ('13:30—16:30', '工作坊D｜M515与价值共生生态', '明哥 ／ 保哥 ／ 天玉 ／ 革命姐'),
    ('13:30—16:30', '工作坊E｜愿力实践社区', '朱洁 · 专业教练'),
    ('13:30—16:30', '工作坊F｜餐饮文化传承社区 · 下午场', '望舒&雅琪 · 饮食文明传承实践者'),
  ]),
 ],
}

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap_text(draw, text, fnt, max_w):
    if not text:
        return []
    lines, cur = [], ''
    for ch in text:
        if draw.textlength(cur + ch, font=fnt) <= max_w:
            cur += ch
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines

def draw_multiline(draw, x, y, text, fnt, fill, max_w, lh):
    lines = wrap_text(draw, text, fnt, max_w)
    for i, ln in enumerate(lines):
        draw.text((x, y + i * lh), ln, font=fnt, fill=fill)
    return len(lines)

def make_gradient_mask(w, h, top_a, bot_a, blur=0):
    import numpy as np
    arr = np.linspace(top_a, bot_a, h, dtype=np.float32)[:, None]
    mask = np.tile(arr, (1, w)).astype(np.uint8)
    im = Image.fromarray(mask)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    return im

def draw_panel(base, y0, y1):
    """深蓝半透明面板 + 金边 + 上下柔和渐隐"""
    panel_mask = Image.new('L', (W, H), 0)
    pm = ImageDraw.Draw(panel_mask)
    pm.rounded_rectangle([PANEL_MX, y0, W - PANEL_MX, y1], radius=26, fill=255)
    # 上下渐隐
    fh = 130
    top_zone = panel_mask.crop((0, y0, W, y0 + fh))
    fade_top = make_gradient_mask(W, fh, 0, 255, blur=10)
    top_zone = Image.composite(Image.new('L', (W, fh), 0), top_zone, fade_top)
    panel_mask.paste(top_zone, (0, y0))
    bot_zone = panel_mask.crop((0, y1 - fh, W, y1))
    fade_bot = make_gradient_mask(W, fh, 255, 0, blur=10)
    bot_zone = Image.composite(Image.new('L', (W, fh), 0), bot_zone, fade_bot)
    panel_mask.paste(bot_zone, (0, y1 - fh))
    panel_mask = panel_mask.filter(ImageFilter.GaussianBlur(3))
    color_layer = Image.new('RGBA', (W, H), PANEL_BG + (210,))
    cd = ImageDraw.Draw(color_layer)
    cd.rounded_rectangle([PANEL_MX, y0, W - PANEL_MX, y1], radius=26,
                         outline=GOLD_DEEP + (255,), width=4)
    return Image.composite(color_layer, base.convert('RGBA'), panel_mask).convert('RGB')

def draw_bottom(base):
    base = base.convert('RGBA')
    hh = H - BOT_TOP
    grad = Image.new('RGBA', (W, hh), PANEL_BG + (255,))
    grad_mask = make_gradient_mask(W, hh, 240, 252, blur=4)
    base.paste(grad, (0, BOT_TOP), grad_mask)
    d = ImageDraw.Draw(base)
    d.line([(PANEL_MX + 400, BOT_TOP + 10), (W - PANEL_MX - 400, BOT_TOP + 10)],
           fill=GOLD_DEEP + (220,), width=3)
    f_big = font(FONT_BOLD, 84)
    t1 = '2026年8月15日—16日'
    d.text(((W - d.textlength(t1, font=f_big)) / 2, BOT_TOP + 130), t1, font=f_big, fill=GOLD)
    f_mid = font(FONT_BOLD, 60)
    t2 = '上海 · 徐汇'
    d.text(((W - d.textlength(t2, font=f_mid)) / 2, BOT_TOP + 330), t2, font=f_mid, fill=WHITE_W)
    f_small = font(FONT_REG, 38)
    t3 = '具体地点以报名成功通知为准'
    d.text(((W - d.textlength(t3, font=f_small)) / 2, BOT_TOP + 480), t3, font=f_small, fill=GOLD_DIM)
    return base.convert('RGB')

def main():
    base = Image.open(BASE).convert('RGB')
    d = ImageDraw.Draw(base)
    cx = W / 2

    # ---- 字号（紧凑参数） ----
    FS = dict(tag=74, day=58, sec=40, time=44, cont=46, guest=36)
    # 行高常量
    LH_CONT = int(FS['cont'] * 1.30)   # 60
    LH_GUEST = int(FS['guest'] * 1.28) # 46
    ROW_GAP = 14
    SEC_GAP = 20
    CONT_X = PANEL_MX + 620
    CONT_MAXW = W - PANEL_MX * 2 - 620 - 60

    f_tag = font(FONT_BOLD, FS['tag'])
    f_day = font(FONT_BOLD, FS['day'])
    f_sub = font(FONT_REG, FS['day'] - 14)
    f_sec = font(FONT_BOLD, FS['sec'])
    f_time = font(FONT_BOLD, FS['time'])
    f_cont = font(FONT_BOLD, FS['cont'])
    f_guest = font(FONT_REG, FS['guest'])

    # ---- 预测量高（兜底压缩用） ----
    def row_h(cont, guest):
        c = len(wrap_text(d, cont, f_cont, CONT_MAXW))
        g = len(wrap_text(d, guest, f_guest, CONT_MAXW))
        h = LH_CONT * c + (LH_GUEST * g + 6 if guest else 0) + ROW_GAP
        return h

    def day_h(rows):
        h = int(FS['day'] * 1.5) + 22
        for _, _, items in rows:
            h += int(FS['sec'] * 1.5) + SEC_GAP
            for tm, cont, guest in items:
                h += row_h(cont, guest)
        return h

    tag_h = int(FS['tag'] * 1.35) + 26
    h1 = day_h(AGENDA['DAY1'])
    h2 = day_h(AGENDA['DAY2'])
    total = tag_h + h1 + 40 + h2
    avail = BOT_TOP - FADE - (PANEL_TOP + FADE)
    print(f'tag={tag_h} h1={h1} h2={h2} total={total} avail={avail}')

    scale = 1.0
    if total > avail:
        scale = (avail - 20) / total
        print(f'超出 -> 压缩系数 {scale:.3f}')
        # 重新按比例缩字号
        for k in FS:
            FS[k] = max(int(FS[k] * scale), 30)
        LH_CONT = int(FS['cont'] * 1.28)
        LH_GUEST = int(FS['guest'] * 1.26)
        ROW_GAP = max(int(14 * scale), 8)
        SEC_GAP = max(int(20 * scale), 12)
        f_tag = font(FONT_BOLD, FS['tag']); f_day = font(FONT_BOLD, FS['day'])
        f_sub = font(FONT_REG, max(FS['day'] - 14, 26))
        f_sec = font(FONT_BOLD, FS['sec']); f_time = font(FONT_BOLD, FS['time'])
        f_cont = font(FONT_BOLD, FS['cont']); f_guest = font(FONT_REG, FS['guest'])
        tag_h = int(FS['tag'] * 1.32) + 22
        h1 = day_h(AGENDA['DAY1']); h2 = day_h(AGENDA['DAY2'])
        total = tag_h + h1 + 40 + h2
        print(f'压缩后 total={total}')

    # ---- 面板边界 ----
    y0 = PANEL_TOP + FADE
    y1 = y0 + total + 46
    print(f'面板 y0={y0} y1={y1} (底部区 {BOT_TOP})')

    # ---- 画面板 ----
    base = draw_panel(base, y0 - 24, y1)
    d = ImageDraw.Draw(base)

    # ---- 顶部「会议议程」标签 ----
    y = y0 + 20
    tag = '会 议 议 程'
    d.text(((W - d.textlength(tag, font=f_tag)) / 2, y), tag, font=f_tag, fill=GOLD)
    y += int(FS['tag'] * 1.30)
    ly = y - 20
    for lx, rx in [(cx - 500, cx - 88), (cx + 88, cx + 500)]:
        d.line([(lx, ly), (rx, ly)], fill=GOLD_DEEP, width=3)
    d.line([(cx - 58, ly), (cx + 58, ly)], fill=GOLD, width=4)
    y += 6

    # ---- 行绘制 ----
    def draw_day(day_label, sub_label, rows):
        nonlocal y
        d.text((PANEL_MX + 60, y), day_label, font=f_day, fill=GOLD)
        sw = d.textlength(sub_label, font=f_sub)
        d.text((W - PANEL_MX - 60 - sw, y + 8), sub_label, font=f_sub, fill=BLUE_SOFT)
        y += int(FS['day'] * 1.5)
        d.line([(PANEL_MX + 60, y), (W - PANEL_MX - 60, y)], fill=GOLD_DEEP + (170,), width=2)
        y += 20
        for sec_lbl, sec_sub, items in rows:
            lbl = sec_lbl + '｜' + sec_sub
            lbl_w = d.textlength(lbl, font=f_sec)
            by0 = y; by1 = y + int(FS['sec'] * 1.5)
            d.rounded_rectangle([PANEL_MX + 60, by0, PANEL_MX + 60 + lbl_w + 44, by1],
                                radius=(by1 - by0) // 2, fill=GOLD_DEEP + (210,))
            d.text((PANEL_MX + 60 + 22, by0 + int((by1 - by0 - FS['sec']) / 2) - 2),
                   lbl, font=f_sec, fill=(10, 20, 40))
            y = by1 + SEC_GAP
            for tm, cont, guest in items:
                d.text((PANEL_MX + 60, y), tm, font=f_time, fill=GOLD)
                n = draw_multiline(d, CONT_X, y, cont, f_cont, WHITE_W, CONT_MAXW, LH_CONT)
                y += LH_CONT * n
                if guest:
                    ng = draw_multiline(d, CONT_X, y + 4, guest, f_guest, GOLD_DIM, CONT_MAXW, LH_GUEST)
                    y += LH_GUEST * ng + 6
                y += ROW_GAP

    wd1 = '周六' if datetime.date(2026, 8, 15).weekday() == 5 else ''
    wd2 = '周日' if datetime.date(2026, 8, 16).weekday() == 6 else ''
    draw_day('DAY 1 · 8月15日' + (' · ' + wd1 if wd1 else ''), '愿力实践共生大会', AGENDA['DAY1'])
    y += 40
    draw_day('DAY 2 · 8月16日' + (' · ' + wd2 if wd2 else ''), '愿力实践自由共建日', AGENDA['DAY2'])

    # ---- 底部 ----
    base = draw_bottom(base)

    base.save(OUT, 'JPEG', quality=95, subsampling=2)
    pv = base.resize((int(W * 800 / H), 800), Image.LANCZOS)
    pv.save(PREVIEW, 'JPEG', quality=90)
    print('saved:', OUT, base.size)
    print('saved:', PREVIEW, pv.size)

if __name__ == '__main__':
    main()
