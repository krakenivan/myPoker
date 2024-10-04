from .player import Player


class Betting:
    def __init__(self, game, blind: int | float):
        self.game = game  # запущенная игра
        self.bet: float = blind  # Бет: минимальная ставка поле флопа
        self.big_blind: float = blind  # величина большого блайнда
        self.small_blind: float = blind/2  # величина малого блайнда
        self.bet_call: float = self.big_blind  # размер ставки колл
        self.bet_min_raise: float = self.bet_call * 2  # размер минимального рейза
        self.is_raise = False  # индикатор рейза
        self.is_allin = False  # индикатор ол-ина
        self.min_allin = self.big_blind  # минимальный ол-ин
        self.max_allin = 0  # максимальный ол-ин
        self.word_allin = ['all-in', 'allin', 'all', 'ол-ин', 'олин', 'на все', 'все']  # слова для ставки ол-ин
        self.word_check = ['check', 'chek', 'chec', 'чек', 'чэк']  # слова для ставки чек
        self.word_bet = ['bet', 'beet', 'бет', 'бэт', 'ставка', 'bid']  # слова для ставки бет
        self.word_rais = ["рейз", "райз", "повышаю", "повышение", 'raise', 'raising', 'promotion', 'rase',
                          'reraise',
                          'rerase',
                          'рирейз', 'ререйз', 'рирайз', 'рерайз', 'rais', 'reis']  # слова для ставки рейз
        self.word_call = ["кол", "колл", "кал", "калл", "поддерживаю", 'call', 'cal', 'kal', 'kall',
                          'col', 'coll', 'kol', 'koll', 'support']  # слова для ставки колл
        self.word_fold = ["фолд", "пас", "пасс", "сброс", "сбрасываю", 'fold', 'fould', 'pas', 'pass',
                          'reset']  # слова для сброса
        self.world_preflop = self.word_rais + self.word_call + self.word_fold + self.word_allin
        # возможные ответы для ставки на префлопе
        self.all_word = (self.word_check + self.word_bet + self.word_rais + self.word_call + self.word_fold +
                         self.word_allin)  # все возможные ставки
        self.count_bet = 0  # счетчик ставок
        self.count_fold = 0  # счетчик фолда
        self.count_allin = 0  # счетчик ол-инов
        self.count_check = 0  # счетчик чеков
        self.count_call = 0  # счетчик колов
        self.count_raise = 0  # счетчик рейзов
        self.count_over_all_in = 0
        self.all_counter = 0  # общий вспомогательный счетчик
        self.is_bet_postflop = False  # был ли бэт
        self.side_bank = 0  # побочный банк для ол-инов
        self.allin_in_bank = False  # флаг зачисления ол-инов в банк
        self.save_max_allin = 0  # сохранение максимального ол-ина
        self.another_bank_all_in = 0  # побочный банк вне ол-ина
        self.is_trans_bank = False  # флаг зачисления ставок в банк
        self.over_allin_bank = 0

    def bet_blind(self):
        """Выставление блайндов"""
        for player in self.game.players_in_game:
            if player:
                if player.sb:
                    if player.stack < self.small_blind:  # если в стеке не хватает фишек идет ол-ин
                        print('Недостаточно фишек для ставки')
                        self.all_in(player)
                    else:
                        self.game._bank += player.bet(self.small_blind)
                        self.another_bank_all_in += self.small_blind
                if player.bb:
                    if player.stack < self.big_blind:  # если в стеке не хватает фишек идет ол-ин
                        print('Недостаточно фишек для ставки')
                        self.all_in(player)
                    else:
                        self.game._bank += player.bet(self.big_blind)
                        self.another_bank_all_in += self.big_blind

    def bet_preflop(self, player: Player):
        """Запрос ставок на префлопе
        :param player: ставящий игрок
        """
        while True:  # цикл запроса ставки
            bet = input(f"Игрок {player}, ваша ставка: \n").lower().strip().split()  # запрос ставки
            if len(bet) > 2 or bet[0].isdigit() or bet[0] not in self.all_word:
                print("Введите пожалуйста корректную ставку\n")
                continue

            elif (player.bb and (not self.is_raise and not self.is_allin) and
                  (bet[0] in self.word_check or bet[0] in self.word_call)):
                # если игрок на позиции большого блайнда, рейза не было и ставка == чек или кол
                if bet[0] in self.word_check:  # если чек
                    player.bb = False  # убираем метку ББ
                    self.count_bet += 1
                    # увеличиваем счетчик ставок
                    if self.is_allin:
                        self.count_bet += self.count_allin
                    # print('В банке', self.game._bank)
                    return
                elif bet[0] in self.word_call:  # если кол
                    print(f'Ваш {bet[0]} равен чеку. Ставка чек принята')
                    player.bb = False  # убираем метку ББ
                    self.count_bet += 1  # увеличиваем счетчик ставок
                    # print('В банке', self.game._bank)
                    return

            elif bet[0] in self.world_preflop:  # если ставка из списка ставок
                self.bet_calculation(bet, player)  # расчет ставик
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
                self.count_check += 1
                self.count_bet = self.count_allin + self.count_check + self.count_fold
                return
            elif player.last_bet_amount == 0 and (bet[0] in self.word_bet) and (not self.is_bet_postflop):
                # если ставка бет, возможна при отсутствии бета
                self.bet_calculation(bet, player)  # расчет ставки
                return
            elif (bet[0] in self.word_fold) or (bet[0] in self.word_rais) or (bet[0] in self.word_allin):
                # если на постфлопе ставка рейз или фолд
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
        Расчет ставок
        :param bet: название ставки
        :param player: ставящий игрок
        :return: None
        """
        if (((not self.game.is_table_flop) and (bet[0] in self.word_rais)) or
                (self.game.is_table_flop and self.is_bet_postflop and (bet[0] in self.word_rais))):
            # если ставка рейз и флопа не было или если ставка рейз после флопа при наличие бета
            if self.is_allin and player.copy_stack < self.max_allin:
                print('Недостаточно фишек для ставки')
                self.another_bank_all_in -= player.last_bet_amount
                self.all_in(player)
                return
            if player.copy_stack < self.bet_min_raise:
                print('Недостаточно фишек для ставки')
                self.another_bank_all_in -= player.last_bet_amount
                self.all_in(player)
                return
            bet_raise = self.bet_raise(bet)  # вызов функции рейза и сохранить в переменную сумму ставки
            self.bet_call = bet_raise  # колл теперь равен рейзу
            self.bet_min_raise = bet_raise * 2  # установка минимального рейза
            if bet_raise > self.min_allin:
                player.another_bank_over_all_in += bet_raise - self.min_allin
                bet_raise -= player.another_bank_over_all_in
                self.min_allin += player.another_bank_over_all_in
                self.count_over_all_in = 1
                self.is_trans_bank = True
            # if self.is_allin:
            #     if bet_raise > self.min_allin:
            #         player.another_bank_over_all_in += bet_raise - self.min_allin
            #         bet_raise -= self.min_allin
            # self.another_bank_all_in += bet_raise - player.last_bet_amount
            if player.last_bet_amount != 0:  # если ставка у игрока уже была
                self.game._bank -= player.last_bet_amount
                self.another_bank_all_in -= player.last_bet_amount
                player.bet_increase(bet_raise)  # повышение
                self.game._bank += bet_raise  # добавление в банк
            else:
                self.game._bank += player.bet(bet_raise)  # иначе ставка
            # if not self.is_allin:
            # self.another_bank_all_in += bet_raise - player.last_bet_amount

            # self.bet_call = bet_raise  # колл теперь равен рейзу
            # self.bet_min_raise = bet_raise * 2  # установка минимального рейза
            self.is_raise = True  # метка рейза
            self.count_bet = 1 + self.count_fold + self.count_allin   # счетчик ставок = 1 + количество сбросов
            self.count_raise += 1

            self.remove_bet_check_and_bet(self.game.players_in_game)  # удаляем чек и бэт из списка
            return

        elif bet[0] in self.word_call:  # если ставка колл
            if player.copy_stack <= self.min_allin:
                print('Недостаточно фишек для ставки')
                self.another_bank_all_in -= player.last_bet_amount
                self.all_in(player)
                return
            if len(bet) > 1:
                print('Кол в данный момент равен', self.bet_call)

            print(f'Ставка кол {self.bet_call} принята')
            if self.is_allin:
                self.another_bank_all_in -= player.last_bet_amount
                if self.is_trans_bank:
                    player.another_bank_over_all_in = 0
                if self.is_raise:
                    self.another_bank_all_in += player.last_bet_amount
                    self.is_trans_bank = True
                    player.another_bank_over_all_in = 0
            # self.another_bank_all_in += self.bet_call - player.last_bet_amount

            if player.last_bet_amount != 0:  # если ставка у игрока уже была
                self.another_bank_all_in -= player.last_bet_amount
                self.game._bank -= player.last_bet_amount
                player.bet_increase(self.bet_call)
                self.another_bank_all_in += player.last_bet_amount
                self.game._bank += self.bet_call
            else:
                player.bet(self.bet_call)
                self.another_bank_all_in += player.last_bet_amount

                self.game._bank += self.bet_call
            if self.bet_call == self.min_allin:
                self.count_over_all_in += 1

            self.count_bet += 1  # счетчик ставок увеличить на 1
            self.count_call += 1
            return

        elif bet[0] in self.word_allin:
            self.another_bank_all_in -= player.last_bet_amount
            # если ставка ол-ин
            self.all_in(player)
            return

        elif bet[0] in self.word_bet or ((bet[0] in self.word_rais) and not self.is_bet_postflop and not self.is_allin):
            # если ставка бет (не работает на префлопе) или если ставка рейз при отсутствии бета
            if bet[0] in self.word_rais:  # если рейз
                print(f'Ваш {bet[0]} приравнивается к бэту. Минимальная сумма бэта {self.big_blind}')
            bet_bet = self.bet_bet(bet)  # вызов функции бета и сохранить в переменную сумму ставки
            if bet_bet > player.copy_stack:
                print('Недостаточно фишек для ставки')
                self.all_in(player)
                return
            player.bet(bet_bet)
            self.another_bank_all_in += bet_bet
            self.game._bank += bet_bet  # прибавить бет в банк
            self.bet_call = bet_bet  # колл теперь равен бету
            self.bet_min_raise = bet_bet * 2  # минимальный рейз
            self.is_bet_postflop = True  # метка бета на постфлопе
            self.count_bet = 1 + self.count_allin + self.count_fold  # счетчик ставок = 1
            self.remove_bet_check_and_bet(self.game.players_in_game)  # удаляем чек и бэт из списка
            return

        elif bet[0] in self.word_fold:  # если ставка фолд выйти из функции
            player.bet_fold = True  # метка сброса на игрока
            player.drop()  # сброс карт
            self.count_bet += 1
            self.count_fold += 1
            if self.is_allin:
                self.another_bank_all_in += player.last_bet_amount
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

    def all_in(self, player):
        """Обработка ол-ина"""
        self.game._bank -= player.last_bet_amount
        bet_allin = player.bet_allin()

        if bet_allin > self.max_allin:
            self.max_allin = bet_allin
            self.save_max_allin = player.actual_allin
        # if self.is_allin:
        #     if self.min_allin > bet_allin:
        #         self.min_allin = bet_allin
        if not self.is_allin:
            self.is_allin = True
            self.min_allin = bet_allin

        if self.min_allin < bet_allin:
            self.min_allin = bet_allin

        if self.bet_call < self.max_allin:
            self.bet_call = self.max_allin  # колл теперь равен ол-ину
        self.bet_min_raise = self.bet_call * 2
        if self.game.is_table_flop:
            self.is_bet_postflop = True  # метка бета на постфлопе
        # if bet_allin < self.min_allin:
        #     self.count_allin += self.count_over_all_in
        self.count_bet = 1 + self.count_fold + self.count_allin  # счетчик ставок = 1 + количество сбросов
        self.count_allin += 1
        if bet_allin <= self.min_allin:
            self.count_bet += self.count_over_all_in
        self.remove_bet_check_and_bet(self.game.players_in_game)
        print('ОЛ-ИН', bet_allin)

    def bank_recalculation(self, players):
        """Перерасчет банка игроков в зависимости от ол-ина"""
        # new_bank = 0
        players_not_fold = [player for player in players if not player.bet_fold]
        # count_player_is_allin_outside_side_bank = len([pl for pl in players_not_fold if not pl.is_sum_all_in_bank])

        if self.is_trans_bank:
            for player in players_not_fold:
                player.stack -= player.another_bank_over_all_in
                if not player.is_allin:
                    player.last_bet_amount += player.another_bank_over_all_in
                self.game._bank += player.another_bank_over_all_in
                player.another_bank_over_all_in = 0
                if player.last_bet_amount > self.min_allin:
                    surplus = player.last_bet_amount - self.min_allin
                    player.stack += surplus  # возврат излишка в стек
                    self.another_bank_all_in -= surplus
                    player.last_bet_amount = self.min_allin  # перерасчет последней ставки
        if self.is_allin:
            new_bank = 0
            self.over_allin_bank += sum([player.last_bet_amount - self.max_allin
                                         for player in players_not_fold if not player.is_allin])
            self.game._bank -= self.over_allin_bank

            if not self.allin_in_bank:
                allin_player = [player for player in players_not_fold if player.is_allin and not player.is_sum_all_in_bank]
                # список игроков с ол_ином
                # count_all_in = len(allin_player)  # количество игроков с ол-ином
                list_sum_allin = list(set(pl_alin.sum_allin for pl_alin in allin_player if not pl_alin.is_sum_all_in_bank))
                sort_sum_allin = sorted(list_sum_allin)
                # список уникальных сум ставок
                if len(list_sum_allin) > 1:
                    sum_allin = sort_sum_allin[-2]  # берем предпоследнюю
                    if self.min_allin < self.max_allin:
                        self.max_allin = sum_allin  # ставим последнюю как максимальную
                    self.save_max_allin = self.max_allin
                    for player in allin_player:
                        if player.sum_allin > self.max_allin:  # если сумма олина у игрока больше максимального
                            player.stack += player.sum_allin - self.max_allin  # возврат излишка в стек
                            player.sum_allin = self.max_allin  # перерасчет суммы ол-ина
                            player.actual_allin = self.max_allin
                # else:
                #     sum_allin = sort_sum_allin[0]

                            # if count_all_in > 1:  # если ол-инов больше 1
                for pl in allin_player:
                    if not pl.is_sum_all_in_bank:
                        if pl.actual_allin == self.max_allin:
                        # pl.player_allin_bank += (pl.actual_allin * len(players_not_fold))
                            pl.player_allin_bank += sum([player.actual_allin for player in players])
                        else:
                            pl.player_allin_bank += (pl.actual_allin * len(players_not_fold))
                        # self.side_bank += sum_allin
                        # self.side_bank += sum_allin * count_player_is_allin_outside_side_bank

                        pl.player_another_bank_all_in += self.another_bank_all_in
                        if self.another_bank_all_in > pl.actual_allin:
                            pl.player_another_bank_all_in -= (self.another_bank_all_in - pl.actual_allin)
                        # self.side_bank += self.another_bank_all_in
                        # self.is_another_bank_in_side_bank = True
                        # добавляем их суммы в побочный банк
                        new_bank += pl.sum_allin
                        pl.is_sum_all_in_bank = True
                # self.side_bank += sum_allin * count_player_is_allin_outside_side_bank
                self.side_bank += sum([player.actual_allin for player in players])
                self.game._bank += new_bank  # кладем побочный банк в общий банк
                self.allin_in_bank = True

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

    def return_allin_to_stack(self, player):
        """Возвращает ставку последнего игрока в стек"""
        if player.is_allin:
            player.stack += player.actual_allin
            player.is_allin = False
        else:
            player.stack += player.last_bet_amount
            self.game._bank -= player.last_bet_amount

    def remove_bet_check_and_bet(self, players):
        for player in players:
            if player.stack < self.bet_min_raise and 'рейз' in player.list_bet:
                player.list_bet.remove('рейз')
            if "чек" in player.list_bet:
                player.list_bet.remove("чек")
            if "бэт" in player.list_bet:
                player.list_bet.remove("бэт")
            if "фолд" not in player.list_bet:
                player.list_bet.insert(0, "фолд")
            if "кол" not in player.list_bet:
                player.list_bet.insert(1, "кол")





