from .hand import Hand
from .combination import *


class Player:
    def __init__(self, name: str):
        self.name = name
        self.stack: int = 1000
        self.dealer = False
        self.sb = False
        self.bb = False
        self.hand: Hand = Hand()
        self.combination = None

    def __str__(self):
        output = f'{self.name}: {self.hand}'
        if self.combination:
            output += f'{self.name}: {self.hand} - {self.combination}'
        if self.dealer:
            output += ' Dealer'
        if self.sb:
            output += ' SB'
        if self.bb:
            output += ' BB'
        return output

    def __repr__(self):
        if self.combination:
            return f'{self.name}: {self.hand} - {self.combination}'
        return f'{self.name}: {self.hand}'

    def show_rating_combination(self):
        return self.combination.rating

    # def show_high_card(self):
    #     return self.combination.high_card

    def drop(self):
        self.hand.drop()
        self.combination = None

    def bid(self, bet_size):
        self.stack -= bet_size
        return bet_size

    def __eq__(self, other):
        return isinstance(other, Player) and self.combination.rating == self.combination.rating
