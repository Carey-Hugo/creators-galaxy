"""
蓝色系科技感模板库
包含多种科技感封面模板配置
"""

from pathlib import Path

# 模板配置
TEMPLATE_CONFIGS = {
    "tech_blue": {
        "name": "科技蓝",
        "description": "深空背景 + 三节点警示 + 蓝金配色",
        "background_color": (10, 20, 40),  # 深蓝色背景
        "grid_color": (30, 60, 100),       # 网格线颜色
        "node_colors": [(0, 120, 200), (100, 180, 255), (180, 220, 255)],  # 节点颜色
        "node_outline_color": (255, 215, 0),  # 金色边框
        "node_center_color": (255, 255, 255),  # 白色中心
        "connection_color": (255, 215, 0),     # 金色连接线
        
        # 文字配置
        "title_color": (255, 255, 255),        # 白色标题
        "title_outline_color": (255, 215, 0),   # 金色轮廓
        "title_font_size": 64,
        "title_position": (640, 200),          # 中心位置
        
        "subtitle_color": (200, 220, 255),     # 浅蓝色副标题
        "subtitle_font_size": 36,
        "subtitle_position": (640, 280),
        
        "metadata_color": (150, 180, 220),     # 浅蓝色元数据
        "metadata_font_size": 24,
        "metadata_position": (640, 400),
        
        "font_path": "fonts/default.ttf",
    },
    
    "tech_blue_dark": {
        "name": "科技深蓝",
        "description": "更深的太空背景 + 金色元素",
        "background_color": (5, 10, 25),       # 更深的蓝色
        "grid_color": (20, 40, 80),
        "node_colors": [(0, 100, 180), (80, 160, 240), (140, 200, 255)],
        "node_outline_color": (255, 215, 0),
        "node_center_color": (255, 255, 255),
        "connection_color": (255, 215, 0),
        
        "title_color": (255, 255, 255),
        "title_outline_color": (255, 215, 0),
        "title_font_size": 64,
        "title_position": (640, 200),
        
        "subtitle_color": (180, 200, 240),
        "subtitle_font_size": 36,
        "subtitle_position": (640, 280),
        
        "metadata_color": (130, 160, 200),
        "metadata_font_size": 24,
        "metadata_position": (640, 400),
        
        "font_path": "fonts/default.ttf",
    },
    
    "tech_blue_light": {
        "name": "科技浅蓝",
        "description": "浅色科技感背景",
        "background_color": (230, 240, 255),   # 浅蓝色背景
        "grid_color": (180, 200, 220),
        "node_colors": [(30, 140, 230), (70, 170, 250), (120, 200, 255)],
        "node_outline_color": (255, 215, 0),
        "node_center_color": (255, 255, 255),
        "connection_color": (255, 215, 0),
        
        "title_color": (20, 40, 80),           # 深蓝色标题
        "title_outline_color": (255, 215, 0),
        "title_font_size": 64,
        "title_position": (640, 200),
        
        "subtitle_color": (40, 70, 120),
        "subtitle_font_size": 36,
        "subtitle_position": (640, 280),
        
        "metadata_color": (60, 100, 160),
        "metadata_font_size": 24,
        "metadata_position": (640, 400),
        
        "font_path": "fonts/default.ttf",
    },
    
    "tech_blue_gradient": {
        "name": "科技渐变蓝",
        "description": "渐变蓝色背景 + 动态效果",
        "background_color": (10, 20, 40),
        "grid_color": (30, 60, 100),
        "node_colors": [(0, 120, 200), (100, 180, 255), (180, 220, 255)],
        "node_outline_color": (255, 215, 0),
        "node_center_color": (255, &255, 255),
        "connection_color": (255, 215, 0),
        
        "title_color": (255, 255, 255),
        "title_outline_color": (255, 215, 0),
        "title_font_size": 64,
        "title_position": (640, 200),
        
        "subtitle_color": (200, 220, 255),
        "subtitle_font_size": 36,
        "subtitle_position": (640, 280),
        
        "metadata_color": (150, 180, 220),
        "metadata_font_size": 24,
        "metadata_position": (640, 400),
        
        "font_path": "fonts/default.ttf",
        "gradient_enabled": True,
        "gradient_start": (10, 20, 40),
        "gradient_end": (80, 160, 240),
    },
    
    "tech_blue_corporate": {
        "name": "企业科技蓝",
        "description": "企业级专业科技风格",
        "background_color": (15, 30, 60),
        "grid_color": (40, 80, 160),
        "node_colors": [(0, 100, 200), (50, 150, 250), (100, 200, 255)],
        "node_outline_color": (220, 180, 40),  # 金色
        "node_center_color": (255, 255, 255),
        "connection_color": (220, 180, 40),
        
        "title_color": (255, 255, 255),
        "title_outline_color": (220, 180, 40),
        "title_font_size": 72,
        "title_position": (640, 180),
        
        "subtitle_color": (180, 200, 240),
        "subtitle_font_size": 32,
        "subtitle_position": (640, 260),
        
        "metadata_color": (140, 170, 220),
        "metadata_font_size": 20,
        "metadata_position": (640, 420),
        
        "font_path": "fonts/default.ttf",
    }
}


def get_template(template_name):
    """
    获取模板配置
    
    Args:
        template_name: 模板名称
        
    Returns:
        模板配置字典
        
    Raises:
        ValueError: 如果模板不存在
    """
    if template_name not in TEMPLATE_CONFIGS:
        raise ValueError(f"模板 '{template_name}' 不存在。可用模板: {list(TEMPLATE_CONFIGS.keys())}")
    
    return TEMPLATE_CONFIGS[template_name]


def list_templates():
    """列出所有可用模板"""
    return list(TEMPLATE_CONFIGS.keys())


def get_template_info(template_name):
    """获取模板详细信息"""
    config = get_template(template_name)
    return {
        "name": config["name"],
        "description": config["description"],
        "colors": {
            "background": config["background_color"],
            "title": config["title_color"],
            "subtitle": config["subtitle_color"]
        }
    }