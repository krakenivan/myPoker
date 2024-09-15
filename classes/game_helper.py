from .card import Card
from copy import deepcopy


def get_suit_dict(cards: list[Card]) -> dict:
    suit_dict = {}
    for card in cards:
        suit_dict[card.suit] = suit_dict.get(card.suit, 0) + 1
    return suit_dict


def get_rank_dict(cards: list[Card]) -> dict:
    rank_dict = {}
    for card in cards:
        rank_dict[card.rank] = rank_dict.get(card.rank, 0) + 1
    return rank_dict


def find_ranks(card_dict: dict, combination: str) -> str | list[str]:
    list_rank = []
    if combination == 'pair':
        for check_rank, count in card_dict.items():
            if count == 2:
                return check_rank
    if combination == 'two pairs':
        for check_rank, count in card_dict.items():
            if count == 2:
                list_rank.append(check_rank)
        return list_rank
    if combination == 'set':
        for check_rank, count in card_dict.items():
            if count == 3:
                list_rank.append(check_rank)
        return list_rank


def find_suit(card_dict: dict) -> str:
    for check_suit, count in card_dict.items():
        if count >= 5:
            return check_suit


def check_low_straight(cards: list[Card]):
    # list_card_low_straight = lst.copy()
    for card in cards:
        if card.rank == 'A':
            cards.insert(0, card)
            break
    else:
        return
    card_rank = [card.rank for card in cards]
    check_low = ','.join(list(map(str, card_rank[:5])))
    if check_low == 'A,2,3,4,5':
        low_comb = cards[:5]
        copy_low_comb = deepcopy(low_comb)
        copy_low_comb[0].score = 1
        # for low_card in low_comb:
        #     if low_card.rank == 'A':
        #         low_card.score = 1
        return copy_low_comb


def straight_check(cards, combination=None):
    print()
    print('Функция вызвана')
    comb_cart: list[Card] = []
    copy_cards = cards.copy()
    print('Переданные карты', copy_cards)
    list_cart_rank = [card.rank for card in cards]
    copy_list_card_rank = list_cart_rank.copy()
    print('список рангов', list_cart_rank)
    print()
    str_check = '2,3,4,5,6,7,8,9,10,J,Q,K,A'
    if combination == 'royal flush':
        str_check = '10,J,Q,K,A'
    print(str_check)
    ind = -1
    while len(copy_list_card_rank) > 4:
        check = ','.join(list(map(str, copy_list_card_rank[ind - 4:])))
        print('Проверка на стрит', check)
        if check in str_check:
            copy_list_card_rank = copy_list_card_rank[ind - 4:]
            print('Итоговай стрит', copy_list_card_rank)
            flag_straight = True
            break
        else:
            copy_list_card_rank.pop()
    else:
        if combination != 'royal flush' and len(cards) > 4:
            comb_cart = check_low_straight(cards.copy())
            if comb_cart:
                print("Малый стрит", comb_cart)
                return comb_cart
            else:
                return
        else:
            return
    if flag_straight:
        list_index = [list_cart_rank.index(score) for score in copy_list_card_rank]
        print('Список индексов', list_index)
        rank_comb = []
        for index in list_index:
            for i in range(4):  # Проверяем до 4 элементов вперед
                if (index + i < len(cards) and
                        cards[index + i].rank not in rank_comb):
                    comb_cart.append(cards[index + i])
                    rank_comb.append(cards[index + i].rank)
                    break
        print("Ранги карт", rank_comb)
        print("стрит", comb_cart)

        return comb_cart


def remove_duplicate_cards(cards: list[Card]):
    cards_no_duplicate = []
    set_score_card = set()
    for card in cards:
        if card.score not in set_score_card:
            cards_no_duplicate.append(card)
            set_score_card.add(card.score)
    return cards_no_duplicate

