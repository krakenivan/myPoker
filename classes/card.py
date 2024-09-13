class Card:
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, rank: str, suit: str):
        self.__rank = rank
        self.__suit = suit
        self.__score = self.ranks.index(self.__rank) + 1

    @property
    def rank(self):
        return self.__rank

    @property
    def suit(self):
        return self.__suit

    @property
    def score(self):
        return self.__score

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def __hash__(self):
        return hash(self.__rank) + hash(self.__suit)

    def __eq__(self, other):
        return isinstance(other, Card) and self.score == other.score

    def __gt__(self, other):
        return isinstance(other, Card) and self.score > other.score
