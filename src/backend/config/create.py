# src.backend.config.create
"""创建配置文件"""

import configparser
from loguru import logger
from backend.utils import get_cache_path, create_folder
from .defs import DEFAULT_CONFIG


def create_config() -> None:
    """
    创建默认配置文件（如果不存在的话）

    :return: None
    """

    # 配置文件目录
    config_path = get_cache_path(is_path=True) / "Config" / "config.ini"
    config_dir = config_path.parent

    # 创建配置目录
    if not create_folder(config_dir):
        logger.error("无法创建配置文件目录: {}", config_dir)
        return

    # 检查配置文件是否已存在
    if not config_path.exists():
        # 创建配置解析器对象
        config = configparser.ConfigParser()

        # 添加默认配置
        config.read_dict(DEFAULT_CONFIG)

        # 写入配置文件
        with config_path.open("w", encoding="utf-8") as configfile:
            config.write(configfile)
        logger.info("已创建默认配置文件: {}", config_path)
    else:
        # 如果文件存在，检查并更新缺失的配置项
        update_existing_config()
        logger.info("配置文件已存在: {}", config_path)


def update_existing_config() -> None:
    """
    更新已存在的配置文件，添加缺失的配置项

    :return: None
    """
    # 配置文件目录
    config_path = get_cache_path(is_path=True) / "Config" / "config.ini"

    # 检查配置文件是否存在
    if not config_path.exists():
        logger.warning("配置文件不存在，跳过更新: {}", config_path)
        return

    # 创建配置解析器对象
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option

    # 读取现有配置文件
    try:
        config.read(config_path, encoding="utf-8")
    except configparser.Error as e:
        logger.error("读取配置文件失败 (格式错误): {}, 错误信息: {}", config_path, e)
        raise
    except Exception as e:
        logger.error("读取配置文件失败: {}, 错误信息: {}", config_path, e)
        raise

    # 检查并添加缺失的配置项
    updated = False
    for section, options in DEFAULT_CONFIG.items():
        # 补充缺失的节
        if not config.has_section(section):
            config.add_section(section)
            updated = True
        # 补充节下缺失的配置项
        for option, value in options.items():
            if not config.has_option(section, option):
                config.set(section, option, str(value))
                updated = True

    # 如果有更新，写回配置文件
    if updated:
        try:
            with config_path.open("w", encoding="utf-8") as configfile:
                config.write(configfile)
            logger.info("已更新配置文件，添加缺失的配置项: {}", config_path)
        except PermissionError as e:
            logger.error("权限不足，无法写入配置文件: {}", e)
            raise
        except OSError as e:
            logger.error("写入配置文件失败: {}", e)
            raise
    else:
        logger.info("配置文件无缺失项，无需更新: {}", config_path)
