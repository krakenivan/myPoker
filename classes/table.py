from random import choice

from .player import Player
from .game import Game


class Table:
    table_id = 0

    def __init__(self, host: Player, blind: int = 10):
        Table.table_id += 1
        self.table_id = Table.table_id
        self.guests: list[Player] = []
        self.players: list[Player | None] = [host, *[None]*5]
        self.blind = blind
        self._game: Game | None = None
        self.set_dealer()

    def join(self, player: Player):
        self.guests.append(player)

    def kick(self, del_player: Player):
        for ind, player in enumerate(self.players):
            if isinstance(player, Player) and player.name == del_player.name:
                self.players[ind] = None
                break

    def drop_cards_quest(self):
        for quest in self.guests:
            quest.drop()

    def set_dealer(self):
        players = [player for player in self.players if player]
        choice(players).dealer = True

    def clearing_marks(self):
        for player in self.players:
            if player:
                player.sb = False
                player.bb = False

    def change_dealer(self):
        players = [player for player in self.players if player]
        for ind, player in enumerate(players):
            if player.dealer:
                player.dealer = False
                players[(ind + 1) % len(players)].dealer = True
                break




    # def set_blind(self):
    #     players = [player for player in self.players if player]
    #     for ind, player in enumerate(players):
    #         if player.dealer:
    #             players[(ind + 1) % len(players)].sb = True
    #             break

    def new_game(self):
        while self.guests and None in self.players:
            for ind, player in enumerate(self.players):
                if not player and self.guests:
                    self.players[ind] = self.guests.pop(0)
        # while self.guest and False in self.players:
        #     self.players.append(self.guest.pop(0))
        self.clearing_marks()
        self._game = Game(tuple(self.players), self.blind)
        self.drop_cards_quest()
        self._game.drop_cards()
        self._game.start()
        self.change_dealer()
        # a = self._game.check_winner()
        # self._game.show_players()
        # return a
