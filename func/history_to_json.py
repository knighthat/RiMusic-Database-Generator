from sys import stderr, exit
from json import load as toJson, dumps
from ytmusicapi import YTMusic

import os
import re
from models import Song, Artist


HISTORY_DIR: str = 'Takeout/YouTube and YouTube Music/history'
WATCH_HISTORY_FILENAME: str = 'watch-history.json'

SONG_URL_REGEX = r'https:\/\/(?:www|music)\.youtube\.com\/watch\?v(?:=|\\u003d)([a-zA-Z0-9_-]{11})'
CHANNEL_URL_REGEX = r'https:\/\/www\.youtube\.com\/channel\/([a-zA-Z0-9_-]+)'



def save(filepath: str, video_details: dict) -> None:
    dirname: str = os.path.dirname(filepath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    if not os.path.exists(filepath):
        with open(filepath, 'w') as file:
            file.write(dumps(video_details,indent=2))


def main(
    watched_history_path: str = f'{HISTORY_DIR}/', 
    save_path: str = 'listened',
    max_retrieve: int = 20,
    max_query: int = 200
) -> None:
    """
    Go through watch-history.json to get video's information.

    :param watch_history_path:  where watch-history.json lives
    :param save_path:           location where retrieved information will be saved
    :param max_retrieve:        stop requesting more information once the number of valid YTM songs achieved
    :param max_query:           stop requesting more information once the total queries reaches this number
    """

    # Parse watch-history.json
    watched: list[dict]
    try:
        watch_history_filepath: str = os.path.join(watched_history_path, WATCH_HISTORY_FILENAME)
        with open(watch_history_filepath, 'r') as watched_file:
            watched = toJson(watched_file)

        print(f'found {len(watched)} entries from {WATCH_HISTORY_FILENAME}.')
    except Exception as e:
        print(f'error occurs while reading {WATCH_HISTORY_FILENAME}.', file=stderr)
        print(e, file=stderr)
        exit(2)

    video_ids: set[str] = set()
    # Extract URLs from entries
    for entry in watched:
        url: str = entry['titleUrl']

        match: re.Match = re.match(SONG_URL_REGEX, url)
        if match:
            video_ids.add(match.group(1))
        else:
            print(f'{url} is not a valid YouTube/YouTube Music url.')

    print(f'{len(video_ids)}/{len(watched)} enique entries filtered.')

    # Retrive song's info
    ytm = YTMusic()

    author_song_map: dict[str, list] = {}

    valid_count, total = 0, 0
    for id in video_ids:
        if valid_count >= max_retrieve:
            print(f'Number of retrieved files reached the maximum allowed ({max_retrieve}). Stopping...')
            break
        if total >= max_query:
            print(f'Number of queries reached the maximum allowed ({max_query}). Stopping...')
            break

        try:
            response: dict = ytm.get_song(id)

            # Checking if video can be played via YouTubeMusic
            if response['playabilityStatus']['status'] == 'OK':
                video_details: dict = response['videoDetails']

                author: str = video_details['channelId']
                if not author in author_song_map.keys():
                    # Init song list of this author if this author is new
                    author_song_map[author] = []
                
                author_song_map[author].append(video_details)

                valid_count += 1

            else:
                print(f'{id} is not playable')

        except Exception as e:
            print(f'error occurs while retriving {id}\'s information!', file=stderr)
            print(e)
            continue

        total += 1

    print(f'{len(author_song_map.values())}/{len(video_ids)} ids are playable songs')
    
    for author_id, song_list in author_song_map.items():
        author_path: str
        if len(song_list) > 1:
            # Skip path making & author's information retrival 
            # if there's only 1 song belongs to this artist
            author_path = os.path.join(save_path, author_id)

            try:
                response: dict = ytm.get_artist(author_id)
                artist: Artist = Artist(response)

                author_path = os.path.join(save_path, artist.name)
                save(os.path.join(author_path, 'author.json'), response)

            except Exception as e:
                print(e)
                print(f'failed to retrieve information of author {author_id}.', file=stderr)
                print('songs will be saved without \"author.json\" inside artist\'s folder', file=stderr)
        else:
            author_path = save_path

        for song in song_list:
            filename: str = f'{song['title']}.json'
            filepath: str = os.path.join(author_path, filename)

            save(filepath, song)