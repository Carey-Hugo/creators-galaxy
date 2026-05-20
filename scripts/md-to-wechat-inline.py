#!/usr/bin/env python3
"""Markdown → WeChat inline-style HTML — CGHub 07篇专用"""
import re

P       = 'margin: 0 0 16px 0; font-size: 15px; line-height: 1.9; color: #333; font-family: -apple-system, "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif; text-align: justify;'
LEAD_P  = 'margin: 0 0 14px 0; font-size: 16px; line-height: 1.8; color: rgba(0,0,0,0.8); font-family: -apple-system, "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif;'
STRONG  = 'font-weight:700;color:#111'
H2_WRAP = 'background:#0d1828;border-radius:8px;padding:14px 18px;margin:28px 0 16px;'
H2_NUM  = 'margin:0 0 6px 0;font-size:10px;color:#4a9de8;letter-spacing:3px;text-transform:uppercase;font-weight:700;'
H2_TEXT = 'margin:0;font-size:18px;color:#dde8ff;font-weight:700;line-height:1.4;'
QUOTE   = 'background:#f9f6f0;border-left:3px solid #c09060;padding:16px 20px;margin:22px 0;'
QUOTE_P = 'margin:0;font-size:16px;color:#444;line-height:1.8;font-style:italic;'
BOOK    = 'margin:14px 0;padding:14px 18px;border-left:4px solid #576b95;background:#f7f7f7;font-size:15px;color:#555;line-height:1.8;font-family:-apple-system,"PingFang SC","Noto Sans SC","Microsoft YaHei",sans-serif;'
HR      = 'border:none;height:1px;background:linear-gradient(to right,transparent,#ddd,transparent);margin:28px 0;'
DIV_W   = 'display:flex;align-items:center;gap:16px;margin:36px 0;'
DIV_L   = 'flex:1;height:1px;background:linear-gradient(to right,transparent,#ddd,transparent);'
DIV_T   = 'font-size:10px;color:#aaa;letter-spacing:3px;text-transform:uppercase;'
INT_W   = 'background:#f0f6fc;border-radius:8px;padding:16px 20px;margin:24px 0;border:1px solid #d0e8ff;'
INT_P   = 'margin:0 0 8px 0;font-size:15px;color:#333;line-height:1.8;'
SERIES  = 'margin:14px 0;padding:14px 18px;border-left:4px solid #576b95;background:#f7f7f7;font-size:15px;color:#555;font-style:italic;line-height:1.8;font-family:-apple-system,"PingFang SC","Noto Sans SC","Microsoft YaHei",sans-serif;'
FOOTER  = 'margin:14px 0;padding:14px 18px;border-left:4px solid #576b95;background:#f7f7f7;font-size:15px;color:#555;line-height:1.8;font-family:-apple-system,"PingFang SC","Noto Sans SC","Microsoft YaHei",sans-serif;'
Q_W     = 'text-align:center;padding:24px 20px;margin:20px 0 0;'
Q_P1    = 'margin:0 0 10px 0;font-size:20px;font-weight:700;color:#0F4C81;line-height:1.5;'
Q_P2    = 'margin:0;font-size:13px;color:#888;line-height:1.8;'
GOLD_W  = 'background:#f9f6f0;border-left:3px solid #c09060;padding:18px 22px;margin:24px 0;border-radius:0 8px 8px 0;'
GOLD_L  = 'margin:0 0 8px 0;font-size:11px;color:#c09060;letter-spacing:2px;text-transform:uppercase;font-weight:700;'
GOLD_Q  = 'margin:0;font-size:17px;color:#444;line-height:1.7;font-weight:500;'

def mi(text):
    """Markdown inline: **bold**, \n → <br>"""
    text = re.sub(r'\*\*(.+?)\*\*', '<strong style="font-weight:700;color:#111">\\1</strong>', text)
    text = text.replace('\n', '<br>')
    return text

# ── 读取MD ──
with open("/home/ubuntu/creators-galaxy/docs/04-book-plan/07-传统分配的三个致命缺陷-定稿.md", encoding="utf-8") as f:
    md = f.read()

# 去掉front-matter
lines = md.split('\n')
md_lines = [l for l in lines if not (re.match(r'^>\s', l) or re.match(r'^#\s', l) or re.match(r'^---', l))]
md = '\n'.join(md_lines).strip()

# ── 解析blocks ──
blocks_raw = re.split(r'\n{2,}', md)
blocks = []
i = 0
while i < len(blocks_raw):
    b = blocks_raw[i].strip()
    if not b:
        i += 1
        continue
    # 检测金句标签 + 紧跟的blockquote
    gold_m = re.match(r'^(\*\*金句[一二三]：\*\*)\s*$', b)
    if gold_m and i+1 < len(blocks_raw):
        next_b = blocks_raw[i+1].strip()
        if next_b.startswith('>'):
            blocks.append(('GOLD', gold_m.group(1).replace('**',''), next_b.lstrip('>').strip()))
            i += 2
            continue
    blocks.append(('BLOCK', b))
    i += 1

