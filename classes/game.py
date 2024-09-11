from .player import Player
from .deck import Deck
from .hand import Hand
from.card import Card

class Game:
    def __init__(self, players: tuple[Player, ...], blind: int):
        self._bank = 0
        # self.table: Hand = Hand()
        self.board: list[Card] = []
        self.blind = blind
        self._players: tuple[Player, ...] = players
        self._deck = Deck()


    def start(self):
        self._deck.shuffle()
        for _ in range(2):
            for player in self._players:
                player.hand += self._deck.deal_card()
        self._deck.deal_card()
        for _ in range(3):
            self.board.append(self._deck.deal_card())

        print(f'Флоп:', *self.board)
        for player in self._players:
            print(player)

        for player in self._players:
            player.drop()
