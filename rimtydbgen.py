from sys import argv, stderr, exit

from func import HistoryToJson


if __name__ == '__main__':
    if len(argv) < 2:
        print(f'Usage: python {argv[0]} <convert>', file=stderr)
        exit(1)

    try:
        if argv[1] == 'convert':
            HistoryToJson()
    except KeyboardInterrupt:
        print('Program stopped as requested by user')
        exit(0)
