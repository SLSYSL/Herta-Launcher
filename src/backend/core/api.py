# src.backend.core.api
"""接收前端请求"""

import time
from webview import FileDialog
from loguru import logger
from backend.utils import restart_program, get_file_list, get_cache_path
from .handlers import general_change, send_command, add_page, remove_page


def register_handlers(app) -> None:
    """
    注册所有前端变量变化处理器

    :param app: 应用实例
    :return: None
    """
    logger.info("注册前端变量变化处理器")

    # 主题变化处理器
    @app.onValueChange("system_theme")
    def theme_change_handler(_key, old_value, new_value) -> None:
        general_change("UI", "theme", old_value, new_value)

    # 侧边栏变化处理器
    @app.onValueChange("system_nav")
    def nav_change_handler(_key, old_value, new_value) -> None:
        general_change("UI", "nav_open", old_value, new_value)

    @app.onValueChange("hot_updata")
    def hot_updata_change_handler(_key, old_value, new_value) -> None:
        general_change("DEBUG", "hot_updata", old_value, new_value)

    @app.onValueChange("direct_output")
    def direct_output_change_handler(_key, old_value, new_value) -> None:
        general_change("DEBUG", "direct_output", old_value, new_value)

    @app.onValueChange("add_page")
    def add_page_handler(_key, _old_value, _new_value) -> None:
        xaml_path = app.api._window.create_file_dialog(
            FileDialog.OPEN,
            file_types=['Allowed files (*.xaml;*.zip)'],
        )
        if not xaml_path:
            logger.info("取消添加页面")
            return
        add_page(app, xaml_path[0])
        restart_program()

    @app.onValueChange("remove_*_custom_xaml")
    def remove_custom_page_handler(key, _old_value, _new_value) -> None:
        # 获取序号
        key_id = int(key.split("_")[1])

        # 获取路径
        file_path = get_file_list(
            get_cache_path(is_path=True) / "Custom Xaml", file_extension="xaml"
        )

        remove_page(app, file_path[key_id])
        restart_program()

    @app.onValueChange("*_send_command")
    def send_command_handler(_key, _old_value, new_value) -> None:
        # 找到第一个 '-' 的位置
        dash_index = new_value["value"].find("-")

        # 如果没有则直接发送
        if dash_index == -1:
            send_command(app, new_value)
            return

        # 获取 '-' 左边的部分
        operation = new_value["value"][:dash_index].strip()

        # 获取 '-' 右边直到字符串结束的部分
        new_value["value"] = new_value["value"][dash_index + 1 :].strip()
        send_command(app, new_value, operation)

    logger.info("前端变量变化处理器注册完成")
