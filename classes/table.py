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
        self.ind_dealer: int = 0  # индекс дилера в списке игроков
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
        play_dealer = choice(players)
        play_dealer.dealer = True
        self.ind_dealer = self.players.index(play_dealer)

    def reset_marks(self):
        """Очистка меток  у игроков и гостей"""
        for player in self.players:
            if player:
                player.sb = False
                player.bb = False
                player.bet_fold = False
                player.is_allin = False
                player.make_copy_stack(player.stack)
                player.sum_allin = 0
                player.player_allin_bank = 0
                player.is_sum_all_in_bank = False
                player.last_bet_amount = 0
                player.list_bet = []
                player.actual_allin = 0
                player.another_bank_over_all_in = 0
                player.another_bank_over_all_in = 0
                player.player_another_bank_all_in = 0
        for quest in self.guests:
            quest.sb = False
            quest.bb = False
            quest.bet_fold = False
            quest.is_allin = False
            quest.make_copy_stack(quest.stack)
            quest.sum_allin = 0
            quest.player_allin_bank = 0
            quest.is_sum_all_in_bank = False
            quest.last_bet_amount = 0
            quest.list_bet = []
            quest.actual_allin = 0
            quest.another_bank_over_all_in = 0
            quest.another_bank_over_all_in = 0
            quest.player_another_bank_all_in = 0

    def del_player_not_stack(self):
        """Удаление игроков с нулевым стеком"""
        for ind, player in enumerate(self.players):
            if player and player.stack == 0:
                self.players[ind] = None
                self.guests.append(player)




    def change_dealer(self):
        """Передвижение метки диллера"""
        players = [player for player in self.players if player]
        for ind, player in enumerate(players):
            if player.dealer:
                player.dealer = False
                players[(ind + 1) % len(players)].dealer = True
                break
        else:
            while True:
                self.ind_dealer = (self.ind_dealer + 1) % len(players)
                if self.players[self.ind_dealer]:
                    players[self.ind_dealer].dealer = True
                    break



    def crediting_winnings(self, winning_players):
        """Начисление выиграша"""
        if any([player.is_allin for player in winning_players]):  # если в победителях есть игроки ол_ин
            if len(winning_players) == 1:
                for player in winning_players:  # обходим список победителей
                    print("Игрок олин", player.player_allin_bank)
                    # if self._game.not_allin_player:  # если есть игроки без ол ина
                    player.stack += player.player_allin_bank + player.player_another_bank_all_in
                    # добавляем в стек победителю только потенциальный выиграш
                    self._game._bank -= player.player_allin_bank + player.player_another_bank_all_in
                    # и вычитаем его из банка
                    # else:  # если игроков без ол ина нет
                    #     player.stack += self._game._bank  # забираем в стек весь банк
                    #     self._game._bank = 0  # обнуляем банк

                    print("Остаток банка", self._game._bank)
                if self._game._bank:  # если в банке есть остаток
                    player_win_not_allin = max(self._game.not_allin_player)
                    # выявляем игрока без ол_ина с самой сильной комбинацией
                    player_win_not_allin.stack += self._game._bank  # отдаем ему остаток в банке
                    # quantity_winner_not_allin = len(self._game.not_allin_player)
                    # for player in player_win_not_allin:
                    #     player.stack += (self._game._bank / quantity_winner_not_allin)
                # if hasattr(self._game, 'another_bank'):
                #     player_win_not_allin = max(self._game.not_allin_player)
                #     player_win_not_allin.stack += player_win_not_allin
            else:
                another_bank_winer = sum((pl.player_another_bank_all_in for pl in winning_players))
                sorted_win_player = sorted([pl for pl in winning_players], key=lambda x: x.player_another_bank_all_in)
                while another_bank_winer != 0:
                    for player in sorted_win_player:
                        player.stack += (player.player_allin_bank + player.player_another_bank_all_in
                                         / len(winning_players))
                        self._game._bank -= (player.player_allin_bank + player.player_another_bank_all_in
                                             / len(winning_players))
                        another_bank_winer -= player.player_another_bank_all_in / len(winning_players)
                    min_another_bank = min([pl.player_another_bank_all_in for pl in winning_players])
                    for player in sorted_win_player:
                        if player.player_another_bank_all_in == min_another_bank:
                            sorted_win_player.remove(player)
                if self._game._bank:  # если в банке есть остаток
                    player_win_not_allin = max(self._game.not_allin_player)
                    # выявляем игрока без ол_ина с самой сильной комбинацией
                    player_win_not_allin.stack += self._game._bank

        else:  # если игроков с ол_ином нет в победителях
            quantity_winner = len(winning_players)  # количество победителей
            for player in winning_players:  # делим банк на всех победителей
                player.stack += (self._game._bank/quantity_winner)

    def new_game(self):
        """Запуск игры"""
        # while (len(self.players) + len(self.guests)) > 1:  # если игроков больше 1
        #     while self.guests and None in self.players:  # добавление гостей за стол
        #         for ind, player in enumerate(self.players):
        #             while any((not bool(i) for i in self.players)) or any((bool(i.stack) for i in self.guests)):
        #                 if not player and self.guests:
        #                     added_player = self.guests.pop(0)
        #                     if added_player.stack > 0:
        #                         self.players[ind] = added_player
        while (len(self.players) + len(self.guests)) > 1:
            ind = 0
            while any((not bool(i) for i in self.players)) and any((bool(i.stack) for i in self.guests)):
                # если игроков больше 1
                if not self.players[ind] and self.guests:
                    added_player = self.guests.pop(0)
                    if added_player.stack > 0:
                        self.players[ind] = added_player
                    else:
                        continue
                ind += 1
            # while self.guest and False in self.players:
            #     self.players.append(self.guest.pop(0))
            self.reset_marks()
            self._game = Game(tuple(self.players), self.blind)
            self.drop_cards_quest()
            self._game.drop_cards()
            # self._game.show_players()
            # print()
            winner = self._game.start()
            self.crediting_winnings(winner)
            print()
            print('Победитель', len(winner), *winner)
            print()
            self._game.show_players()
            print()
            self.del_player_not_stack()
            self.change_dealer()
