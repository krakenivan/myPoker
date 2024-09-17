from .player import Player
from .deck import Deck
from .bet import Bet
from .hand import Hand
from .card import Card
from .combination import *
from .game_helper import *

# TODO доработать размешение меток дилера и сб и бб
class Game:
    def __init__(self, players: tuple[Player, ...], blind: int | float):
        self._bank: int = 0
        # self.table: Hand = Hand()
        self.board: list[Card] = []
        self.blind = blind
        self._players: tuple[Player, ...] = players
        self.players_in_game: list[Player] = [player for player in self._players if player]
        self.list_players_preflop: list[Player] = []  # список игроков для ставок на префлопе
        self.list_players_postflop: list[Player] = []  # список игроков для ставок на постфлопе
        self.bet: Bet = Bet(self, blind)
        self._deck = Deck()
        self.is_table_flop: bool = False

    def start(self):
        # self._players[0].hand._hand = [Card('2', '♠'), Card('A', '♠')]
        # self._players[1].hand._hand = [Card('2', '♠'), Card('6', '♠')]
        self.set_blind()
        self.show_players()
        print()


        self.preflop()
        # self.show_table()
        if len(self.players_in_game) == 1:
            return self.players_in_game

        self.flop()
        # self.show_table()
        if len(self.players_in_game) == 1:
            return self.players_in_game
        self.turn_or_river()
        # self.board.append(Card('9', '♣'))
        # self.show_table()
        if len(self.players_in_game) == 1:
            return self.players_in_game
        self.turn_or_river()
        # self.board.append(Card('10', '♦'))
        # self.show_table()
        if len(self.players_in_game) == 1:
            return self.players_in_game
        winner = self.showdown()

        self.show_players()
        return winner

    def preflop(self):
        self.bet.bet_blind()
        self.dealing_cards()
        self.show_table()
        # self.show_players()
        print()
        self.accept_bet(self.list_players_preflop)
        self.update_list_player()
        self.resetting_blind_markers()


    def flop(self):
        self._deck.deal_card()
        for _ in range(3):
            self.board.append(self._deck.deal_card())
        # self.board.append(Card('6', '♥'))
        # self.board.append(Card('7', '♥'))
        # self.board.append(Card('8', '♣'))
        self.show_table()
        # self.show_players()
        self.is_table_flop = True
        self.bet_reset(self.blind)
        self.accept_bet(self.list_players_postflop)
        self.update_list_player()
        self.resetting_blind_markers()


    def turn_or_river(self):
        self._deck.deal_card()
        self.board.append(self._deck.deal_card())
        self.show_table()
        self.bet_reset(self.blind)
        self.accept_bet(self.list_players_postflop)
        self.update_list_player()
        self.resetting_blind_markers()

    def show_table(self):
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
        for player in self.players_in_game:
            print(player)

    def dealing_cards(self):
        self._deck.shuffle()
        print(self._deck)
        index_player = tuple(range(len(self.players_in_game)))
        next_had = 0

        def dealing(pl: Player):

            for _ in range(2):
                pl.hand += self._deck.deal_card()

        for ind, player in enumerate(self.players_in_game):
            if player.sb:  # выявление игрока на малом блайнде
                next_had: int = ind  # переменная следующей руки для раздачи
                break
        count_had: int = 0  # счетчик количества рук
        while count_had != len(self.players_in_game):  # раздача карт, начинается с малого блайнда,
            # пока количество розданных рук не равно количеству игроков
            dealing(self.players_in_game[next_had])  # выдача руки
            self.list_players_preflop.insert(abs(count_had-2), self.players_in_game[next_had])  # размешение в порядке начала ставок на префлопе
            # (первый следующий после большого блайнда)
            self.list_players_postflop.insert(count_had, self.players_in_game[next_had])  # размешение в порядке начала ставок на постфлопе
            # (первый малый блайнд)
            next_had = index_player[(next_had + 1) % len(index_player)]  # переход к следующе руке
            count_had += 1  # увеличение счетчика
        print(self.list_players_preflop)
        print(self.list_players_postflop)
        self.show_players()

    def drop_cards(self):
        for player in self._players:
            if player:
                player.drop()

    def set_blind(self):
        # players = [player for player in self._players if player]
        for ind, player in enumerate(self.players_in_game):
            if player.dealer:
                self.players_in_game[(ind + 1) % len(self.players_in_game)].sb = True
                self.players_in_game[(ind + 2) % len(self.players_in_game)].bb = True
                break

    def resetting_blind_markers(self):
        for player in self._players:
            if player:
                player.sb = False
                player.bb = False

    def update_list_player(self):
        self.players_in_game = [player for player in self.players_in_game if not player.bet_fold]
        self.list_players_postflop = [player for player in self.list_players_postflop if not player.bet_fold]

    def accept_bet(self, players):
        flag_bet = True  # Флаг ставок
        while flag_bet:  # Ставки пока флаг ставок True
            for player in players:  # прием ставок игроков, первый ставит следующий после большого блайнда
                if not player.bet_fold:  # если игрок не скинул еще карты
                    if not self.is_table_flop:
                        self.bet.bet_preflop(player)  # запрос ставки
                    else:
                        self.bet.bet_postflop(player)
                if self.bet.count_bet == len(self.players_in_game):  # Если количество ставок равно количеству игроков
                    flag_bet = False  # флаг ставок False
                    break  # остановка цикла

    def bet_reset(self, blind):
        for player in self._players:
            if player:
                player.last_bet_amount = 0
        # self.bet.bet = blind  # Бет: минимальная ставка
        # self.bet.bet_blind = blind  # величина большого блайнда
        # self.bet.small_blind = blind / 2  # величина малого блайнда
        self.bet.bet_call = blind  # ставка колла
        self.bet.bet_min_raise = self.bet.bet_call * 2  # ставка минимального рейза
        self.bet.is_raise = False
        self.bet.count_bet = 0
        self.bet.is_bet_postflop = False

    # def check_winner(self, players):
    #     if len(players)

    def showdown(self):
        rating_win_combination = 0
        check_list = (self.check_royal_flush, self.check_straight_flush, self.check_four_of_kind, self.check_full_house,
                      self.check_flush, self.check_straight, self.check_set, self.check_two_pairs, self.check_pair,
                      self.check_kicker)
        for player in self.players_in_game:
            if player:
                hand_board: list[Card] = self.board + player.hand.show()
                for check in check_list:
                    combination: tuple[bool, ...] | None = check(hand_board)
                    if combination:
                        setattr(player, 'combination', combination)
                        break
                if player.combination and player.show_rating_combination() > rating_win_combination:
                    rating_win_combination = player.show_rating_combination()

        list_winner = [player for player in self.players_in_game if player and
                       player.show_rating_combination() == rating_win_combination]
        if len(list_winner) > 1:
            win_high_card = max([player.combination for player in list_winner])
            winner = [player for player in list_winner if not (player.combination < win_high_card)]
        else:
            winner = list_winner
        # print('Победитель', len(winner), *winner)
        # print()
        return winner

    @staticmethod
    def check_kicker(cards: list[Card]) -> Kicker:
        """
        Метод проверки старшей карты
        :param cards: список проверяемых карт
        :return: сформированная комбинация Kicker
        """
        list_card: list[Card] = sorted(cards, key=lambda x: x.score)
        no_comb: list[Card] = []
        comb_cart = max(cards)
        list_card.remove(max(cards))
        for i in range(4):
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
        rank = find_ranks(get_rank_dict(cards), 'pair')
        if rank:
            for card in cards:
                if card.rank == rank:
                    comb_cart.append(card)
                    list_card.remove(card)
            for i in range(3):
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
        rank = find_ranks(get_rank_dict(cards), 'two pairs')
        if rank:
            if len(rank) == 2:
                for card in cards:
                    if card.rank in rank:
                        comb_cart.append(card)
                        list_card.remove(card)
            elif len(rank) > 2:
                ind_min_rank = 12
                for i in rank:
                    if Card.ranks.index(i) < ind_min_rank:
                        ind_min_rank = Card.ranks.index(i)
                min_rank = Card.ranks[ind_min_rank]
                rank.remove(min_rank)
                for card in cards:
                    if card.rank in rank:
                        comb_cart.append(card)
                        list_card.remove(card)
            else:
                return None
            no_comb: Card = list_card[-1]
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
        rank = find_ranks(get_rank_dict(cards), 'set')
        if rank:
            if len(rank) == 1:
                for card in cards:
                    if card.rank == rank[0]:
                        comb_cart.append(card)
                        list_card.remove(card)
            else:
                ind_max_rank = 0
                for i in rank:
                    if Card.ranks.index(i) > ind_max_rank:
                        ind_max_rank = Card.ranks.index(i)
                max_rank = Card.ranks[ind_max_rank]
                for card in cards:
                    if card.rank == max_rank:
                        comb_cart.append(card)
                        list_card.remove(card)
            for i in range(2):
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
        list_cards_no_duplicate = remove_duplicate_cards(list_card.copy())
        comb_cart = straight_check(list_cards_no_duplicate)
        if comb_cart:
            return Straight(comb_cart)
        return None

    @staticmethod
    def check_flush(cards: list[Card]) -> Flush | None:
        """
        метод проверки флеша
        :param cards: список проверяемых карт
        :return: сформированная комбинация Flush или None
        """
        suit = find_suit(get_suit_dict(cards))
        if suit:
            comb_cart: list[Card] = []
            for card in cards:
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
        ranks = get_rank_dict(cards)
        if 3 in ranks.values() and 2 in ranks.values():
            comb_cart: list[Card] = []
            max_high_rank = 0
            max_low_rank = 0
            for rank, count in ranks.items():
                if count == 3 and (Card.ranks.index(rank)+2) > max_high_rank:
                    max_high_rank = Card.ranks.index(rank)+2
                if count == 2 and (Card.ranks.index(rank)+2) > max_low_rank:
                    max_low_rank = Card.ranks.index(rank)+2
            for card in cards:
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
        ranks = get_rank_dict(cards)
        list_card = sorted(cards, key=lambda x: x.score)
        if 4 in ranks.values():
            comb_cart: list[Card] = []
            for card in cards:
                if ranks[card.rank] == 4:
                    comb_cart.append(card)
                    list_card.remove(card)
            no_comb: Card = list_card[-1]
            return FourOfKind(comb_cart, no_comb)
        return None

    @staticmethod
    def check_straight_flush(cards: list[Card]) -> StraightFlush | None:
        """
        метод проверки стрит флеша
        :param cards: список проверяемых карт
        :return: сформированная комбинация StraightFlush или None
        """
        suit = find_suit(get_suit_dict(cards))
        list_suit_card = [card for card in cards if card.suit == suit]
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
        suit = find_suit(get_suit_dict(cards))
        list_suit_card = [card for card in cards if card.suit == suit]
        list_card = sorted(list_suit_card, key=lambda x: x.score)
        list_cards_no_duplicate = remove_duplicate_cards(list_card.copy())
        comb_cart = straight_check(list_cards_no_duplicate, 'royal flush')
        if comb_cart:
            return RoyalFlush(comb_cart)
        return None
