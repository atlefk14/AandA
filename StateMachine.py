import State
import random
class StateMachine():

    def __init__(self):
        self.states = dict()
        self.currentState = None


    def addStates(self, key, human=True):

        self.states[key] = State.State(human)

    def setState(self, key):

        self.currentState = self.states[key]

    def loop(self, game):
        while game.currentPlayer.human == False:
            '''results = game.doBattle(game.battles[0])
            attacker = results[0]
            defender = results[1]
            
            if defender[1] > 0:
                defenderKeys = list(defender[0].keys())
                game.currentPlayer = defender[0][defenderKeys[0]][0].owner
                break
            '''
            game.randomBot()
            game.currentPlayer = game.nations[0]
            print("Jeg er ikke mennesk")

