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
        self.appsecret = "6058c6ecdced8df42af3a3356eb045b7"
        
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
        
        # 确保HTML有完整结构（微信API要求）
        if not cleaned_html.strip().startswith('<html'):
            cleaned_html = '<html><body>' + cleaned_html
        if not cleaned_html.strip().endswith('</html>'):
            cleaned_html = cleaned_html + '</body></html>'
        
        # 构建草稿数据（微信API正确格式：articles数组）
        draft_data = {
            "articles": [{
                "title": title,
                "author": "Hugo",
                "digest": f"AI新时代的生产关系变革探讨",
                "content": cleaned_html,
                "content_source_url": "",
                "thumb_media_id": thumb_media_id
            }]
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