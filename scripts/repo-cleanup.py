#!/usr/bin/env python3
"""
知识库清理扫描脚本（只扫描、不删除）
用途：定期扫描 ~/creators-galaxy，生成清理建议报告发给你确认
每月1日 09:00 执行，报告发到 Telegram
"""

import os
import re
from pathlib import Path
from datetime import datetime

REPO = Path(os.environ.get("REPO_PATH", "/home/ubuntu/creators-galaxy"))

# ========== 保护清单：这些文件/目录不列入删除候选 ==========
# 规则：精确匹配关键文件；目录保护子目录内容
PROTECTED_EXACT = {
    "docs/00-brand/wechat-article-style-guide.md",
    "docs/00-brand/wechat-article-template.html",
    "docs/00-brand/wechat-article-serial-template.html",
    "docs/00-brand/logo-v1-square-clean.png",
    "docs/00-brand/logo-v2-horizontal-clean.png",
    "docs/04-book-plan/main-agent-protocol.md",
    "docs/04-book-plan/conversation-index.md",
    "docs/04-book-plan/CGHub-当前上下文同步.md",
    "docs/04-book-plan/content-serialization-plan.md",
    "scripts/repo-cleanup.py",
}

PROTECTED_PREFIXES = [
    "docs/04-book-plan/0",   # 书籍连载文件 01-xx.md, 02-xx.md...
    "docs/04-book-plan/1",
    "docs/04-book-plan/conversation-",  # conversation 历史归档
    "docs/00-brand/logo",
    "docs/04-content-strategy/",
    "content/",
    "demo/",
]

def is_protected(rel_path):
    """判断路径是否受保护"""
    rel = rel_path.replace("\\", "/")
    # 精确匹配
    if rel in PROTECTED_EXACT:
        return True
    # 前缀匹配
    for prefix in PROTECTED_PREFIXES:
        if rel.startswith(prefix):
            return True
    # conversation-*.md 全部保护
    if re.match(r"^docs/04-book-plan/conversation-\d{4}-\d{2}-\d{2}\.md$", rel):
        return True
    return False

def scan():
    candidates = []  # (index, path, reason, size_kb)

    def add(path, reason, size_kb=0):
        rel = str(Path(path).relative_to(REPO))
        if not is_protected(rel):
            candidates.append((len(candidates) + 1, rel, reason, size_kb))

    # ========== 规则1：多版本 HTML 预览文件 ==========
    version_suffixes = [
        r"-inline版?", r"-inline排版", r"-v\d+-inline版",
        r"-排版\.html", r"-520排版", r"-增强版", r"-修正",
        r"-文章预览", r"-公众号发布版", r"-hot\.html",
    ]
    version_pattern = re.compile(
        r"^(\d{2}-.*?)(" + "|".join(version_suffixes) + r")(\.md|\.html)$"
    )

    for scan_dir in [REPO / "docs/04-book-plan", REPO / "docs/00-brand"]:
        if not scan_dir.exists():
            continue
        for f in scan_dir.iterdir():
            if f.is_file() and version_pattern.match(f.name):
                rel = str(f.relative_to(REPO))
                if not is_protected(rel):
                    add(f, "多版本HTML预览文件（已定稿后遗留）", f.stat().st_size // 1024)

    # ========== 规则2：theme-previews 调试目录 ==========
    tp_dir = REPO / "docs/04-book-plan/theme-previews"
    if tp_dir.exists():
        files = list(tp_dir.glob("*.html"))
        if files:
            total = sum(f.stat().st_size for f in files) // 1024
            add(tp_dir, f"调试预览目录（含{len(files)}个HTML，约{total}KB）", total)

    # ========== 规则3：空目录（与保护目录冲突时优先保留）==========
    protected_prefixes = tuple(p.replace("/", "") for p in PROTECTED_PREFIXES)
    for dirpath, subdirs, files in os.walk(REPO):
        dirpath = Path(dirpath)
        rel = str(dirpath.relative_to(REPO))
        # 跳过 .git node_modules demo 等系统目录
        parts = rel.split("/")
        if any(p in parts for p in [".git", "node_modules", "demo", "coverage", "cache", "test"]):
            continue
        # 跳过已保护的前缀
        if any(rel.startswith(p.replace("/", "")) for p in PROTECTED_PREFIXES if p.endswith("/")):
            continue
        if is_protected(rel):
            continue
        # 仅当目录完全为空且非刻意保留时列入
        if not subdirs and not files:
            add(dirpath, "空目录", 0)

    # ========== 规则4：超大文件（>10MB，非保护类）==========
    for f in REPO.rglob("*"):
        if not f.is_file():
            continue
        rel = str(f.relative_to(REPO))
        if is_protected(rel):
            continue
        parts = rel.split("/")
        if any(p in parts for p in [".git", "node_modules", "demo", "coverage", "cache"]):
            continue
        size_mb = f.stat().st_size / 1024 / 1024
        if size_mb > 10:
            add(f, f"超大文件（{size_mb:.1f}MB）", f.stat().st_size // 1024)

    # ========== 生成报告 ==========
    lines = []
    lines.append(f"🧹 CGHub 知识库月度清理报告")
    lines.append(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 56)

    if not candidates:
        lines.append("")
        lines.append("✅ 知识库状态良好，未发现冗余文件")
        lines.append("")
        lines.append("📌 说明：")
        lines.append("  • 书籍连载、战略框架、规范模板已纳入保护清单")
        lines.append("  • conversation 历史归档已纳入保护清单")
        lines.append("  • 大文件（>10MB）仅在非保护类时列出")
    else:
        lines.append(f"📋 共发现 {len(candidates)} 个待清理项目：")
        lines.append("")

        for idx, path, reason, size in candidates:
            if path.endswith("/"):
                lines.append(f"  [{idx}] 📁 {path}  — {reason}")
            elif size > 0:
                lines.append(f"  [{idx}] 🗑️ {path}  ({reason}, {size}KB)")
            else:
                lines.append(f"  [{idx}] 🗑️ {path}  ({reason})")

        lines.append("")
        lines.append("=" * 56)
        lines.append("💡 操作指引：")
        lines.append("  回复格式示例：")
        lines.append("    1,3,7     → 删除第1、3、7项")
        lines.append("    1-6       → 删除第1到第6项")
        lines.append("    all       → 删除全部")
        lines.append("    skip      → 跳过本次清理")
        lines.append("")
        lines.append("⚠️ 书籍连载、战略框架、conversation归档不会被列入")

    return "\n".join(lines)

if __name__ == "__main__":
    print(scan())