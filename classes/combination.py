from .card import Card


class RoyalFlush:
    __name = 'Royal Flush'
    __rating = 10

    def __init__(self, combination: list[Card]):
        self.combination = combination
        self.high_card: Card | None = None


class StraightFlush:
    __name = 'Straight Flush'
    __rating = 9

    def __init__(self, combination: list[Card]):
        self.combination = combination
        self.high_card: Card | None = None


class FourOfKind:
    __name = 'Four of kind'
    __rating = 8

    def __init__(self, combination: list[Card]):
        self.combination = combination
        self.high_card: Card | None = None


class FullHouse:
    __name = 'Full House'
    __rating = 7

    def __init__(self, combination: list[Card]):
        self.combination = combination
        self.high_card: Card | None = None


class Flush:
    __name = 'Flush'
    __rating = 6

    def __init__(self, combination: list[Card]):
        self.combination = sorted(combination, key=lambda x: x.score)
        # self.high_card: Card = self.combination[-1]

    def __str__(self):
        return f'{self.name}: {self.combination}'

    def __eq__(self, other):
        my_comb = sorted(self.combination, key=lambda x: x.score)
        other_comb = sorted(other.combination, key=lambda x: x.score)
        return all([my_card == other_card for my_card, other_card in zip(my_comb, other_comb)])

    def __gt__(self, other):
        my_comb = sorted(self.combination, key=lambda x: x.score)
        other_comb = sorted(other.combination, key=lambda x: x.score)
        while True:
            if len(my_comb) == 1 or len(other_comb) == 1:
                break
            elif max(my_comb) == max(other_comb):
                my_comb.remove(max(my_comb))
                other_comb.remove(max(other_comb))
            else:
                break
        return max(my_comb) > max(other_comb)

    @property
    def name(self):
        return self.__name

    @property
    def rating(self):
        return self.__rating


class Straight:
    __name = 'Straight'
    __rating = 5

    def __init__(self, combination: list[Card]):
        self.combination = combination
        self.high_card: Card | None = self.combination[-1]

    @property
    def name(self):
        return self.__name

    @property
    def rating(self):
        return self.__rating

    def __str__(self):
        return f'{self.name}: {self.combination}'

    def __eq__(self, other):
        return self.high_card.score == other.hhigh_card.score

    def __gt__(self, other):
        return self.high_card.score > other.high_card.score


class SetCard:
    __name = 'Set'
    __rating = 4

    def __init__(self, combination: list[Card]):
        self.combination = combination
        self.combination_card: Card | None = self.combination[-1]

    @property
    def name(self):
        return self.__name

    @property
    def rating(self):
        return self.__rating

    def __str__(self):
        return f'{self.name}: {self.combination}'

    def __eq__(self, other):
        return self.combination_card.score == other.combination_card.score

    def __gt__(self, other):
        return self.combination_card.score > other.combination_card.score


class TwoPairs:
    __name = 'Two Pairs'
    __rating = 3

    def __init__(self, combination: list[Card]):
        self.combination = combination
        self.high_card: Card | None = self.combination[-1]
        self.low_card: Card | None = self.combination[0]

    @property
    def name(self):
        return self.__name

    @property
    def rating(self):
        return self.__rating

    def __str__(self):
        return f'{self.name}: {self.combination}'

    def __eq__(self, other):
        return self.high_card.score == other.high_card.score and self.low_card.score == other.low_card.score

    def __gt__(self, other):
        if self.high_card.score == other.high_card.score:
            return self.low_card.score > other.low_card.score
        return self.high_card.score > other.high_card.score



class Pair:
    __name = 'Pair'
    __rating = 2

    def __init__(self, combination: list[Card]):
        self.combination = combination

    @property
    def name(self):
        return self.__name

    @property
    def rating(self):
        return self.__rating

    def __str__(self):
        return f'{self.name}: {self.combination}'

    def __eq__(self, other):
        return self.combination[-1].score == other.combination[-1].score

    def __gt__(self, other):
        return self.combination[-1].score > other.combination[-1].score


class Kicker:
    __name = 'Kicker'
    __rating = 1

    def __init__(self, combination: Card):
        self.combination: Card = combination

    @property
    def name(self):
        return self.__name

    @property
    def rating(self):
        return self.__rating

    def __str__(self):
        return f'{self.name}: {self.combination}'

    def __eq__(self, other):
        return self.combination.score == other.combination.score

    def __gt__(self, other):
        return self.combination.score > other.combination.score
