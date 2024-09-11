from classes import Deck, Player, Hand, Table, Game



ivan = Player('Иван')
andrew = Player('Андрей')
igor = Player('Игорь')
valentin = Player('Валентин')
maxim = Player('Максим')
jon = Player('Джон')
nikolay = Player('Николай')

table_1 = Table(ivan, 50)
table_1.join(andrew)
table_1.join(igor)
table_1.new_game()

print()
table_1.join(valentin)
table_1.new_game()
print()

table_1.join(maxim)
table_1.join(jon)
table_1.join(nikolay)
table_1.new_game()

print(table_1.players)
print(table_1.guest)
print()

table_1.kick(jon)
table_1.new_game()

print(table_1.players)
print(table_1.guest)
