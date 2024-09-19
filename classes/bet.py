from .player import Player

# TODO проработать ставку ол-ин
class Betting:
    def __init__(self, game, blind: int | float):
        self.game = game  # запущенная игра
        self.bet: float = blind  # Бет: минимальная ставка поле флопа
        self.big_blind: float = blind  # величина большого блайнда
        self.small_blind: float = blind/2  # величина малого блайнда
        self.bet_call: float = self.big_blind  # размер ставки колл
        self.bet_min_raise: float = self.bet_call * 2  # размер минимального рейза
        self.is_raise = False  # индикатор рейза
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
        self.all_word = self.word_check + self.word_bet + self.word_rais + self.word_call + self.word_fold
        self.count_bet = 0  # счетчик ставок
        self.count_fold = 0  # счетчик фолда
        self.is_bet_postflop = False  # был ли бэт
        # self.last_bid_amount = 0  # сумма последней ставки

    def bet_blind(self):
        """Выставление блайндов"""
        for player in self.game.players_in_game:
            if player:
                if player.sb:
                    self.game._bank += player.bet(self.small_blind)
                if player.bb:
                    self.game._bank += player.bet(self.big_blind)

    def bet_preflop(self, player: Player):
        """Запрос ставок на префлопе
        :param player: ставящий игрок
        """
        while True:  # цикл запроса ставки
            bet = input(f"Игрок {player}, ваша ставка: \n").lower().strip().split()  # запрос ставки
            if len(bet) > 2 or bet[0].isdigit() or bet[0] not in self.all_word:
                print("Введите пожалуйста корректную ставку\n")
                continue

            elif player.bb and (not self.is_raise) and (bet[0] in self.word_check or bet[0] in self.word_call):
                # если игрок на позиции большого блайнда, рейза не было и ставка == чек или кол
                if bet[0] in self.word_check:  # если чек
                    player.bb = False  # убираем метку ББ
                    self.count_bet += 1  # увеличиваем счетчик ставок
                    print('В банке', self.game._bank)
                    return
                elif bet[0] in self.word_call:  # если кол
                    print(f'Ваш {bet[0]} равен чеку. Ставка чек принята')
                    player.bb = False  # убираем метку ББ
                    self.count_bet += 1  # увеличиваем счетчик ставок
                    print('В банке', self.game._bank)
                    return

            elif bet[0] in self.world_preflop:  # если ставка из списка ставок
                self.bet_calculation(bet, player)  # расчет ставик

                # if not player.bb and not player.sb:  # если игрок не на позиции блайндов
                #     # counts_the_bet(bid, player)
                #     return
                # elif player.bb and not player.sb:  # если игрок на позиции большого блайнда
                #     # counts_the_bet(bid, player, BB=True)
                #     return
                # elif not player.bb and player.sb:  # если игрок на позиции малого блайнда
                #     # counts_the_bet(bid, player, SB=True)
                print('В банке', self.game._bank)
                return

            else:  # если ставка не чек и не из списка ставок перезапуск цикла
                print("Ставка не верна Вы не можете сделать", bet[0])
                continue

    def bet_postflop(self, player: Player):
        """Запрос ставок на постфлопе
        :param player: ставящий игрок
        """
        while True:  # цикл запроса ставки
            bet = input(f"Игрок {player}, ваша ставка: \n").lower().strip().split()  # запрос ставки

            if len(bet) > 2 or bet[0].isdigit() or bet[0] not in self.all_word:
                print("Введите пожалуйста корректную ставку\n")
                continue

            elif player.last_bet_amount == 0 and (bet[0] in self.word_check) and (not self.is_bet_postflop):
                # если ставка чек выход из функции, возможна при отсутствии бета
                self.count_bet += 1
                return
            elif player.last_bet_amount == 0 and (bet[0] in self.word_bet) and (not self.is_bet_postflop):
                # если ставка бет, возможна при отсутствии бета
                self.bet_calculation(bet, player)  # расчет ставки
                return
            elif (bet[0] in self.word_fold) or (bet[0] in self.word_rais):  # если на постфлопе ставка рейз или фолд
                self.bet_calculation(bet, player)  # расчет ставки
                return
            elif (bet[0] in self.word_call) and self.is_bet_postflop:
                # если на постфлопе ставка колл, возможна только при наличии ставки бет
                self.bet_calculation(bet, player)  # расчет ставки
                return
            else:  # если ставка не чек и не из списка ставок перезапуск цикла
                print("Ставка не верна. Вы не можете сделать", bet[0])
                continue

    def bet_calculation(self, bet: list, player: Player):
        """
        Расчет ставоки
        :param bet: название ставки
        :param player: ставящий игрок
        :return: None
        """
        if (((not self.game.is_table_flop) and (bet[0] in self.word_rais)) or
                ((self.game.is_table_flop) and self.is_bet_postflop and (bet[0] in self.word_rais))):
            # если ставка рейз и флопа не было или если ставка рейз после флопа при наличие бета

            bet_raise = self.bet_raise(bet)  # вызов функции рейза и сохранить в переменную сумму ставки

            if player.last_bet_amount != 0:  # если ставка у игрока уже была
                self.game._bank -= player.last_bet_amount
                player.bet_increase(bet_raise)  # повышение
                self.game._bank += bet_raise  # добавление в банк
            else:
                # player.bid(bid_raise)
                self.game._bank += player.bet(bet_raise) # иначе ставка

            self.bet_call = bet_raise  # колл теперь равен рейзу
            self.bet_min_raise = bet_raise * 2  # установка минимального рейза
            self.is_raise = True  # метка рейза
            self.count_bet = 1 + self.count_fold  # счетчик ставок = 1 + количество сбросов
            self.remove_bet_check_and_bet(self.game.players_in_game)  # удаляем чек и бэт из списка
            return

        elif bet[0] in self.word_call:  # если ставка колл
            if len(bet) > 1:
                print('Кол в данный момент равен', self.bet_call)

            print(f'Ставка кол {self.bet_call} принята')

            if player.last_bet_amount != 0:  # если ставка у игрока уже была
                self.game._bank -= player.last_bet_amount
                player.bet_increase(self.bet_call)
                self.game._bank += self.bet_call
            else:
                player.bet(self.bet_call)
                self.game._bank += self.bet_call

            self.count_bet += 1  # счетчик ставок увеличить на 1
            return

        elif bet[0] in self.word_bet or ((bet[0] in self.word_rais) and not self.is_bet_postflop):
            # если ставка бет (не работает на префлопе) или если ставка рейз при отсутствии бета
            if bet[0] in self.word_rais:  # если рейз
                print(f'Ваш {bet[0]} приравнивается к бэту. Минимальная сумма бэта {self.big_blind}')
            bet_bet = self.bet_bet(bet)  # вызов функции бета и сохранить в переменную сумму ставки
            player.bet(bet_bet)
            self.game._bank += bet_bet  # прибавить бет в банк
            self.bet_call = bet_bet  # колл теперь равен бету
            self.bet_min_raise = bet_bet * 2  # минимальный рейз
            self.is_bet_postflop = True  # метка бета на постфлопе
            self.count_bet = 1  # счетчик ставок = 1
            self.remove_bet_check_and_bet(self.game.players_in_game)  # удаляем чек и бэт из списка

            return

        elif bet[0] in self.word_fold:  # если ставка фолд выйти из функции
            player.bet_fold = True  # метка сброса на игрока
            player.drop()  # сброс карт
            self.count_bet += 1
            self.count_fold += 1
            # self.remove_bet_check_and_bet(self.game.players_in_game)
            print("Вы скинули карты")
            return


    def bet_raise(self, bet) -> float:
        """Обработка рейза"""
        while True:

            try:
                if len(bet) > 1:
                    bet_raise = float(bet[1])
                else:
                    bet_raise = float(input(f"Введите сумму рейза. Минимум {self.bet_min_raise}\n"))
            except ValueError:
                print("Введена неверная сумма. Пожалуйста, введите сумму в виде числа.")
                bet = []
                continue

            if ((not self.game.is_table_flop and (bet_raise < self.bet_min_raise)) or
                    (self.game.is_table_flop and self.is_bet_postflop and (bet_raise < self.bet_min_raise))):
                print(f"Минимальная сумма рейза {self.bet_min_raise}")
                bet = []
                continue
            else:
                print(f"Ставка рейз {bet_raise} принята")
                return bet_raise



    def bet_bet(self, bet) -> float:
        """
        Функция для ставки бет (не работает на префлопе)
        :return:
        """
        while True:
            try:
                if len(bet) > 1:
                    bet_bet = float(bet[1])
                else:
                    bet_bet = float(input(f"Введите сумму бэта. Минимум {self.bet_blind}\n"))
            except ValueError:
                print("Введено неверное значение. Пожалуйста, введите сумму в виде числа.")
                bet = []
                continue

            if bet_bet < self.big_blind:
                print(f"Минимальная сумма бэта {self.bet_blind}")
                bet = []
                continue
            else:
                print(f"Ставка {bet_bet} принята")
                return bet_bet

    def remove_bet_check_and_bet(self, players):
        for player in players:
            if "чек" in player.list_bet:
                player.list_bet.remove("чек")
            if "бэт" in player.list_bet:
                player.list_bet.remove("бэт")
            if "фолд" not in player.list_bet:
                player.list_bet.insert(0, "фолд")
            if "кол" not in player.list_bet:
                player.list_bet.insert(1, "кол")





