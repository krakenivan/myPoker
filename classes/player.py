from .hand import Hand
# from .combination import *


class Player:
    def __init__(self, name: str):
        self.name: str = name
        self.stack: int | float = float(1000)
        self.copy_stack = self.stack
        self.dealer: bool = False
        self.sb: bool = False
        self.bb: bool = False
        self.hand: Hand = Hand()
        self.bet_fold: bool = False
        self.is_allin = False
        self.sum_allin = 0
        self.player_allin_bank = 0
        self.is_sum_all_in_bank = False
        self.last_bet_amount: int | float = 0
        self.list_bet: list = []
        self.actual_allin = 0
        self.another_bank_over_all_in = 0
        self.player_another_bank_all_in = 0

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
        # if self.list_bet:
        #     output += f'\nДоступные ставки: {self.list_bet}'
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
        """Сброс карт"""
        self.hand.drop()
        self.combination = None

    def bet(self, bet_size: int | float):
        """Ставка"""
        self.copy_stack = self.stack
        self.stack -= bet_size
        self.last_bet_amount = bet_size

        return bet_size

    def bet_increase(self, bet_size):
        """Увеличение ставки"""
        self.stack += self.last_bet_amount
        self.stack -= bet_size
        self.last_bet_amount = bet_size

    def bet_allin(self):
        self.stack += self.last_bet_amount
        # return_sum = self.stack
        self.actual_allin = self.copy_stack

        self.is_allin = True
        self.sum_allin = self.stack
        self.stack = 0
        return self.sum_allin

    def make_copy_stack(self, stack):
        self.copy_stack = self.stack

    def __eq__(self, other):
        return isinstance(other, Player) and self.combination.rating == self.combination.rating

    def __gt__(self, other):
        if isinstance(other, Player) and self.combination.rating == other.combination.rating:
            return self.combination > other.combination
        return isinstance(other, Player) and self.combination.rating > other.combination.rating
