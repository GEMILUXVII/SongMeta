"""
封面下载器 - 从QQ音乐分享链接下载封面

用法:
    uv run python cover.py <分享链接> [保存路径]
    
示例:
    uv run python cover.py "https://c.y.qq.com/base/fcgi-bin/u?__=xxx"
    uv run python cover.py "https://y.qq.com/n/ryqq/songDetail/xxx" ./cover.jpg
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from api.qq_music import get_api


def main():
    if len(sys.argv) < 2:
        print("用法: uv run python cover.py <QQ音乐分享链接> [保存路径]")
        print()
        print("示例:")
        print('  uv run python cover.py "https://c.y.qq.com/base/fcgi-bin/u?__=xxx"')
        print('  uv run python cover.py "https://y.qq.com/n/ryqq/songDetail/xxx" ./cover.jpg')
        sys.exit(1)
    
    share_link = sys.argv[1]
    
    # 获取API实例
    api = get_api()
    
    # 解析链接获取歌曲信息
    print(f"正在解析链接...")
    song_mid = api.parse_share_link(share_link)
    
    if not song_mid:
        print("[错误] 无法解析分享链接")
        sys.exit(1)
    
    print(f"歌曲MID: {song_mid}")
    
    # 获取歌曲信息
    song_info = api.get_song_info_by_mid(song_mid)
    
    if not song_info.get('title'):
        print("[错误] 无法获取歌曲信息")
        sys.exit(1)
    
    title = song_info.get('title', '未知')
    artist = song_info.get('artist', '未知')
    
    print(f"歌曲: {title}")
    print(f"歌手: {artist}")
    
    # 确定保存路径
    if len(sys.argv) >= 3:
        save_path = Path(sys.argv[2])
    else:
        save_path = Path(f"./{title}.jpg")
    
    # 下载封面
    if song_info.get('cover_url'):
        print(f"正在下载封面...")
        if api.download_cover(song_info['cover_url'], save_path):
            print(f"[成功] 封面已保存到: {save_path.resolve()}")
        else:
            print("[错误] 下载封面失败")
            sys.exit(1)
    else:
        print("[错误] 无法获取封面URL")
        sys.exit(1)


if __name__ == '__main__':
    main()
