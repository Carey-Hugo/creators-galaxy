#!/usr/bin/env python3
"""王慧中老师海报 V4：AI书法标题 + 双图拼贴"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

W, H = 1080, 1920
base = Image.open('/tmp/wang-v4-base.png').convert('RGB').resize((W, H), Image.LANCZOS).convert('RGBA')

F_HEI = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
f_quote = ImageFont.truetype(F_HEI, 23)
f_body = ImageFont.truetype(F_HEI, 25)
f_body2 = ImageFont.truetype(F_HEI, 23)
f_date = ImageFont.truetype(F_HEI, 26)
f_addr = ImageFont.truetype(F_HEI, 21)
f_slogan = ImageFont.truetype(F_HEI, 24)

WHITE = (255, 255, 255, 255)
WARM = (245, 240, 230, 255)
GOLD = (212, 175, 55, 255)
GOLD_BRIGHT = (255, 226, 148, 255)
NAVY = (13, 24, 40, 255)

draw = ImageDraw.Draw(base)

def center_text(text, y, font, fill, outline=None):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw)//2
    if outline:
        for ox in range(-2, 3):
            for oy in range(-2, 3):
                if ox*ox + oy*oy <= 4:
                    draw.text((x+ox, y+oy), text, font=font, fill=outline)
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]

def gold_line(y):
    for x in range(80, W-80, 6):
        draw.rectangle([x, y, min(x+3, W-80), y+2], fill=GOLD)

def blend_photo(photo_path, crop_box, target_w, x, y, fade_t=70, fade_b=70, fade_l=20, fade_r=20, blur=16, tint=0, radius=14, border=False, edge_shade=0):
    p = Image.open(photo_path).convert('RGB').crop(crop_box)
    target_h = int(p.height * target_w / p.width)
    p = p.resize((target_w, target_h), Image.LANCZOS).convert('RGBA')
    hh, ww = target_h, target_w
    alpha = np.ones((hh, ww), dtype=np.float32) * 255
    if fade_l:
        for i in range(fade_l):
            alpha[:, i] = 255 * i / fade_l
    if fade_r:
        for i in range(fade_r):
            alpha[:, -i-1] = 255 * i / fade_r
    for i in range(fade_t):
        alpha[i, :] = np.minimum(alpha[i, :], 255 * i / fade_t)
    for i in range(fade_b):
        alpha[-i-1, :] = np.minimum(alpha[-i-1, :], 255 * i / fade_b)
    mask = Image.fromarray(alpha.astype(np.uint8), 'L').filter(ImageFilter.GaussianBlur(blur))
    # 圆角 mask
    if radius:
        rmask = Image.new('L', (ww, hh), 0)
        rd = ImageDraw.Draw(rmask)
        rd.rounded_rectangle([0, 0, ww-1, hh-1], radius=radius, fill=255)
        rmask = rmask.filter(ImageFilter.GaussianBlur(6))
        mask = Image.fromarray(np.minimum(np.array(mask), np.array(rmask)).astype(np.uint8), 'L')
    base.paste(p, (x, y), mask)
    # 色调统一
    if tint:
        tint_layer = Image.new('RGBA', (ww, hh), (8, 18, 42, tint))
        base.alpha_composite(tint_layer, (x, y))
    # 内部右缘暗化（vignette，消除边缘杂物，不碰金边）
    if edge_shade:
        sh = Image.new('RGBA', (ww, hh), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sh)
        for i in range(edge_shade):
            a = int(205 * i / edge_shade)
            sd.rectangle([ww-edge_shade+i, 0, ww-edge_shade+i+1, hh], fill=(8, 18, 42, a))
        base.alpha_composite(sh, (x, y))
    # 金边
    if border:
        bd = ImageDraw.Draw(base)
        bd.rounded_rectangle([x, y, x+ww-1, y+hh-1], radius=radius, outline=(255, 226, 148, 160), width=2)
    return target_h

# ═══ 拼图区（中部，AI已留空 30-62%）═══
# 主：王老师单人特写（裁窄去蓝衣，突出主体）
pw = 450
px = 50
ph1 = blend_photo('/home/ubuntu/.hermes/image_cache/img_98f5dc2ebe50.jpg',
                  (0, 220, 450, 1005), pw, px, 700,
                  fade_t=30, fade_b=30, fade_l=8, fade_r=8, blur=10, tint=30, radius=16, border=True, edge_shade=42)
# 副：生活教育馆合影（裁中间突出王老师）
sw = 280
sx = 590
sh1 = blend_photo('/home/ubuntu/.hermes/image_cache/img_edd1e619952f.jpg',
                  (280, 250, 568, 1000), sw, sx, 700,
                  fade_t=30, fade_b=30, fade_l=8, fade_r=8, blur=10, tint=42, radius=16, border=True)
# 注：blend_photo 按目标宽等比算高，两图高可能略有差异，接受

# ═══ 底部面板（84% 起，给照片/简介留空间）═══
panel_y0 = int(H * 0.84)
arr = np.array(base)
overlay = np.zeros((H - panel_y0, W, 4), dtype=np.uint8)
overlay[:, :, 0] = 8; overlay[:, :, 1] = 18; overlay[:, :, 2] = 42
fade = 90
for i in range(overlay.shape[0]):
    if i < fade:
        overlay[i, :, 3] = int(255 * i / fade)
    else:
        overlay[i, :, 3] = 255
panel = Image.fromarray(overlay, 'RGBA').filter(ImageFilter.GaussianBlur(5))
base.alpha_composite(panel, (0, panel_y0))
draw = ImageDraw.Draw(base)

# 简介（照片下方、面板上方）
y = 700 + max(ph1, sh1) + 30
y += center_text('胖东来、德胜之后', y, f_body, WARM) + 6
y += center_text('《企业文化地图》《胖东来你要怎么学？》', y, f_body2, GOLD_BRIGHT) + 6
y += center_text('从德胜、胖东来 到 AI时代 —— 这一问，海南一起答', y, f_body2, GOLD_BRIGHT)
gold_line(panel_y0 + 8)

y3 = panel_y0 + fade + 18
y3 += center_text('2026年8月30日（星期日）· 海口', y3, f_date, GOLD_BRIGHT) + 10
y3 += center_text('海南 · 海口 · 秀英区 · 海南人才大厦 1楼OPC社区会议室', y3, f_addr, WARM) + 14
center_text('共同看见未来 · 看见真实样本 · 看见自己的位置', y3, f_slogan, GOLD)

out = base.convert('RGB')
out.save('/tmp/wang-poster-v4.png', 'PNG')
out.save('/tmp/wang-poster-v4.jpg', 'JPEG', quality=92)
print('王老师V4完成', out.size, '主照片高', ph1, '副照片高', sh1, '最后y', y)
