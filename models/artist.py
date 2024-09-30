from sqlite3 import Cursor
import time

from utils import Json
from models import Song



class Artist(Json):

    def __init__(self, json: dict) -> None:
        super().__init__(json)

        self._thumbnailUrl: str = ''
        self._current_time: int = int(time.time() * 1000)
        
        self._songs: dict[str, Song] = {}

    @property
    def id(self) -> str:
        return self['channelId']

    @property
    def name(self) -> str:
        return self['name']

    @property
    def thumbnailUrl(self) -> str:
        if not self._thumbnailUrl:
            max_width, max_height = 1280, 720
            pre_width, pre_height = 0, 0

            for thumbnail in self['thumbnails']:
                width, height = thumbnail['width'], thumbnail['height']

                if width <= pre_width or height <= pre_height:
                    continue
                if width > max_width or height > max_height:
                    continue

                self._thumbnailUrl = thumbnail['url']
                
                pre_width = width
                pre_height = height
    
        return self._thumbnailUrl

    @property
    def timestamp(self) -> int:
        return self._current_time

    @property
    def bookmarkedAt(self) -> int:
        return self._current_time
    
    def get(self, song_name: str) -> Song | None:
        if song_name in self._songs.keys():
            return self._songs[song_name]
        else:
            return None
        
    def add(self, song: Song) -> None:
        self._songs[song.title] = song
        
    def write_to_database(self, cursor: Cursor) -> None:
        for song in self._songs.values():
            cursor.execute(
                f'INSERT INTO SongArtistMap (songId, artistid) VALUES (?, ?)',
                (song.id, self.id)
            )