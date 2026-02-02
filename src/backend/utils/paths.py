# src.backend.utils.paths
"""路径操作"""

import os
import sys
from pathlib import Path
from loguru import logger


def get_resource_path(relative_path: str, is_path: bool = False) -> Path | str:
    """
    获取资源的真实路径

    :param relative_path: 相对路径
    :type relative_path: str
    :param is_path: 路径是否返回 Path 格式
    :type is_path: bool
    :return: 绝对路径
    :rtype: Path | str
    """
    # 判断当前运行环境并获取基路径
    if hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)  # pylint: disable=protected-access
    else:
        base_path = Path.cwd()

    # 拼接绝对路径
    clean_relative_path = Path(relative_path).as_posix()
    real_path = base_path.joinpath(clean_relative_path).resolve()

    # 文件不存在将警告
    if not real_path.exists():
        logger.warning("警告：资源文件不存在 -> {}", real_path)

    # 返回 Path 路径
    if is_path:
        return Path(real_path)

    # 返回 str 路径
    return str(real_path)


def get_cache_path(is_path: bool = False) -> Path | str:
    """
    获取本程序缓存路径

    :param is_path: 路径是否返回 Path 格式
    :type is_path: bool
    :return: 返回路径
    :rtype: Path | str
    """
    # 定义程序缓存文件夹名称
    cache_name = "HertaLauncherCache"

    # 访问 %AppData% 并拼接程序缓存文件夹名称
    cache_path = Path(os.getenv("APPDATA")) / cache_name

    # 无法访问返回 C:\\HertaLauncherCache
    if not cache_path:
        cache_path = f"C:\\{cache_name}"
        logger.warning("无法访问 %%AppData%%, 使用备用缓存路径 C:\\{}", cache_path)

    # 返回 %AppData%\\HertaLauncherCache 路径 (Path)
    if is_path:
        return Path(cache_path)

    # 返回 %AppData%\\HertaLauncherCache 路径 (str)
    return str(cache_path)
