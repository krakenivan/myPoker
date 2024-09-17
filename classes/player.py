from .hand import Hand
from .combination import *


class Player:
    def __init__(self, name: str):
        self.name = name
        self.stack: int | float = float(1000)
        self.dealer = False
        self.sb = False
        self.bb = False
        self.hand: Hand = Hand()
        self.combination = None
        self.bet_fold = False
        self.last_bet_amount = 0
        self.list_bet = []

    def __str__(self):
        output = f'{self.name}: {self.hand} | Стэк={self.stack}'
        if self.combination:
            output += f' - {self.combination}'
        if self.dealer:
            output += ' Dealer'
        if self.sb:
            output += ' SB'
        if self.bb:
            output += ' BB'
        if self.list_bet:
            output += f'\nДоступные ставки: {self.list_bet}'
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

    def bet(self, bet_size: int | float):
        self.stack -= bet_size
        self.last_bet_amount = bet_size
        return bet_size

    def bet_increase(self, bet_size):
        self.stack += self.last_bet_amount
        self.stack -= bet_size
        self.last_bet_amount = bet_size




    def __eq__(self, other):
        return isinstance(other, Player) and self.combination.rating == self.combination.rating
