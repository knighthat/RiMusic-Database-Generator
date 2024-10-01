from sys import argv, stderr, exit

from func import HistoryToJson, PlaylistMapping, WriteToDatabase, GenerateDatabase


if __name__ == '__main__':
    if len(argv) < 2:
        print(f'Usage: python {argv[0]} <convert|get-playlist-map|write|generate>', file=stderr)
        exit(1)

    try:
        if argv[1] == 'convert':
            HistoryToJson()
        if argv[1] == 'get-playlist-map':
            PlaylistMapping()
        if argv[1] == 'write':
            WriteToDatabase()
        if argv[1] == 'generate':
            GenerateDatabase()
    except KeyboardInterrupt:
        print('Program stopped as requested by user')
        exit(0)