output = []
for bt, b in blocks:
    if bt == 'GOLD':
        label = b[0]
        quote_text = b[1]
        output.append(
            '<div style="' + GOLD_W + '">'
            '<p style="' + GOLD_L + '">' + label + '</p>'
            '<p style="' + GOLD_Q + '">' + mi(quote_text) + '</p>'
            '</div>'
        )
        continue

    b = b.strip()
    if not b: continue

    # 分割线
    if re.match(r'^-{3,}$', b):
        output.append('<hr style="' + HR + '">')
        continue
    # CGHub分割文字
    if b == 'CGHub':
        output.append('<div style="' + DIV_W + '"><span style="' + DIV_L + '"></span><span style="' + DIV_T + '">CGHub</span><span style="' + DIV_L + '"></span></div>')
        continue
    # H2章节
    h2_m = re.match(r'^## (.+)$', b)
    if h2_m:
        title = h2_m.group(1).strip()
        if '：' in title:
            parts = title.split('：', 1)
            output.append('<div style="' + H2_WRAP + '"><p style="' + H2_NUM + '">' + parts[0].strip() + '</p><p style="' + H2_TEXT + '">' + mi(parts[1].strip()) + '</p></div>')
        else:
            output.append('<div style="' + H2_WRAP + '"><p style="' + H2_NUM + '"></p><p style="' + H2_TEXT + '">' + mi(title) + '</p></div>')
        continue
    # blockquote
    if b.startswith('>'):
        inner = re.sub(r'^>\s?', '', b, flags=re.MULTILINE)
        output.append('<div style="' + QUOTE + '"><p style="' + QUOTE_P + '">' + mi(inner) + '</p></div>')
        continue
    # 推荐阅读
    if '推荐阅读' in b and '《' in b:
        output.append('<div style="' + BOOK + '">' + mi(b) + '</div>')
        continue
    # 互动
    if '互动环节' in b:
        inner = b.replace('**互动环节**  ', '').strip()
        output.append('<div style="' + INT_W + '"><p style="' + INT_P + '">' + mi(inner) + '</p></div>')
        continue
    # 结尾
    if '关于本书与连载' in b:
        output.append('<div style="' + FOOTER + '">' + mi(b) + '</div>')
        continue
    # 普通段落
    output.append('<p style="' + P + '">' + mi(b) + '</p>')

body_html = '\n'.join(output)

footer_text = (
    '📖 <strong style="font-weight:700;color:#0F4C81">关于本书与连载</strong><br>'
    '这是《AI新时代，当机器人学会分配》第07篇连载。<br><br>'
    '上篇聊了分配权的历史从来不在普通人手里，这篇聊了传统分配的三个致命缺陷：不透明、中心化、可篡改——'
    '以及<strong style="font-weight:700;color:#0F4C81">破局的可能</strong>。<br><br>'
    '下篇，我们聊一个更具体的问题：区块链如何用代码重构分配规则，让机器第一次学会了"分配"——'
    '让技术为普通人服务，而不是为平台服务。<br><br>'
    '如果你认同我的观察、思考与探索实践，'
    '<strong style="font-weight:700;color:#0F4C81">欢迎关注本公众号</strong>，'
    '一起交流，一起成为同路人，一起创造那个更公平、更透明的未来。'
)

html = (
    '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n'
    '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    '<title>不透明、中心化、可篡改：AI时代如何破局？ · CGHub</title>\n</head>\n'
    '<body style="max-width:680px;margin:0 auto;padding:20px;font-family:-apple-system,\'PingFang SC\',\'Noto Sans SC\',\'Microsoft YaHei\',sans-serif;">\n\n'
    '<div style="' + SERIES + '">📖 公众号首发，本文为书籍《AI新时代，当机器人学会分配》<br>'
    '（AI生产力跃迁驱动新型生产关系变革——共同富裕探路者自组织实践）<br>第07篇连载</div>\n\n'
    '<p style="' + LEAD_P + '">'
    '上周，一个做外卖的朋友跟我说，他跑了三年，收入从八千降到五千。'
    '平台说"算法动态调整"。我说：这不是你的错，这是第一个坑——'
    '<strong style="font-weight:700;color:#111">不透明</strong>。'
    '但好消息是，这个坑，现在有办法填了。'
    '</p>\n\n'
    '<hr style="' + HR + '">\n\n'
    + body_html + '\n\n'
    '<div style="' + INT_W + '">'
    '<p style="' + INT_P + '">你有没有遇到过这三个坑？在评论区聊聊你的经历。</p>'
    '<p style="' + INT_P + '">如果觉得这篇文章给了你新的思路和希望，'
    '<strong style="font-weight:700;color:#111">转发</strong>给同样在寻找突破的朋友。</p>'
    '</div>\n\n'
    '<div style="' + Q_W + '">'
    '<p style="' + Q_P1 + '">你，现在在哪个坑里？</p>'
    '<p style="' + Q_P2 + '">是不透明的坑，不知道规则是什么？<br>'
    '是中心化的坑，没有发言权？<br>'
    '还是可篡改的坑，承诺随时可能被推翻？</p>'
    '</div>\n\n'
    '<hr style="' + HR + '">\n'
    '<div style="' + FOOTER + '">' + footer_text + '</div>\n'
    '</body>\n</html>'
)

out_path = '/home/ubuntu/creators-galaxy/docs/04-book-plan/07-公众号文章-inline排版.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Done, %d chars' % len(html))
