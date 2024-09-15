from .player import Player
from .deck import Deck
from .hand import Hand
from .card import Card
from .combination import *
from .game_helper import *



class Game:
    def __init__(self, players: tuple[Player, ...], blind: int):
        self._bank = 0
        # self.table: Hand = Hand()
        self.board: list[Card] = []
        self.blind = blind
        self._players: tuple[Player, ...] = players
        self._deck = Deck()

    def start(self):
        self._deck.shuffle()
        for _ in range(2):
            for player in self._players:
                player.hand += self._deck.deal_card()
        # for player in self._players:
        #     player.hand += Card('2', '♠')
        #     player.hand += Card('A', '♠')
        # self._players[0].hand._hand = [Card('2', '♠'), Card('A', '♠')]
        # self._players[1].hand._hand = [Card('2', '♠'), Card('6', '♠')]
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
        print(f'{street}:', *self.board)

    def show_players(self):
        for player in self._players:
            print(player)

    def drop_cards(self):
        for player in self._players:
            player.drop()

    def check_winner(self):
        rating_win_combination = 0
        check_list = (self.check_royal_flush, self.check_straight_flush, self.check_four_of_kind, self.check_full_house,
                      self.check_flush, self.check_straight, self.check_set, self.check_two_pairs, self.check_pair,
                      self.check_kicker)
        for player in self._players:
            hand_board: list[Card] = self.board + player.hand.show()
            for check in check_list:
                combination: tuple[bool, ...] | None = check(hand_board)
                if not combination:
                    continue
                if combination[0]:
                    setattr(player, 'combination', combination[1])
                    break
            if player.combination and player.show_rating_combination() > rating_win_combination:
                rating_win_combination = player.show_rating_combination()
        list_winner = [player for player in self._players if player.show_rating_combination() == rating_win_combination]
        if len(list_winner) > 1:
            win_high_card = max([player.combination for player in list_winner])
            winner = [player for player in list_winner if not (player.combination < win_high_card)]
        else:
            winner = list_winner
        print('Победитель', len(winner), *winner)
        print()
        return winner

    # @staticmethod
    # def get_suit_dict(cards: list[Card]) -> dict:
    #     suit_dict = {}
    #     for card in cards:
    #         suit_dict[card.suit] = suit_dict.get(card.suit, 0) + 1
    #     return suit_dict
    #
    # @staticmethod
    # def get_rank_dict(cards: list[Card]) -> dict:
    #     rank_dict = {}
    #     for card in cards:
    #         rank_dict[card.rank] = rank_dict.get(card.rank, 0) + 1
    #     return rank_dict

    @staticmethod
    def check_kicker(cards: list[Card]):
        list_card: list[Card] = sorted(cards, key=lambda x: x.score)
        no_comb: list[Card] = []
        comb_cart = max(cards)
        list_card.remove(max(cards))
        for i in range(4):
            card = list_card.pop()
            no_comb.append(card)
        return True, Kicker(comb_cart, no_comb)

    def check_pair(self, cards: list[Card]):
        comb_cart: list[Card] = []
        list_card: list[Card] = sorted(cards, key=lambda x: x.score)
        no_comb: list[Card] = []

        # def pair(card_dict: dict):
        #     for check_rank, count in card_dict.items():
        #         if count == 2:
        #             return check_rank

        rank = find_ranks(get_rank_dict(cards), 'pair')
        if rank:
            for card in cards:
                if card.rank == rank:
                    comb_cart.append(card)
                    list_card.remove(card)
            for i in range(3):
                card = list_card.pop()
                # if card > max(comb_cart):
                no_comb.append(card)
            return True, Pair(comb_cart, no_comb)

    def check_two_pairs(self, cards: list[Card]):
        comb_cart: list[Card] = []
        list_card: list[Card] = sorted(cards, key=lambda x: x.score)
        # no_comb: list[Card] | None = None

        # def tow_pairs(card_dict: dict):
        #     list_rank = []
        #     for check_rank, count in card_dict.items():
        #         if count == 2:
        #             list_rank.append(check_rank)
        #     return list_rank

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
                return
            # if list_card[-1] > max(comb_cart):
            no_comb: Card = list_card[-1]
            return True, TwoPairs(sorted(comb_cart, key=lambda x: x.score), no_comb)

    def check_set(self, cards: list[Card]):
        comb_cart: list[Card] = []
        list_card: list[Card] = sorted(cards, key=lambda x: x.score)
        no_comb: list[Card] = []

        # def set_cart(card_dict: dict):
        #     list_rank = []
        #     for check_rank, count in card_dict.items():
        #         if count == 3:
        #             list_rank.append(check_rank)
        #     return list_rank

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
                # if card > max(comb_cart):
                no_comb.append(card)
            return True, SetCard(comb_cart, no_comb)

    @staticmethod
    def check_straight(cards: list[Card]) -> tuple[bool, Straight] | None:
        list_card = sorted(cards, key=lambda x: x.score)
        print("Карты", list_card)
        list_cards_no_duplicate = remove_duplicate_cards(list_card.copy())
        print('Без дубликатов', list_cards_no_duplicate)
        comb_cart = straight_check(list_cards_no_duplicate)
        if comb_cart:
            return True, Straight(comb_cart)
        return None
    # @staticmethod
    # def check_straight(cards: list[Card]) -> tuple[bool, Straight] | None:
    #     comb_cart: list[Card] = []
    #     list_card = sorted(cards, key=lambda x: x.score)
    #     # set_score_card = set()
    #     list_cards_no_duplicate = remove_duplicate_cards(list_card.copy())
    #     ## for card_del_duplicate in list_card:
    #     ##     if card_del_duplicate.score not in set_score_card:
    #     ##         list_cards_no_duplicate.append(card_del_duplicate)
    #     ##         set_score_card.add(card_del_duplicate.score)
    #     list_cart_rank = [card.rank for card in list_cards_no_duplicate]
    #     copy_list_card_rank = list_cart_rank.copy()
    #
    #     ## def check_low_straight(list_card_low_straight: list[Card]):
    #     ##     # list_card_low_straight = lst.copy()
    #     ##     for card in list_card_low_straight:
    #     ##         if card.rank == 'A':
    #     ##             list_card_low_straight.insert(0, card)
    #     ##             break
    #     ##     else:
    #     ##         return
    #     ##     list_cart_rank_low_straight = [card.rank for card in list_card_low_straight]
    #     ##     check_low = ','.join(list(map(str, list_cart_rank_low_straight[:5])))
    #     ##     if check_low == 'A,2,3,4,5':
    #     ##         low_comb = list_card_low_straight[:5]
    #     ##         low_comb[0].score = 1
    #     ##         # for low_card in low_comb:
    #     ##         #     if low_card.rank == 'A':
    #     ##         #         low_card.score = 1
    #     ##         return low_comb
    #
    #     ## list_score_card = [card.score for card in list_card]
    #     ## copy_list_score_card = sorted(set(list_score_card))
    #     ind = -1
    #     while len(copy_list_card_rank) > 4:
    #         check = ','.join(list(map(str, copy_list_card_rank[ind-4:])))
    #         if check in '2,3,4,5,6,7,8,9,10,J,Q,K,A':
    #             copy_list_card_rank = copy_list_card_rank[ind-4:]
    #             flag_straight = True
    #             break
    #         else:
    #             copy_list_card_rank.pop()
    #     else:
    #         if len(list_cards_no_duplicate) > 4:
    #             low_straight = check_low_straight(list_cards_no_duplicate.copy())
    #             if low_straight:
    #                 return True, Straight(low_straight)
    #             else:
    #                 return
    #         else:
    #             return
    #     if flag_straight:
    #         list_index = [list_cart_rank.index(score) for score in copy_list_card_rank]
    #         rank_comb = []
    #         for index in list_index:
    #             for i in range(4):  # Проверяем до 4 элементов вперед
    #                 if (index + i < len(list_cards_no_duplicate) and
    #                         list_cards_no_duplicate[index + i].rank not in rank_comb):
    #                     comb_cart.append(list_cards_no_duplicate[index + i])
    #                     rank_comb.append(list_cards_no_duplicate[index + i].rank)
    #                     break
    #         return True, Straight(comb_cart)

    def check_flush(self, cards: list[Card]) -> tuple[bool, Flush]:


        suit = find_suit(get_suit_dict(cards))
        if suit:
            comb_cart: list[Card] = []
            for card in cards:
                if card.suit == suit:
                    comb_cart.append(card)
            return True, Flush(comb_cart)

    def check_full_house(self, cards: list[Card]) -> tuple[bool, FullHouse]:
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
            return True, FullHouse(comb_cart)

    def check_four_of_kind(self, cards: list[Card]) -> tuple[bool, FourOfKind]:
        ranks = get_rank_dict(cards)
        list_card = sorted(cards, key=lambda x: x.score)
        # no_comb: list[Card] | None = None
        if 4 in ranks.values():
            comb_cart: list[Card] = []
            for card in cards:
                if ranks[card.rank] == 4:
                    comb_cart.append(card)
                    list_card.remove(card)
            # if list_card[-1] > max(comb_cart):
            no_comb: Card = list_card[-1]
            return True, FourOfKind(comb_cart, no_comb)

    def check_straight_flush(self, cards: list[Card]) -> tuple[bool, StraightFlush] | None:
        suit = find_suit(get_suit_dict(cards))
        print('Масть', suit)
        list_suit_card = [card for card in cards if card.suit == suit]
        list_card = sorted(list_suit_card, key=lambda x: x.score)
        list_cards_no_duplicate = remove_duplicate_cards(list_card.copy())
        comb_cart = straight_check(list_cards_no_duplicate)
        if comb_cart:
            return True, StraightFlush(comb_cart)



    # def check_straight_flush(self, cards: list[Card]) -> tuple[bool, StraightFlush] | None:
    #     comb_cart: list[Card] = []
    #     suit = find_suit(get_suit_dict(cards))
    #     list_suit_card = [card for card in cards if card.suit == suit]
    #     list_card = sorted(list_suit_card, key=lambda x: x.score)
    #     ## set_score_card = set()
    #     list_cards_no_duplicate = remove_duplicate_cards(list_card.copy())
    #     ## for card_del_duplicate in list_card:
    #     ##     if card_del_duplicate.score not in set_score_card:
    #     ##         list_cards_no_duplicate.append(card_del_duplicate)
    #     ##         set_score_card.add(card_del_duplicate.score)
    #     list_cart_rank = [card.rank for card in list_cards_no_duplicate]
    #     copy_list_card_rank = list_cart_rank.copy()
    #
    #     ind = -1
    #     while len(copy_list_card_rank) > 4:
    #         check = ','.join(list(map(str, copy_list_card_rank[ind - 4:])))
    #         if check in '2,3,4,5,6,7,8,9,10,J,Q,K,A':
    #             copy_list_card_rank = copy_list_card_rank[ind - 4:]
    #             flag_straight = True
    #             break
    #         else:
    #             copy_list_card_rank.pop()
    #     else:
    #         if len(list_cards_no_duplicate) > 4:
    #             low_straight = check_low_straight(list_cards_no_duplicate.copy())
    #             if low_straight:
    #                 return True, StraightFlush(low_straight)
    #             else:
    #                 return
    #         else:
    #             return
    #     if flag_straight:
    #         list_index = [list_cart_rank.index(score) for score in copy_list_card_rank]
    #         rank_comb = []
    #         for index in list_index:
    #             for i in range(4):  # Проверяем до 4 элементов вперед
    #                 if (index + i < len(list_cards_no_duplicate) and
    #                         list_cards_no_duplicate[index + i].rank not in rank_comb):
    #                     comb_cart.append(list_cards_no_duplicate[index + i])
    #                     rank_comb.append(list_cards_no_duplicate[index + i].rank)
    #                     break
    #         return True, StraightFlush(comb_cart)
