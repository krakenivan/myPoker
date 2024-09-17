from .player import Player
# from .game import Game


class Bet:
    def __init__(self, game, blind: int | float):
        self.game = game
        self.bet: float = blind  # Бет: минимальная ставка
        self.big_blind: float = blind  # величина большого блайнда
        self.small_blind: float = blind/2  # величина малого блайнда
        self.bet_call: float = self.big_blind  # ставка колла
        self.bet_min_raise: float = self.bet_call * 2  # ставка минимального рейза
        self.is_raise = False
        self.word_check = ['check', 'chek', 'chec', 'чек', 'чэк']  # слова для ставки чек чека
        self.word_bet = ['bet', 'beet', 'бет', 'бэт', 'ставка', 'bid']  # слова для ставки бет
        self.word_rais = ["рейз", "райз", "повышаю", "повышение", 'raise', 'raising', 'promotion', 'rase',
                          'reraise',
                          'rerase',
                          'рирейз', 'ререйз', 'рирайз', 'рерайз', 'rais', 'reis']  # слова для ставки рейз
        self.word_call = ["кол", "колл", "кал", "калл", "поддерживаю", 'call', 'cal', 'kal', 'kall',
                          'col', 'coll', 'kol', 'koll', 'support']  # слова для ставки колл
        self.word_fold = ["фолд", "пас", "пасс", "сброс", "сбрасываю", 'fold', 'fould', 'pas', 'pass',
                          'reset']  # слова для сброса
        self.world_preflop = self.word_rais + self.word_call + self.word_fold  # возможные ответы для ставки на префлопе
        self.count_bet = 0
        self.is_bet_postflop = False  # был ли бэт
        # self.last_bid_amount = 0  # сумма последней ставки

    def bet_blind(self):
        for player in self.game.players_in_game:
            if player:
                if player.sb:
                    self.game._bank += player.bet(self.small_blind)
                if player.bb:
                    self.game._bank += player.bet(self.big_blind)

    def bet_preflop(self, player: Player):
        # self.count_bid = 0
        while True:  # цикл запроса ставки
            bet = input(f"Игрок {player}, ваша ставка: \n").lower()  # запрос ставки

            if player.bb and (not self.is_raise) and (bet in self.word_check or bet in self.word_call):  # если игрок на позиции большого блайнда,
                # рейза не было и ставка == чек выход из функции
                if bet in self.word_check:
                    player.bb = False  # убираем метку ББ
                    self.count_bet += 1  # увеличиваем счетчик ставок
                    print(self.game._bank)
                    return
                elif bet in self.word_call:
                    print(f'Ваш {bet} равен чеку. Ставка принята')
                    player.bb = False  # убираем метку ББ
                    self.count_bet += 1  # увеличиваем счетчик ставок
                    print(self.game._bank)
                    return

            elif bet in self.world_preflop:  # если ставка из списка ставок
                self.bet_calculation(bet, player)

                # if not player.bb and not player.sb:  # если игрок не на позиции блайндов
                #     # counts_the_bet(bid, player)
                #     return
                # elif player.bb and not player.sb:  # если игрок на позиции большого блайнда
                #     # counts_the_bet(bid, player, BB=True)
                #     return
                # elif not player.bb and player.sb:  # если игрок на позиции малого блайнда
                #     # counts_the_bet(bid, player, SB=True)
                print(self.game._bank)
                return

            else:  # если ставка не чек и не из списка ставок перезапуск цикла
                print("Ставка не верна")
                continue

    def bet_postflop(self, player):
        while True:  # цикл запроса ставки
            bet = input(f"Игрок {player}, ваша ставка: \n").lower()  # запрос ставки

            if player.last_bet_amount == 0 and (bet in self.word_check) and (not self.is_bet_postflop):  # если ставка чек выход из функции,
                # возможна при отсутствии бета
                self.count_bet += 1
                return
            elif player.last_bet_amount == 0 and (bet in self.word_bet) and (not self.is_bet_postflop):  # если ставка бет,
                # возможна при отсутствии бета
                self.bet_calculation(bet, player)
                return
            elif (bet in self.word_fold) or (bet in self.word_rais):  # если на постфлопе ставка рейз или фолд
                self.bet_calculation(bet, player)
                return
            elif (bet in self.word_call) and self.is_bet_postflop:  # если на постфлопе ставка колл,
                # возможна только при наличии ставки бет
                self.bet_calculation(bet, player)
                return
            else:  # если ставка не чек и не из списка ставок перезапуск цикла
                print("Ставка не верна")
                continue

    def bet_calculation(self, bet, player):
        if (((not self.game.is_table_flop) and (bet in self.word_rais)) or
                ((self.game.is_table_flop) and self.is_bet_postflop and (bet in self.word_rais))):
            # если ставка рейз и флопа не было или если ставка рейз после флопа при наличие бета

            # if player.sb or player.bb:  # если позиция на блайнде
            #     self.processing_bid_blind_positions(player)  # функция обработки ставок блайндов

            bet_raise = self.bet_raise()  # вызов функции рейза и сохранить в переменную сумму ставки

            if player.last_bet_amount != 0:  # если ставка уже была
                self.game._bank -= player.last_bet_amount
                player.bet_increase(bet_raise)
                self.game._bank += bet_raise
            else:
                # player.bid(bid_raise)
                self.game._bank += player.bet(bet_raise)
            # self.game._bank -= player.last_bid_amount  # вычесть ставку из банка
            # player['stack'] += player['sum_bid']  # добавить ставку к стеку
            # self.game.bank += bid_raise
            # player['stack'] -= bid_raise  # вычисть сумму рейза из стэка игрока
            # player['sum_bid'] = bid_raise  # устанавливаем сумму последней ставки
            # bank += bid_raise  # прибавить рейз в банк
            # bank = round(bank, 2)

            # if player not in gammer:  # если игроку отсутствует в списке играющих
            #     gammer.append(player)  # добавить игрока в список играющих

            self.bet_call = bet_raise  # колл теперь равен рейзу
            self.bet_min_raise = bet_raise * 2
            self.is_raise = True
            self.count_bet = 1  # счетчик ставок = 1
            return

        elif bet in self.word_call:  # если ставка колл

            # if player.sb or player.bb:  # если позиция на блайнде
            #     self.processing_bid_blind_positions(player)  # функция обработки ставок блайндов

            print(f'Ставка {self.bet_call} принята')

            if player.last_bet_amount != 0:  # если ставка уже была
                self.game._bank -= player.last_bet_amount
                player.bet_increase(self.bet_call)
                self.game._bank += self.bet_call
            else:
                player.bet(self.bet_call)
                self.game._bank += self.bet_call

            # self.game._bank -= player.last_bid_amount  # вычесть ставку из банка
            # player['stack'] += player['sum_bid']  # добавить ставку к стеку
            # self.game._bank += self.bid_call

            # if player not in gammer:
            #     gammer.append(player)  # добавить игрока в список играющих

            self.count_bet += 1  # счетчик ставок увеличить на 1
            return

        elif bet in self.word_bet or ((bet in self.word_rais) and not self.is_bet_postflop):
            # если ставка бет (не работает на префлопе)
            # или если ставка рейз при отсутствии бета
            if bet in self.word_rais:
                print(f'Ваш {bet} приравнивается к бэту. Минимальная сумма {self.bet_blind}')
            bet_bet = self.bet_bet()  # вызов функции бета и сохранить в переменную сумму ставки
            player.bet(bet_bet)
            # player['stack'] -= bid_bet  # вычисть сумму бета из стэка игрока
            # player['sum_bid'] = bid_bet  # устанавливаем сумму последней ставки
            self.game._bank += bet_bet  # прибавить бет в банк
            # bank = round(bank, 2)
            self.bet_call = bet_bet  # колл теперь равен бету
            self.bet_min_raise = bet_bet * 2
            self.is_bet_postflop = True
            self.count_bet = 1  # счетчик ставок = 1
            return

        elif bet in self.word_fold:  # если ставка фолд выйти из функции
            # remove_player(player, players)
            player.bet_fold = True
            player.drop()
            self.count_bet += 1
            return


    def bet_raise(self) -> float:
        while True:
            # bet_raise = input("Введите сумму:\n")
            try:
                bet_raise = float(input("Введите сумму:\n"))
                if ((not self.game.is_table_flop and (bet_raise < self.bet_min_raise)) or
                        (self.game.is_table_flop and self.is_bet_postflop and (bet_raise < self.bet_min_raise))):
                    print(f"Минимальная сумма {self.bet_min_raise}")
                else:
                    print(f"Ставка {bet_raise} принята")
                    return bet_raise
            except ValueError:
                print("Введено неверное значение. Пожалуйста, введите сумму в виде числа.")
                continue



    def bet_bet(self) -> float:
        """
        Функция для ставки бет (не работает на префлопе)
        :return:
        """
        while True:
            # bet_bet = input("Введите сумму:\n")
            try:
                bet_bet = float(input("Введите сумму:\n"))
                if bet_bet < self.big_blind:
                    print(f"Минимальная сумма {self.bet_blind}")
                else:
                    print(f"Ставка {bet_bet} принята")
                    return bet_bet
            except ValueError:
                print("Введено неверное значение. Пожалуйста, введите сумму в виде числа.")
                continue






