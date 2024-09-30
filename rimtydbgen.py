from sys import argv, stderr, exit

from func import HistoryToJson, PlaylistMapping


if __name__ == '__main__':
    if len(argv) < 2:
        print(f'Usage: python {argv[0]} <convert|get-playlist-map>', file=stderr)
        exit(1)

    try:
        if argv[1] == 'convert':
            HistoryToJson()
        if argv[1] == 'get-playlist-map':
            PlaylistMapping()
    except KeyboardInterrupt:
        print('Program stopped as requested by user')
        exit(0)
