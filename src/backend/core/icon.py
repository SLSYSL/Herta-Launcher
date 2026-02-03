# src.backend.core.icon
"""图标处理"""

import os
from loguru import logger
from backend.utils import (
    get_file_list,
    get_resource_path,
    get_cache_path,
    get_icon_as_base64,
)

__icons__ = get_file_list(
    get_resource_path(get_cache_path(), is_path=True), file_extension="ico"
)


def games_icon(icon: str) -> str:
    """
    获取游戏图标的 Base64 编码

    :param icon: 图标路径
    :type icon: str
    :return: Base64 编码字符串
    :rtype: str
    """
    icon_path = get_resource_path(icon)
    return "data:image/x-icon;base64," + get_icon_as_base64(icon_path)


def apply_icons(app) -> None:
    """
    应用图标列表

    :param app: 应用实例
    :return: None
    """
    logger.info("应用图标列表: {}", __icons__)

    if not __icons__:
        logger.warning("图标列表为空，跳过应用图标")
        return

    for _, icon_path in enumerate(__icons__):
        icon_path_data = games_icon(icon_path)
        name = os.path.splitext(os.path.basename(icon_path))[0]
        logger.info("应用图标: {}", name)
        app.values[f"{name}"] = icon_path_data
