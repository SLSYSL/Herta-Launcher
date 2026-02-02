# src.main
"""入口文件"""

import sys
from loguru import logger
from packages.pywebwinui3.core import MainWindow
from backend import __version__, __titile__
from backend.logger import init_logger
from backend.utils import (
    get_cache_path,
    get_icon_as_base64,
    get_admin,
    get_resource_path,
)  # , window_resize
from backend.config import create_config, read_config
from backend.core import register_handlers, apply_config, load_pages, create_custom_page_folder
from backend.dev import XamlWatcher, on_xaml_change


def main(is_hot_updata: bool = False) -> None:
    """
    主函数 (生产/开发环境通用)

    :param mode: 模式
    :param is_hot_updata: Xaml 热更新
    :return: None
    """
    # 初始化日志
    init_logger()

    # 创建默认配置文件
    create_config()

    logger.info("程序已启动")

    # 获取 Base64 编码的图标数据
    icon_path = get_resource_path("./assets/icon.ico")
    icon_base64 = get_icon_as_base64(icon_path)
    if not icon_base64:
        logger.warning("未能获取图标的Base64编码数据")

    # 获取 MainWindow
    app = MainWindow(
        f"{__titile__} v{__version__}",
        icon=f"data:image/x-icon;base64,{icon_base64}",
    )

    # 设置前端变量
    app.values["version"] = __version__

    # 添加页面
    load_pages(app)

    # 获取自定义 Xaml 路径
    custom_xaml_path = get_cache_path(is_path=True) / "Custom Xaml"

    # 创建自定义页面文件夹
    create_custom_page_folder()

    # 开启 Xaml 热更新
    if is_hot_updata:
        watcher = XamlWatcher(
            watch_paths=["./xaml", custom_xaml_path],
            callback=lambda *args, **kwargs: on_xaml_change(*args, app=app, **kwargs),
        )
        watcher.start()

    # 从配置文件读取并设置主题
    apply_config(app)

    # 注册前端变量变化处理器
    register_handlers(app)

    # 开启窗口大小调整
    # window_resize()

    # 开始运行应用
    app.start()

    # 当应用关闭时输出日志
    logger.info("程序已结束")
    logger.info("=" * 40)


# 程序入口
if __name__ == "__main__":
    # 检查是否以管理员权限运行
    if not get_admin():
        sys.exit(0)

    # 读取配置
    hot_updata = read_config("DEBUG", "hot_updata", False)

    # 运行程序
    main(hot_updata)
