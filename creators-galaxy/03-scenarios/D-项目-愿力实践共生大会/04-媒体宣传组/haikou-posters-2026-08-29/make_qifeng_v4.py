#!/usr/bin/env python3
"""七凤黄海报 V4：AI书法标题 + 三图拼贴"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

W, H = 1080, 1920
base = Image.open('/tmp/qifeng-v4-base.png').convert('RGB').resize((W, H), Image.LANCZOS).convert('RGBA')

F_HEI = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
f_body = ImageFont.truetype(F_HEI, 25)
f_data = ImageFont.truetype(F_HEI, 26)
f_card_sm = ImageFont.truetype(F_HEI, 20)
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

def blend_photo(photo_path, crop_box, target_w, x, y, fade_t=40, fade_b=40, fade_l=8, fade_r=8, blur=10, tint=36, radius=14, border=True):
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
    if radius:
        rmask = Image.new('L', (ww, hh), 0)
        rd = ImageDraw.Draw(rmask)
        rd.rounded_rectangle([0, 0, ww-1, hh-1], radius=radius, fill=255)
        rmask = rmask.filter(ImageFilter.GaussianBlur(5))
        mask = Image.fromarray(np.minimum(np.array(mask), np.array(rmask)).astype(np.uint8), 'L')
    base.paste(p, (x, y), mask)
    if tint:
        tint_layer = Image.new('RGBA', (ww, hh), (8, 18, 42, tint))
        base.alpha_composite(tint_layer, (x, y))
    if border:
        bd = ImageDraw.Draw(base)
        bd.rounded_rectangle([x, y, x+ww-1, y+hh-1], radius=radius, outline=(255, 226, 148, 150), width=2)
    return target_h

# ═══ 拼图区（中部 26-58% 留空）═══
# 主：阿姨合影（裁顶部 12% 突出人物，下移避开标题）
mw = 720
mx = (W - mw) // 2
mh = blend_photo('/home/ubuntu/.hermes/image_cache/img_fc930f538393.jpg',
                 (0, 90, 1256, 749), mw, mx, 500,
                 fade_t=20, fade_b=20, fade_l=8, fade_r=8, blur=10, tint=30, radius=16, border=True)
# 次1：门店门头（裁掉左侧过曝区）
sw = 420
sx = 70
sh = blend_photo('/home/ubuntu/.hermes/image_cache/img_0c9450c98b9b.jpg',
                 (150, 0, 1280, 719), sw, sx, 960,
                 fade_t=20, fade_b=20, fade_l=8, fade_r=8, blur=10, tint=42, radius=14, border=True)
# 次2：辣椒酱产品（横 1.50）右下
pw = 320
px = 570
ph = blend_photo('/home/ubuntu/.hermes/image_cache/img_0eb2c9f40377.jpg',
                 (0, 0, 913, 608), pw, px, 970,
                 fade_t=20, fade_b=20, fade_l=8, fade_r=8, blur=10, tint=36, radius=14, border=True)

# ═══ 文案（加深蓝底条防背景干扰）═══
y = 1260
# 深蓝底条
draw.rounded_rectangle([60, y-8, W-60, y+92], radius=14, fill=(8, 18, 42, 200))
y += center_text('如果未来是真的，为什么不能先发生在她们身上？', y, f_body, WARM, outline=NAVY) + 14

# 评分卡
card_w, card_h = 620, 96
cx = (W - card_w) // 2
draw.rounded_rectangle([cx, y, cx+card_w, y+card_h], radius=14, fill=(10, 22, 48, 235), outline=GOLD, width=2)
draw.text((cx+50, y+18), '美团 4.9 分 · 川菜好评榜第 1 名', font=f_data, fill=GOLD_BRIGHT)
draw.text((cx+50, y+58), '一碗鸡煲，7个阿姨，一个品牌', font=f_card_sm, fill=WARM)
y = y + card_h + 20

gold_line(y)
y += 18

# ═══ 底部面板 ═══
panel_y0 = int(H * 0.80)
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

y3 = panel_y0 + fade + 20
y3 += center_text('2026年8月30日（星期日）· 海口', y3, f_date, GOLD_BRIGHT) + 10
y3 += center_text('海南 海口 · 秀英区 · 海南人才大厦 1楼OPC社区会议室', y3, f_addr, WARM) + 14
center_text('共同看见未来 · 看见真实样本 · 看见自己的位置', y3, f_slogan, GOLD)

out = base.convert('RGB')
out.save('/tmp/qifeng-poster-v4.png', 'PNG')
out.save('/tmp/qifeng-poster-v4.jpg', 'JPEG', quality=92)
print('七凤黄V4完成', out.size, '阿姨高', mh, '门店高', sh, '产品高', ph, '最后y', y3)
