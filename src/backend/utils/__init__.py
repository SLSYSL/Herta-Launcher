"""src.backend.utils"""

from .paths import get_cache_path, get_resource_path
from .files import get_file_list, create_folder, move_file, extract_zip
from .encode import get_icon_as_base64
from .window import window_resize, active_window, set_window_topmost
from .log import log_and_notice
from .admin import get_admin
from .restart import restart_program

__all__ = [
    "get_cache_path",
    "get_resource_path",
    "get_icon_as_base64",
    "window_resize",
    "log_and_notice",
    "active_window",
    "set_window_topmost",
    "get_admin",
    "restart_program",
    "get_file_list",
    "create_folder",
    "move_file",
    "extract_zip",
]
