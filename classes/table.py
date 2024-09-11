from .player import Player
from .game import Game
class Table:
    table_id = 0
    def __init__(self, host: Player, blind: int = 10):
        Table.table_id += 1
        self.table_id = Table.table_id
        self.guest: list[Player] = []
        self.players: list[Player] = [host]
        self.blind = blind
        self._game = None


    def join(self, player: Player):
        self.guest.append(player)

    def kick(self, player: Player):
        if player in self.players:
            self.players.remove(player)
        if player in self.guest:
            self.guest.remove(player)


    def new_game(self):
        while self.guest and len(self.players) < 6:
            self.players.append(self.guest.pop(0))
        self._game = Game(tuple(self.players), self.blind)
        self._game.start()
