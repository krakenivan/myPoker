class Card:
    def __init__(self, rank: str, suit: str):
        self.__rank = rank
        self.__suit = suit

    @property
    def rank(self):
        return self.__rank

    @property
    def suit(self):
        return self.__suit

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def __hash__(self):
        return hash(self.__rank) + hash(self.__suit)

    def __eq__(self, other):
        return isinstance(other, Card) and self.rank == other.rank

    def __gt__(self, other):
        return isinstance(other, Card) and self.rank > other.rank
