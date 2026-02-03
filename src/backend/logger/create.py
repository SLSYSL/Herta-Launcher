# src.backend.logger.create
"""创建日志文件"""

import sys
from datetime import datetime
from pathlib import Path
from loguru import logger
from backend.utils import get_cache_path, create_folder


def init_logger():
    """
    设置应用程序的日志记录器

    :return: 配置完成的 logger 对象
    """
    # 获取本程序缓存路径
    path = get_cache_path()

    # 转换为Path对象
    cache_path = Path(path) if not isinstance(path, Path) else path

    # 构建日志目录路径
    date_str = datetime.now().strftime("%Y%m%d")
    log_dir = cache_path / "Logs"
    log_file = log_dir / f"HertaLauncher_{date_str}.log"

    # 创建日志目录
    if not create_folder(log_dir):
        logger.error("无法创建日志目录: {}", log_dir)
        return

    # 移除默认的处理器
    logger.remove()

    # 添加文件处理器（按天轮转，保留30天）
    try:
        # 控制台
        logger.add(
            sys.stdout,
            format=(
                "<g>{time:YYYY-MM-DD HH:mm:ss}</g> | "
                "<lvl>{level}</lvl> | "
                "<c>{name}:{function}:{line}</c> | "
                "<w>{message}</w>"
            ),
            level="DEBUG",
            colorize=True,
            enqueue=True,
        )
        # 日志文件
        logger.add(
            str(log_file),
            format=(
                "{time:YYYY-MM-DD HH:mm:ss} | "
                "{level} | "
                "{name}:{function}:{line} | "
                "{message}"
            ),
            level="INFO",
            rotation="00:00",  # 每天午夜轮转
            retention="30 days",  # 保留30天
            encoding="utf-8",
            enqueue=True,  # 异步写入，线程安全
            backtrace=True,  # 显示异常堆栈
            diagnose=True,  # 显示变量值
        )
    except Exception as e:
        logger.error("无法创建或写入日志文件 {}: {}", log_file, e)
        raise

    # 记录一条初始化成功的日志
    logger.info("日志系统初始化完成, 日志文件位于: {}", log_file)
    return logger


# 导出 logger 实例
__all__ = ["logger", "init_logger"]
