# utils.admin
"""获取管理员权限"""

import ctypes
import sys
from loguru import logger

def get_admin() -> bool:
    """
    获取管理员权限

    :return: 是否拥有管理员权限
    :rtype: bool
    """
    # 检测是否已经为管理员权限运行
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True

    # 定义变量
    script = sys.argv[0]
    params = " ".join([f'"{x}"' for x in sys.argv[1:]])

    try:
        hwnd = 0
        operation = "runas"
        file = sys.executable
        arguments = f'"{script}" {params}'

        # 以管理员权限重新运行
        result = ctypes.windll.shell32.ShellExecuteW(
            hwnd, operation, file, arguments, None, 1
        )

        # 如果无法以管理员权限运行则报错
        if result <= 32:
            logger.error("无法以管理员权限运行，请手动以管理员身份运行此程序")

        return False

    except Exception as e:
        logger.error(f"请求管理员权限失败: {e}")
        return False
