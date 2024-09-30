from sqlite3 import Cursor

from .table import Table
from models import Song as SongModel



class Song(Table):

    def __init__(self) -> None:
        super().__init__('Song')
        
        self._songs: set[SongModel] = set()
        
    @property
    def songs(self) -> set[SongModel]:
        return self._songs
    
    def add(self, song: SongModel) -> None:
        self._songs.add(song)
        
    def write_to_database(self, cursor: Cursor) -> None:
        for song in self.songs:
            cursor.execute(
                f'INSERT INTO {self.tableName} (id, title, artistsText, durationText, thumbnailUrl, likedAt, totalPlayTimeMs) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (song.id, song.title, song.artistsText, song.durationText, song.thumbnailUrl, song.likedAt, song.totalPlayTimeMs)
            )
            