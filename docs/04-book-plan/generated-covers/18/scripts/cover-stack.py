"""v5 v2: 修复关键词位置 — 全部水平（不旋转），调整到不在马斯克剪影和金字塔裂光柱上"""
from PIL import Image, ImageDraw, ImageFont

FONT_HEI = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
FONT_FALLBACK = "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"

base = Image.open("/home/ubuntu/creators-galaxy/docs/04-book-plan/generated-covers/18/18-cover-base-v5-nocracked.png").convert("RGBA")
W, H = base.size  # 1918x820

overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

WHITE = (255, 255, 255, 255)
GOLD = (212, 168, 67, 255)
GOLD_SOFT = (212, 168, 67, 200)
GOLD_DIM = (212, 168, 67, 140)
GOLD_FAINT = (212, 168, 67, 100)

# === 主标题 LINE 1: 马斯克预言的全民高收入 ===
line1 = "马斯克预言的全民高收入"
font_l1 = ImageFont.truetype(FONT_FALLBACK, 92)
bbox = draw.textbbox((0, 0), line1, font=font_l1)
tw = bbox[2] - bbox[0]
x1 = (W - tw) // 2
y1 = 215
# 暖色微阴影
draw.text((x1+2, y1+3), line1, font=font_l1, fill=(140, 100, 30, 100))
# 纯白
draw.text((x1, y1), line1, font=font_l1, fill=WHITE)

# === 主标题 LINE 2: 绕不开财富该如何分配这道坎 ===
line2 = "躲不开财富该如何分配这道坎"
font_l2 = ImageFont.truetype(FONT_FALLBACK, 60)
bbox = draw.textbbox((0, 0), line2, font=font_l2)
tw2 = bbox[2] - bbox[0]
x2 = (W - tw2) // 2
y2 = y1 + 110
draw.text((x2+1, y2+2), line2, font=font_l2, fill=(140, 100, 30, 90))
draw.text((x2, y2), line2, font=font_l2, fill=WHITE)

# === 副标题 ===
subtitle = "算法封建  ·  技术利维坦  ·  第三条路  ·  分配问题的答案在规律手里"
font_sub = ImageFont.truetype(FONT_HEI, 26)
bbox = draw.textbbox((0, 0), subtitle, font=font_sub)
tw3 = bbox[2] - bbox[0]
x3 = (W - tw3) // 2
y3 = y2 + 90
draw.text((x3, y3), subtitle, font=font_sub, fill=GOLD_SOFT)

# === 8 关键词（完全不旋转，全部水平）===
# 避让马斯克剪影（≈ x 820-1100, y 50-180）
# 避让主标题区（≈ y 200-460）
# 避让副标题（≈ y 405-440）
# 避让金字塔裂光柱（≈ x 940-980, y 480-700 中央狭长）
# 避让 logo 区（≈ x 1775+, y 677+）

kw_l = ImageFont.truetype(FONT_HEI, 32)  # 大号
kw_m = ImageFont.truetype(FONT_HEI, 26)  # 中号
kw_s = ImageFont.truetype(FONT_HEI, 22)  # 小号

keywords = [
    # 顶部左侧（马斯克剪影左）
    ("全民高收入",    100,  50, kw_s,  GOLD_DIM),
    # 顶部右侧（马斯克剪影右）
    ("第三条路",      1480, 60, kw_s,  GOLD_DIM),
    # 左侧中部（主标题左侧空白）
    ("财富分配",      50,  300, kw_m,  GOLD_SOFT),
    # 右侧中部
    ("算法封建",      1620, 295, kw_m,  GOLD_SOFT),
    # 左侧下半（避开裂光柱左侧）
    ("技术利维坦",    50,  500, kw_m,  GOLD_SOFT),
    # 右侧下半（裂光柱右侧）
    ("规则写进代码",  1450, 510, kw_m,  GOLD_SOFT),
    # 顶部正中间上方（马斯克剪影上方留白）
    ("顺势而为",      820,  10, kw_s,  GOLD_DIM),
    # 右下上（logo 上方）
    ("共同富裕",      1620, 660, kw_s,  GOLD_DIM),
]

for (text, x, y, font, color) in keywords:
    draw.text((x, y), text, font=font, fill=color)

final = Image.alpha_composite(base, overlay)

# logo 合成
LOGO_PATH = "/home/ubuntu/creators-galaxy/docs/00-brand/logo-v1-square-clean.png"
logo = Image.open(LOGO_PATH).convert("RGBA")
logo_target_size = 115
logo_resized = logo.resize((logo_target_size, logo_target_size), Image.LANCZOS)
margin = 28
lx = W - logo_target_size - margin
ly = H - logo_target_size - margin
final.paste(logo_resized, (lx, ly), logo_resized)

final.convert("RGB").save("/home/ubuntu/creators-galaxy/docs/04-book-plan/generated-covers/18/18-cover-final.png", "PNG", optimize=True)

final_thumb = final.copy()
final_thumb.thumbnail((960, 410))
final_thumb.save("/tmp/cover18-review/v5-final-v2-thumb.png", optimize=True)

print(f"Saved final v2")
print(f"Logo at ({lx}, {ly})")
