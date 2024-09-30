from sqlite3 import Cursor

from .table import Table
from models import Playlist as PlaylistModel



class Playlist(Table):
    
    def __init__(self) -> None:
        super().__init__('Playlist')
        
        self._position: int = 0
        self._playlists: dict[str, PlaylistModel] = {}
        
    @property
    def playlists(self) -> set[PlaylistModel]:
        return set(self._playlists.values())
    
    def add(self, name: str, browseId: str = None) -> None:
        self._playlists[name] = PlaylistModel(self._position, name, browseId)
        self._position += 1    
        
    def get_or_create(self, name: str) -> PlaylistModel:
        if not name in self._playlists.keys():
            self.add(name)
            
        return self._playlists[name]

    def write_to_database(self, cursor: Cursor) -> None:
        for playlist in self.playlists:
            playlist.write_to_database(cursor)
            
            cursor.execute(
                f'INSERT INTO {self.tableName} (id, name, browseId) VALUES (?, ?, ?)',
                (playlist.id, playlist.name, playlist.browseId)
            )