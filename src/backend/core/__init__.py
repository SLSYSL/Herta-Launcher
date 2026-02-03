"""src.backend.core"""

from .handlers import apply_config, general_change
from .api import register_handlers
from .pages import load_pages
from .icon import apply_icons

__all__ = [
    "apply_config",
    "general_change",
    "register_handlers",
    "load_pages",
    "apply_icons",
]
