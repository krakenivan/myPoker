from .hand import Hand
class Player:
    def __init__(self, name: str):
        self.name = name
        self._stack: int = 1000
        self.hand: Hand = Hand()

    def __str__(self):
        return f'{self.name}: {self.hand.show()}'
    def __repr__(self):
        return f'{self.name}: {self.hand.show()}'

    def drop(self):
        self.hand.drop()