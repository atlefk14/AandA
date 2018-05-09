import StateMachine
import Nations
import Game
import Units



Germany = Nations.Nation(name='Germany', human=False)
Russia = Nations.Nation(name='Russia', human=False)
game = Game.Game(size=(2, 2), nations=[Germany, Russia])

info = None

while True:
    game.randomBot()