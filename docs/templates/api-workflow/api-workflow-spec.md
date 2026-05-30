# 创客星球CGHub微信公众号API工作流模板

## 核心信息
**AppID:** wx34cf0b6a53435a05
**AppSecret:** 6058c6ecdced8df42af3a3356eb045b7

**⚠️ 关键原则：**
1. **不要每次问AppID/AppSecret** - 应该主动查找并保存到memory
2. **用词务实** - 问题未解决前不说"完美"、"很好"等词
3. **承认错误** - 当排版不一致、封面图错误时，直接承认并立即修正
4. **提供解决方案** - 不要问"怎么办"，直接给出具体可执行的方案

## 完整工作流程图

```
✅ 文章定稿完成
↓
✅ HTML生成完成（基于520文章样式）
↓
✅ 封面图生成完成（1280×547，Logo合成）
↓
[开始API推送流程]

1. 获取access_token（每次必须重新获取）
2. 上传logo到微信图片CDN（uploadimg接口）
3. 上传封面图为永久素材（add_material?type=image）
4. 调用草稿箱接口（draft/add）
5. 验证草稿箱中出现文章
6. Git归档推送
```

## 故障排查流程图

```
❌ 文章不在草稿箱？
↓
[排查顺序]

1. 检查AppID/AppSecret是否正确
2. 重新获取access_token（可能过期）
3. 检查invalid media_id错误（创建新草稿而非更新）
4. 清理HTML控制字符导致JSON解码失败
5. 检查标题更改→封面必须重新上传
6. 检查IP白名单是否设置（43.130.52.123）
```

## 完整API推送脚本

