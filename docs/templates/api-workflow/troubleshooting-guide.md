# 微信公众号API故障排查指南

## 快速诊断流程图

```
❌ 文章不在草稿箱？
│
├─▶ 检查AppID/AppSecret
│   ├─▶ 正确 → 下一步
│   └─▶ 错误 → 重新配置
│
├─▶ 检查access_token是否过期
│   ├─▶ 过期 → 重新获取
│   └─▶ 有效 → 下一步
│
├─▶ 检查invalid media_id错误
│   ├─▶ 存在 → 创建新草稿而非更新
│   └─▶ 不存在 → 下一步
│
├─▶ 检查HTML控制字符
│   ├─▶ 有问题 → 清理控制字符
│   └─▶ 正常 → 下一步
│
├─▶ 检查IP白名单
│   ├─▶ 未设置 → 添加43.130.52.123
│   └─▶ 已设置 → 下一步
│
└─▶ 检查封面图与标题同步
    ├─▶ 不同步 → 重新生成封面并上传
    └─▶ 同步 → 联系技术支持
```

## 详细排查步骤

### 1. 检查AppID/AppSecret
```bash
# 查找已保存的微信凭证
grep -n "AppID\\|AppSecret" ~/creators-galaxy/AGENT_MEMORY_创客星球对话记录.md

# 或直接使用已知值
AppID: wx34cf0b6a53435a05
AppSecret: 6058c6ecdced8df42af3a3356eb045b7
```

**关键：** 一旦找到AppID/AppSecret，立即保存到memory，以后不再问用户。

### 2. 重新获取access_token
```bash
ACCESS_TOKEN=$(curl -s "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx34cf0b6a53435a05&secret=6058c6ecdced8df42af3a3356eb045b7" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
echo "新token: $ACCESS_TOKEN"
```

**注意：** access_token 2小时过期，每次推送前必须重新获取，不能复用上次的。

### 3. 处理invalid media_id错误
当API返回 `{"errcode":40007,"errmsg":"invalid media_id"}`：

**问题原因：**
- 旧草稿的 `media_id` 已失效
- 尝试更新不存在的草稿

**解决方案：**
```python
# 不要尝试更新旧草稿，直接创建新草稿
# 使用 POST /cgi-bin/draft/add 而不是 update
# 所有旧media_id作废，重新上传封面图获取新media_id
```

### 4. HTML控制字符导致JSON解码失败
```python
import re
import json

def clean_html_for_wechat(html_content):
    """清理HTML中的控制字符"""
    # 移除控制字符（除了制表符、换行、回车）
    cleaned = re.sub(r'[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f\\x7f]', '', html_content)
    
    # 移除可能导致JSON问题的特殊字符
    cleaned = cleaned.replace('\u2028', '').replace('\u2029', '').replace('\ufeff', '')
    
    # 确保中文不转义
    return cleaned

# 使用方式
with open('article.html', 'r', encoding='utf-8') as f:
    content = f.read()
    clean_content = clean_html_for_wechat(content)

# 构建草稿数据时直接用清理后的内容
draft_data = {
    "title": "文章标题",
    "author": "Hugo",
    "digest": "摘要",
    "content": clean_content,  # 使用清理后的内容
    "content_source_url": "",
    "thumb_media_id": thumb_media_id
}

# ⚠️ 关键：中文必须不转义
import requests
r = requests.post(
    url,
    data=json.dumps(draft_data, ensure_ascii=False).encode("utf-8"),
    headers={"Content-Type": "application/json; charset=utf-8"}
)
```

### 5. 标题更改→封面必须同步
```bash
# 1. 重新生成封面图（同比例1280×547）
# 2. 重新上传为永久素材
curl -F "media=@new_cover.png" "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=$ACCESS_TOKEN&type=image"
# 3. 获取新media_id用于新草稿
```

**关键教训：** 封面图标题必须与文章标题完全一致。用户明确要求"封面图必须与标题同步，标题改了封面必须重新生成，不能有旧标题元素"。

### 6. IP白名单设置
```bash
# 测试API连接
python3 wechat_publisher.py --test

# 如果返回 "invalid ip" 错误
echo "需要添加IP白名单: 43.130.52.123"
echo "操作路径: 公众号后台 → 设置与开发 → 基本配置 → IP白名单 → 添加 43.130.52.123"
```

## 常见错误代码及解决方案

### 40007: invalid media_id
**原因：** 媒体文件media_id无效
**解决方案：**
1. 重新上传封面图获取新的media_id
2. 创建新草稿而非更新旧草稿

### 45003: title size out of limit
**原因：** 标题长度超过限制或包含转义字符
**解决方案：**
1. 确保标题不超过64个字符
2. 使用 `ensure_ascii=False` 避免中文转义

### 45009: API freq out of limit
**原因：** API调用频率过高
**解决方案：** 等待5分钟后重试

### 40001: invalid credential
**原因：** access_token无效或已过期
**解决方案：** 重新获取access_token

### 40003: invalid openid
**原因：** 不合法的OpenID
**解决方案：** 检查用户是否已关注公众号

### 40004: invalid media type
**原因：** 不合法的媒体文件类型
**解决方案：** 确保封面图为PNG/JPG格式，且使用 `type=image` 而非 `type=thumb`

## 调试脚本

