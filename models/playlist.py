from sqlite3 import Cursor

from .song import Song



class Playlist:
    
    def __init__(self, id: int, name: str, browseId: str = None) -> None:
        self._id: int = id
        self._name: str = name
        self._browseId: str = browseId
        self._songs: dict[str, Song] = {}
        
        self._position: int = 0
        self._song_positions: [Song, int] = {}
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def browseId(self) -> str | None:
        return self._browseId
    
    @property
    def songs(self) -> set[Song]:
        return set(self._songs.values())
    
    def add(self, song: Song) -> None:
        self._songs[song.title] = song
        
        self._song_positions[song] = self._position
        self._position += 1
        
    def get(self, song_name: str) -> Song | None:
        if song_name in self._songs.keys():
            return self._songs[song_name]
        else:
            return None
        
    def write_to_database(self, cursor: Cursor) -> None:
        for song in self.songs:
            cursor.execute(
                f'INSERT INTO SongPlaylistMap (songId, playlistId, position) VALUES (?, ?, ?)',
                (song.id, self.id, self._song_positions[song])
            )
        