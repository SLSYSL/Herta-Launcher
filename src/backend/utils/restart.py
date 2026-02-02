# src.backend.utils.restart
"""重启程序"""

import os
import sys


def restart_program() -> None:
    """
    重启当前程序

    :return: None
    """
    # 获取当前脚本路径和参数
    python = sys.executable  # 当前Python解释器路径
    script = sys.argv[0]  # 当前脚本路径
    args = sys.argv[1:]  # 当前脚本参数

    # 使用 execv 替换当前进程
    os.execv(python, [python, script] + args)
