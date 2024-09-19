from random import choice

from .player import Player
from .game import Game


class Table:
    table_id = 0

    def __init__(self, host: Player, blind: int | float = 10):
        Table.table_id += 1
        self.table_id = Table.table_id
        self.guests: list[Player] = []
        self.players: list[Player | None] = [host, *[None]*5]
        self.blind: int | float = blind
        self._game: Game | None = None
        self.set_dealer()  # выставление метки дилера

    def join(self, player: Player):
        """Добавить игрока"""
        self.guests.append(player)

    def kick(self, del_player: Player):
        """Удалить игрока"""
        for ind, player in enumerate(self.players):
            if isinstance(player, Player) and player.name == del_player.name:
                self.players[ind] = None
                break

    def drop_cards_quest(self):
        """Сброс карт у гостей"""
        for quest in self.guests:
            quest.drop()

    def set_dealer(self):
        """Выставление метки дилера"""
        players = [player for player in self.players if player]
        choice(players).dealer = True

    def clearing_marks(self):
        """Очистка меток блайндов и фолда у игроков"""
        for player in self.players:
            if player:
                player.sb = False
                player.bb = False
                player.bet_fold = False

    def change_dealer(self):
        """Передвижение метки диллера"""
        players = [player for player in self.players if player]
        for ind, player in enumerate(players):
            if player.dealer:
                player.dealer = False
                players[(ind + 1) % len(players)].dealer = True
                break

    def crediting_winnings(self, winning_players):
        """Начисление выиграша"""
        quantity_winner = len(winning_players)
        for player in winning_players:
            player.stack += (self._game._bank/quantity_winner)

    def new_game(self):
        """Запуск игры"""
        while (len(self.players) + len(self.guests)) > 1:  # если игроков больше 1
            while self.guests and None in self.players:  # добавление гостей за стол
                for ind, player in enumerate(self.players):
                    if not player and self.guests:
                        self.players[ind] = self.guests.pop(0)
            # while self.guest and False in self.players:
            #     self.players.append(self.guest.pop(0))
            self.clearing_marks()
            self._game = Game(tuple(self.players), self.blind)
            self.drop_cards_quest()
            self._game.drop_cards()
            # self._game.show_players()
            # print()
            winner = self._game.start()
            self.crediting_winnings(winner)

            print('Победитель', len(winner), *winner)
            print()
            self.change_dealer()
