# src.backend.config
"""配置文件处理逻辑"""

import configparser
from loguru import logger
from backend.utils import get_cache_path
from .defs import DEFAULT_CONFIG
from .create import create_config


def read_config(section: str, option: str = "", fallback=None):
    """
    读取配置文件

    :param section: 配置节名称
    :type section: str
    :param option: 配置项名称
    :type option: str
    :param fallback: 最终兜底值
    :return: 配置项的具体值
    """
    # 配置文件目录
    config_path = get_cache_path(is_path=True) / "Config" / "config.ini"
    if not config_path.exists():
        logger.warning("配置文件不存在，返回默认配置: [{}] {}", section, option)
        return DEFAULT_CONFIG.get(section, {}).get(option, fallback)

    # 创建配置解析器对象
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option
    config.read(config_path, encoding="utf-8")

    # 读取配置项
    try:
        if not option:
            values = []

            for config_option, config_value in config.items(section):
                values.append({"option": config_option, "value": config_value})

            return values

        value = config.get(
            section,
            option,
            fallback=DEFAULT_CONFIG.get(section, {}).get(option, fallback),
        )

        # 尝试将布尔字符串转换为布尔值
        if isinstance(value, str):
            value_lower = value.lower()
            if value_lower == "true":
                return True
            elif value_lower == "false":
                return False

        return value
    except configparser.NoSectionError:
        logger.warning("配置节不存在，返回默认值: {}", section)
        return DEFAULT_CONFIG.get(section, {}).get(option, fallback)


def modify_config(section: str, option: str, value) -> None:
    """
    修改配置文件

    :param section: 配置节名称
    :param option: 配置项名称
    :return: None
    """
    # 获取配置文件路径
    config_path = get_cache_path(is_path=True) / "Config" / "config.ini"

    # 检查配置文件是否存在
    if not config_path.exists():
        logger.warning("配置文件不存在, 正在创建默认配置文件: {}", config_path)
        create_config()

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

    # 处理配置节
    if not config.has_section(section):
        config.add_section(section)
        logger.info("新增配置节: {}", section)

    # 设置配置项
    config.set(section, option, str(value))

    # 写回配置文件
    try:
        with config_path.open("w", encoding="utf-8") as configfile:
            config.write(configfile)
            logger.info(
                "修改配置项成功: [{}] {} = {} | 路径: {}",
                section,
                option,
                value,
                config_path,
            )
    except PermissionError as e:
        logger.error("权限不足，无法写入配置文件: {}", e)
        raise
    except OSError as e:
        logger.error("写入配置文件失败（磁盘满/路径非法）: {}", e)
        raise

def remove_config(section: str, option: str) -> None:
    """
    移除配置文件中的配置项
    :return: None
    """
    # 获取配置文件路径
    config_path = get_cache_path(is_path=True) / "Config" / "config.ini"

    # 检查配置文件是否存在
    if not config_path.exists():
        logger.warning("配置文件不存在, 无法移除配置项: {}", config_path)
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

    # 移除配置项
    if config.has_section(section) and config.has_option(section, option):
        config.remove_option(section, option)
        logger.info("已移除配置项: [{}] {}", section, option)
    else:
        logger.warning("配置项不存在，无法移除: [{}] {}", section, option)
        return

    # 写回配置文件
    try:
        with config_path.open("w", encoding="utf-8") as configfile:
            config.write(configfile)
    except PermissionError as e:
        logger.error("权限不足，无法写入配置文件: {}", e)
        raise
    except OSError as e:
        logger.error("写入配置文件失败: {}", e)
        raise
