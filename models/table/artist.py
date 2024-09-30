from sqlite3 import Cursor

from .table import Table
from models import Artist as ArtistModel



class Artist(Table):
    
    def __init__(self) -> None:
        super().__init__('Artist')
        
        self._position: int = 0
        self._artists: dict[str, ArtistModel] = {}
        
    @property
    def artists(self) -> set[ArtistModel]:
        return set(self._artists.values())
    
    def get(self, artist_name: str) -> ArtistModel | None:
        if not artist_name in self._artists.keys():
            return None
        else:
            return self._artists[artist_name]
    
    def add(self, artist: ArtistModel) -> None:
        self._artists[artist.name] = artist
        self._position += 1
        
    def write_to_database(self, cursor: Cursor) -> None:
        for artist in self.artists:
            cursor.execute(
                f'INSERT INTO {self.tableName} (id, name, thumbnailUrl, timestamp, bookmarkedAt) VALUES (?, ?, ?, ?, ?)',
                (artist.id, artist.name, artist.thumbnailUrl, artist.timestamp, artist.bookmarkedAt)
            )