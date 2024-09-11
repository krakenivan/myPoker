from .card import Card

class Hand:

    def __init__(self, card_list: list[Card] = None):
        if card_list is None:
            self._hand: list[Card] = []
        else:
            self._hand = card_list


    def show(self):
        return self._hand

    def __add__(self, other):
        if isinstance(other, Card):
            other = Hand([other])
        return Hand(self.show() + other.show())

    def drop(self):
        self._hand.clear()
