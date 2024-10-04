from classes import Deck, Player, Hand, Table, Game, Card

# TODO разработать базу данных
ivan = Player('Иван')
ivan.stack = 1500
bob = Player('Боб')
jon = Player('Джон')
# jon.stack = 0
maks = Player('Макс')
maks.stack = 200
maks.copy_stack = 500
kris = Player('Крис')
kris.stack = 1500
alex = Player('Алекс')
danila = Player('Данила')
gans = Player('Ганс')
sam = Player('Cэм')

table = Table(ivan, blind=20)
# table.set_dealer()

# print(table.players)
table.join(bob)
table.join(jon)
table.join(maks)
table.join(kris)
table.join(alex)
table.join(danila)
print()
table.new_game()


# print('Игроки', table.players)
# print('Гости', table.guests)
# table.kick(bob)
# table.kick(maks)
# print()
# table.new_game()
# # print('Игроки', table.players)
# # print('Гости', table.guests)
# table.join(danila)
# table.join(gans)
# # table.join(sam)
# # print()
# #
# table.new_game()
# # print('Игроки', table.players)
# # print('Гости', table.guests)
# # table.kick(gans)
# table.join(bob)
# # table.join(maks)
# # print()
# #
# table.new_game()
# # print('Игроки', table.players)
# print('Гости', table.guests)
# print(table.players)

# table.join(alex)
# for i in range(10):
# # flag = True
# # while flag:
#     # try:
#     print()
#     a = table.new_game()
    # for i in a:
    #     if i.combination.name == 'Royal Flush':
    #         flag = False
    #         break
    # else:
    #     print()
    #     continue
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


