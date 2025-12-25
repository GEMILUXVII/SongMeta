"""
工具函数模块
提供通用的辅助功能：日期转换、文件名提取等
"""

import re
from datetime import datetime
from pathlib import Path


def extract_song_name(filename: str) -> str | None:
    """
    从文件名中提取《》包裹的歌曲名
    
    Args:
        filename: 原始文件名，如 "【星瞳】《红山果》.mp3"
    
    Returns:
        提取的歌曲名，如 "红山果"；若无匹配则返回 None
    """
    pattern = r'《(.+?)》'
    match = re.search(pattern, filename)
    return match.group(1) if match else None


def timestamp_to_date(timestamp: int | float) -> str:
    """
    将Unix时间戳转换为 YYYY-MM-DD 格式的日期字符串
    
    Args:
        timestamp: Unix时间戳（秒）
    
    Returns:
        格式化的日期字符串，如 "2025-01-25"
    """
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%Y-%m-%d')


def ensure_directory(path: str | Path) -> Path:
    """
    确保目录存在，如不存在则创建
    
    Args:
        path: 目录路径
    
    Returns:
        Path对象
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def safe_filename(name: str) -> str:
    """
    清理文件名中的非法字符
    
    Args:
        name: 原始文件名
    
    Returns:
        清理后的安全文件名
    """
    # Windows 文件名非法字符
    illegal_chars = r'[<>:"/\\|?*]'
    return re.sub(illegal_chars, '', name)
