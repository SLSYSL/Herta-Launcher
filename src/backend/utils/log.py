# src.backend.utils.log
"""日志工具"""

from typing import Optional
from loguru import logger
from packages.pywebwinui3.core import Status

def log_and_notice(app, content: str, level: str) -> None:
    """
    打印日志并前端弹窗

    :param app: 应用实例
    :param content: 弹窗与日志内容
    :type content: str
    :param level: 等级
    :type level: str
    :return: None
    """
    status_level_map = {
        "info": {"status": Status.Success, "title": "成功", "log_method": logger.info},
        "warning": {
            "status": Status.Caution,
            "title": "警告",
            "log_method": logger.warning,
        },
        "error": {
            "status": Status.Critical,
            "title": "错误",
            "log_method": logger.error,
        },
    }

    # 小写转换
    level_config: Optional[dict] = status_level_map.get(level.lower())

    # 不支持类型的弹窗
    if not level_config:
        # 弹出警告弹窗，并打印 warning 级别的日志
        app.notice(
            Status.Caution,
            "警告",
            f"不支持 {level} 类型弹窗, 仅支持: info/warning/error",
        )
        logger.warning("尝试使用不支持的弹窗级别: %s, 内容: %s", level, content)
        return

    # 提取映射后的配置
    status_enum = level_config["status"]
    title = level_config["title"]
    log_func = level_config["log_method"]

    # 执行前端弹窗
    app.notice(status_enum, title, content)

    # 打印对应级别的日志
    log_func(content)
