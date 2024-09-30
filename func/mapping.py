from json import dumps

import os



def main(
    query_path: str = 'listened',
    playlist_filepath: str = 'playlists.json'
) -> None:
    """
    This functionality creates a JSON file that contains
    info related to artists such as language, genre, etc.

    It allows a more fine-grined database.
    """
 
    artists: dict[str, list] = {}
    for name in os.listdir(query_path):
        filepath: str = os.path.join(query_path, name)
        # Filter out directories
        if not os.path.isdir(filepath):
            continue
        
        artists[name] = []

    with open(playlist_filepath, 'w') as file:
        file.write(dumps(artists, indent=2, ensure_ascii=False))    