```python
#!/usr/bin/env python3
"""
微信公众号API调试脚本
"""

import requests
import json

def debug_api_connection():
    """调试API连接"""
    appid = "wx34cf0b6a53435a05"
    appsecret = "6058c6ecdced8df42af3a3356eb045b7"
    
    # 1. 测试token获取
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}"
    response = requests.get(token_url, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        if 'access_token' in data:
            token = data['access_token']
            print(f"✅ Token获取成功: {token[:20]}...")
            
            # 2. 测试素材上传
            cover_path = "test_cover.png"
            if os.path.exists(cover_path):
                upload_url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
                with open(cover_path, 'rb') as f:
                    files = {"media": ("test.png", f, "image/png")}
                    upload_response = requests.post(upload_url, files=files, timeout=30)
                
                upload_data = upload_response.json()
                if 'media_id' in upload_data:
                    print(f"✅ 素材上传成功: media_id={upload_data['media_id'][:20]}...")
                else:
                    print(f"❌ 素材上传失败: {upload_data}")
            else:
                print("⚠️ 测试封面图不存在，跳过素材上传测试")
            
            # 3. 测试草稿创建
            test_draft = {
                "title": "测试文章标题",
                "author": "Hugo",
                "digest": "测试摘要",
                "content": "<p>测试内容</p>",
                "content_source_url": "",
                "thumb_media_id": "test_media_id"
            }
            
            draft_url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
            draft_response = requests.post(
                draft_url,
                data=json.dumps(test_draft, ensure_ascii=False).encode("utf-8"),
                headers={"Content-Type": "application/json; charset=utf-8"},
                timeout=30
            )
            
            draft_data = draft_response.json()
            if 'media_id' in draft_data:
                print(f"✅ 草稿创建成功: media_id={draft_data['media_id'][:20]}...")
            else:
                print(f"❌ 草稿创建失败: {draft_data}")
                
        else:
            print(f"❌ Token获取失败: {data}")
            if data.get('errmsg') == "invalid ip":
                print("⚠️ 需要添加IP白名单: 43.130.52.123")
    else:
        print(f"❌ HTTP错误: {response.status_code}")

if __name__ == "__main__":
    debug_api_connection()
```

## 预防措施

### 1. 标准化工作流
```bash
# 每次推送前执行
cd ~/creators-galaxy
python3 docs/templates/api-workflow/wechat_publisher.py --test
```

### 2. 定期清理旧草稿
```python
# 定期清理无效的草稿
def cleanup_old_drafts(access_token):
    """清理旧的无效草稿"""
    # 获取草稿列表
    list_url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={access_token}"
    response = requests.post(list_url, json={"offset": 0, "count": 20})
    
    if response.status_code == 200:
        drafts = response.json().get('item', [])
        for draft in drafts:
            media_id = draft.get('media_id')
            title = draft.get('content', {}).get('news_item', [{}])[0].get('title', '')
            print(f"草稿: {title[:30]}... (media_id: {media_id[:20]}...)")
```

### 3. 备份关键数据
```bash
# 备份AppID/AppSecret
echo "AppID: wx34cf0b6a53435a05" >> ~/creators-galaxy/wechat_credentials_backup.txt
echo "AppSecret: 6058c6ecdced8df42af3a3356eb045b7" >> ~/creators-galaxy/wechat_credentials_backup.txt
echo "IP白名单: 43.130.52.123" >> ~/creators-galaxy/wechat_credentials_backup.txt
```

### 4. 监控日志
```bash
# 查看推送日志
tail -f ~/creators-galaxy/wechat_publish.log

# 记录推送历史
echo "$(date): 推送文章《$TITLE》成功" >> ~/creators-galaxy/wechat_publish_history.log
```

## 紧急恢复流程

### 情况1：access_token失效
```bash
# 立即重新获取token
ACCESS_TOKEN=$(curl -s "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx34cf0b6a53435a05&secret=6058c6ecdced8df42af3a3356eb045b7" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

# 测试token有效性
curl -s "https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token=$ACCESS_TOKEN"
```

### 情况2：封面图media_id失效
```bash
# 重新上传封面图
python3 docs/templates/api-workflow/wechat_publisher.py "文章标题" "文章HTML" "新封面图.png"
```

### 情况3：HTML格式错误
```python
# 使用清理脚本
python3 docs/templates/api-workflow/html_cleaner.py "原始HTML.html" "清理后HTML.html"
```

### 情况4：IP白名单未设置
```
立即登录微信公众号后台：
1. 设置与开发 → 基本配置
2. IP白名单 → 添加IP
3. 添加: 43.130.52.123
4. 保存
5. 等待5分钟生效
```

## 最佳实践

### 1. 每次推送前
- [ ] 测试API连接
- [ ] 检查IP白名单
- [ ] 重新获取access_token
- [ ] 清理HTML控制字符
- [ ] 确认封面图与标题同步

### 2. 推送成功后
- [ ] 验证草稿箱中出现文章
- [ ] 记录推送日志
- [ ] Git归档
- [ ] 备份关键数据

### 3. 定期维护
- [ ] 清理无效草稿
- [ ] 更新IP白名单
- [ ] 备份凭证
- [ ] 检查日志错误

---
*最后更新：2026-05-19*
*版本：V1.0*