import Nations
import Game
import Units



Germany = Nations.Nation(name='Germany', human=False)
Russia = Nations.Nation(name='Russia', human=False)
game = Game.Game(size=(4, 4), nations=[Germany, Russia])

game.purchases[Germany.name] = []
game.purchases[Russia.name] = []

while True:
    val = game.randomBot()
    if val == True:
        break