import time

from utils import Json
from models import Song as SongModel



class Artist(Json):

    def __init__(self, json: dict) -> None:
        super().__init__(json)

        self._thumbnailUrl: str = ''
        self._current_time: int = int(time.time() * 1000)

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

                if width <= pre_width or pre_height <= pre_height:
                    continue
                if width > max_width or height > max_height:
                    continue

                self._thumbnailUrl = thumbnail['url']
    
        return self._thumbnailUrl

    @property
    def timestamp(self) -> int:
        return self._current_time

    @property
    def bookmarkedAt(self) -> int:
        return self._current_time