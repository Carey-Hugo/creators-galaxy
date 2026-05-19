#!/usr/bin/env python3
"""
微信公众号草稿箱推送脚本
"""

import os
import requests
import json
import sys
from pathlib import Path

# 微信公众号配置
WECHAT_APPID = os.getenv('WECHAT_APPID')
WECHAT_APPSECRET = os.getenv('WECHAT_APPSECRET')

if not WECHAT_APPID or not WECHAT_APPSECRET:
    print("⚠️ 请设置环境变量:")
    print("export WECHAT_APPID='你的微信公众号AppID'")
    print("export WECHAT_APPSECRET='你的微信公众号AppSecret'")
    sys.exit(1)

class WechatDraftPublisher:
    def __init__(self):
        self.appid = WECHAT_APPID
        self.appsecret = WECHAT_APPSECRET
        self.access_token = None
    
    def get_access_token(self):
        """获取微信公众号access_token"""
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.appid}&secret={self.appsecret}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'access_token' in data:
                self.access_token = data['access_token']
                print(f"✅ Access_token获取成功: {self.access_token[:20]}...")
                return True
            else:
                print(f"❌ 获取access_token失败: {data}")
                return False
        else:
            print(f"❌ HTTP请求失败: {response.status_code}")
            return False
    
    def upload_media(self, image_path):
        """上传封面图到微信媒体库"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={self.access_token}&type=image"
        
        try:
            with open(image_path, 'rb') as f:
                files = {'media': f}
                response = requests.post(url, files=files)
                if response.status_code == 200:
                    data = response.json()
                    if 'media_id' in data:
                        print(f"✅ 封面图上传成功，media_id: {data['media_id']}")
                        return data['media_id']
                    else:
                        print(f"❌ 上传封面图失败: {data}")
                        return None
                else:
                    print(f"❌ HTTP请求失败: {response.status_code}")
                    return None
        except Exception as e:
            print(f"❌ 上传封面图时出错: {e}")
            return None
    
    def create_draft(self, title, content_html, cover_media_id=None):
        """创建草稿"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={self.access_token}"
        
        # 构建请求数据
        draft_data = {
            "articles": [
                {
                    "title": title,
                    "author": "胡戈",
                    "digest": "AI生产力跃迁驱动新型生产关系变革——共同富裕探路者自组织实践。传统分配的三个致命缺陷：不透明、中心化、可篡改。",
                    "content": content_html,
                    "content_source_url": "",
                    "thumb_media_id": cover_media_id if cover_media_id else "",
                    "need_open_comment": 1,
                    "only_fans_can_comment": 0
                }
            ]
        }
        
        response = requests.post(url, data=json.dumps(draft_data, ensure_ascii=False).encode('utf-8'), headers={'Content-Type': 'application/json; charset=utf-8'})
        if response.status_code == 200:
            data = response.json()
            if 'media_id' in data:
                print(f"✅ 草稿创建成功，media_id: {data['media_id']}")
                return data['media_id']
            else:
                print(f"❌ 创建草稿失败: {data}")
                return None
        else:
            print(f"❌ HTTP请求失败: {response.status_code}")
            return None
    
    def publish(self, media_id):
        """发布草稿"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/publish?access_token={self.access_token}"
        
        publish_data = {
            "media_id": media_id
        }
        
        response = requests.post(url, data=json.dumps(publish_data, ensure_ascii=False).encode('utf-8'), headers={'Content-Type': 'application/json; charset=utf-8'})
        if response.status_code == 200:
            data = response.json()
            if 'publish_id' in data:
                print(f"✅ 发布成功，publish_id: {data['publish_id']}")
                return True
            else:
                print(f"❌ 发布失败: {data}")
                return False
        else:
            print(f"❌ HTTP请求失败: {response.status_code}")
            return False

def main():
    # 检查参数
    if len(sys.argv) < 4:
        print("用法:")
        print("python3 wechat_draft_push.py <标题> <HTML文件路径> <封面图路径>")
        print("示例:")
        print("python3 wechat_draft_push.py '不透明、中心化、可篡改' '07-公众号文章.html' '/tmp/cover-07.png'")
        sys.exit(1)
    
    title = sys.argv[1]
    html_path = sys.argv[2]
    cover_path = sys.argv[3]
    
    # 检查文件是否存在
    if not Path(html_path).exists():
        print(f"❌ HTML文件不存在: {html_path}")
        sys.exit(1)
    
    if not Path(cover_path).exists():
        print(f"❌ 封面图不存在: {cover_path}")
        sys.exit(1)
    
    # 读取HTML内容
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content_html = f.read()
    except Exception as e:
        print(f"❌ 读取HTML文件失败: {e}")
        sys.exit(1)
    
    # 创建推送器
    publisher = WechatDraftPublisher()
    
    # 获取access_token
    if not publisher.get_access_token():
        sys.exit(1)
    
    # 上传封面图
    cover_media_id = publisher.upload_media(cover_path)
    
    # 创建草稿
    draft_media_id = publisher.create_draft(title, content_html, cover_media_id)
    
    if draft_media_id:
        print(f"✅ 草稿创建成功！")
        print(f"草稿media_id: {draft_media_id}")
        print(f"标题: {title}")
        
        # 询问是否发布
        print("是否立即发布？(y/n)")
        choice = input().strip().lower()
        if choice == 'y':
            if publisher.publish(draft_media_id):
                print("✅ 发布完成！")
            else:
                print("❌ 发布失败")
        else:
            print("📝 草稿已保存到微信公众号草稿箱，可在后台查看")
    else:
        print("❌ 草稿创建失败")

if __name__ == '__main__':
    main()
