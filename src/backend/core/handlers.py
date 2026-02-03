# src.backend.core.handlers
"""前端处理"""

import os
import tempfile
import time
from pathlib import Path
import pyperclip
import pyautogui
import pygetwindow as gw
import keyboard
from loguru import logger
from backend.utils import (
    log_and_notice,
    active_window,
    set_window_topmost,
    get_cache_path,
    get_file_list,
    move_file,
    extract_zip,
)
from backend.config import read_config, modify_config, remove_config


def apply_config(app) -> None:
    """
    从配置文件读取并设置到应用

    :param app: 应用实例
    :return: None
    """
    # 读取配置
    theme_value = read_config("UI", "theme", "system")
    nav_value = read_config("UI", "nav_open", True)
    hot_updata = read_config("DEBUG", "hot_updata", False)
    direct_output = read_config("DEBUG", "direct_output", False)
    custom_xaml_list = get_file_list(
        get_cache_path(is_path=True) / "Custom Xaml", file_extension="xaml"
    )

    # 输出日志
    logger.info("从配置读取主题: {}", theme_value)
    logger.info("从配置读取导航栏状态: {}", nav_value)
    logger.info("从配置读取 Xaml 热更新设置: {}", hot_updata)
    logger.info("从配置读取指令输出至弹窗设置: {}", direct_output)
    logger.info("从配置读取自定义 Xaml 列表: {}", custom_xaml_list)

    # 设置前端变量
    app.values["system_theme"] = theme_value
    app.values["system_nav"] = nav_value
    app.values["hot_updata"] = hot_updata
    app.values["direct_output"] = direct_output
    app.values["custom_xaml_list_len"] = len(custom_xaml_list)

    # 设置自定义 Xaml 页面变量
    for i, name in enumerate(custom_xaml_list):
        app.values[f"custom_xaml_{i}_name"] = name.split("\\")[-1]
        app.values[f"custom_xaml_{i}_path"] = name


def general_change(
    section: str, option: str, old_value=None, new_value=None, is_remove: bool = False
) -> None:
    """
    通用修改配置文件的回调函数

    :param old_value: 旧值
    :param new_value: 新值
    :return: None
    """
    if is_remove:
        remove_config(section, option)
        return

    logger.info("'[{}] {}' 从 '{}' 变更为 '{}'", section, option, old_value, new_value)
    modify_config(section, option, new_value)


def _process_extracted_files(app, temp_dir: str) -> str:
    """
    处理解压缩后的文件

    :param app: 应用实例
    :param temp_dir: 临时目录路径
    :type temp_dir: str
    :return: 错误信息
    """
    error = ""

    # 递归遍历临时目录所有文件
    for root, _, files in os.walk(temp_dir):
        for file_name in files:
            # 获取文件完整路径
            full_path = os.path.join(root, file_name)

            # 提取文件后缀并统一小写
            _, file_extension = os.path.splitext(file_name)
            file_extension = file_extension.lstrip(".").lower()

            # 初始化自定义路径
            custom_path = None

            # 分类 icon 与 xaml 文件
            if file_extension == "xaml":
                custom_path = get_cache_path(is_path=True) / "Custom Xaml"
            elif file_extension == "ico":
                logger.info("找到图标文件: {}", full_path)
                # 获取自定义图标文件夹路径
                custom_path = get_cache_path(is_path=True) / "Custom Icons"
            else:
                logger.info("跳过不支持的文件类型: {}", full_path)
                continue

            # 移动文件
            move_error = move_file(full_path, str(custom_path))
            if move_error != "":
                error = f"文件移动失败: {move_error}"
                log_and_notice(app, error, "error")

    return error


def add_page(app, file_path: str) -> None:
    """
    添加自定义 Xaml 页面

    :param app: 应用实例
    :param file_path: 文件路径
    :type file_path: str
    :return: None
    """

    # 判断是否为压缩包
    if Path(file_path).suffix.lower() == ".zip":
        # 初始化错误信息
        error = ""

        # 打印日志
        logger.info("检测到压缩包: {}", file_path)

        # 解压缩至临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 解压ZIP文件
            success, extract_error = extract_zip(file_path, temp_dir)
            if not success:
                log_and_notice(app, extract_error, "error")
                return

            # 处理解压后的文件
            error = _process_extracted_files(app, temp_dir)

        if error:
            return
        else:
            log_and_notice(app, "自定义 Xaml 已添加成功", "info")

    else:
        logger.info("检测到 Xaml 文件: {}", file_path)

        # 获取文件夹
        folder = get_cache_path(is_path=True) / "Custom Xaml"

        # 打印日志
        logger.info("自定义 Xaml 文件路径: {}, %AppData% 路径: {}", file_path, folder)

        # 移动文件
        error = move_file(file_path, folder)
        if error != "":
            log_and_notice(app, f"自定义页面添加失败，文件移动出错: {error}", "error")
        else:
            log_and_notice(app, "自定义页面添加成功", "info")


def remove_page(app, xaml_path: str) -> None:
    """
    移除自定义 Xaml 页面

    :param app: 应用实例
    :param xaml_path: Xaml 路径
    :type xaml_path: str
    :return: None
    """
    # 转化为 Path 对象
    xaml_path = Path(xaml_path)

    try:
        xaml_path.unlink(missing_ok=True)
        log_and_notice(app, "自定义页面删除成功", "info")
    except Exception as e:
        log_and_notice(app, f"自定义页面删除时出错: {e}", "error")


def send_command(app, command: dict, operation: str = "") -> None:
    """
    置顶程序后发送指令

    :param app: 应用实例
    :param command: 发送的命令
    :type command: dict
    :param operation: 额外操作 (如右Ctrl+/)
    :type operation: str
    :return: None
    """
    # 解析命令格式
    page_path = command["path"]
    command_value = command.get("value", command)

    # 获取目标程序标题
    page_data = app.values["system_pages"][page_path]
    title = page_data.get("attr", {}).get("app", "")

    # 指令输出至弹窗
    if read_config("DEBUG", "direct_output", False):
        log_and_notice(app, f"目标程序: {title}, 输出: {command_value}", "info")
        return

    # 获取程序对象
    target_window = gw.getWindowsWithTitle(title)

    # 找不到程序直接报错
    if not target_window:
        log_and_notice(app, f"未找到目标程序: {title}, 请确保是否已启动", "error")
        return

    # 置顶窗口
    error = set_window_topmost(target_window[0])

    # 无法置顶窗口则报错
    if error != "":
        log_and_notice(app, f"置顶 '{title}' 窗口失败: {error}", "error")
        return

    # 一系列操作
    try:
        active_window(target_window)
        time.sleep(0.1)
        pyperclip.copy(command_value)
        if operation == "slash":
            pyautogui.hotkey("ctrlright", "/")
        elif operation == "wave":
            keyboard.press_and_release("`")
        time.sleep(0.1)
        keyboard.press_and_release("ctrl+v")
        time.sleep(0.1)
        keyboard.press_and_release("enter")
        log_and_notice(app, f"命令已发送至 '{title}'", "info")
    except Exception as e:
        log_and_notice(app, f"命令发送失败: '{e}'", "error")
