from .player import Player
from .deck import Deck
from .hand import Hand
from .card import Card
from .combination import *
from .game_helper import *


class Game:
    def __init__(self, players: tuple[Player, ...], blind: int):
        self._bank: int = 0
        # self.table: Hand = Hand()
        self.board: list[Card] = []
        self.blind = blind
        self._players: tuple[Player, ...] = players
        self._deck = Deck()

    def start(self):
        self._deck.shuffle()
        for _ in range(2):
            for player in self._players:
                if player:
                    player.hand += self._deck.deal_card()
        # for player in self._players:
        #     player.hand += Card('2', '♠')
        #     player.hand += Card('A', '♠')
        # self._players[0].hand._hand = [Card('2', '♠'), Card('A', '♠')]
        # self._players[1].hand._hand = [Card('2', '♠'), Card('6', '♠')]
        self.set_blind()
        self.bid_blind()
        self.show_table()

        self.flop()
        self.show_table()

        self.turn_or_river()
        # self.board.append(Card('9', '♣'))
        self.show_table()

        self.turn_or_river()
        # self.board.append(Card('10', '♦'))
        self.show_table()

        self.show_players()

    def flop(self):
        self._deck.deal_card()
        for _ in range(3):
            self.board.append(self._deck.deal_card())
        # self.board.append(Card('6', '♥'))
        # self.board.append(Card('7', '♥'))
        # self.board.append(Card('8', '♣'))

    def turn_or_river(self):
        self._deck.deal_card()
        self.board.append(self._deck.deal_card())

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
        for player in self._players:
            if player:
                print(player)

    def drop_cards(self):
        for player in self._players:
            if player:
                player.drop()

    def set_blind(self):
        players = [player for player in self._players if player]
        for ind, player in enumerate(players):
            if player.dealer:
                players[(ind + 1) % len(players)].sb = True
                players[(ind + 2) % len(players)].bb = True
                break

    def bid_blind(self):
        for player in self._players:
            if player:
                if player.sb:
                    self._bank += player.bid(self.blind/2)
                if player.bb:
                    self._bank += player.bid(self.blind)

    def check_winner(self):
        rating_win_combination = 0
        check_list = (self.check_royal_flush, self.check_straight_flush, self.check_four_of_kind, self.check_full_house,
                      self.check_flush, self.check_straight, self.check_set, self.check_two_pairs, self.check_pair,
                      self.check_kicker)
        for player in self._players:
            if player:
                hand_board: list[Card] = self.board + player.hand.show()
                for check in check_list:
                    combination: tuple[bool, ...] | None = check(hand_board)
                    if combination:
                        setattr(player, 'combination', combination)
                        break
                if player.combination and player.show_rating_combination() > rating_win_combination:
                    rating_win_combination = player.show_rating_combination()

        list_winner = [player for player in self._players if player and
                       player.show_rating_combination() == rating_win_combination]
        if len(list_winner) > 1:
            win_high_card = max([player.combination for player in list_winner])
            winner = [player for player in list_winner if not (player.combination < win_high_card)]
        else:
            winner = list_winner
        print('Победитель', len(winner), *winner)
        print()
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
