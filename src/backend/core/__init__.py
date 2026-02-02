"""src.backend.core"""

from .handlers import apply_config, general_change
from .api import register_handlers
from .pages import load_pages, create_custom_page_folder, get_custom_pages

__all__ = [
    "apply_config",
    "general_change",
    "register_handlers",
    "load_pages",
    "create_custom_page_folder",
    "get_custom_pages",
]
