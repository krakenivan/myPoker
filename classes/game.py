from .player import Player
from .deck import Deck
from .hand import Hand
from .card import Card
from .combination import *


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
        self.show_table()
        self.flop()
        self.show_table()
        self.turn_or_river()
        self.show_table()
        self.turn_or_river()
        self.show_table()
        self.show_players()

    def flop(self):
        self._deck.deal_card()
        for _ in range(3):
            self.board.append(self._deck.deal_card())

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
        winner = None
        rating_win_combination = 0
        check_list = (self.check_royal_flush, self.check_straight_flush, self.check_four_of_kind, self.check_full_house,
                      self.check_flush, self.check_straight, self.check_set, self.check_tow_pairs, self.check_pair,
                      self.check_kicker)
        for player in self._players:
            hand_board: list[Card] = self.board + player.hand.show()
            for check in check_list:
                combination: tuple[bool, ...] | None = check(hand_board)
                if not combination:
                    continue
                elif combination[0]:
                    setattr(player, 'combination', combination[1])
                    break
            if player.combination and player.show_rating_combination() > rating_win_combination:
                rating_win_combination = player.show_rating_combination()
        list_winner = [player for player in self._players if
                       player.combination and player.show_rating_combination() == rating_win_combination]
        if list_winner and len(list_winner) > 1:
            win_high_card = max([player.combination for player in list_winner])
            winner = [player for player in list_winner if not (player.combination < win_high_card)]
        else:
            winner = list_winner
        print('Победитель', *winner)
        return

    @staticmethod
    def get_suit_dict(cards: list[Card]) -> dict:
        suit_dict = {}
        for card in cards:
            suit_dict[card.suit] = suit_dict.get(card.suit, 0) + 1
        return suit_dict

    @staticmethod
    def get_rank_dict(cards: list[Card]) -> dict:
        rank_dict = {}
        for card in cards:
            rank_dict[card.rank] = rank_dict.get(card.rank, 0) + 1
        return rank_dict

    @staticmethod
    def check_kicker(cards: list[Card]):
        return True, Kicker(max(cards))

    def check_pair(self, cards: list[Card]):
        comb_cart: list[Card] = []

        def pair(card_dict: dict):
            for check_rank, count in card_dict.items():
                if count == 2:
                    return check_rank

        rank = pair(self.get_rank_dict(cards))
        if rank:
            for card in cards:
                if card.rank == rank:
                    comb_cart.append(card)
            return True, Pair(comb_cart)

    def check_tow_pairs(self, cards: list[Card]):
        comb_cart: list[Card] = []

        def tow_pairs(card_dict: dict):
            list_rank = []
            for check_rank, count in card_dict.items():
                if count == 2:
                    list_rank.append(check_rank)
            return list_rank

        rank = tow_pairs(self.get_rank_dict(cards))
        if rank:
            if len(rank) == 2:
                for card in cards:
                    if card.rank in rank:
                        comb_cart.append(card)
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
            else:
                return

            return True, TwoPairs(sorted(comb_cart, key=lambda x: x.score))

    def check_set(self, cards: list[Card]):
        comb_cart: list[Card] = []

        def set_cart(card_dict: dict):
            list_rank = []
            for check_rank, count in card_dict.items():
                if count == 3:
                    list_rank.append(check_rank)
            return list_rank

        rank = set_cart(self.get_rank_dict(cards))
        if rank:
            if len(rank) == 1:
                for card in cards:
                    if card.rank == rank[0]:
                        comb_cart.append(card)
            else:
                ind_max_rank = 0
                for i in rank:
                    if Card.ranks.index(i) > ind_max_rank:
                        ind_max_rank = Card.ranks.index(i)
                max_rank = Card.ranks[ind_max_rank]
                for card in cards:
                    if card.rank == max_rank:
                        comb_cart.append(card)
            return True, SetCard(comb_cart)

    @staticmethod
    def check_straight(cards: list[Card]) -> tuple[bool, Straight] | None:
        comb_cart: list[Card] = []
        list_card = sorted(cards, key=lambda x: x.score)
        list_score_card = [card.score for card in list_card]
        copy_list_score_card = sorted(set(list_score_card))
        ind = -1
        while len(copy_list_score_card) > 4:
            check = ','.join(list(map(str, copy_list_score_card[ind-4:])))
            if check in '2,3,4,5,6,7,8,9,10,11,12,13':
                copy_list_score_card = copy_list_score_card[ind-4:]
                flag_straight = True
                break
            else:
                copy_list_score_card.pop()
        else:
            return
        if flag_straight:
            list_index = [list_score_card.index(score) for score in copy_list_score_card]
            score_comb = []
            for index in list_index:
                for i in range(4):  # Проверяем до 4 элементов вперед
                    if index + i < len(list_card) and list_card[index + i].score not in score_comb:
                        comb_cart.append(list_card[index + i])
                        score_comb.append(list_card[index + i].score)
                        break
            return True, Straight(comb_cart)

    def check_flush(self, cards: list[Card]) -> tuple[bool, Flush]:

        def flush(card_dict: dict) -> str:
            for check_suit, count in card_dict.items():
                if count >= 5:
                    return check_suit

        suit = flush(self.get_suit_dict(cards))
        if suit:
            comb_cart: list[Card] = []
            for card in cards:
                if card.suit == suit:
                    comb_cart.append(card)
            return True, Flush(comb_cart)

    def check_full_house(self, cards: list[Card]):
        pass

    def check_four_of_kind(self, cards: list[Card]):
        pass

    def check_straight_flush(self, cards: list[Card]):
        pass

    def check_royal_flush(self, cards: list[Card]):
        pass
