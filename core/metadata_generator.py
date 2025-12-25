"""
元数据生成模块
负责生成格式化的歌曲元数据并导出
"""

from pathlib import Path
from typing import Any


def create_song_metadata(
    title: str,
    subtitle: str,
    date: str,
    artist: str = "星瞳",
    tags: list[str] | None = None,
    cover_path: str = "/covers",
    audio_path: str = "/audio"
) -> dict:
    """
    创建单首歌曲的元数据对象
    
    Args:
        title: 歌曲名
        subtitle: 原唱歌手
        date: 发布日期 YYYY-MM-DD
        artist: 翻唱歌手，默认 "星瞳"
        tags: 标签列表，默认 ['翻唱']
        cover_path: 封面路径前缀
        audio_path: 音频路径前缀
    
    Returns:
        格式化的元数据字典
    """
    if tags is None:
        tags = ['翻唱']
    
    return {
        'title': title,
        'subtitle': subtitle or '',
        'artist': artist,
        'date': date,
        'cover': f"{cover_path}/{title}.jpg",
        'audio': f"{audio_path}/{title}.mp3",
        'tags': tags,
    }


def generate_all_metadata(songs_data: list[dict]) -> list[dict]:
    """
    批量生成所有歌曲元数据
    
    Args:
        songs_data: 歌曲数据列表，每项包含 title, subtitle, date
    
    Returns:
        元数据列表
    """
    metadata_list = []
    
    for song in songs_data:
        metadata = create_song_metadata(
            title=song.get('title', ''),
            subtitle=song.get('subtitle', ''),
            date=song.get('date', ''),
        )
        metadata_list.append(metadata)
    
    return metadata_list


def format_metadata_as_js(metadata_list: list[dict]) -> str:
    """
    将元数据列表格式化为JavaScript数组格式
    
    Args:
        metadata_list: 元数据列表
    
    Returns:
        JavaScript代码字符串
    """
    lines = ["export const songs = ["]
    
    for item in metadata_list:
        lines.append("  {")
        lines.append(f"    title: '{item['title']}',")
        lines.append(f"    subtitle: '{item['subtitle']}',")
        lines.append(f"    artist: '{item['artist']}',")
        lines.append(f"    date: '{item['date']}',")
        lines.append(f"    cover: '{item['cover']}',")
        lines.append(f"    audio: '{item['audio']}',")
        lines.append(f"    tags: {item['tags']},")
        lines.append("  },")
    
    lines.append("];")
    
    return "\n".join(lines)


def export_to_js(metadata_list: list[dict], output_path: str | Path) -> Path:
    """
    将元数据导出为JavaScript文件
    
    Args:
        metadata_list: 元数据列表
        output_path: 输出文件路径
    
    Returns:
        输出文件路径
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    js_content = format_metadata_as_js(metadata_list)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    return output_file


def export_to_json(metadata_list: list[dict], output_path: str | Path) -> Path:
    """
    将元数据导出为JSON文件
    
    Args:
        metadata_list: 元数据列表
        output_path: 输出文件路径
    
    Returns:
        输出文件路径
    """
    import json
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata_list, f, ensure_ascii=False, indent=2)
    
    return output_file
