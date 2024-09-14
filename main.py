from classes import Deck, Player, Hand, Table, Game, Card

ivan = Player('Иван')
bob = Player('Боб')
jon = Player('Джон')
maks = Player('Макс')
kris = Player('Крис')
alex = Player('Алекс')

table = Table(ivan, blind=10)
table.join(bob)
table.join(jon)
table.join(maks)
table.join(kris)
table.join(alex)
# for i in range(10):
flag = True
while flag:
    # try:
    a = table.new_game()
    for i in a:
        if i.combination.name == 'Royal Flush':
            flag = False
            break
    else:
        print()
        continue
    # except TypeError:
    #     pass
# c1 = Card('A', '♦')
# c2 = Card('K', '♦')
# c3 = Card('Q', '♦')
# c4 = Card('7', '♦')
# p1 = Card('5', '♦')
# p2 = Card('3', '♦')
# p3 = Card('9', '♦')
#
# pl1 = Flush([c1, c2, c3, c4, p1])
# pl2 = Flush([c1, c2, c3, c4, p2])
# pl3 = Flush([c1, c2, c3, c4, p3])
#
# list_winner = [pl1, pl2, pl3]
# print('w', *list_winner)
# if list_winner and len(list_winner) > 1:
#     win_high_card = max([player.combination for player in list_winner])
#     print()
#     print(win_high_card)
#     print()
#     winner = [player for player in list_winner if not(player.combination < win_high_card)]
#     # for player in list_winner:
#     #     print('p', player)
#     #     if player.combination < win_high_card:
#     #         list_winner.remove(player)
#     #         print()
#     #         print(*list_winner)
# print()
# print(*winner)



    # deck = Deck()
    # deck.shuffle()
    #
    # hand = Hand([deck.deal_card(), deck.deal_card()])
    # print(hand.show())
    # board = Hand([deck.deal_card(), deck.deal_card(), deck.deal_card(), deck.deal_card(), deck.deal_card()])
    # print(board.show())
    #
    # komb = hand + board
    # print(komb.show())
    #
    # w = ['pair', 'tow pair', 'set', 'straight', 'flush',
    #      'full house', 'four of kind', 'straight flush', 'royal flush']
    #
    # rank_dict = {}
    # for card in komb:
    #     rank_dict[card.rank] = rank_dict.get(card.rank, 0) + 1
    #
    # suit_dict = {}
    # for card in komb:
    #     suit_dict[card.suit] = suit_dict.get(card.suit, 0) + 1
    #
    # print(rank_dict)
    # print(suit_dict)
    #
    # for s in suit_dict.values():
    #     if s >= 5:
    #         print('flush')
    #
    # def flush(card_dict: dict) -> str:
    #     for suit, count in card_dict.items():
    #         if count >= 5:
    #             return suit
    # win_hand = Hand()
    #
    # for card in komb:
    #     if card.suit == flush(suit_dict):
    #         win_hand += card
    #
    # print('Победная рука', str(sorted(win_hand.show(), key=lambda x: x.score)))
    # if win_hand._hand:
    #     break