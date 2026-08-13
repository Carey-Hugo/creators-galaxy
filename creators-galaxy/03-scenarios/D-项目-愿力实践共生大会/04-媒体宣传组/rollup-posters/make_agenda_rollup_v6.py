#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会议议程内容图易拉宝合成脚本 v6
调整：①日期放整个议程上方 ②嘉宾=姓名亮金粗体+头衔暗金细体(分段绘制) ③无斑马纹只留细金线
布局：左右两列——时间胶囊居左、内容+嘉宾居右，行间细金线
风格：A款 深蓝暖金·曙光之路 | 尺寸：80x200cm -> 3172x7932
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import datetime

W, H = 3172, 7932
BASE = 'A-易拉宝主题意象图-印刷版.jpg'
OUT = 'B-易拉宝会议议程-印刷版-v6.jpg'
PREVIEW = 'B-议程预览-v6.jpg'

FONT_BOLD = '/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Bold.ttf'
FONT_REG  = '/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Regular.ttf'
FONT_HEI  = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'

GOLD      = (255, 223, 122)
GOLD_DEEP = (234, 161, 53)
GOLD_DIM  = (217, 179, 106)
WHITE_W   = (245, 240, 230)
BLUE_SOFT = (201, 214, 240)
PANEL_BG  = (8, 18, 42)

PANEL_TOP = int(H * 0.410)
BOT_TOP   = H - 470
PANEL_MX  = 130
FADE      = 60