```python
#!/usr/bin/env python3
"""
微信公众号草稿箱推送脚本
包含完整故障排查和优化
"""

import os
import sys
import json
import re
import requests
from pathlib import Path

class WeChatPublisher:
    def __init__(self):
        # 核心凭证
        self.appid = "wx34cf0b6a53435a05"
        self.appsecret = "6058c8e6cdced8df42af3a3356eb045b7"
        
        # API端点
        self.token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.appid}&secret={self.appsecret}"
        self.upload_img_url = "https://api.weixin.qq.com/cgi-bin/media/uploadimg"
        self.add_material_url = "https://api.weixin.qq.com/cgi-bin/material/add_material"
        self.add_draft_url = "https://api.weixin.qq.com/cgi-bin/draft/add"
        self.delete_draft_url = "https://api.weixin.qq.com/cgi-bin/draft/delete"
        
    def get_access_token(self):
        """获取access_token"""
        print("获取access_token...")
        response = requests.get(self.token_url, timeout=30)
        
        if response.status_code != 200:
            print(f"HTTP错误: {response.status_code}")
            return None
        
        data = response.json()
        if 'access_token' in data:
            token = data['access_token']
            expires_in = data.get('expires_in', 7200)
            print(f"✅ token获取成功，有效期: {expires_in}秒")
            return token
        else:
            print(f"❌ API错误: {data}")
            if data.get('errmsg') == "invalid ip":
                print("⚠️ 需要添加IP白名单: 43.130.52.123")
                print("操作路径: 公众号后台 → 设置与开发 → 基本配置 → IP白名单")
            return None
    
    def upload_logo_to_cdn(self, access_token):
        """上传logo到微信图片CDN"""
        logo_path = "/home/ubuntu/creators-galaxy/docs/00-brand/cghub-logo-official.png"
        
        if not os.path.exists(logo_path):
            print(f"❌ logo文件不存在: {logo_path}")
            return None
        
        print(f"上传logo到CDN...")
        url = f"{self.upload_img_url}?access_token={access_token}"
        
        try:
            with open(logo_path, 'rb') as f:
                files = {"media": ("cghub-logo.png", f, "image/png")}
                response = requests.post(url, files=files, timeout=30)
            
            data = response.json()
            if 'url' in data:
                logo_url = data['url']
                print(f"✅ logo上传成功: {logo_url}")
                return logo_url
            else:
                print(f"❌ logo上传失败: {data}")
                return None
        except Exception as e:
            print(f"❌ logo上传异常: {e}")
            return None
    
    def upload_cover_as_material(self, access_token, cover_path):
        """上传封面图为永久素材"""
        if not os.path.exists(cover_path):
            print(f"❌ 封面图不存在: {cover_path}")
            return None
        
        print(f"上传封面图为永久素材...")
        url = f"{self.add_material_url}?access_token={access_token}&type=image"
        
        try:
            with open(cover_path, 'rb') as f:
                files = {"media": ("article-cover.png", f, "image/png")}
                response = requests.post(url, files=files, timeout=30)
            
            data = response.json()
            if 'media_id' in data:
                media_id = data['media_id']
                media_url = data.get('url', '')
                print(f"✅ 封面图上传成功")
                print(f"   media_id: {media_id}")
                print(f"   media_url: {media_url}")
                return media_id
            else:
                print(f"❌ 封面图上传失败: {data}")
                return None
        except Exception as e:
            print(f"❌ 封面图上传异常: {e}")
            return None
    
    def clean_html_content(self, html_content):
        """清理HTML中的控制字符"""
        # 移除控制字符（除了制表符、换行、回车）
        cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', html_content)
        
        # 移除可能导致JSON问题的特殊字符
        cleaned = cleaned.replace('\u2028', '').replace('\u2029', '').replace('\ufeff', '')
        
        print(f"HTML清理完成: 原始{len(html_content)}字符 → 清理后{len(cleaned)}字符")
        return cleaned
    
    def create_draft(self, access_token, title, html_content, thumb_media_id):
        """创建草稿"""
        print(f"创建草稿: '{title}'")
        
        # 清理HTML内容
        cleaned_html = self.clean_html_content(html_content)
        
        # 构建草稿数据
        draft_data = {
            "title": title,
            "author": "Hugo",
            "digest": f"AI新时代的生产关系变革探讨",
            "content": cleaned_html,
            "content_source_url": "",
            "thumb_media_id": thumb_media_id
        }
        
        url = f"{self.add_draft_url}?access_token={access_token}"
        
        # ⚠️ 关键：中文必须不转义，否则微信服务器会误判标题长度
        try:
            response = requests.post(
                url,
                data=json.dumps(draft_data, ensure_ascii=False).encode("utf-8"),
                headers={"Content-Type": "application/json; charset=utf-8"},
                timeout=30
            )
            
            data = response.json()
            
            if 'media_id' in data:
                draft_media_id = data['media_id']
                print(f"✅ 草稿创建成功")
                print(f"   draft_media_id: {draft_media_id}")
                return draft_media_id
            else:
                print(f"❌ 草稿创建失败: {data}")
                
                # 错误分析
                errcode = data.get('errcode')
                errmsg = data.get('errmsg')
                
                if errcode == 40007:
                    print("⚠️ invalid media_id: 封面图media_id无效，需要重新上传封面图")
                elif errcode == 45003:
                    print("⚠️ title size out of limit: 标题可能包含转义字符，请确保中文不转义")
                elif errcode == 45009:
                    print("⚠️ API调用频率过高，稍后重试")
                
                return None
        except Exception as e:
            print(f"❌ 草稿创建异常: {e}")
            return None
    
    def delete_draft(self, access_token, media_id):
        """删除草稿"""
        print(f"删除草稿: {media_id}")
        
        url = f"{self.delete_draft_url}?access_token={access_token}"
        
        try:
            response = requests.post(
                url,
                data=json.dumps({"media_id": media_id}, ensure_ascii=False).encode("utf-8"),
                headers={"Content-Type": "application/json; charset=utf-8"},
                timeout=30
            )
            
            data = response.json()
            if data.get('errcode') == 0:
                print(f"✅ 草稿删除成功")
                return True
            else:
                print(f"❌ 草稿删除失败: {data}")
                return False
        except Exception as e:
            print(f"❌ 草稿删除异常: {e}")
            return False
    
    def publish_article(self, title, html_file_path, cover_path):
        """完整发布流程"""
        print(f"开始发布文章: '{title}'")
        
        # 1. 获取access_token
        access_token = self.get_access_token()
        if not access_token:
            return False
        
        # 2. 上传logo到CDN（供HTML内嵌）
        logo_url = self.upload_logo_to_cdn(access_token)
        if logo_url:
            # 在HTML中替换logo路径
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            html_content = html_content.replace('LOCAL_LOGO_PATH', logo_url)
            print(f"✅ logo路径更新完成")
        else:
            print("⚠️ logo上传失败，使用默认HTML")
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
        
        # 3. 上传封面图为永久素材
        thumb_media_id = self.upload_cover_as_material(access_token, cover_path)
        if not thumb_media_id:
            print("❌ 封面图上传失败，无法创建草稿")
            return False
        
        # 4. 创建草稿
        draft_media_id = self.create_draft(access_token, title, html_content, thumb_media_id)
        if not draft_media_id:
            print("❌ 草稿创建失败")
            return False
        
        print(f"🎉 文章推送完成!")
        print(f"   文章标题: {title}")
        print(f"   草稿media_id: {draft_media_id}")
        print(f"   IP白名单已确认: 43.130.52.123")
        
        return True
    
    def test_api_connection(self):
        """测试API连接"""
        print("测试微信公众号API连接...")
        
        response = requests.get(self.token_url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if 'access_token' in data:
                print("✅ 微信公众号API连接成功")
                return True
            else:
                print(f"❌ API错误: {data}")
                if data.get('errmsg') == "invalid ip":
                    print("⚠️ 需要添加IP白名单: 43.130.52.123")
                    print("操作路径: 公众号后台 → 设置与开发 → 基本配置 → IP白名单")
                return False
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            return False

def main():
    """命令行入口"""
    publisher = WeChatPublisher()
    
    if len(sys.argv) < 4:
        print("用法:")
        print("  python3 wechat_publisher.py \"文章标题\" \"HTML文件路径\" \"封面图路径\"")
        print("  python3 wechat_publisher.py --test")
        print("  python3 wechat_publisher.py --delete <media_id>")
        print("\n示例:")
        print("  python3 wechat_publisher.py \"不透明、中心化、可篡改\" \"07-公众号文章.html\" \"07-传统分配-cover-final.png\"")
        return
    
    if sys.argv[1] == "--test":
        success = publisher.test_api_connection()
        sys.exit(0 if success else 1)
    
    elif sys.argv[1] == "--delete":
        if len(sys.argv) < 3:
            print("删除草稿需要media_id")
            return
        
        access_token = publisher.get_access_token()
        if access_token:
            publisher.delete_draft(access_token, sys.argv[2])
        return
    
    else:
        title = sys.argv[1]
        html_path = sys.argv[2]
        cover_path = sys.argv[3]
        
        success = publisher.publish_article(title, html_path, cover_path)
        
        if success:
            print("\n✅ 发布流程成功完成!")
            print("请前往微信公众号后台草稿箱查看")
        else:
            print("\n❌ 发布流程失败")
            print("请检查:")
            print("1. AppID/AppSecret是否正确")
            print("2. IP白名单是否设置")
            print("3. 封面图media_id是否有效")
            print("4. HTML内容是否包含控制字符")

if __name__ == "__main__":
    main()
```

