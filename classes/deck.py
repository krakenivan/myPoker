from random import shuffle
from .card import Card

class Deck:
    # suits = ['\033[30m♠\033[0m', '\033[31m♥\033[0m', '\033[31m♦\033[0m', '\033[30m♣\033[0m']
    suits = ['♠', '♥', '♦', '♣']
    ranks = list(map(str, range(2, 11))) + list('JQKA')

    def __init__(self):
        self._deck: list[Card] = [Card(rank, suit) for rank in Deck.ranks for suit in Deck.suits]

    def shuffle(self):
        """перемешивание колоды"""
        shuffle(self._deck)

    def deal_card(self) -> Card:
        """Выдача карты"""
        return self._deck.pop()

    def __str__(self):
        rows = len(self._deck)//9
        res = ''
        for i in range(rows + 1):
            res += ' '.join(list(map(lambda x: f'{str(x):>12}', self._deck[10*i:10*i + 10]))) + '\n'
        return res
