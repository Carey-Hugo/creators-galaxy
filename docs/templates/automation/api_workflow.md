# 微信公众号API标准化工作流

## 弯路总结
1. **定时发表文章media_id无效** → 应手动获取一篇已发布文章HTML作为排版样板
2. **access_token频繁失效** → 需实现缓存机制（本地文件缓存）
3. **封面图同步不及时** → 标题更改必须立即重新生成封面并更新media_id
4. **分身工作被对话打断** → 使用Cron定时任务让分身独立运行

## 标准化步骤
### 1. 获取排版样板
```
curl -s "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=XXXX" | grep -A 1000 "已发表文章"
# 手动保存一篇已发布文章的完整HTML
```

### 2. access_token缓存
```python
import json
import time
import requests

def get_access_token(appid, secret):
    cache_file = "~/.hermes/cache/wechat_token.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cache = json.load(f)
            if time.time() - cache["timestamp"] < 7000:  # 2小时有效期
                return cache["access_token"]
    
    # 重新获取
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}"
    response = requests.get(token_url)
    data = response.json()
    
    if "access_token" in data:
        with open(cache_file, "w") as f:
            json.dump({"access_token": data["access_token"], "timestamp": time.time()}, f)
        return data["access_token"]
    return None
```

### 3. 封面图生成同步流程
```python
def update_cover_sync(title, article_content):
    # 1. 生成新封面图
    cover_prompt = f"创客星球CGHub公众号封面图，标题: {title}，蓝色系，1280×547"
    new_cover_path = image_generate(cover_prompt)
    
    # 2. 立即上传到微信素材库
    media_id = wechat_upload_media(new_cover_path)
    
    # 3. 更新草稿封面图
    update_draft_cover(media_id)
    
    # 4. 保存记录
    save_cover_record(title, media_id, time.time())
```

### 4. Cron任务调度
```bash
# 每天定时检查草稿箱状态
0 9,15,21 * * * ~/creators-galaxy/scripts/check_drafts.py

# 每周三、六自动发布检查
0 17 * * 3,6 ~/creators-galaxy/scripts/auto_publish.py

# 模型评估任务（独立运行）
0 2 * * * ~/creators-galaxy/scripts/model_evaluation.py
```
