#!/bin/bash
# CGHub 仓库健康检查 · W3 文件名核验
# 用途：Hugo 看到"异常"时直接跑，看真实文件名

echo "🔍 CGHub 仓库健康检查 · $(date '+%Y-%m-%d %H:%M')"
echo "================================================================"

echo ""
echo "【1】本地文件系统（WSL）"
echo "----------------------------------------------------------------"
ls -1 /home/ubuntu/ai-web3-school-cghub/submissions/ 2>/dev/null | grep -E "W3-1[0-9]" || echo "  (无 W3-1x 文件)"

echo ""
echo "【2】GitHub 官方 API（最权威）"
echo "----------------------------------------------------------------"
curl -s "https://api.github.com/repos/Carey-Hugo/ai-web3-school-cghub/contents/submissions" 2>/dev/null | \
  python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for item in data:
        if item['name'].startswith('W3-') and 'hackathon' not in item['name']:
            print(f\"  ✅ {item['name']}  (sha: {item['sha'][:12]})\")
except Exception as e:
    print(f'  ERROR: {e}')
"

echo ""
echo "【3】Git 提交历史（最近 10 次）"
echo "----------------------------------------------------------------"
cd /home/ubuntu/ai-web3-school-cghub 2>/dev/null && \
  git log --oneline -10 2>/dev/null || echo "  (无法访问 git 仓库)"

echo ""
echo "📊 结论：以上 3 路结果应一致。如不一致，告诉我哪一路对，我立刻排查。"
