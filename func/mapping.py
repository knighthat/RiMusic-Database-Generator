from json import dumps

import os


SUPPORTED_PLAYLIST = [
    "language",
    "genre"
]



def main(
    query_path: str = 'listened',
    playlist_filepath: str = 'playlists.json'
) -> None:
    """
    This functionality creates a JSON file that contains
    info related to artists such as language, genre, etc.

    It allows a more fine-grined database.
    """
 
    artists: list[str] = []
    for root, dirs, files in os.walk(query_path):
        artist_name: str = os.path.basename(root)

        if not os.path.samefile(query_path, root):
            artists.append(artist_name)

    playlist_file: dict[str, dict] = {}
    for playlist in SUPPORTED_PLAYLIST:
        playlist_file[playlist] = {artist: "" for artist in artists}

    with open(playlist_filepath, 'w') as file:
        file.write(dumps(playlist_file, indent=2, ensure_ascii=False))    

