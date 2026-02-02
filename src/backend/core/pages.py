# src.backend.core.pages
"""页面管理"""

from typing import List
from loguru import logger
from backend.utils import get_resource_path, get_cache_path

# 默认页面配置
__pages__ = [
    "./xaml/Home.xaml",
    "./xaml/PageManager.xaml",
    "./xaml/About.xaml",
]


def create_custom_page_folder() -> None:
    """
    生成自定义 Xaml 文件夹

    :retrun: None
    """
    custom_dir = get_cache_path(is_path=True) / "Custom Xaml"

    try:
        custom_dir.mkdir(parents=True, exist_ok=True)
        logger.info("已创建自定义 Xaml 目录")
    except PermissionError as e:
        logger.error("权限不足，无法创建自定义 Xaml 目录: {}", e)
        raise
    except OSError as e:
        logger.error("创建自定义 Xaml 目录失败: {}", e)
        raise
    except Exception as e:
        logger.error("未知报错: {}", e)
        raise


def get_custom_pages() -> List[str]:
    """
    获取自定义 Xaml 页面

    :return: 绝对路径列表
    :rtype: List[str]
    """
    # 获取文件夹
    folder = get_cache_path(is_path=True) / "Custom Xaml"

    # 递归搜索所有.xaml文件
    xaml_files = list(folder.rglob("*.xaml"))

    # 转换为绝对路径字符串列表
    pages_list = [str(file.absolute()) for file in xaml_files]

    logger.info("自定义 Xaml 页面文件列表: {}", pages_list)
    return pages_list


def load_pages(app) -> None:
    """
    加载 Xaml 页面

    :param app: 应用实例
    :return: None
    """
    # 添加基础页面
    for default_pages in __pages__:
        app.addPage(get_resource_path(default_pages))

    # 添加自定义页面
    for custon_pages in get_custom_pages():
        app.addPage(custon_pages)

    # 添加设置
    app.addSettings(get_resource_path("./xaml/Settings.xaml"))
