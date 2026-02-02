# src.backend.utils.window
"""关于窗口的操作"""

import ctypes
import threading
import time
from ctypes import windll, c_void_p, c_ulong, c_int
from loguru import logger

# 定义 WinAPI 类型和函数
user32 = windll.user32
HWND = c_void_p
DWORD = c_ulong
BOOL = c_int

# 定义 SetWindowPos 函数原型
SetWindowPos = user32.SetWindowPos

# 常量定义
HWND_TOPMOST = -1
HWND_NOTOPMOST = -2
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_SHOWWINDOW = 0x0040


def window_resize() -> None:
    """
    Windows 原生调整大小

    :return: None
    """

    def apply_styles():
        # 等待窗口创建
        time.sleep(2)

        try:
            # 获取句柄
            hwnd = ctypes.windll.user32.GetForegroundWindow()

            # 如果无法获取句柄
            if not hwnd:
                logger.warning("无法获取窗口句柄")
                return

            # 启用调整大小
            gwl_style = -16
            style = user32.GetWindowLongW(hwnd, gwl_style)
            style |= 0x00040000
            user32.SetWindowLongW(hwnd, gwl_style, style)

            # 刷新窗口
            user32.SetWindowPos(
                hwnd,
                None,
                0,
                0,
                0,
                0,
                0x0020 | 0x0002 | 0x0001 | 0x0004,
            )

            logger.info("窗口调整大小已启用")
        except Exception as e:
            logger.error("调整大小启用失败: {}", e)

    # 异步应用样式
    threading.Thread(target=apply_styles, daemon=True).start()


def set_window_topmost(target_window, topmost: bool = True) -> str:
    """
    设置窗口置顶状态

    :param target_window: Windows 窗口对象
    :param topmost: 是否置顶
    :type topmost: bool
    :return: 是否成功
    :rtype: str
    """

    try:
        hwnd_top = HWND_TOPMOST if topmost else HWND_NOTOPMOST
        SetWindowPos(
            target_window._hWnd,
            hwnd_top,
            0,
            0,
            0,
            0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW,
        )
        return ""
    except Exception as e:
        return e


def active_window(target_window) -> None:
    """
    激活窗口

    :param target_window: Windows 窗口对象
    :return: None
    """
    try:
        target_window[0].activate()
    except Exception as e:
        logger.error(f"窗口激活失败: {e}")
        target_window[0].minimize()
        target_window[0].restore()
