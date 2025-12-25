"""
QQ音乐API模块
负责搜索歌曲、获取歌手信息和下载封面
"""

import re
import requests
from pathlib import Path
from typing import Optional


class QQMusicAPI:
    """QQ音乐API封装类"""
    
    # 搜索API端点
    SEARCH_URL = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
    
    # 请求头，模拟浏览器
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://y.qq.com/',
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def search_song(self, song_name: str, limit: int = 10) -> list[dict]:
        """
        搜索歌曲
        
        Args:
            song_name: 歌曲名
            limit: 返回结果数量限制
        
        Returns:
            搜索结果列表
        """
        params = {
            'w': song_name,
            'format': 'json',
            'p': 1,
            'n': limit,
            'aggr': 1,
            'lossless': 1,
            'cr': 1,
            'new_json': 1,
        }
        
        try:
            response = self.session.get(self.SEARCH_URL, params=params, timeout=10)
            response.raise_for_status()
            
            # 处理JSONP响应
            text = response.text
            if text.startswith('callback('):
                text = text[9:-1]  # 移除 callback( 和 )
            elif text.startswith('MusicJsonCallback('):
                text = text[18:-1]
            
            data = response.json() if response.text.startswith('{') else __import__('json').loads(text)
            
            songs = data.get('data', {}).get('song', {}).get('list', [])
            return songs
        
        except requests.RequestException as e:
            print(f"[错误] 搜索歌曲失败 '{song_name}': {e}")
            return []
        except Exception as e:
            print(f"[错误] 解析搜索结果失败: {e}")
            return []
    
    def get_song_artist(self, song_name: str) -> Optional[str]:
        """
        获取歌曲的原唱歌手名
        
        Args:
            song_name: 歌曲名
        
        Returns:
            歌手名，若未找到则返回None
        """
        songs = self.search_song(song_name, limit=5)
        
        if not songs:
            return None
        
        # 取第一个匹配结果的歌手
        first_song = songs[0]
        
        # 提取歌手信息
        singers = first_song.get('singer', [])
        if singers:
            # 多个歌手用 / 分隔
            artist_names = [s.get('name', '') for s in singers if s.get('name')]
            return ' / '.join(artist_names) if artist_names else None
        
        return None
    
    def get_album_cover_url(self, song_name: str) -> Optional[str]:
        """
        获取歌曲专辑封面URL
        
        Args:
            song_name: 歌曲名
        
        Returns:
            封面图片URL
        """
        songs = self.search_song(song_name, limit=1)
        
        if not songs:
            return None
        
        first_song = songs[0]
        
        # 获取专辑mid
        album_mid = first_song.get('album', {}).get('mid', '')
        if album_mid:
            # 使用高质量封面URL
            return f"https://y.gtimg.cn/music/photo_new/T002R300x300M000{album_mid}.jpg"
        
        # 备用：使用albumid
        album_id = first_song.get('album', {}).get('id', 0)
        if album_id:
            return f"http://imgcache.qq.com/music/photo/album_300/{album_id % 100}/300_albumpic_{album_id}_0.jpg"
        
        return None
    
    def download_cover(self, url: str, save_path: str | Path) -> bool:
        """
        下载封面图片到本地
        
        Args:
            url: 封面图片URL
            save_path: 保存路径
        
        Returns:
            是否下载成功
        """
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            save_file = Path(save_path)
            save_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_file, 'wb') as f:
                f.write(response.content)
            
            return True
        
        except requests.RequestException as e:
            print(f"[错误] 下载封面失败 '{url}': {e}")
            return False
    
    def get_song_info(self, song_name: str) -> dict:
        """
        获取歌曲完整信息（歌手、封面URL）
        
        Args:
            song_name: 歌曲名
        
        Returns:
            包含 artist 和 cover_url 的字典
        """
        songs = self.search_song(song_name, limit=1)
        
        result = {
            'artist': None,
            'cover_url': None,
        }
        
        if not songs:
            return result
        
        first_song = songs[0]
        
        # 提取歌手
        singers = first_song.get('singer', [])
        if singers:
            artist_names = [s.get('name', '') for s in singers if s.get('name')]
            result['artist'] = ' / '.join(artist_names) if artist_names else None
        
        # 提取封面URL
        album_mid = first_song.get('album', {}).get('mid', '')
        if album_mid:
            result['cover_url'] = f"https://y.gtimg.cn/music/photo_new/T002R300x300M000{album_mid}.jpg"
        
        return result


# 模块级便捷函数
_api_instance = None

def get_api() -> QQMusicAPI:
    """获取API单例实例"""
    global _api_instance
    if _api_instance is None:
        _api_instance = QQMusicAPI()
    return _api_instance


def search_song(song_name: str) -> list[dict]:
    """搜索歌曲"""
    return get_api().search_song(song_name)


def get_song_artist(song_name: str) -> Optional[str]:
    """获取歌曲歌手"""
    return get_api().get_song_artist(song_name)


def get_song_info(song_name: str) -> dict:
    """获取歌曲信息"""
    return get_api().get_song_info(song_name)


def download_cover(song_name: str, save_path: str | Path) -> bool:
    """下载歌曲封面"""
    api = get_api()
    url = api.get_album_cover_url(song_name)
    if url:
        return api.download_cover(url, save_path)
    return False