# TODO рефакторить код на флеш рояль
    def check_royal_flush(self, cards: list[Card]) -> tuple[bool, RoyalFlush] | None:
        comb_cart: list[Card] = []
        suit = find_suit(get_suit_dict(cards))
        list_suit_card = [card for card in cards if card.suit == suit]
        list_card = sorted(list_suit_card, key=lambda x: x.score)
        # list_score_card = [card.score for card in list_card]
        # copy_list_score_card = sorted(set(list_score_card))

        # set_score_card = set()
        list_cards_no_duplicate = remove_duplicate_cards(list_card.copy())
        # for card_del_duplicate in list_card:
        #     if card_del_duplicate.score not in set_score_card:
        #         list_cards_no_duplicate.append(card_del_duplicate)
        #         set_score_card.add(card_del_duplicate.score)
        list_cart_rank = [card.rank for card in list_cards_no_duplicate]
        copy_list_card_rank = list_cart_rank.copy()

        ind = -1
        while len(copy_list_card_rank) > 4:
            check = ','.join(list(map(str, copy_list_card_rank[ind - 4:])))
            if check in '10,J,Q,K,A':
                copy_list_card_rank = copy_list_card_rank[ind - 4:]
                flag_straight = True
                break
            else:
                copy_list_card_rank.pop()
        else:
            return
        if flag_straight:
            list_index = [list_cart_rank.index(score) for score in copy_list_card_rank]
            rank_comb = []
            for index in list_index:
                for i in range(4):  # Проверяем до 4 элементов вперед
                    if (index + i < len(list_cards_no_duplicate)
                            and list_cards_no_duplicate[index + i].rank not in rank_comb):
                        comb_cart.append(list_cards_no_duplicate[index + i])
                        rank_comb.append(list_cards_no_duplicate[index + i].rank)
                        break
            return True, RoyalFlush(comb_cart)
