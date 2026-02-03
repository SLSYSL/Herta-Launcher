# src.backend.utils.files
"""文件操作"""

import zipfile
import shutil
from pathlib import Path
from typing import List, Tuple
from loguru import logger


def get_file_list(folder_path: str, file_extension: str = "*") -> List[str]:
    """
    获取指定文件夹下的指定类型文件列表

    :param folder_path: 文件夹路径
    :type folder_path: str
    :param file_extension: 文件扩展名
    :type file_extension: str
    :return: 返回文件列表
    :rtype: List[str]
    """
    # 打印日志
    logger.info(
        "获取文件列表，文件夹路径: {}, 文件扩展名: {}", folder_path, file_extension
    )

    # 转换为 Path 对象
    folder_path = Path(folder_path)

    # 递归搜索文件
    files = list(folder_path.rglob(f"*.{file_extension}"))

    # 转换为绝对路径字符串列表
    file_list = [str(file.absolute()) for file in files]

    return file_list


def create_folder(folder_path: str) -> bool:
    """
    创建文件夹

    :param folder_path: 文件夹路径
    :type folder_path: str
    :return: 是否创建成功
    :rtype: bool
    """
    # 转换为 Path 对象
    folder_path = Path(folder_path)

    # 创建文件夹
    try:
        folder_path.mkdir(parents=True, exist_ok=True)
        logger.info("已创建文件夹: {}", folder_path)
        return True
    except PermissionError as e:
        logger.error("权限不足，无法创建文件夹: {}", e)
        raise PermissionError(f"无法创建目录 {folder_path}: 权限不足") from e
    except OSError as e:
        logger.error("创建文件夹失败: {}", e)
        raise OSError(f"创建目录 {folder_path} 失败") from e
    except Exception as e:
        logger.error("创建文件夹时发生未知错误: {}", e)
        raise RuntimeError(f"创建目录时发生未知错误: {e}") from e


def move_file(src_path: str, dest_path: str) -> str:
    """
    移动文件

    :param src_path: 源文件路径
    :type src_path: str
    :param dest_path: 目标文件路径
    :type dest_path: str
    :return: 报错信息
    :rtype: str
    """
    try:
        shutil.move(src_path, dest_path)
        logger.info("已移动文件从 {} 到 {}", src_path, dest_path)
        return ""
    except FileNotFoundError as e:
        logger.error("源文件不存在: {}", e)
        return f"文件不存在: {e}"
    except PermissionError as e:
        logger.error("权限不足: {}", e)
        return f"权限错误: {e}"
    except IsADirectoryError as e:
        logger.error("目录错误: {}", e)
        return f"目录错误: {e}"
    except shutil.Error as e:
        logger.error("移动文件失败: {}", e)
        return str(e)
    except OSError as e:
        logger.error("系统错误: {}", e)
        return str(e)
    except RuntimeError as e:
        logger.error("运行时错误: {}", e)
        return str(e)
    except Exception as e:
        logger.error("未知错误: {}", e)
        return f"未知错误: {e}"


def extract_zip(file_path: str, temp_dir: str) -> Tuple[bool, str]:
    """
    解压 ZIP 文件到指定目录

    :param file_path: ZIP 文件路径
    :type file_path: str
    :param temp_dir: 目标解压目录
    :type temp_dir: str
    :return: 是否解压成功及错误信息
    :rtype: Tuple[bool, str]
    """
    try:
        logger.info("解压缩至临时目录: {}", temp_dir)

        # 解压缩到临时目录
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(path=temp_dir)
            logger.info("成功解压缩压缩包, 共{}个文件", len(zip_ref.namelist()))

        return True, ""
    except Exception as e:
        error_msg = f"解压缩失败: {str(e)}"
        logger.error(error_msg)
        return False, error_msg
