"""
xaml_watcher.py
检测 Xaml 是否更新
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional, Callable, Iterable, List
from watchdog.observers import Observer
from watchdog.events import (
    FileSystemEventHandler,
    FileCreatedEvent,
    FileModifiedEvent,
    FileDeletedEvent,
)


class XamlFileHandler(FileSystemEventHandler):
    """专门处理XAML文件事件的处理器"""

    def __init__(self, callback: Optional[Callable[[str], None]] = None):
        self.callback = callback

    def _is_xaml_file(self, path: str) -> bool:
        """判断是否为XAML文件"""
        return Path(path).suffix.lower() == ".xaml"

    def on_created(self, event: FileCreatedEvent) -> None:
        """处理文件新增事件"""
        if (
            not event.is_directory
            and self._is_xaml_file(event.src_path)
            and self.callback
        ):
            self.callback(event.src_path)

    def on_modified(self, event: FileModifiedEvent) -> None:
        """处理文件修改事件"""
        if (
            not event.is_directory
            and self._is_xaml_file(event.src_path)
            and self.callback
        ):
            self.callback(event.src_path)

    def on_deleted(self, event: FileDeletedEvent) -> None:
        """处理文件删除事件"""
        if (
            not event.is_directory
            and self._is_xaml_file(event.src_path)
            and self.callback
        ):
            self.callback(event.src_path)


class XamlWatcher:
    """XAML文件监控类"""

    def __init__(
        self,
        watch_paths: str | Path | Iterable[str | Path],
        callback: Optional[Callable[[str], None]] = None,
    ):
        if isinstance(watch_paths, (str, Path)):
            self.watch_paths: List[Path] = [Path(watch_paths).resolve()]
        else:
            self.watch_paths = [Path(p).resolve() for p in watch_paths]
        for path in self.watch_paths:
            if not path.exists():
                raise FileNotFoundError(f"监控路径不存在：{path}")
        self.callback = callback
        self.observer: Optional[Observer] = None  # Watchdog的观察者对象 # type: ignore
        self.event_handler = XamlFileHandler(callback=callback)

    def start(self) -> None:
        """启动监控（保持原有方法名和用法）"""
        self.observer = Observer()
        for watch_path in self.watch_paths:
            self.observer.schedule(
                self.event_handler,
                str(watch_path),
                recursive=True,  # 保持递归监控子目录的逻辑
            )
        self.observer.start()

    def stop(self, timeout: float = 5.0) -> None:
        """停止监控（保持原有方法名和用法，带超时保护）"""
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.join(timeout=timeout)
            self.observer = None