## 弯路总结与优化方案

### 弯路总结
1. **access_token过期**：每次推送必须重新获取，不能复用
2. **invalid media_id错误**：旧草稿的media_id失效，需创建新草稿而非更新
3. **HTML控制字符**：导致JSON解码失败，必须清理
4. **中文转义问题**：requests.post(json=payload)会把中文转义为`\\u5206\\u914d`，微信服务器误判为字段超长，报`45003 title size out of limit`
5. **封面图同步**：标题改了封面必须重新生成并上传
6. **IP白名单**：必须添加`43.130.52.123`到公众号后台

### 优化方案
#### 1. 标准化access_token获取
```python
# 每次推送前必须重新获取
ACCESS_TOKEN=$(curl -s "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx34cf0b6a53435a05&secret=6058c6ecdced8df42af3a3356eb045b7" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
```

#### 2. 正确的JSON编码方式
```python
# ⚠️ 必须使用ensure_ascii=False，中文不转义
import json, requests
r = requests.post(
    url,
    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
    headers={"Content-Type": "application/json; charset=utf-8"}
)
```

#### 3. HTML控制字符清理
```python
import re
content = re.sub(r'[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f\\x7f]', '', content)
```

#### 4. 封面图同步机制
```bash
# 1. 重新生成封面图（同比例1280×547）
# 2. 重新上传为永久素材
curl -F "media=@new_cover.png" "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=$ACCESS_TOKEN&type=image"
# 3. 获取新media_id用于新草稿
```

## 故障排查指令集

### 找回AppID/AppSecret
```bash
# 查找已保存的微信凭证
grep -n "AppID\\|AppSecret" ~/creators-galaxy/AGENT_MEMORY_创客星球对话记录.md
```

### 重新获取access_token
```bash
ACCESS_TOKEN=$(curl -s "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx34cf0b6a53435a05&secret=6058c6ecdced8df42af3a3356eb045b7" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
echo "新token: $ACCESS_TOKEN"
```

### 测试API连接
```bash
python3 wechat_publisher.py --test
```

### 清理旧草稿
```bash
python3 wechat_publisher.py --delete "旧的media_id"
```

### 查看草稿箱
```bash
# 无法直接查看，需要登录公众号后台
# 推送成功后，提醒用户登录后台查看
```

## 排版一致性修复流程

### 获取用户定时发表文章的HTML源码
1. **用户提供完整HTML源码**：右键文章页面→"查看页面源代码"→复制整个HTML
2. **分析HTML结构**：
```python
import re

with open('520-article.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 提取段落样式
paragraph_styles = re.findall(r'<p[^>]* style="([^"]*)">', html_content)
# 提取标题样式
title_styles = re.findall(r'<p data-pm-slice[^>]* style="([^"]*)">', html_content)
```

3. **重建新文章HTML**：
   - 完全复制520文章的段落样式：`margin: 0 0 14px 0; font-size: 15px; line-height: 1.9; color: #333; font-family: -apple-system...`
   - 完全复制520文章的标题样式：`margin: 12px 0px; font-size: 17px; color: rgba(0, 0, 0, 0.9);`
   - **不自作主张优化排版**，严格复制用户样式

4. **验证与推送**：
   - 生成预览让用户确认
   - 确认无误后推送

## Git归档规范
```bash
cd ~/creators-galaxy
git add -A
git commit -m "feat: 第0X篇公众号定稿-[文章主题]-[关键词]"
git push origin main
```

**⚠️ 只推送到 `origin`（Gitee），不推GitHub**

## 模板文件结构
```
docs/templates/api-workflow/
├── wechat-publisher.py                  # 完整的推送脚本
├── api-workflow-spec.md                 # 本文件
├── troubleshooting-guide.md             # 故障排查指南
├── ip-whitelist-instructions.md        # IP白名单设置指南
├── html-cleanup-script.py              # HTML清理脚本
├── logo-sync-guidelines.md             # Logo同步指南
└── git-commit-template.md              # Git提交模板
```

---
*最后更新：2026-05-19*
*版本：V1.0*