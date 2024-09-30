import os
import json
import sqlite3

from models import Song, Artist, Playlist
from models.table import Song as SongTable, Artist as ArtistTable, Playlist as PlaylistTable



def load_json(filepath: str) -> dict:
    with open(filepath, 'r') as file:
        data = json.load(file)
        
    return data
    

def main(
    query_path: str = 'listened',
    playlist_map_path: str = 'playlists.json',
    databse_path: str = 'RiMusic.db'
):
    channel_to_songs: dict[str, list] = {}
    channel_to_author: dict[str, Artist] = {}            
    
    for root, dirs, names in os.walk(query_path):
        for filename in names:
            
            if not filename.endswith('.json'):
                continue
            
            filepath: str = os.path.join(root, filename)
            jsonfile: dict = load_json(filepath)
            if 'author.json' == filename:
                artist: Artist = Artist(jsonfile)
                                    
                channel_to_author[artist.id] = artist
            else:
                song: Song = Song(jsonfile)
                channelId: str = song['channelId']
                
                if not song.id in channel_to_songs:
                    channel_to_songs[channelId] = []
                    
                channel_to_songs[channelId].append(song)
                                
    songs: SongTable = SongTable()
    artists: ArtistTable = ArtistTable()
    
    for channelId, artist in channel_to_author.items():
        artists.add(artist)
        
        # Check if artist has any song
        if not channelId in channel_to_songs.keys():
            continue
        
        # Map songs to artists
        for song in channel_to_songs[channelId]:
            artist.add(song)
        
    for song_list in channel_to_songs.values():
        for song in song_list:
            songs.add(song)    
        
    
    # Open databse for modification
    connection = sqlite3.connect(databse_path)
    cursor = connection.cursor()
                
    songs.write_to_database(cursor)
    artists.write_to_database(cursor)
    
    # Apply changes
    connection.commit()
    connection.close()
        