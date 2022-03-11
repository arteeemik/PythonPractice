import argparse
from typing import List

import urllib.request as req

from .bullscows import gameplay


def ask(message: str, list_words: List[str] = None) -> str:
    while True:
        in_word = input(message)
        if in_word in list_words or list_words is None:
            return in_word


def inform(format_string: str, byks: int, korovs: int) -> None:
    print(format_string.format(byks, korovs))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Byks and korovs.')
    parser.add_argument('vocab', nargs='?', type=str, help='Slovar (url or path to file.')
    parser.add_argument('len', nargs='?', type=int, default=5, help='Len words.')

    args = parser.parse_args()

    if args.vocab.startswith('https://') or args.vocab.startswith('http://'):
        with req.urlopen(args.vocab) as file:
            words = [word for word in file.read().decode('utf-8').split() if len(word) == args.len]
    else:
        with open(args.vocab, encoding='utf-8') as file:
            words = [word for word in '\n'.join(file.readlines()).split() if len(word) == args.len]

    ans = gameplay(ask, inform, words)
    print(f'Количество попыток: {ans}')
