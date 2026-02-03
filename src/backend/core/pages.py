# src.backend.core.pages
"""页面管理"""

from loguru import logger
from backend.utils import get_resource_path, get_cache_path, get_file_list

# 默认页面配置
__pages__ = [
    "./xaml/Home.xaml",
    "./xaml/PageManager.xaml",
    "./xaml/About.xaml",
]


def load_pages(app) -> None:
    """
    加载 Xaml 页面

    :param app: 应用实例
    :return: None
    """
    # 添加基础页面
    for default_pages in __pages__:
        app.addPage(get_resource_path(default_pages))
        logger.info("已加载页面: {}", default_pages)

    # 添加自定义页面
    for custon_pages in get_file_list(
        get_cache_path(is_path=True) / "Custom Xaml", file_extension="xaml"
    ):
        app.addPage(custon_pages)
        logger.info("已加载自定义页面: {}", custon_pages)

    # 添加设置
    app.addSettings(get_resource_path("./xaml/Settings.xaml"))
    logger.info("已加载设置页面")
