import MapGenerator as mapGen
import Units
import Buildings

class Game(object):
    def __init__(self, size, nations):
        self.map = mapGen.MapClass(size, nations)
        self.terminal = False
        self.turn = 0
        self.phase = 0
        self.currentPlayer = None
        self.purchases = dict()
        self.PCUs = self.calculatePCUs()
        self.deployablePlaces = self.findDeployablePlaces()

    def findDeployablePlaces(self):
        deployablePlaces = []
        for w in self.map.board:
            for h in w:
                #h.constructions.append(Buildings.Industry('Germany'))
                for const in h.constructions:
                    if isinstance(const, Buildings.Industry):
                        deployablePlaces.append(h)
        return deployablePlaces

    def calculatePCUs(self):
        PCUs = 0
        for w in self.map.board:
            for h in w:
                if h.owner == self.currentPlayer:
                    PCUs += h.value
        return PCUs

    def nextTurn(self):
        self.turn += 1
        self.phase = 0
        return

    def nextPhase(self):
        self.phase+=1
        return

    def recruitUnit(self, n, type):
        if type == 1:
            inf = Units.Infantry(self.currentPlayer)

        if type in self.purchases:
            self.purchases[type] = []
        self.purchases[type].append(inf)


game = Game((4,4), [('Germany', 2), ('Russia',2 )])