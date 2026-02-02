# src.backend.core.handlers
"""前端处理"""

import time
import shutil
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
    get_resource_path,
    get_icon_as_base64
)
from backend.config import read_config, modify_config, remove_config
from .pages import get_custom_pages


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
    custom_xaml_list = get_custom_pages()

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
    app.values["mwiii_icon"] = "data:image/x-icon;base64," + get_icon_as_base64(get_resource_path("./assets/cod20.ico"))
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


def add_page(app, xaml_path: str) -> None:
    """
    添加自定义 Xaml 页面

    :param app: 应用实例
    :param xaml_path: Xaml 路径
    :type xaml_path: str
    :return: None
    """
    # 获取文件夹
    folder = get_cache_path(is_path=True) / "Custom Xaml"

    # 打印日志
    logger.info("自定义 Xaml 文件路径: {}, %AppData% 路径: {}", xaml_path, folder)

    # 移动文件
    try:
        # 移动文件
        shutil.move(xaml_path, folder)

        log_and_notice(app, "自定义页面已添加", "info")
    except (FileNotFoundError, PermissionError) as e:
        log_and_notice(app, f"文件操作错误: {e}", "error")
    except shutil.Error as e:
        log_and_notice(app, f"移动文件失败: {e}", "error")
    except OSError as e:
        log_and_notice(app, f"系统错误: {e}", "error")
    except Exception as e:
        log_and_notice(app, f"自定义页面添加失败: '{e}'", "error")


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
