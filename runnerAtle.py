import StateMachine
import Nations
import Game
import Units



Germany = Nations.Nation(name='Germany')
Russia = Nations.Nation(name='Russia', human=False)
game = Game.Game(size=(2, 2), nations=[Germany, Russia])


stateMachine = StateMachine.StateMachine()
stateMachine.addStates(Germany.name)
stateMachine.addStates(Russia.name, False)
game.nextTurn()
print(game.currentPlayer)
stateMachine.currentState = stateMachine.states[game.currentPlayer.name]
game.moveableUnits()
#game.moveUnit(game.map.board[0][1], game.map.board[0][0], 2, Units.Infantry)   #Ser ikke forskjell når eg sende 1 og 2 units

stateMachine.loop(game)

print(stateMachine.states)