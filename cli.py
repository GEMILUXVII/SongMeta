"""
音乐元数据处理器 - CLI入口

用法:
    uv run python cli.py --source <源目录> --output <输出目录>
    
示例:
    uv run python cli.py --source D:/music/source --output ./output
"""

import argparse
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from core.file_processor import scan_source_directory, rename_mp3_file, export_song_names
from core.metadata_parser import extract_date_from_metadata
from core.metadata_generator import create_song_metadata, export_to_js
from api.qq_music import get_song_info, download_cover
from utils.helpers import ensure_directory


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='音乐元数据处理器 - 处理MP3文件并生成格式化元数据',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  uv run python cli.py --source D:/music/source --output ./output
  uv run python cli.py -s ./input -o ./output --covers ./output/covers
        '''
    )
    
    parser.add_argument(
        '-s', '--source',
        type=str,
        required=True,
        help='源文件目录路径（包含MP3和JSON文件）'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='./output',
        help='输出目录路径（默认: ./output）'
    )
    
    parser.add_argument(
        '--covers',
        type=str,
        default=None,
        help='封面保存目录（默认: <output>/covers）'
    )
    
    parser.add_argument(
        '--no-rename',
        action='store_true',
        help='不重命名原始MP3文件，仅复制到输出目录'
    )
    
    parser.add_argument(
        '--skip-api',
        action='store_true',
        help='跳过QQ音乐API调用（不获取歌手信息和封面）'
    )
    
    return parser.parse_args()


def main():
    """主程序入口"""
    args = parse_args()
    
    # 解析路径
    source_dir = Path(args.source).resolve()
    output_dir = Path(args.output).resolve()
    covers_dir = Path(args.covers).resolve() if args.covers else output_dir / 'covers'
    audio_dir = output_dir / 'audio'  # 音频输出目录
    
    # 验证源目录
    if not source_dir.exists():
        print(f"[错误] 源目录不存在: {source_dir}")
        sys.exit(1)
    
    # 创建输出目录
    ensure_directory(output_dir)
    ensure_directory(covers_dir)
    ensure_directory(audio_dir)
    
    print(f"源目录: {source_dir}")
    print(f"输出目录: {output_dir}")
    print(f"音频目录: {audio_dir}")
    print(f"封面目录: {covers_dir}")
    print("-" * 50)
    
    # 1. 扫描源目录
    print("[1/6] 扫描源目录...")
    file_pairs = scan_source_directory(source_dir)
    print(f"      找到 {len(file_pairs)} 个MP3文件")
    
    if not file_pairs:
        print("[完成] 未找到符合条件的文件")
        return
    
    # 2. 提取歌名并导出
    print("[2/6] 提取歌曲名...")
    song_names = [pair['song_name'] for pair in file_pairs]
    songs_file = export_song_names(song_names, output_dir / 'songsname.txt')
    print(f"      已导出歌名列表到: {songs_file}")
    
    # 3. 重命名并复制MP3文件
    print("[3/6] 重命名并复制MP3文件...")
    for i, pair in enumerate(file_pairs, 1):
        song_name = pair['song_name']
        new_path = rename_mp3_file(pair['mp3_path'], song_name, audio_dir)
        print(f"      [{i}/{len(file_pairs)}] {pair['original_name']} -> {new_path.name}")
    
    # 4. 处理每首歌曲元数据
    print("[4/6] 处理歌曲元数据...")
    processed_songs = []
    
    for i, pair in enumerate(file_pairs, 1):
        song_name = pair['song_name']
        print(f"      [{i}/{len(file_pairs)}] {song_name}")
        
        # 提取日期
        date = ''
        if pair['json_path']:
            date = extract_date_from_metadata(pair['json_path']) or ''
        
        # 获取QQ音乐信息
        subtitle = ''
        if not args.skip_api:
            print(f"            正在获取歌手信息...")
            song_info = get_song_info(song_name)
            subtitle = song_info.get('artist', '') or ''
            
            # 下载封面
            if song_info.get('cover_url'):
                cover_path = covers_dir / f"{song_name}.jpg"
                if download_cover(song_name, cover_path):
                    print(f"            已下载封面")
                else:
                    print(f"            封面下载失败")
        
        processed_songs.append({
            'title': song_name,
            'subtitle': subtitle,
            'date': date,
        })
    
    # 5. 生成元数据
    print("[5/6] 生成元数据...")
    metadata_list = []
    for song in processed_songs:
        metadata = create_song_metadata(
            title=song['title'],
            subtitle=song['subtitle'],
            date=song['date'],
        )
        metadata_list.append(metadata)
    
    # 6. 导出
    print("[6/6] 导出结果...")
    js_file = export_to_js(metadata_list, output_dir / 'songs_metadata.js')
    print(f"      已导出元数据到: {js_file}")
    
    print("-" * 50)
    print(f"[完成] 成功处理 {len(processed_songs)} 首歌曲")
    print(f"       歌名列表: {output_dir / 'songsname.txt'}")
    print(f"       元数据文件: {js_file}")
    print(f"       音频目录: {audio_dir}")
    print(f"       封面目录: {covers_dir}")


if __name__ == '__main__':
    main()
