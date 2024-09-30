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
    author_to_songs: dict[str, list] = {}
    channel_to_songs: dict[str, list] = {}
    channel_to_author: dict[str, Artist] = {}            
    playlist_map: dict[str, list] = {}

    # Read playlist names from 'playlist_map_path'
    jsonfile: dict = load_json(playlist_map_path)
    for artist_name, playlist_names in jsonfile.items():
        # Skip if playlist name is empty
        if len(playlist_names) == 0:
            continue
        
        for playlist_name in playlist_names:
            if not playlist_name in playlist_map:
                playlist_map[playlist_name] = []
                
            playlist_map[playlist_name].append(artist_name)

    # Query songs from 'query_path'
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
                
                dirname: str = os.path.dirname(filepath)
                if dirname == query_path:
                    continue
                
                author_name: str = os.path.basename(dirname)
                if not author_name in author_to_songs:
                    author_to_songs[author_name] = []    
                author_to_songs[author_name].append(song)
                                
    songs: SongTable = SongTable()
    artists: ArtistTable = ArtistTable()
    playlists: PlaylistTable = PlaylistTable()
    
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
            
    for playlist_name, artist_names in playlist_map.items():
        playlist: Playlist = playlists.get_or_create(playlist_name)
    
        for artist_name in artist_names:
            if not artist_name in author_to_songs:
                continue
            
            for song in author_to_songs[artist_name]:
                playlist.add(song)
            
    # Open databse for modification
    connection = sqlite3.connect(databse_path)
    cursor = connection.cursor()
                
    songs.write_to_database(cursor)
    artists.write_to_database(cursor)
    playlists.write_to_database(cursor)
    
    # Apply changes
    connection.commit()
    connection.close()
        