import random

import textdistance
from typing import List


def bullscows(guess: str, secret: str) -> (int, int):
    cnt_byks = textdistance.hamming.similarity(guess, secret)
    cnt_korov = textdistance.bag.similarity(guess, secret) - cnt_byks
    return (cnt_byks, cnt_korov)


def gameplay(ask: callable, inform: callable, words: List[str]) -> int:
    random_word = random.choice(words)
    cnt_asks = 0
    while True:
        user_word = ask("Введите слово: ", words)
        cnt_asks += 1
        cnt_byks, cnt_korov = bullscows(user_word, random_word)
        inform("Быки: {}, Коровы: {}", cnt_byks, cnt_korov)
        if cnt_byks == len(random_word):
            return cnt_asks
