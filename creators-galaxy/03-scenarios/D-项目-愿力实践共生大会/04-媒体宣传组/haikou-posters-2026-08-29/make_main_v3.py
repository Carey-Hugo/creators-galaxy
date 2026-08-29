#!/usr/bin/env python3
"""主海报 V3：六大板块 + 金色徽章立体图标"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

W, H = 1080, 1920
base = Image.open('/tmp/main-v3-base.png').convert('RGB').resize((W, H), Image.LANCZOS).convert('RGBA')

F_HEI = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
f_intro = ImageFont.truetype(F_HEI, 25)
f_name = ImageFont.truetype(F_HEI, 26)
f_desc = ImageFont.truetype(F_HEI, 19)
f_date = ImageFont.truetype(F_HEI, 26)
f_addr = ImageFont.truetype(F_HEI, 21)
f_slogan = ImageFont.truetype(F_HEI, 24)

WHITE = (255, 255, 255, 255)
WARM = (245, 240, 230, 255)
GOLD = (212, 175, 55, 255)
GOLD_BRIGHT = (255, 226, 148, 255)
PANEL_BG = (8, 18, 42)

# ── 信息面板（62% 起）
panel_y0 = int(H * 0.62)
arr = np.array(base)
overlay = np.zeros((H - panel_y0, W, 4), dtype=np.uint8)
overlay[:, :, 0] = PANEL_BG[0]; overlay[:, :, 1] = PANEL_BG[1]; overlay[:, :, 2] = PANEL_BG[2]
fade = 120
for i in range(overlay.shape[0]):
    if i < fade:
        overlay[i, :, 3] = int(255 * i / fade)
    else:
        overlay[i, :, 3] = 255
panel = Image.fromarray(overlay, 'RGBA').filter(ImageFilter.GaussianBlur(5))
base.alpha_composite(panel, (0, panel_y0))
draw = ImageDraw.Draw(base)

def center_text(text, y, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw)//2, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]

def gold_line(y):
    for x in range(80, W-80, 6):
        draw.rectangle([x, y, min(x+3, W-80), y+2], fill=GOLD)

# ═══ 六大板块图标（金色徽章简笔）═══
def draw_icon(itype, cx, cy, r):
    """在 (cx,cy) 画半径 r 的金色简笔图标，返回图标层"""
    ic = Image.new('RGBA', (W, H), (0,0,0,0))
    d = ImageDraw.Draw(ic)
    # 徽章圆底
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(212,175,55,36), outline=(255,226,148,230), width=2)
    lw = 3
    g = GOLD_BRIGHT
    s = r * 0.72  # 内部图形半尺寸
    if itype == 'aci':      # AI脑：圆+内弧
        d.ellipse([cx-s, cy-s*0.9, cx+s, cy+s*0.9], outline=g, width=lw)
        d.arc([cx-s*0.55, cy-s*0.75, cx+s*0.55, cy+s*0.75], 180, 360, fill=g, width=lw)
        d.line([cx-s*0.3, cy-s*0.2, cx-s*0.3, cy+s*0.5], fill=g, width=lw)
        d.line([cx+s*0.3, cy-s*0.2, cx+s*0.3, cy+s*0.5], fill=g, width=lw)
    elif itype == 'sprout': # 生命品牌：茎+两叶
        d.line([cx, cy+s*0.7, cx, cy-s*0.1], fill=g, width=lw)
        d.ellipse([cx-s*0.05, cy-s*0.75, cx+s*0.75, cy-s*0.15], outline=g, width=lw)
        d.ellipse([cx-s*0.75, cy-s*0.75, cx+s*0.05, cy-s*0.15], outline=g, width=lw)
    elif itype == 'people': # 未来组织：三人组
        for dx in (-s*0.55, 0, s*0.55):
            d.ellipse([cx+dx-s*0.18, cy-s*0.65, cx+dx+s*0.18, cy-s*0.29], outline=g, width=lw)
        d.arc([cx-s*0.75, cy-s*0.1, cx+s*0.75, cy+s*0.75], 0, 180, fill=g, width=lw)
    elif itype == 'bowl':   # 七凤黄：碗+蒸汽
        d.pieslice([cx-s*0.75, cy-s*0.45, cx+s*0.75, cy+s*0.75], 0, 180, outline=g, width=lw)
        d.line([cx-s*0.75, cy+s*0.15, cx+s*0.75, cy+s*0.15], fill=g, width=lw)
        for dx in (-s*0.25, s*0.25):
            d.arc([cx+dx-s*0.18, cy-s*0.85, cx+dx+s*0.18, cy-s*0.35], 200, 340, fill=g, width=lw)
    elif itype == 'heart':  # 启愿师：爱心
        d.ellipse([cx-s*0.75, cy-s*0.55, cx-s*0.05, cy+s*0.05], outline=g, width=lw)
        d.ellipse([cx+s*0.05, cy-s*0.55, cx+s*0.75, cy+s*0.05], outline=g, width=lw)
        d.polygon([(cx-s*0.68, cy-s*0.05), (cx+s*0.68, cy-s*0.05), (cx, cy+s*0.8)], outline=g)
    elif itype == 'link':   # 海南价值共生：双环
        d.ellipse([cx-s*0.75, cy-s*0.55, cx+s*0.05, cy+s*0.25], outline=g, width=lw)
        d.ellipse([cx-s*0.05, cy-s*0.55, cx+s*0.75, cy+s*0.25], outline=g, width=lw)
    return ic

# ═══ 排版 ═══
# 引言
y = panel_y0 + fade + 16
y += center_text('人、事业、组织与价值关系，正在怎样重新生长？', y, f_intro, GOLD_BRIGHT) + 10
gold_line(y)
y += 14

# 六大板块 2×3 网格（带图标）
blocks = [
    ('aci', 'ACI', 'AI怎样真正服务人的愿力与生命'),
    ('sprout', '生命品牌', '一个生命怎样自然长成一门事业'),
    ('people', '未来组织', '从德胜、胖东来到AI时代「把人当人」'),
    ('bowl', '七凤黄', '7位普通阿姨与100多㎡里的未来组织实践'),
    ('heart', '启愿师', 'AI时代正在出现的新型生命陪伴者'),
    ('link', '海南价值共生', '新生命、新事业、新组织 在海南先做出一批真的'),
]
col_w, row_h = 500, 96
gap_x, gap_y = 20, 8
x0 = 40
y0 = y
for i, (itype, name, desc) in enumerate(blocks):
    r, c = divmod(i, 2)
    bx = x0 + c * (col_w + gap_x)
    by = y0 + r * (row_h + gap_y)
    draw.rounded_rectangle([bx, by, bx+col_w, by+row_h-4], radius=9, fill=(16, 32, 62, 150), outline=(212, 175, 55, 60), width=1)
    # 图标（徽章 44px）
    ic = draw_icon(itype, bx+40, by+48, 26)
    base.alpha_composite(ic, (0, 0))
    # 板块名 + 描述
    draw = ImageDraw.Draw(base)
    draw.text((bx+78, by+12), name, font=f_name, fill=GOLD_BRIGHT)
    dw = col_w - 94
    lines = []
    cur = ''
    for ch in desc:
        if draw.textlength(cur + ch, font=f_desc) <= dw:
            cur += ch
        else:
            lines.append(cur); cur = ch
    lines.append(cur)
    for li, ln in enumerate(lines[:2]):
        draw.text((bx+78, by + 52 + li*24), ln, font=f_desc, fill=WARM)

y = y0 + 3 * (row_h + gap_y) - 4 + 10
gold_line(y)
y += 12

# 底部信息（整体上移，留底部安全区 ≥8%）
y += center_text('2026年8月30日（星期日）· 海口', y, f_date, GOLD_BRIGHT) + 8
y += center_text('海南 · 海口 · 秀英区 · 海南人才大厦 1楼OPC社区会议室', y, f_addr, WARM) + 14
center_text('共同看见未来 · 看见真实样本 · 看见自己的位置', y, f_slogan, GOLD)

out = base.convert('RGB')
out.save('/tmp/main-poster-v3.png', 'PNG')
out.save('/tmp/main-poster-v3.jpg', 'JPEG', quality=92)
print('主海报V3完成', out.size, '最后y', y)
