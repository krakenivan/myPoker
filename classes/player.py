from .hand import Hand
from .combination import *


class Player:
    def __init__(self, name: str):
        self.name = name
        self._stack: int = 1000
        self.hand: Hand = Hand()
        self.combination = None

    def __str__(self):
        if self.combination:
            return f'{self.name}: {self.hand} - {self.combination}'
        return f'{self.name}: {self.hand}'

    def __repr__(self):
        if self.combination:
            return f'{self.name}: {self.hand} - {self.combination}'
        return f'{self.name}: {self.hand}'

    def show_rating_combination(self):
        return self.combination.rating

    def show_high_card(self):
        return self.combination.high_card

    def drop(self):
        self.hand.drop()
        self.combination = None

    def __eq__(self, other):
        return isinstance(other, Player) and self.combination.rating == self.combination.rating
