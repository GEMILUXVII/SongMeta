"""
元数据解析模块
负责读取JSON文件中的元数据信息
"""

import json
from pathlib import Path

from utils.helpers import timestamp_to_date


def parse_json_metadata(json_path: str | Path) -> dict | None:
    """
    解析JSON元数据文件
    
    Args:
        json_path: JSON文件路径
    
    Returns:
        包含解析后元数据的字典，或None（如果文件不存在/解析失败）
    """
    json_file = Path(json_path)
    
    if not json_file.exists():
        return None
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        result = {}
        
        # 提取并转换 pubtimestamp
        if 'pubtimestamp' in data:
            result['date'] = timestamp_to_date(data['pubtimestamp'])
            result['pubtimestamp'] = data['pubtimestamp']
        
        # 保留其他可能有用的字段
        for key in ['title', 'author', 'description']:
            if key in data:
                result[key] = data[key]
        
        return result
    
    except (json.JSONDecodeError, IOError) as e:
        print(f"[错误] 解析JSON文件失败 {json_path}: {e}")
        return None


def extract_date_from_metadata(json_path: str | Path) -> str | None:
    """
    从JSON元数据中提取日期
    
    Args:
        json_path: JSON文件路径
    
    Returns:
        YYYY-MM-DD 格式的日期字符串，或None
    """
    metadata = parse_json_metadata(json_path)
    return metadata.get('date') if metadata else None
