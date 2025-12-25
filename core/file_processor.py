"""
文件处理模块
负责扫描源目录、重命名MP3文件、导出歌名列表
"""

import shutil
from pathlib import Path

from utils.helpers import extract_song_name, safe_filename


def scan_source_directory(source_dir: str | Path) -> list[dict]:
    """
    扫描源目录，获取MP3和对应JSON文件对
    
    Args:
        source_dir: 源文件目录路径
    
    Returns:
        文件对列表，每项包含 mp3_path, json_path, song_name
    """
    source_path = Path(source_dir)
    file_pairs = []
    
    # 获取所有MP3文件
    mp3_files = list(source_path.glob('*.mp3'))
    
    for mp3_file in mp3_files:
        # 提取歌曲名
        song_name = extract_song_name(mp3_file.name)
        if not song_name:
            print(f"[跳过] 无法从文件名提取歌曲名: {mp3_file.name}")
            continue
        
        # 查找对应的JSON文件（文件名前缀相同）
        # 文件名格式: 【星瞳】《歌名》.mp3 -> 【星瞳】《歌名》.json
        json_name = mp3_file.stem + '.json'
        json_path = source_path / json_name
        
        # 也尝试其他可能的JSON命名格式
        if not json_path.exists():
            # 尝试带BW后缀的格式
            for json_file in source_path.glob('*.json'):
                if song_name in json_file.name:
                    json_path = json_file
                    break
        
        file_pairs.append({
            'mp3_path': mp3_file,
            'json_path': json_path if json_path.exists() else None,
            'song_name': song_name,
            'original_name': mp3_file.name
        })
    
    return file_pairs


def rename_mp3_file(mp3_path: Path, song_name: str, output_dir: Path | None = None) -> Path:
    """
    重命名MP3文件，使用提取的歌曲名
    
    Args:
        mp3_path: 原始MP3文件路径
        song_name: 新的歌曲名
        output_dir: 可选，输出目录（若指定则复制而非重命名）
    
    Returns:
        新文件路径
    """
    safe_name = safe_filename(song_name)
    new_filename = f"{safe_name}.mp3"
    
    if output_dir:
        new_path = output_dir / new_filename
        shutil.copy2(mp3_path, new_path)
    else:
        new_path = mp3_path.parent / new_filename
        mp3_path.rename(new_path)
    
    return new_path


def export_song_names(song_names: list[str], output_path: str | Path) -> Path:
    """
    将歌曲名列表导出到文本文件
    
    Args:
        song_names: 歌曲名列表
        output_path: 输出文件路径
    
    Returns:
        输出文件路径
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for name in song_names:
            f.write(f"{name}\n")
    
    return output_file
