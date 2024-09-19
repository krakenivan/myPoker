from .player import Player
from .deck import Deck
from .bet import Bet
from .combination import *
from .game_helper import *


class Game:
    def __init__(self, players: tuple[Player, ...], blind: int | float):
        self._bank: int | float = 0  # банк арздачи
        self.board: list[Card] = []  # открытые карты на столе (флоп, терн, ривер)
        self.blind: int | float = blind  # размер большого блайнда
        self._players: tuple[Player, ...] = players  # игроки за столом
        self.players_in_game: list[Player] = [player for player in self._players if player]  # игроки в игре
        self.list_players_preflop: list[Player] = []  # список игроков для ставок на префлопе
        self.list_players_postflop: list[Player] = []  # список игроков для ставок на постфлопе
        self.bet: Bet = Bet(self, blind)  # ставка
        self._deck: Deck = Deck()  # колода
        self.is_table_flop: bool = False  # индикатор флопа на столе

    def start(self) -> list[Player]:
        """
        метод запускает раздачу
        :return: победитель раздачи
        """
        # self._players[0].hand._hand = [Card('2', '♠'), Card('A', '♠')]
        # self._players[1].hand._hand = [Card('2', '♠'), Card('6', '♠')]
        self.set_blind()  # установка блайндов
        print()
        for round_bet in (self.preflop, self.flop, self.turn_or_river, self.turn_or_river, self.showdown):
            winner: list[Player] = round_bet()
            self.show_players()
            if winner:
                break
        self.is_table_flop = False
        return winner

    def preflop(self) -> list[Player] | None:
        """
        Запуск префлоп события
        :return: возможный победитель
        """
        self.bet.bet_blind()  # выставление блайндов
        self.add_bet()  # добавление возможных ставок
        self.dealing_cards()  # раздача карт игрокам
        self.show_table()  # показывает стол
        print()
        winner = self.accept_bet(self.list_players_preflop)  # принятие ставок
        self.update_list_player()  # обновление списков игроков
        self.resetting_blind_markers()  # сброс маркеров блайндов
        if winner:
            return winner

    def flop(self) -> list[Player] | None:
        """
        Запуск события флопа
        :return: возможный победитель
        """
        self._deck.deal_card()  # карта вне игры
        for _ in range(3):  # выставление флопа
            self.board.append(self._deck.deal_card())
        # self.board.append(Card('6', '♥'))
        # self.board.append(Card('7', '♥'))
        # self.board.append(Card('8', '♣'))
        self.is_table_flop = True  # добавление метки флопа

        self.add_bet()
        print()
        self.show_table()
        self.bet_reset(self.blind)  # сброс индикаторов ставки
        winner = self.accept_bet(self.list_players_postflop)
        self.update_list_player()
        self.resetting_blind_markers()
        if winner:
            return winner

    def turn_or_river(self) -> list[Player] | None:
        """
        Запуск события терна или ривера
        :return: возможный победитель
        """
        self._deck.deal_card()
        self.board.append(self._deck.deal_card())
        self.add_bet()
        print()
        self.show_table()
        self.bet_reset(self.blind)
        winner = self.accept_bet(self.list_players_postflop)
        self.update_list_player()
        self.resetting_blind_markers()
        if winner:
            return winner

    def show_table(self):
        """Показ стола"""
        street = 'Префлоп'
        match len(self.board):
            case 3:
                street = 'Флоп'
            case 4:
                street = 'Терн'
            case 5:
                street = 'Ривер'
        print(f'{street}:', *self.board, 'Банк=', self._bank)

    def show_players(self):
        """Показ игроков"""
        for player in self.players_in_game:
            print(player)

    def dealing_cards(self):
        """Раздача карт и формирование списков для ставок"""
        self._deck.shuffle()  # перемешивание колоды
        # print(self._deck)
        index_player: tuple = tuple(range(len(self.players_in_game)))  # вспомогательный кортеж с индексами игроков
        next_had: int = 0  # следующая рука
        count_had: int = 0  # счетчик количества розданных рук

        def dealing(pl: Player):
            """Выдача карт игрокам"""
            for _ in range(2):
                pl.hand += self._deck.deal_card()  # добавление карт в руку

        for ind, player in enumerate(self.players_in_game):
            if player.sb:  # выявление игрока на малом блайнде (для начала раздачи)
                next_had = ind  # переменная следующей руки для раздачи
                break
        while count_had != len(self.players_in_game):  # раздача карт, начинается с малого блайнда,
            # пока количество розданных рук не равно количеству игроков за столом
            dealing(self.players_in_game[next_had])  # выдача руки (начало с малого блайнда)
            self.list_players_preflop.insert(abs(count_had-2), self.players_in_game[next_had])
            # размещение в порядке начала ставок на префлопе (первый следующий после большого блайнда)
            self.list_players_postflop.insert(count_had, self.players_in_game[next_had])
            # размещение в порядке начала ставок на постфлопе (первый малый блайнд)
            next_had = index_player[(next_had + 1) % len(index_player)]  # переход к следующе руке
            count_had += 1  # увеличение счетчика
        print(self.list_players_preflop)
        print(self.list_players_postflop)

    def add_bet(self):
        """Добавление возможных ставок игрокам в зависимости от позиции и от наличия флопа на столе"""
        for player in self.players_in_game:
            player.list_bet.clear()
            player.list_bet.extend(["фолд", "чек",  "кол", "рейз", "ол-ин"])
            if not player.bb:
                player.list_bet.remove("чек")
            if player.bb:
                player.list_bet.remove("фолд")
                player.list_bet.remove("кол")

            if self.is_table_flop:
                player.list_bet.remove("кол")
                player.list_bet.remove("фолд")
                player.list_bet.insert(0, "чек")
                player.list_bet.insert(1, "бэт")

    def drop_cards(self):
        """Сброс карт игрокам"""
        for player in self._players:
            if player:
                player.drop()

    def set_blind(self):
        """Установка меток блайндов относительно дилера"""
        for ind, player in enumerate(self.players_in_game):
            if player.dealer:
                self.players_in_game[(ind + 1) % len(self.players_in_game)].sb = True
                self.players_in_game[(ind + 2) % len(self.players_in_game)].bb = True
                break

    def resetting_blind_markers(self):
        """Сброс меток блайндов"""
        for player in self._players:
            if player:
                player.sb = False
                player.bb = False

    def update_list_player(self):
        """Обновление списка игроков"""
        self.players_in_game = [player for player in self.players_in_game if not player.bet_fold]
        self.list_players_postflop = [player for player in self.list_players_postflop if not player.bet_fold]

    def accept_bet(self, players):
        """
        Принятие ставок игроками
        :param players:  список игроков в зависимости от наличия флопа
        :return: возможный победитель (если все скинули карты)
        """
        flag_bet = True  # Флаг ставок
        while flag_bet:  # Ставки пока флаг ставок True
            for player in players:  # прием ставок
                if not player.bet_fold:  # если игрок не скинул еще карты
                    if not self.is_table_flop:  # на префлопе первый ставит следующий после большого блайнда
                        self.bet.bet_preflop(player)  # запрос ставки
                    else:
                        self.bet.bet_postflop(player)  # на постфлопе первый малый блайнд
                if self.bet.count_bet == len(self.players_in_game):  # Если количество ставок равно количеству игроков
                    flag_bet = False  # флаг ставок False
                    break  # остановка цикла
                winner = [player for player in players if not player.bet_fold]  # проверка победителя
                if len(winner) == 1:  # Если есть один победитель
                    return winner

    def bet_reset(self, blind):
        """Сброс индикаторов для ставок"""
        for player in self._players:
            if player:
                player.last_bet_amount = 0  # обнуление максимальной ставки игрока
        # self.bet.bet = blind  # Бет: минимальная ставка
        # self.bet.bet_blind = blind  # величина большого блайнда
        # self.bet.small_blind = blind / 2  # величина малого блайнда
        self.bet.bet_call = blind  # ставка колла
        self.bet.bet_min_raise = self.bet.bet_call * 2  # ставка минимального рейза
        self.bet.is_raise = False  # индикатор рейза
        self.bet.count_bet = 0  # количества сделанных ставок
        self.bet.count_fold = 0  # количество сброшенных карт
        self.bet.is_bet_postflop = False  # индикатор постфлопа

    def showdown(self) -> list[Player]:
        """
        Вскрытие карт
        :return: Победители
        """
        rating_win_combination = 0  # переменная рейтинга комбинации для сравнения
        check_list = (self.check_royal_flush, self.check_straight_flush, self.check_four_of_kind, self.check_full_house,
                      self.check_flush, self.check_straight, self.check_set, self.check_two_pairs, self.check_pair,
                      self.check_kicker)  # список проверки комбинации

        for player in self.players_in_game:
            if player:
                hand_board: list[Card] = self.board + player.hand.show()
                # карты для проверки комбинации (рука + карты на столе
                for check in check_list:
                    combination: tuple[bool, ...] | None = check(hand_board)  # формирование сильнейшей комбинации
                    if combination:  # добавление сильнейшей комбинации игроку
                        setattr(player, 'combination', combination)
                        break
                if player.combination and player.show_rating_combination() > rating_win_combination:
                    rating_win_combination = player.show_rating_combination()
                    # установка рейтинга самой сильной обнаруженной комбинации

        list_winner = [player for player in self.players_in_game if player and
                       player.show_rating_combination() == rating_win_combination]
        # список лидеров по рейтингу комбинации
        if len(list_winner) > 1:  # если в списке больше одного игрока
            win_high_card = max([player.combination for player in list_winner])  # находим самую сильную комбинацию
            winner = [player for player in list_winner if not (player.combination < win_high_card)]
            #  формирование окончательного списка победителей
        else:
            winner = list_winner
        return winner

    @staticmethod
    def check_kicker(cards: list[Card]) -> Kicker:
        """
        Метод проверки старшей карты
        :param cards: список проверяемых карт
        :return: сформированная комбинация Kicker
        """
        list_card: list[Card] = sorted(cards, key=lambda x: x.score)  # сортировка карт
        no_comb: list[Card] = []  # список карт вне комбинации
        comb_cart = max(cards)  # комбинация
        list_card.remove(max(cards))  # удаление карты комбинации из списка карт
        for i in range(4):  # формирование списка карт вне комбинации
            card = list_card.pop()
            no_comb.append(card)
        return Kicker(comb_cart, no_comb)

    @staticmethod
    def check_pair(cards: list[Card]) -> Pair | None:
        """
        метод проверки пары
        :param cards: список проверяемых карт
        :return: сформированная комбинация Pair или None
        """
        comb_cart: list[Card] = []
        list_card: list[Card] = sorted(cards, key=lambda x: x.score)
        no_comb: list[Card] = []
        rank = find_ranks(get_rank_dict(cards), 'pair')  # определяем ранг в котором есть пара
        if rank:  # если такой ранг есть
            for card in cards:  # формируем комбинацию
                if card.rank == rank:
                    comb_cart.append(card)
                    list_card.remove(card)
            for i in range(3):  # формирование списка карт вне комбинации
                card = list_card.pop()
                no_comb.append(card)
            return Pair(comb_cart, no_comb)
        return None

    @staticmethod
    def check_two_pairs(cards: list[Card]) -> TwoPairs | None:
        """
        метод проверки двух пар
        :param cards: список проверяемых карт
        :return: сформированная комбинация TwoPairs или None
        """
        comb_cart: list[Card] = []
        list_card: list[Card] = sorted(cards, key=lambda x: x.score)
        rank = find_ranks(get_rank_dict(cards), 'two pairs')  # ранги с парами
        if rank:  # если ранг есть
            if len(rank) == 2:  # если ранга 2
                for card in cards:  # формируем комбинацию
                    if card.rank in rank:
                        comb_cart.append(card)
                        list_card.remove(card)
            elif len(rank) > 2:  # если рангов больше двух
                ind_min_rank = 12  # переменная минимального индекса для ранга
                for i in rank:  # устанавливаем минимальный ранга
                    if Card.ranks.index(i) < ind_min_rank:
                        ind_min_rank = Card.ranks.index(i)
                min_rank = Card.ranks[ind_min_rank]
                rank.remove(min_rank)  # удаляем минимальный ранг
                for card in cards:  # формируем комбинацию
                    if card.rank in rank:
                        comb_cart.append(card)
                        list_card.remove(card)
            else:  # если рангов меньше 2 значит комбинации ент
                return None
            no_comb: Card = list_card[-1]  # карта вне комбинации
            return TwoPairs(sorted(comb_cart, key=lambda x: x.score), no_comb)
        return None

    @staticmethod
    def check_set(cards: list[Card]) -> SetCard | None:
        """
        метод проверки сета
        :param cards: список проверяемых карт
        :return: сформированная комбинация SetCard или None
        """
        comb_cart: list[Card] = []
        list_card: list[Card] = sorted(cards, key=lambda x: x.score)
        no_comb: list[Card] = []
        rank = find_ranks(get_rank_dict(cards), 'set')  # находим ранг
        if rank: # сели ранг есть
            if len(rank) == 1:  # если ранг 1
                for card in cards:  # формируем комбинацию
                    if card.rank == rank[0]:
                        comb_cart.append(card)
                        list_card.remove(card)
            else:  # если рангов больше 1
                ind_max_rank = 0
                for i in rank:
                    if Card.ranks.index(i) > ind_max_rank:
                        ind_max_rank = Card.ranks.index(i)
                max_rank = Card.ranks[ind_max_rank]  # устанавливаем мксимальный ранг
                for card in cards:  # формируем комбинацию
                    if card.rank == max_rank:
                        comb_cart.append(card)
                        list_card.remove(card)
            for i in range(2):  # формируем список карт вне комбинации
                card = list_card.pop()
                no_comb.append(card)
            return SetCard(comb_cart, no_comb)
        return None

    @staticmethod
    def check_straight(cards: list[Card]) -> Straight | None:
        """
        метод проверки стрита
        :param cards: список проверяемых карт
        :return: сформированная комбинация Straight или None
        """
        list_card = sorted(cards, key=lambda x: x.score)
        list_cards_no_duplicate = remove_duplicate_cards(list_card.copy())  # удаляем дубликаты карт
        comb_cart = straight_check(list_cards_no_duplicate)  # формируем комбинацию
        if comb_cart:  # если комбинация сформирована
            return Straight(comb_cart)
        return None

    @staticmethod
    def check_flush(cards: list[Card]) -> Flush | None:
        """
        метод проверки флеша
        :param cards: список проверяемых карт
        :return: сформированная комбинация Flush или None
        """
        suit = find_suit(get_suit_dict(cards))  # находим масть
        if suit:  # если масть есть
            comb_cart: list[Card] = []
            for card in cards:  # формируем комбинацию
                if card.suit == suit:
                    comb_cart.append(card)
            return Flush(comb_cart)
        return None

    @staticmethod
    def check_full_house(cards: list[Card]) -> FullHouse | None:
        """
        метод проверки фул-хаоса
        :param cards: список проверяемых карт
        :return: сформированная комбинация FullHouse или None
        """
        ranks = get_rank_dict(cards)  # формируем словарь рангов
        if 3 in ranks.values() and 2 in ranks.values():  # если есть ранги с 3 и 2 карты
            comb_cart: list[Card] = []
            max_high_rank = 0  # максимальны й ранг
            max_low_rank = 0  # минимальный ранг
            for rank, count in ranks.items():  # устанвливаем максимальный и минимальный ранги
                if count == 3 and (Card.ranks.index(rank)+2) > max_high_rank:
                    max_high_rank = Card.ranks.index(rank)+2
                if count == 2 and (Card.ranks.index(rank)+2) > max_low_rank:
                    max_low_rank = Card.ranks.index(rank)+2
            for card in cards:  # формируем комбинацию
                if card.score == max_high_rank:
                    comb_cart.append(card)
                if card.score == max_low_rank:
                    comb_cart.insert(0, card)
            return FullHouse(comb_cart)
        return None

    @staticmethod
    def check_four_of_kind(cards: list[Card]) -> FourOfKind | None:
        """
        метод проверки каре
        :param cards: список проверяемых карт
        :return: сформированная комбинация FourOfKind или None
        """
        ranks = get_rank_dict(cards)  # словарь рангов
        list_card = sorted(cards, key=lambda x: x.score)
        if 4 in ranks.values():  # берем ранги с 4 картами
            comb_cart: list[Card] = []
            for card in cards:  # формируем комбинацию
                if ranks[card.rank] == 4:
                    comb_cart.append(card)
                    list_card.remove(card)
            no_comb: Card = list_card[-1]  # карта вне комбинации
            return FourOfKind(comb_cart, no_comb)
        return None

    @staticmethod
    def check_straight_flush(cards: list[Card]) -> StraightFlush | None:
        """
        метод проверки стрит флеша
        :param cards: список проверяемых карт
        :return: сформированная комбинация StraightFlush или None
        """
        suit = find_suit(get_suit_dict(cards))  # ищем масть
        list_suit_card = [card for card in cards if card.suit == suit]  # список карт с нужной мастью
        list_card = sorted(list_suit_card, key=lambda x: x.score)
        list_cards_no_duplicate = remove_duplicate_cards(list_card.copy())
        comb_cart = straight_check(list_cards_no_duplicate)
        if comb_cart:
            return StraightFlush(comb_cart)
        return None

    @staticmethod
    def check_royal_flush(cards: list[Card]) -> RoyalFlush | None:
        """
        метод проверки флеш рояля
        :param cards: список проверяемых карт
        :return: сформированная комбинация RoyalFlush или None
        """
        suit = find_suit(get_suit_dict(cards))  # ищем масть
        list_suit_card = [card for card in cards if card.suit == suit]  # список карт с нужной мастью
        list_card = sorted(list_suit_card, key=lambda x: x.score)
        list_cards_no_duplicate = remove_duplicate_cards(list_card.copy())
        comb_cart = straight_check(list_cards_no_duplicate, 'royal flush')  # формирование комбинации
        if comb_cart:
            return RoyalFlush(comb_cart)
        return None
