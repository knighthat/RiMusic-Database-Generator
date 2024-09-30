from utils import Json

from utils.converter import sec_2_min


class Song(Json):

    def __init__(self, json: dict) -> None:
        super().__init__(json)
        
        self._thumbnailUrl: str = ''

    @property
    def id(self) -> str:
        return self['videoId']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def artistsText(self) -> str:
        return self['author']

    @property
    def durationText(self) -> str:
        lengthSeconds: int = int(self['lengthSeconds'])
        mins, secs = sec_2_min(lengthSeconds)
        
        return f'{mins}:{secs:02}'

    @property
    def thumbnailUrl(self) -> str | None:
        if not self._thumbnailUrl:
            size: int = 0
            for url in self['thumbnail']['thumbnails']:
                if url['width'] > size:
                    self._thumbnailUrl = url['url']
        
        return self._thumbnailUrl

    @property
    def likedAt(self) -> str | None:
        return None

    @property
    def totalPlayTimeMs(self) -> str:
        # Avoid getting deleted
        return 1000

    @property
    def channelId(self) -> str:
        return self['channel_id']
        