"""
hot_updata.py
Xaml热更新
"""

import xml.etree.ElementTree as ET
from loguru import logger


def load_xaml_file(filepath):
    """加载XAML文件并转换为JSON格式"""

    def xaml_to_dict(element):
        return {
            "tag": element.tag,
            "attr": element.attrib,
            "text": (element.text or "").strip(),
            "child": [xaml_to_dict(e) for e in element],
        }

    return xaml_to_dict(ET.parse(filepath).getroot())


def on_xaml_change(filepath, app):
    """当XAML文件发生变化时调用此函数"""
    logger.info("检测到XAML文件变化: {}", filepath)
    try:
        # 重新加载XAML文件
        xaml_data = load_xaml_file(filepath)

        # 更新应用中的页面
        app.addPage(filepath, xaml_data)
        logger.info("页面已更新")

    except Exception as e:
        logger.error("更新XAML文件时出错: {}", e)
