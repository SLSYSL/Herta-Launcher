# src.backend.utils.encode
"""资源编码"""

import base64
from loguru import logger


def get_icon_as_base64(icon_path: str) -> str:
    """
    获取程序图标的Base64编码字符串

    :param path: 图片路径
    :type path: str
    :return: Base64编码
    :rtype: str
    """
    try:
        with open(icon_path, "rb") as f:
            icon_data = f.read()
        icon_base64 = base64.b64encode(icon_data).decode("utf-8")
        return icon_base64
    except FileNotFoundError:
        logger.error("图标文件不存在: {}", icon_path)
    except PermissionError:
        logger.error("没有权限读取图标文件: {}", icon_path)
    except (OSError, IOError) as e:
        logger.error("无法加载图标文件: {}", e)
    except UnicodeDecodeError:
        logger.error("图标文件编码错误")
    except ValueError as e:
        logger.error("图标文件格式错误: {}", e)
    except Exception as e:
        logger.error("意外的错误加载图标: {}", e)

    return ""