AGENDA = {
 'DAY1': [
  ('上午', '愿力实践共生大会主论坛', [
    ('08:30—09:10', '签到 · 入场 · 大会开场', ''),
    ('09:10—09:35', '主题分享一｜当智能成为文明基础设施，我们选择怎样的未来？',
     '明哥 · MoWa愿力文明零号志愿者'),
    ('09:35—10:10', '主题分享二｜从人类之源到愿力实践',
     '天玉 · 资深法律人/东方文化实践者/MoWa愿力文明志愿者/生命花园源头主理人'),
    ('10:10—10:45', '主题分享三｜量子时代：智慧灯塔建设与愿力实践',
     '王慧中 · 上海自主创新工程研究院院长兼董事/上海宽和企业管理咨询有限公司董事长/企业文化首席执行官高峰论坛（CCO）创始人'),
    ('10:45—11:05', '午餐 · 自由交流 · 休息', ''),
    ('11:05—11:20', '愿力实践生命样本分享',
     '李悦心 · 知行者工程联合总召集人/“好漾之境”创始人/两岸著名广播主持人'),
    ('11:20—11:30', '静默 · 《愿力实践宣言》共读', '天玉带领'),
    ('11:30—11:35', '认知与生命感收束', ''),
    ('11:35—13:30', '午餐 · 自由交流 · 休息', ''),
  ]),
  ('下午', '从时代之问到愿力实践行动', [
    ('13:30—14:20', '圆桌沙龙｜AI时代，什么不再稀缺？什么真正开始稀缺？',
     '保哥 · 资深资本财务顾问/美股港股IPO/跨境税务架构设计/曾任多家港股主板公司财务负责人 ／ '
     '陆鸿 · 感动中国年度人物/苏州市吴江区残联副主席/苏州缘跃纸制品有限公司主理人 ／ '
     '林俊廷 · 新媒体艺术家/擅于数字技术活化中国古典美学/策展人与艺术总监/四川美术学院特聘教授/光影“造梦”者/致力于打造沉浸式互动艺术体验'),
    ('14:20—15:10', '未来样本｜已经发生的未来',
     '雅淇&望舒 · 饮食文明传承实践者/探索者 ／ '
     '罗海棠（第3类人H） · 觉醒创富体系创始人/伦敦大学学院UCL物理博士/国际教练联合会ICF认证专业教练PCC/前阿里战略专家'),
    ('15:10—15:30', '茶歇 · 自由交流', ''),
    ('15:30—16:10', '生命品牌共生体联合发布',
     '天玉 · MoWa愿力文明志愿者 ／ 京鱼 · 京鹿鹿0号生命品牌主理人 ／ 悦心 · “好漾之境”创始人 ／ 杨靖 · 老磁窑主理人'),
    ('16:10—16:30', '愿库发布 · 捐赠与价值流转', '天玉带领'),
    ('16:30—16:50', '愿力实践共学基地发布',
     '朱斌 · 生命教练/连续创业者/清华创新管理研究/愿力文明志愿者/MoWa生态智慧教练主理人'),
    ('16:50—17:20', '愿力实践行动认领 · 8月16日共建主题发布', '各工作坊主理人'),
    ('17:20—17:25', '大会收束', ''),
  ]),
 ],
 'DAY2': [
  ('上午', '工作坊 · 自由共建', [
    ('08:30—09:00', '签到 · 工作坊分流', ''),
    ('09:00—12:00', '工作坊A｜个人愿力与智慧教练',
     '朱斌 · 生命教练/连续创业者/清华创新管理研究/愿力文明志愿者/MoWa生态智慧教练主理人'),
    ('09:00—12:00', '工作坊B｜生命品牌与生命花园落地',
     '天玉 · 资深法律人/东方文化实践者/MoWa愿力文明志愿者/生命花园源头主理人'),
    ('09:00—12:00', '工作坊F｜餐饮文化传承社区 · 上午场', '望舒&雅琪 · 饮食文明传承实践者/探索者'),
    ('12:00—13:30', '午餐 · 自由安排', ''),
  ]),
  ('下午', '工作坊 · 自由共建', [
    ('13:30—16:30', '工作坊C｜智慧灯塔企业与组织实践 · 共学基地',
     '王慧中 · 上海自主创新工程研究院院长兼董事/上海宽和企业管理咨询有限公司董事长/企业文化首席执行官高峰论坛（CCO）创始人'),
    ('13:30—16:30', '工作坊D｜M515与价值共生生态',
     '明哥 · MoWa愿力文明零号志愿者 ／ 保哥 · 资深资本财务顾问 ／ 天玉 · 生命花园源头主理人 ／ 革命姐 · 逍遥旅游创始人/黎想国数字化文旅发起人'),
    ('13:30—16:30', '工作坊E｜愿力实践社区', '朱洁 · 专业教练'),
    ('13:30—16:30', '工作坊F｜餐饮文化传承社区 · 下午场', '望舒&雅琪 · 饮食文明传承实践者/探索者'),
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

def draw_guest_segments(dr, x, y, text, f_name, f_title, max_w, lh):
    """嘉宾富文本：姓名亮金粗体 + 头衔暗金细体，多人用 ／ 分隔，自动换行"""
    segs = [s.strip() for s in text.split('／') if s.strip()]
    cur_x = x
    for seg in segs:
        if '·' in seg:
            name, title = seg.split('·', 1)
            name = name.strip(); title = title.strip()
        else:
            name, title = seg, ''
        w_name = dr.textlength(name, font=f_name)
        w_dot = dr.textlength('·', font=f_name) if title else 0
        w_title = dr.textlength(title, font=f_title) if title else 0
        w_seg = w_name + w_dot + w_title
        w_sep = dr.textlength('／ ', font=f_name) if cur_x > x else 0
        if cur_x + w_sep + w_seg > x + max_w and cur_x > x:
            cur_x = x
            y += lh
            w_sep = 0
        if cur_x > x:
            dr.text((cur_x, y), '／ ', font=f_name, fill=GOLD_DIM)
            cur_x += w_sep
        dr.text((cur_x, y), name, font=f_name, fill=GOLD)
        cur_x += w_name
        if title:
            dr.text((cur_x, y), '·', font=f_name, fill=GOLD_DIM)
            cur_x += w_dot
            dr.text((cur_x, y), title, font=f_title, fill=GOLD_DIM)
            cur_x += w_title
    return 0, 0

def make_gradient_mask(w, h, top_a, bot_a, blur=0):
    import numpy as np
    arr = np.linspace(top_a, bot_a, h, dtype=np.float32)[:, None]
    mask = np.tile(arr, (1, w)).astype(np.uint8)
    im = Image.fromarray(mask)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    return im

def draw_panel(base, y0, y1):
    panel_mask = Image.new('L', (W, H), 0)
    pm = ImageDraw.Draw(panel_mask)
    pm.rounded_rectangle([PANEL_MX, y0, W - PANEL_MX, y1], radius=26, fill=255)
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
    grad_mask = make_gradient_mask(W, hh, 238, 252, blur=4)
    base.paste(grad, (0, BOT_TOP), grad_mask)
    d = ImageDraw.Draw(base)
    d.line([(PANEL_MX + 400, BOT_TOP + 6), (W - PANEL_MX - 400, BOT_TOP + 6)],
           fill=GOLD_DEEP + (220,), width=3)
    f_big = font(FONT_BOLD, 82)
    t1 = '2026年8月15日—16日'
    d.text(((W - d.textlength(t1, font=f_big)) / 2, BOT_TOP + 52), t1, font=f_big, fill=GOLD)
    f_mid = font(FONT_BOLD, 60)
    t2 = '上海 · 徐汇 · 上中路495号揽园'
    d.text(((W - d.textlength(t2, font=f_mid)) / 2, BOT_TOP + 220), t2, font=f_mid, fill=WHITE_W)
    f_small = font(FONT_REG, 44)
    t3 = '（惠达创业园A座7楼）'
    d.text(((W - d.textlength(t3, font=f_small)) / 2, BOT_TOP + 330), t3, font=f_small, fill=GOLD_DIM)
    return base.convert('RGB')

def main():
    base = Image.open(BASE).convert('RGB')
    d = ImageDraw.Draw(base)

    # 字号（左右布局省空间，可加大）
    FS = dict(date=70, tag=64, day=54, sec=36, time=40, cont=52, gname=36, gtitle=32)
    LH_CONT = int(FS['cont'] * 1.25)      # 65
    LH_GUEST = int(FS['gname'] * 1.26)    # 45
    ROW_GAP = 16
    SEC_GAP = 20
    TIME_PAD_X = 18
    TIME_PAD_Y = 6
    TIME_COL_X = PANEL_MX + 60
    CONT_X = PANEL_MX + 560
    CONT_MAXW = W - PANEL_MX - 560 - 50

    def build_fonts():
        return (font(FONT_BOLD, FS['date']), font(FONT_BOLD, FS['tag']),
                font(FONT_BOLD, FS['day']), font(FONT_REG, max(FS['day'] - 12, 26)),
                font(FONT_BOLD, FS['sec']), font(FONT_BOLD, FS['time']),
                font(FONT_HEI, FS['cont']), font(FONT_BOLD, FS['gname']),
                font(FONT_HEI, FS['gtitle']))

    f_date, f_tag, f_day, f_sub, f_sec, f_time, f_cont, f_gname, f_gtitle = build_fonts()

    def guest_h(guest):
        if not guest:
            return 0
        segs = [s.strip() for s in guest.split('／') if s.strip()]
        total = 0
        cur_w = 0
        for seg in segs:
            name = seg.split('·', 1)[0].strip() if '·' in seg else seg.strip()
            title = seg.split('·', 1)[1].strip() if '·' in seg else ''
            w_seg = d.textlength(name, font=f_gname) + \
                    (d.textlength('·', font=f_gname) + d.textlength(title, font=f_gtitle) if title else 0)
            w_sep = d.textlength('／ ', font=f_gname) if cur_w > 0 else 0
            if cur_w + w_sep + w_seg > CONT_MAXW and cur_w > 0:
                total += 1
                cur_w = 0
            cur_w += w_seg
        return (total + 1) * LH_GUEST

    def row_h(tm, cont, guest):
        cap_h = FS['time'] + TIME_PAD_Y * 2
        c = len(wrap_text(d, cont, f_cont, CONT_MAXW))
        body_h = LH_CONT * c + 4 + guest_h(guest)
        return max(cap_h, body_h) + ROW_GAP

    def day_h(rows):
        h = int(FS['day'] * 1.45) + 14
        for _, _, items in rows:
            h += int(FS['sec'] * 1.45) + SEC_GAP
            for tm, cont, guest in items:
                h += row_h(tm, cont, guest)
        return h

    def total_h():
        return int(FS['date'] * 1.3) + 18 + int(FS['tag'] * 1.24) + 18 + \
               day_h(AGENDA['DAY1']) + 36 + day_h(AGENDA['DAY2'])

    avail = BOT_TOP - FADE - (PANEL_TOP + FADE)
    total = total_h()
    print(f'初始 total={total} avail={avail}')

    for _ in range(3):
        if total <= avail:
            break
        scale = (avail - 10) / total
        print(f'压缩 {scale:.3f} ->', end=' ')
        for k in FS:
            FS[k] = max(int(FS[k] * scale), 24)
        LH_CONT = int(FS['cont'] * 1.24)
        LH_GUEST = int(FS['gname'] * 1.25)
        ROW_GAP = max(int(12 * scale), 8)
        SEC_GAP = max(int(16 * scale), 10)
        f_date, f_tag, f_day, f_sub, f_sec, f_time, f_cont, f_gname, f_gtitle = build_fonts()
        total = total_h()
        print(f'total={total} 字号={FS}')

    y0 = PANEL_TOP + FADE
    y1 = y0 + total + 36
    print(f'面板 y0={y0} y1={y1} (底部区 {BOT_TOP})')

    base = draw_panel(base, y0 - 24, y1)
    d = ImageDraw.Draw(base)
    cx = W / 2

    y = y0 + 14
    # 日期（整个议程上方）
    wd1 = '周六' if datetime.date(2026, 8, 15).weekday() == 5 else ''
    wd2 = '周日' if datetime.date(2026, 8, 16).weekday() == 6 else ''
    date_str = f'2026年8月15日—16日（{wd1}—{wd2}）'
    d.text(((W - d.textlength(date_str, font=f_date)) / 2, y), date_str, font=f_date, fill=GOLD)
    y += int(FS['date'] * 1.3)
    # 会议议程标签 + 装饰线
    tag = '会 议 议 程'
    d.text(((W - d.textlength(tag, font=f_tag)) / 2, y), tag, font=f_tag, fill=GOLD)
    y += int(FS['tag'] * 1.22)
    ly = y - 14
    for lx, rx in [(cx - 460, cx - 80), (cx + 80, cx + 460)]:
        d.line([(lx, ly), (rx, ly)], fill=GOLD_DEEP, width=3)
    d.line([(cx - 54, ly), (cx + 54, ly)], fill=GOLD, width=4)
    y += 4

    def draw_day(day_label, sub_label, rows):
        nonlocal y
        d.text((TIME_COL_X, y), day_label, font=f_day, fill=GOLD)
        sw = d.textlength(sub_label, font=f_sub)
        d.text((W - PANEL_MX - 60 - sw, y + 8), sub_label, font=f_sub, fill=BLUE_SOFT)
        y += int(FS['day'] * 1.45)
        d.line([(TIME_COL_X, y), (W - PANEL_MX - 60, y)], fill=GOLD_DEEP + (170,), width=2)
        y += 14
        for sec_lbl, sec_sub, items in rows:
            lbl = sec_lbl + '｜' + sec_sub
            lbl_w = d.textlength(lbl, font=f_sec)
            by0 = y; by1 = y + int(FS['sec'] * 1.45)
            d.rounded_rectangle([TIME_COL_X, by0, TIME_COL_X + lbl_w + 40, by1],
                                radius=(by1 - by0) // 2, fill=GOLD_DEEP + (210,))
            d.text((TIME_COL_X + 20, by0 + int((by1 - by0 - FS['sec']) / 2) - 2),
                   lbl, font=f_sec, fill=(10, 20, 40))
            y = by1 + SEC_GAP
            for tm, cont, guest in items:
                rh = row_h(tm, cont, guest)
                # 时间胶囊（左列）
                tw = d.textlength(tm, font=f_time)
                tx0, ty0 = TIME_COL_X, y
                tx1 = tx0 + tw + TIME_PAD_X * 2
                ty1 = ty0 + FS['time'] + TIME_PAD_Y * 2
                d.rounded_rectangle([tx0, ty0, tx1, ty1], radius=(ty1 - ty0) // 2,
                                    fill=GOLD_DEEP + (48,), outline=GOLD + (255,), width=3)
                d.text((tx0 + TIME_PAD_X, ty0 + TIME_PAD_Y - 2), tm, font=f_time, fill=GOLD)
                # 内容（右列）
                n = draw_multiline(d, CONT_X, y, cont, f_cont, WHITE_W, CONT_MAXW, LH_CONT)
                gy = y + LH_CONT * n + 4
                # 嘉宾（姓名亮金粗+头衔暗金细）
                if guest:
                    gh, glines = draw_guest_segments(d, CONT_X, gy, guest, f_gname, f_gtitle, CONT_MAXW, LH_GUEST)
                y += rh
                # 行间细金线
                d.line([(TIME_COL_X, y - ROW_GAP // 2), (W - PANEL_MX - 60, y - ROW_GAP // 2)],
                       fill=GOLD_DEEP + (70,), width=2)

    draw_day('DAY 1 · 8月15日', '愿力实践共生大会', AGENDA['DAY1'])
    y += 36
    draw_day('DAY 2 · 8月16日', '愿力实践自由共建日', AGENDA['DAY2'])

    base = draw_bottom(base)

    base.save(OUT, 'JPEG', quality=95, subsampling=2)
    pv = base.resize((int(W * 800 / H), 800), Image.LANCZOS)
    pv.save(PREVIEW, 'JPEG', quality=90)
    print('saved:', OUT, base.size)
    print('saved:', PREVIEW, pv.size)

if __name__ == '__main__':
    main()
